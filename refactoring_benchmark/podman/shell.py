import re
import subprocess
import threading
from typing import List, Optional, Tuple

_shell_lock = threading.RLock()


class PodmanCommandError(Exception):
    """Custom exception for Podman command errors."""

    pass


def run_podman_command(args: list[str], timeout: int = 120) -> Tuple[int, Tuple[str, str]]:
    """
    Runs a Podman command securely and returns the exit code, stdout, and stderr.

    Args:
        args: The Podman sub-commands and arguments as a list (e.g., ["run", "fedora"]).
        timeout: Maximum time to wait for the command to finish.
    Returns:
        A tuple of (returncode, stdout, stderr)
    """
    with _shell_lock:
        # Prepend 'podman' to the argument list
        full_command = ["podman"] + args

        try:
            result = subprocess.run(full_command, check=False, capture_output=True, text=True, timeout=timeout)
            return result.returncode, (result.stdout, result.stderr)

        except subprocess.TimeoutExpired:
            return -1, ("", f"Command timed out after {timeout} seconds.")

def podman_container_storage(container_id: str) -> Optional[dict]:
    """
    Parses 'podman ps -s' to find the storage size of a specific container.
    Returns a dictionary with 'writable' and 'virtual' sizes in bytes.
    """
    # Use --format to get specific columns and avoid header parsing issues
    rc, (stdout, stderr) = run_podman_command(
        ["ps", "-a", "-s", "--filter", f"id={container_id}", "--format", "{{.ID}}\t{{.Size}}"]
    )

    if rc != 0 or not stdout.strip():
        return None

    def parse_to_bytes(size_str: str) -> float:
        """Converts Podman size strings (e.g., '11.9kB') to bytes."""
        units = {"B": 1, "kB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12}
        match = re.match(r"([\d\.]+)\s*([a-zA-Z]+)", size_str)
        if not match:
            return 0.0
        number, unit = match.groups()
        return float(number) * units.get(unit, 1)

    parts = stdout.strip().split("\t")
    if len(parts) < 2:
        return None

    size_info = parts[1]
    # Extract writable and virtual sizes using regex
    size_match = re.search(r"([\d\.]+[a-zA-Z]+)\s*\(virtual\s*([\d\.]+[a-zA-Z]+)\)", size_info)

    if size_match:
        writable_raw, virtual_raw = size_match.groups()
        return {
            "container_id": container_id,
            "writable_bytes": parse_to_bytes(writable_raw),
            "virtual_bytes": parse_to_bytes(virtual_raw),
        }
    raise PodmanCommandError(f"Failed to parse size info for container {container_id}.")


def podman_commit_container(
    container_id: str,
    new_image_name: str,
    tag: Optional[str] = None,
    changes: Optional[List[str]] = None,
    squash: bool = True,
    timeout: int = 8 * 60,
) -> Tuple[int, Tuple[str, str]]:
    """
    Commits a container to a new image with custom metadata changes.

    Args:
        container_id: ID or Name of the source container.
        new_image_name: The name for the resulting image.
        tag: Optional tag (defaults to :latest if None).
        changes: A list of Podman instructions, e.g.,
                 ["ENTRYPOINT [\"python3\", \"main.py\"]", "ENV PORT=8080"]
        squash: Whether to collapse the new layers into one.
    """
    full_image_name = f"{new_image_name}:{tag}" if tag else new_image_name

    args = ["commit"]

    # Apply each change as a separate --change flag
    if changes:
        for change in changes:
            args.extend(["--change", change])

    if squash:
        args.append("--squash")

    args.extend([container_id, full_image_name])

    return run_podman_command(args, timeout=timeout)


if __name__ == "__main__":
    container_id = "put_container_id_here"
    print(podman_container_storage(container_id))
    podman_commit_container(container_id, f"{container_id}_squashed_example", squash=True)
