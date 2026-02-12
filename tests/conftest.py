"""Pytest fixtures for testing."""

import podman
import pytest
from podman.domain.containers import Container as PodmanContainer

BASE_IMAGE = "benchmark/benchmark-base-all"

@pytest.fixture(scope="session")
def podman_client():
    """Provide a Podman client for the test session."""
    client = podman.from_env()
    yield client
    client.close()


@pytest.fixture
def base_container(podman_client):
    """Provide a running base container for tests."""
    container: PodmanContainer = podman_client.containers.run(
        BASE_IMAGE,
        command=["sleep", "300"],
        detach=True,
        remove=False,
    )
    yield container
    try:
        container.stop(timeout=1)
    except Exception:
        pass
    try:
        container.remove(force=True)
    except Exception:
        pass
