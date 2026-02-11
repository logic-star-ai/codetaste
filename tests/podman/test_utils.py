"""Tests for podman utility functions."""

import logging
from io import BytesIO
import tarfile
import tempfile
from pathlib import Path
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


def _build_tar(member_name: str, content: bytes) -> tarfile.TarFile:
    stream = BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as tar:
        info = tarfile.TarInfo(name=member_name)
        info.size = len(content)
        tar.addfile(info, BytesIO(content))
    stream.seek(0)
    return tarfile.open(fileobj=stream, mode="r")


def test_safe_extractall_allows_normal_paths():
    with tempfile.TemporaryDirectory() as tmpdir:
        tar = _build_tar("nested/file.txt", b"ok")
        podman_utils._safe_extractall(tar, tmpdir)
        extracted = Path(tmpdir) / "nested" / "file.txt"
        assert extracted.exists()
        assert extracted.read_bytes() == b"ok"


def test_safe_extractall_blocks_path_traversal():
    with tempfile.TemporaryDirectory() as tmpdir:
        tar = _build_tar("../escape.txt", b"nope")
        with pytest.raises(ValueError, match="Unsafe path in tar"):
            podman_utils._safe_extractall(tar, tmpdir)
