"""Tests for bootstrap functionality."""
import json
import time
import logging
from pathlib import Path

import pytest
import podman

from refactoring_benchmark.bootstrap.utils import run_metrics
from refactoring_benchmark.utils.models import InstanceRow, Metrics
import refactoring_benchmark.podman.utils as podman_utils
from tests.conftest import verify_git_state, get_git_commit_hash

# Create a test logger
test_logger = logging.getLogger("test_bootstrap")


class TestGitCommitVerification:
    """Tests to verify repository is at correct commit in bootstrap images."""

    @pytest.mark.integration
    def test_setup_image_at_base_commit(
        self, docker_client: podman.PodmanClient, sample_instance_row: InstanceRow
    ):
        """
        Test that setup image has repository at base commit.

        This test checks already-bootstrapped images (run bootstrap first).
        """
        setup_image = sample_instance_row.setup_image

        try:
            docker_client.images.get(setup_image)
        except podman.errors.ImageNotFound:
            pytest.skip(f"Setup image not found: {setup_image}. Run bootstrap first.")

        container = docker_client.containers.run(
            setup_image, detach=True, command=["sleep", "10"]
        )

        try:
            current_hash = get_git_commit_hash(container, "/testbed")

            assert verify_git_state(container, sample_instance_row.commit_hash), (
                f"Setup image should be at base commit {sample_instance_row.short_hash}, "
                f"but is at {current_hash[:8]}"
            )
        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except:
                pass

    @pytest.mark.integration
    def test_runtime_image_at_base_commit(
        self, docker_client: podman.PodmanClient, sample_instance_row: InstanceRow
    ):
        """
        Test that runtime image has repository at base commit.

        This test checks already-bootstrapped images (run bootstrap first).
        """
        runtime_image = sample_instance_row.runtime_image

        try:
            docker_client.images.get(runtime_image)
        except podman.errors.ImageNotFound:
            pytest.skip(f"Runtime image not found: {runtime_image}. Run bootstrap first.")

        container = docker_client.containers.run(
            runtime_image,
            detach=True,
            entrypoint=["sleep", "infinity"]
        )

        try:
            # Wait for container to be ready
            time.sleep(1)
            container.reload()

            if container.status != "running":
                pytest.skip(f"Container not running (status: {container.status})")

            current_hash = get_git_commit_hash(container, "/testbed")

            assert verify_git_state(container, sample_instance_row.commit_hash), (
                f"Runtime image should be at base commit {sample_instance_row.short_hash}, "
                f"but is at {current_hash[:8]}"
            )
        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except:
                pass

    @pytest.mark.integration
    def test_metadata_matches_commits(self, sample_instance_row: InstanceRow):
        """Test that saved metadata has correct commit hashes."""
        metadata_path = Path(sample_instance_row.instance_dir()) / "metadata.json"

        if not metadata_path.exists():
            pytest.skip(f"Metadata not found: {metadata_path}. Run bootstrap first.")

        with open(metadata_path) as f:
            metadata = json.load(f)

        assert metadata["base_hash"] == sample_instance_row.commit_hash
        assert metadata["golden_commit_hash"] == sample_instance_row.golden_commit_hash


class TestMetricsCapture:
    """Tests for metrics capture and validation."""

    def test_run_test_metrics_success(self, docker_client: podman.PodmanClient):
        """Test successful metrics capture from container."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command=["sleep", "60"]
        )

        try:
            # Create a mock run_tests script
            test_output = '{"passed": 25, "failed": 2, "skipped": 3, "total": 30}'
            container.exec_run("mkdir -p /scripts")

            # Create script content
            script_content = f'''#!/bin/bash
echo '{test_output}'
'''.encode()

            # Use copy_to_container utility
            podman_utils.copy_to_container(container, script_content, "/scripts/run_tests")

            # Capture metrics
            metrics = run_test_metrics(container)

            # Verify
            assert metrics.passed == 25
            assert metrics.failed == 2
            assert metrics.skipped == 3
            assert metrics.total == 30
            assert metrics.error is None

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except:
                pass

    def test_run_test_metrics_failure(self, docker_client: podman.PodmanClient):
        """Test metrics capture when test script fails."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command=["sleep", "60"]
        )

        try:
            # Create a script that outputs invalid JSON
            container.exec_run("mkdir -p /scripts")

            script_content = b'''#!/bin/bash
echo "invalid json"
'''
            podman_utils.copy_to_container(container, script_content, "/scripts/run_tests")

            # Capture metrics (should return error metrics)
            metrics = run_test_metrics(container)

            # Verify error state
            assert metrics.passed == 0
            assert metrics.failed == -1
            assert metrics.total == 0
            assert metrics.error == "Crashed"

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except:
                pass

    def test_success_criteria_validation(self):
        """Test the success criteria logic for metrics."""
        # Success case: >= 10 tests, >= 30% pass rate
        success_metrics = Metrics(passed=25, failed=5, skipped=0, total=30)
        is_success = (
            success_metrics.total >= 10
            and success_metrics.passed >= success_metrics.total * 0.3
            and success_metrics.failed != -1
        )
        assert is_success is True

        # Failure case: Not enough tests
        too_few_tests = Metrics(passed=5, failed=2, skipped=0, total=7)
        is_success = (
            too_few_tests.total >= 10
            and too_few_tests.passed >= too_few_tests.total * 0.3
            and too_few_tests.failed != -1
        )
        assert is_success is False

        # Failure case: Low pass rate
        low_pass_rate = Metrics(passed=2, failed=18, skipped=0, total=20)
        is_success = (
            low_pass_rate.total >= 10
            and low_pass_rate.passed >= low_pass_rate.total * 0.3
            and low_pass_rate.failed != -1
        )
        assert is_success is False

        # Failure case: Crashed (failed == -1)
        crashed = Metrics(passed=0, failed=-1, skipped=0, total=0, error="Crashed")
        is_success = (
            crashed.total >= 10
            and crashed.passed >= crashed.total * 0.3
            and crashed.failed != -1
        )
        assert is_success is False
