"""Tests for podman utility functions."""

import logging
import pytest
from podman.domain.containers import Container as PodmanContainer

import refactoring_benchmark.podman.utils as podman_utils


logger = logging.getLogger("test_podman_utils")


def test_podman_timed_exec_bash_logged_timeout(base_container: PodmanContainer):
    """Test that podman_timed_exec_bash_logged raises TimeoutError when command times out."""
    # Command that sleeps longer than the timeout
    with pytest.raises(TimeoutError, match="Command timed out after 1 seconds"):
        podman_utils.podman_timed_exec_bash_logged(
            base_container,
            "sleep 10",
            logger,
            timeout=1,
        )
