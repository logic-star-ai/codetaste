"""Centralized image naming configuration."""

from __future__ import annotations

import os
from typing import Optional

DEFAULT_IMAGE_REPOSITORY = "ghcr.io/logic-star-ai/codetaste"


def _get_env(name: str) -> str:
    return os.getenv(name, "").strip()


def image_repository() -> str:
    return _get_env("CODETASTE_IMAGE_REPOSITORY") or DEFAULT_IMAGE_REPOSITORY


def image_with_tag(image: str, tag: Optional[str]) -> str:
    return f"{image}:{tag}" if tag else image


def base_image_tag() -> str:
    return _get_env("CODETASTE_BASE_IMAGE_TAG") or "latest"


def instance_image_tag() -> Optional[str]:
    value = _get_env("CODETASTE_INSTANCE_IMAGE_TAG")
    return value or None


def base_image_name(language: str) -> str:
    return image_with_tag(f"{image_repository()}/benchmark-base-{language}", base_image_tag())


def base_image_all() -> str:
    return base_image_name("all")


def instance_image_identifier(instance_id: str) -> str:
    return f"{image_repository()}/{instance_id}"


def instance_setup_image(instance_id: str) -> str:
    return image_with_tag(f"{image_repository()}/{instance_id}__setup", instance_image_tag())


def instance_runtime_image(instance_id: str) -> str:
    return image_with_tag(f"{image_repository()}/{instance_id}__runtime", instance_image_tag())
