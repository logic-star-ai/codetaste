"""Pytest fixtures and configuration for refactoring-benchmark tests."""
import os
import tempfile
from pathlib import Path
from typing import Generator
import pytest
import docker

from refactoring_benchmark.utils.models import InstanceRow, Metrics


@pytest.fixture(scope="session")
def docker_client() -> docker.DockerClient:
    """Provide a Docker client for tests."""
    try:
        # use podman
        uid = os.getuid()
        DOCKER_HOST=f"unix:///run/user/${uid}/podman/podman.sock"
        DOCKER_HOST = os.environ.get("DOCKER_HOST", DOCKER_HOST)
        client = docker.from_env(timeout=300, environment={"DOCKER_HOST": DOCKER_HOST})
        client.ping()
        return client
    except Exception as e:
        pytest.skip(f"Docker not available: {e}")


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_instance_row() -> InstanceRow:
    """Provide a sample InstanceRow for testing."""
    return InstanceRow(
        owner="autokey",
        repo="autokey",
        commit_hash="9309c4fe9c7410546eb83c4ba912075f6dc3b092",
        golden_commit_hash="85b948e7cd0f10f0e2918aad99014d8b848fbe6f",
        category="structural",
        language="python"
    )


@pytest.fixture
def sample_metrics() -> Metrics:
    """Provide sample test metrics."""
    return Metrics(
        passed=25,
        failed=2,
        skipped=3,
        total=30
    )


@pytest.fixture
def mock_instance_dir(temp_dir: Path, sample_instance_row: InstanceRow) -> Path:
    """Create a mock instance directory structure."""
    instance_dir = temp_dir / sample_instance_row.instance_dir()
    instance_dir.mkdir(parents=True)
    return instance_dir


@pytest.fixture
def cleanup_test_images(docker_client: docker.DockerClient) -> Generator[None, None, None]:
    """Clean up any test images created during tests."""
    yield
    # Clean up test images after test completes
    try:
        for image in docker_client.images.list():
            for tag in image.tags:
                if "test-" in tag or "__test" in tag:
                    try:
                        docker_client.images.remove(image.id, force=True)
                    except:
                        pass
    except:
        pass


def get_git_commit_hash(container, cwd: str = "/testbed") -> str:
    """
    Get the current git commit hash from a container.

    Args:
        container: Docker container instance
        cwd: Working directory to run git command in

    Returns:
        Current commit hash (full 40 characters)
    """
    result = container.exec_run(
        "git rev-parse HEAD",
        workdir=cwd
    )
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to get git commit: {result.output.decode()}")
    return result.output.decode().strip()


def verify_git_state(container, expected_hash: str, cwd: str = "/testbed") -> bool:
    """
    Verify the container's git repository is at the expected commit.

    Args:
        container: Docker container instance
        expected_hash: Expected commit hash (can be short or full)
        cwd: Working directory containing the git repository

    Returns:
        True if at expected commit, False otherwise
    """
    current_hash = get_git_commit_hash(container, cwd)
    # Support both short and full hashes
    return current_hash.startswith(expected_hash) or expected_hash.startswith(current_hash[:len(expected_hash)])


def container_file_exists(container, path: str) -> bool:
    """
    Check if a file exists in a container.

    Args:
        container: Docker container instance
        path: Path to check

    Returns:
        True if file exists, False otherwise
    """
    result = container.exec_run(f"test -f {path}")
    return result.exit_code == 0


def container_dir_exists(container, path: str) -> bool:
    """
    Check if a directory exists in a container.

    Args:
        container: Docker container instance
        path: Path to check

    Returns:
        True if directory exists, False otherwise
    """
    result = container.exec_run(f"test -d {path}")
    return result.exit_code == 0


def get_file_permissions(container, path: str) -> str:
    """
    Get file permissions from container.

    Args:
        container: Docker container instance
        path: Path to file

    Returns:
        Permission string (e.g., "755", "700")
    """
    result = container.exec_run(f"stat -c '%a' {path}")
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to get permissions: {result.output.decode()}")
    return result.output.decode().strip()


def get_file_owner(container, path: str) -> tuple[str, str]:
    """
    Get file owner and group from container.

    Args:
        container: Docker container instance
        path: Path to file

    Returns:
        Tuple of (owner, group)
    """
    result = container.exec_run(f"stat -c '%U:%G' {path}")
    if result.exit_code != 0:
        raise RuntimeError(f"Failed to get owner: {result.output.decode()}")
    owner_group = result.output.decode().strip()
    owner, group = owner_group.split(":")
    return owner, group
