"""Docker container utility functions for executing commands and copying files."""

import json
import logging
import os
import tarfile
import threading
from io import BytesIO
import time
from typing import Any, List, Optional, cast
from refactoring_benchmark.utils.logger import get_logger, setup_logging
import podman
from podman.domain.containers import Container as PodmanContainer
from podman.errors import APIError, NotFound


utils_logger = get_logger("container_utils")

_active_containers: set[PodmanContainer] = set()
_containers_lock = threading.RLock()


def get_local_client(timeout: int = 4000) -> Optional[podman.PodmanClient]:
    """Each process needs its own Podman client connection."""
    c = podman.from_env(timeout=timeout)
    c.ping()
    return c


def is_image_existing(client: podman.PodmanClient, setup_image: str) -> bool:
    """Check if a Podman image exists locally."""
    try:
        client.images.get(setup_image)
        return True
    except:
        return False


def safe_container_run(client: podman.PodmanClient, image, **kwargs) -> PodmanContainer:
    """Retries container creation to handle 'POST operation failed' socket errors."""
    for i in range(1, 5):
        try:
            container: PodmanContainer = client.containers.run(image, **kwargs)
            register_container(container)
            return container
        except Exception as e:
            if i == 4:
                raise
            utils_logger.warning(f"Podman containers.run on {image} failed ({e}), retrying in {2**i}s...")
            time.sleep(2**i)


def register_container(container: PodmanContainer) -> None:
    """Register a container for tracking and automatic cleanup."""
    with _containers_lock:
        _active_containers.add(container)
        utils_logger.debug(
            f"Registered container {container.id[:12]} (total active: {len(_active_containers)}). A process only sees his containers, not parents or siblings."
        )


def unregister_container(container: PodmanContainer) -> None:
    """Remove a container from tracking after cleanup."""
    with _containers_lock:
        _active_containers.discard(container)
        utils_logger.debug(
            f"Unregistered container {container.id[:12]} (total active: {len(_active_containers)}). A process only sees his containers, not parents or siblings."
        )


def cleanup_all_containers() -> None:
    """Clean up all tracked containers. Called on exit or interrupt."""
    with _containers_lock:
        if not _active_containers:
            return

        utils_logger.debug(f"Cleaning up {len(_active_containers)} active container(s)...")
        containers_to_cleanup = list(_active_containers)

        for container in containers_to_cleanup:
            try:
                stop_container(container)
                utils_logger.debug(f"✅ Cleaned up container {container.id[:12]}. {len(_active_containers)} remaining.")
            except Exception as e:
                utils_logger.warning(f"⚠️ Failed to cleanup container {container.id[:12]}: {e}")


def stream_exec(
    container: PodmanContainer,
    cmd: List[str],
    env: Optional[dict] = None,
    stream_logger: Optional[logging.Logger] = None,
    is_json_output: bool = False,
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
        stream_logger = get_logger("bootstrap")

    full_output = []
    # exec_run with stream=True returns (None, iterator) where iterator yields bytes chunks
    exit_code, output_stream = container.exec_run(cmd=cmd, environment=env or {}, stream=True, tty=False)

    acc = ""
    for chunk in cast(Any, output_stream):
        if chunk and isinstance(chunk, bytes):
            decoded = chunk.decode("utf-8", errors="replace")
            acc += decoded
            full_output.append(decoded)
            if is_json_output:
                try:
                    json_obj = json.loads(acc)
                    stream_logger.info(f"Agent JSON: {json.dumps(json_obj, indent=2)}")
                    acc = ""
                except json.JSONDecodeError:
                    pass
            else:
                stream_logger.info(decoded.rstrip())
                acc = ""

    return exit_code, "".join(full_output)


def copy_to_container(container: PodmanContainer, src_content: bytes, dst_path: str):
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


def extract_folder_from_container(container: PodmanContainer, container_path: str, local_dest: str) -> None:
    """
    Extract a folder from a container to the local filesystem.

    Args:
        container: Docker container instance
        container_path: Path to folder inside the container
        local_dest: Local destination directory to extract to

    Raises:
        Exception: If extraction fails
    """
    os.makedirs(local_dest, exist_ok=True)

    bits, stat = container.get_archive(container_path)
    stream = BytesIO()
    for chunk in bits:
        stream.write(chunk)
    stream.seek(0)
    with tarfile.open(fileobj=stream, mode="r") as tar:
        tar.extractall(path=local_dest)


def stop_container(container: PodmanContainer, force: bool = True, auto_unregister: bool = True) -> None:
    """
    Stop and remove a Docker container.

    Args:
        container: Docker container instance
        force: Force removal of the container
        auto_unregister: Automatically unregister from tracking set (default: True)
    """
    with _containers_lock:
        if container not in _active_containers:
            return
        if auto_unregister:
            unregister_container(container)
        try:
            container.stop(timeout=2)
        except (APIError, json.JSONDecodeError) as e:
            pass
        except NotFound:
            return



def podman_timed_exec_bash_logged(
    container: PodmanContainer,
    bash_cmd: str,
    logger: Optional[logging.Logger],
    timeout: Optional[int | str] = None,
    **kwargs,
) -> tuple[int, tuple[bytes | None, bytes | None]]:
    """
    Structured wrapper for executing bash commands with optional timeout.

    Args:
        container: podman.domain.containers.Container object
        bash_cmd: Bash command string to execute
        logger: logging.Logger instance
        timeout: Optional timeout in seconds (uses GNU timeout command)
        **kwargs: Passed to podman_exec_logged (e.g. user, workdir, env)

    Returns:
        tuple: (exit_code, (stdout_bytes, stderr_bytes))
    """
    cmd = ["bash", "-c", bash_cmd]
    if timeout is not None:
        cmd = ["timeout", "--signal=KILL", str(timeout)] + cmd

    exit_code, output = podman_exec_logged(container, cmd, logger, **kwargs)

    if exit_code == 137:
        raise TimeoutError(f"Command timed out after {timeout} seconds: {bash_cmd}")

    return exit_code, output


def podman_exec_logged(
    container: PodmanContainer, cmd: list[str] | str, logger: Optional[logging.Logger], **kwargs
) -> tuple[int, tuple[bytes | None, bytes | None]]:
    """
    Structured wrapper for podman-py container.exec_run.

    Args:
        container: podman.domain.containers.Container object
        cmd: Command string or list
        logger: logging.Logger instance
        **kwargs: Passed to exec_run (e.g. user, workdir, env)
    """
    # Force demux for separate stdout/stderr handling
    kwargs["demux"] = True
    image_name = container.image.tags[0] if container.image.tags else container.image.id
    # Format command for logging
    readable_cmd = " ".join(cmd) if isinstance(cmd, list) else cmd
    if logger is not None:
        logger.info(f"\nContainer '{image_name}' executing: {readable_cmd}")

    ts_start = time.time()
    exit_code, (stdout_bytes, stderr_bytes) = container.exec_run(cmd, **kwargs)
    ts_end = time.time()
    elapsed = ts_end - ts_start
    if logger is not None:
        logger.info(f"\nContainer '{image_name}' command completed in {elapsed:.2f}s.")

    def clean_decode(b: Optional[bytes]) -> str:
        return b.decode("utf-8", errors="replace").strip() if b else ""

    stdout_text = clean_decode(stdout_bytes)
    stderr_text = clean_decode(stderr_bytes)

    # Extract and Log Maybe Truncated Output and Metadata
    stdout_lines = stdout_text.splitlines()
    stderr_lines = stderr_text.splitlines()
    stdout_text_trunc = "\n".join(
        (stdout_lines[:25] + ["... (truncated) ..."] + stdout_lines[-25:]) if len(stdout_lines) > 50 else stdout_lines
    )
    stderr_text_trunc = "\n".join(
        (stderr_lines[:25] + ["... (truncated) ..."] + stderr_lines[-25:]) if len(stderr_lines) > 50 else stderr_lines
    )
    if logger is not None:
        if exit_code == 0:
            logger.info(f"\n[Exit {exit_code:3}] Container '{image_name}' command succeeded (in {elapsed:.2f}s).")
        else:
            logger.error(f"\n[Exit {exit_code:3}] Container '{image_name}' command failed (in {elapsed:.2f}s)")
        if stdout_text:
            logger.debug(f"[{image_name} STDOUT]:\n{stdout_text_trunc}")
        if stderr_text:
            if exit_code != 0:
                logger.error(f"[{image_name} STDERR]:\n{stderr_text_trunc}")
            else:
                logger.warning(f"[{image_name} STDERR (non-fatal)]:\n{stderr_text_trunc}")

    return exit_code, (stdout_bytes, stderr_bytes)


def commit_container(
    container: PodmanContainer,
    image_name: str,
    tag: Optional[str] = None,
    changes: Optional[List[str]] = None,
) -> None:
    """
    Commit a container to a new image using podman-py library.

    Args:
        container: Container to commit
        image_name: Name for the resulting image
        tag: Optional tag (defaults to :latest if None)
        changes: List of Dockerfile instructions to apply (e.g., ["ENTRYPOINT [\"/bin/sh\"]"])

    Raises:
        APIError: If commit fails
    """
    # Build repository and tag
    repository = image_name
    if ":" in image_name and tag is None:
        # Split image_name into repo and tag
        repository, tag = image_name.rsplit(":", 1)
    elif tag is None:
        tag = "latest"

    # Commit the container
    container.commit(repository=repository, tag=tag, changes=changes)
    utils_logger.info(f"Committed container {container.id[:12]} to {repository}:{tag}")


def get_container_storage(container: PodmanContainer) -> dict:
    """
    Get container storage size information using podman-py.

    Args:
        container: Container to inspect

    Returns:
        Dictionary with 'container_id', 'writable_bytes', and 'virtual_bytes'

    Raises:
        APIError: If inspection fails
    """
    # Reload container to get fresh data with size info
    container.reload()

    # Get size info from container attributes
    # The SizeRw field contains the writable layer size
    # The SizeRootFs field contains the total size (virtual size)
    attrs = container.attrs

    size_rw = attrs.get("SizeRw", 0)  # Writable layer size in bytes
    size_rootfs = attrs.get("SizeRootFs", 0)  # Total filesystem size in bytes

    return {
        "container_id": container.id,
        "writable_bytes": size_rw,
        "virtual_bytes": size_rootfs,
    }
