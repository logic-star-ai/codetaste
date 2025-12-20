"""Docker container utility functions for executing commands and copying files."""
import json
import logging
import os
import tarfile
from io import BytesIO
from typing import Any, List, Optional, cast

from docker.models.containers import Container as DockerContainer


def stream_exec(
    container: DockerContainer,
    cmd: List[str],
    env: Optional[dict] = None,
    stream_logger: Optional[logging.Logger] = None,
) -> str:
    """
    Execute a command in the container and stream its output.

    Args:
        container: Docker container instance
        cmd: Command to execute as a list of strings
        env: Optional environment variables
        stream_logger: Optional logger for output streaming

    Returns:
        Complete output from the command
    """
    if stream_logger is None:
        from refactoring_benchmark.utils.logger import get_logger

        stream_logger = get_logger("bootstrap")

    full_output = []
    exec_instance = container.exec_run(
        cmd=cmd, environment=env or {}, stream=True, tty=True
    )

    acc = ""
    for chunk in cast(Any, exec_instance.output):
        if chunk and isinstance(chunk, bytes):
            decoded = chunk.decode("utf-8", errors="replace")
            acc += decoded
            full_output.append(decoded)
            try:
                json_obj = json.loads(acc)
                stream_logger.info(f"Agent JSON: {json.dumps(json_obj, indent=2)}")
                acc = ""
            except json.JSONDecodeError:
                pass
    return "".join(full_output)


def copy_to_container(container: DockerContainer, src_content: bytes, dst_path: str):
    """
    Copy a file into a container via tar stream.

    Args:
        container: Docker container instance
        src_content: File content as bytes
        dst_path: Destination path inside the container
    """
    stream = BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as tar:
        info = tarfile.TarInfo(name=os.path.basename(dst_path))
        info.size = len(src_content)
        info.mode = 0o755  # Make executable by default
        tar.addfile(info, BytesIO(src_content))
    stream.seek(0)
    container.put_archive(os.path.dirname(dst_path), stream.read())
