"""Container execution helper for inference steps."""

import logging
import os
from pathlib import Path
from typing import Optional

import podman
from podman.domain.containers import Container as PodmanContainer

from refactoring_benchmark.inference.models import ExecutionContext, InferenceConfig
from refactoring_benchmark.inference.utils import (
    create_fallback_inference_metadata,
    output_container_logs,
)
from refactoring_benchmark.podman import utils as podman_utils
from refactoring_benchmark.utils.models import InstanceRow


class ContainerExecutor:
    """Runs containers for plan/multiplan/inference steps."""

    def __init__(
        self,
        instance: InstanceRow,
        config: InferenceConfig,
        output_dir: Path,
        logger: logging.Logger,
        client: podman.PodmanClient,
    ) -> None:
        self.instance = instance
        self.config = config
        self.output_dir = output_dir
        self.logger = logger
        self.client = client
        self.container: Optional[PodmanContainer] = None

    def run(
        self,
        mode: str,
        timeout: int,
        temp_dir: Path,
        context: ExecutionContext,
    ) -> bool:
        """
        Execute a container step (plan, multiplan, or inference).

        Args:
            mode: Container execution mode ("plan", "multiplan", or "inference")
            timeout: Timeout in seconds for this step
            temp_dir: Temporary directory to mount as /task_description
            context: Execution context for description_type metadata

        Returns:
            True if container executed without errors, False otherwise
        """
        self.logger.info(f"Starting {mode} step for {self.instance.display_path}")
        self.logger.info(f"  Image: {self.instance.runtime_image}")
        self.logger.info(f"  Timeout: {timeout}s")

        env = {
            **self.config.env_vars,
            "DESCRIPTION_TYPE": self.config.description_type,
            "MODE": self.config.mode,
            "TIMEOUT": str(timeout),
        }

        try:
            self.container = podman_utils.safe_container_run(
                self.client,
                self.instance.runtime_image,
                command=[mode],
                detach=True,
                environment=env,
                volumes={
                    str(self.config.agent_dir): {"bind": "/agent", "mode": "rw"},
                    str(self.output_dir): {"bind": "/output", "mode": "rw"},
                    str(temp_dir): {
                        "bind": "/task_description",
                        "extended_mode": ["rw", "z"],
                    },
                    os.path.abspath("./entrypoint.sh"): {
                        "bind": "/usr/local/bin/entrypoint.sh",
                        "extended_mode": ["ro", "z"],
                    },
                },
                network_mode="host",
                working_dir="/testbed",
                remove=False,
                nano_cpus=int(8e9),
            )

            try:
                self.container.wait(timeout=timeout)
            except Exception as e:
                self.logger.error(f"{mode.capitalize()} step timed out: {e}")
                finish_reason = self._get_finish_reason_for_mode(mode)
                create_fallback_inference_metadata(
                    self.output_dir,
                    finish_reason,
                    description_type=context.description_type,
                    mode=context.mode,
                    additional={"error": f"{mode.capitalize()} container timed out: {str(e)}"},
                )
                return False

            log_file = f"{mode}.out"
            output_container_logs(self.container, self.output_dir / log_file, self.logger)
            return True

        except Exception as e:
            self.logger.error(f"{mode.capitalize()} step execution failed: {e}")
            finish_reason = "error"
            create_fallback_inference_metadata(
                self.output_dir,
                finish_reason,
                description_type=context.description_type,
                mode=context.mode,
                additional={"error": f"{mode.capitalize()} step execution failed: {str(e)}"},
            )
            return False
        finally:
            self._container_cleanup()

    def _get_finish_reason_for_mode(self, mode: str) -> str:
        """Get the appropriate finish reason for a given mode."""
        if mode == "plan":
            return "error_planmode"
        if mode == "multiplan":
            return "error_multiplan"
        return "timeout"

    def _container_cleanup(self) -> None:
        """Clean up container after execution."""
        if self.container:
            podman_utils.stop_container(self.container)
            try:
                self.container.remove(force=True)
            except Exception as e:
                self.logger.warning(
                    f"Failed to remove container [{self.instance.id}]. Probably already removed. Error: {e}"
                )
            try:
                podman_utils.reset_output_ownership(self.output_dir)
            except Exception as e:
                self.logger.warning(f"Failed to reset output ownership for {self.output_dir}. Error: {e}")
            self.container = None
