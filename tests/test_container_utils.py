"""Tests for container utilities."""
import pytest
import docker
from pathlib import Path

from refactoring_benchmark.utils.container_utils import (
    copy_to_container,
    extract_folder_from_container,
    stream_exec,
)
from refactoring_benchmark.utils.logger import setup_logging


class TestCopyToContainer:
    """Tests for copy_to_container function."""

    @pytest.mark.slow
    def test_copy_file_to_container(self, docker_client: docker.DockerClient):
        """Test copying a file to a container."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Copy a test file
            test_content = b"Hello from test!\n"
            copy_to_container(container, test_content, "/tmp/test_file.txt")

            # Verify file exists and has correct content
            result = container.exec_run("cat /tmp/test_file.txt")
            assert result.exit_code == 0
            assert result.output == test_content

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)
                else:
                    raise net_err

    @pytest.mark.slow
    def test_copy_script_with_execution_permissions(self, docker_client: docker.DockerClient):
        """Test that copied scripts have execution permissions."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Copy a script
            script_content = b"#!/bin/bash\necho 'Hello'\n"
            copy_to_container(container, script_content, "/tmp/test_script.sh")

            # Verify it's executable
            result = container.exec_run("test -x /tmp/test_script.sh")
            assert result.exit_code == 0, "Script should be executable"

            # Verify it can be executed
            result = container.exec_run("/tmp/test_script.sh")
            assert result.exit_code == 0
            assert b"Hello" in result.output

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)
                else:
                    raise net_err

    @pytest.mark.slow
    def test_copy_to_nested_path(self, docker_client: docker.DockerClient):
        """Test copying to a nested directory path."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Create nested directory first
            container.exec_run("mkdir -p /tmp/nested/deep/path")

            # Copy file to nested location
            test_content = b"Nested content\n"
            copy_to_container(container, test_content, "/tmp/nested/deep/path/file.txt")

            # Verify
            result = container.exec_run("cat /tmp/nested/deep/path/file.txt")
            assert result.exit_code == 0
            assert result.output == test_content

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)
                else:
                    raise net_err


class TestExtractFolderFromContainer:
    """Tests for extract_folder_from_container function."""

    @pytest.mark.slow
    def test_extract_folder(self, docker_client: docker.DockerClient, temp_dir: Path):
        """Test extracting a folder from container."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Create test directory structure in container
            container.exec_run("mkdir -p /tmp/test_extract/subdir")
            container.exec_run("bash -c 'echo \"file1\" > /tmp/test_extract/file1.txt'")
            container.exec_run("bash -c 'echo \"file2\" > /tmp/test_extract/subdir/file2.txt'")

            # Extract to local directory
            local_dest = temp_dir / "extracted"
            local_dest.mkdir()

            extract_folder_from_container(container, "/tmp/test_extract", str(local_dest))

            # Verify extracted files
            assert (local_dest / "test_extract" / "file1.txt").exists()
            assert (local_dest / "test_extract" / "subdir" / "file2.txt").exists()

            # Verify content
            content1 = (local_dest / "test_extract" / "file1.txt").read_text()
            assert "file1" in content1

            content2 = (local_dest / "test_extract" / "subdir" / "file2.txt").read_text()
            assert "file2" in content2

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)

    @pytest.mark.slow
    def test_extract_folder_preserves_structure(self, docker_client: docker.DockerClient, temp_dir: Path):
        """Test that extraction preserves directory structure."""
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Create complex directory structure
            container.exec_run("mkdir -p /tmp/complex/a/b/c")
            container.exec_run("mkdir -p /tmp/complex/x/y")
            container.exec_run("bash -c 'echo \"deep\" > /tmp/complex/a/b/c/deep.txt'")
            container.exec_run("bash -c 'echo \"shallow\" > /tmp/complex/x/shallow.txt'")

            # Extract
            local_dest = temp_dir / "complex_extract"
            local_dest.mkdir()

            extract_folder_from_container(container, "/tmp/complex", str(local_dest))

            # Verify structure
            assert (local_dest / "complex" / "a" / "b" / "c").is_dir()
            assert (local_dest / "complex" / "x" / "y").is_dir()
            assert (local_dest / "complex" / "a" / "b" / "c" / "deep.txt").exists()
            assert (local_dest / "complex" / "x" / "shallow.txt").exists()

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)


class TestStreamExec:
    """Tests for stream_exec function."""

    @pytest.mark.slow
    def test_stream_exec_simple_command(self, docker_client: docker.DockerClient):
        """Test stream_exec with a simple command."""
        setup_logging("/tmp/logs")
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Execute simple command
            output = stream_exec(container, ["echo", "Hello World"], env={})

            assert "Hello World" in output

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)
                else:
                    raise net_err

    @pytest.mark.slow
    def test_stream_exec_with_environment(self, docker_client: docker.DockerClient):
        """Test stream_exec with environment variables."""
        setup_logging("/tmp/logs")
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Execute command that uses environment variable
            output = stream_exec(
                container,
                ["bash", "-c", "echo $TEST_VAR"],
                env={"TEST_VAR": "test_value"}
            )

            assert "test_value" in output

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)
                else:
                    raise net_err

    @pytest.mark.slow
    def test_stream_exec_multiline_output(self, docker_client: docker.DockerClient):
        """Test stream_exec handles multiline output."""
        setup_logging("/tmp/logs")
        container = docker_client.containers.run(
            "benchmark-base-python",
            detach=True,
            command="sleep 60"
        )

        try:
            # Execute command with multiple lines of output
            output = stream_exec(
                container,
                ["bash", "-c", "echo 'line1'; echo 'line2'; echo 'line3'"],
                env={}
            )

            assert "line1" in output
            assert "line2" in output
            assert "line3" in output

        finally:
            try:
                container.stop(timeout=1)
                container.remove(force=True)
            except Exception as net_err:
                if "permission denied" in str(net_err):
                    print("Partially, skipping container removal due to permission denied error.", net_err)
                else:
                    raise net_err
