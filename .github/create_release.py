#!/usr/bin/env python3
"""Create CodeTaste release archives.

The benchmark archive is a normal zip file. The precomputed outputs archive is
created with the system `zip` utility so it matches the split-zip workflow in
README.md and .github/download_outputs.sh.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

DEFAULT_SETTINGS = (
    ("instructed", "direct"),
    ("open", "direct"),
    ("open", "plan"),
    ("open", "multiplan"),
)
EXCLUDED_DISCOVERY_AGENTS = frozenset({"golden_agent", "null_agent"})
REQUIRED_CSV_COLUMNS = ("owner", "repo", "commit_hash", "golden_commit_hash", "category", "language")
BENCHMARK_ARCHIVE_NAME = "codetaste100.zip"
OUTPUTS_ARCHIVE_NAME = "outputs.zip"


@dataclass(frozen=True)
class Instance:
    owner: str
    repo: str
    commit_hash: str
    golden_commit_hash: str
    category: str
    language: str

    @property
    def short_hash(self) -> str:
        return self.commit_hash[:8]

    @property
    def path_parts(self) -> tuple[str, str, str]:
        return (self.owner, self.repo, self.short_hash)

    @property
    def display_path(self) -> str:
        return "/".join(self.path_parts)


@dataclass(frozen=True)
class ArchiveEntry:
    source: Path
    arcname: Path


class ReleaseError(Exception):
    """Raised when release inputs are incomplete or unsafe to package."""


def parse_args(argv: Sequence[str], repo_root: Path) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create CodeTaste benchmark release archives.")
    parser.add_argument("--repo-root", type=Path, default=repo_root, help="Repository root.")
    parser.add_argument("--release-dir", type=Path, default=Path("release"), help="Directory for final zip files.")
    parser.add_argument("--instances-csv", type=Path, default=Path("instances.csv"), help="Benchmark CSV to package.")
    parser.add_argument(
        "--expected-instances",
        type=int,
        default=100,
        help="Expected number of data rows in instances.csv.",
    )
    parser.add_argument(
        "--agent",
        action="append",
        dest="agents",
        help="Agent id to include in outputs.zip. Repeat to include multiple agents.",
    )
    parser.add_argument(
        "--expected-agents",
        type=int,
        default=5,
        help="Expected number of non-pseudo agents in outputs.zip.",
    )
    parser.add_argument(
        "--setting",
        action="append",
        dest="settings",
        help="Output setting to include as <description_type>/<mode>. Repeat to override defaults.",
    )
    parser.add_argument(
        "--split-size",
        default="1g",
        help="Split size passed to `zip -s` for outputs.zip.",
    )
    parser.add_argument(
        "--archive",
        choices=("all", "benchmark", "outputs"),
        default="all",
        help="Which archive family to create.",
    )
    parser.add_argument("--dry-run", action="store_true", default=True, help="Validate and print actions only.")
    parser.add_argument("--live", action="store_false", dest="dry_run", help="Actually create release archives.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing release archive files.")
    parser.add_argument("--yes", action="store_true", help="Skip interactive confirmations.")
    return parser.parse_args(argv)


def resolve_under_repo(repo_root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (repo_root / path).resolve()


def load_instances(instances_csv: Path, expected_instances: int) -> list[Instance]:
    if not instances_csv.is_file():
        raise ReleaseError(f"instances.csv not found: {instances_csv}")

    with instances_csv.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing_columns = [column for column in REQUIRED_CSV_COLUMNS if column not in fieldnames]
        if missing_columns:
            raise ReleaseError(f"{instances_csv} is missing required columns: {', '.join(missing_columns)}")

        instances = [
            Instance(
                owner=row["owner"],
                repo=row["repo"],
                commit_hash=row["commit_hash"],
                golden_commit_hash=row["golden_commit_hash"],
                category=row["category"],
                language=row["language"],
            )
            for row in reader
        ]

    if len(instances) != expected_instances:
        raise ReleaseError(
            f"{instances_csv} contains {len(instances)} data rows; expected {expected_instances}. "
            "Use --expected-instances only if this release intentionally differs."
        )

    seen: set[tuple[str, str, str]] = set()
    duplicates: list[str] = []
    for instance in instances:
        if instance.path_parts in seen:
            duplicates.append(instance.display_path)
        seen.add(instance.path_parts)
    if duplicates:
        raise ReleaseError(f"Duplicate instances in CSV: {', '.join(duplicates[:10])}")

    return instances


def parse_settings(raw_settings: Sequence[str] | None) -> tuple[tuple[str, str], ...]:
    if raw_settings is None:
        return DEFAULT_SETTINGS

    settings: list[tuple[str, str]] = []
    for raw_setting in raw_settings:
        parts = raw_setting.split("/")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ReleaseError(f"Invalid setting {raw_setting!r}; expected <description_type>/<mode>.")
        settings.append((parts[0], parts[1]))

    return tuple(settings)


def require_path(path: Path, missing: list[str]) -> None:
    if not path.exists():
        missing.append(str(path))


def instance_base(root: Path, instance: Instance) -> Path:
    return root.joinpath(*instance.path_parts)


def collect_benchmark_entries(repo_root: Path, instances_csv: Path, instances: Sequence[Instance]) -> list[ArchiveEntry]:
    missing: list[str] = []
    entries: list[ArchiveEntry] = [
        ArchiveEntry(instances_csv, Path("instances.csv")),
        ArchiveEntry(repo_root / "assets" / "default.semgrepignore", Path("assets/default.semgrepignore")),
    ]

    require_path(entries[0].source, missing)
    require_path(entries[1].source, missing)

    for instance in instances:
        description_dir = instance_base(repo_root / "assets" / "descriptions", instance)
        diff_dir = instance_base(repo_root / "assets" / "diffs", instance)
        rules_dir = instance_base(repo_root / "assets" / "rules", instance)
        instance_image_dir = instance_base(repo_root / "instance_images", instance)
        pseudo_output_dir = instance_base(repo_root / "outputs" / "pseudo_agents" / "direct", instance)
        baseline_dir = instance_base(repo_root / "baseline_results", instance)

        required_files = (
            description_dir / "description.md",
            description_dir / "open_description.md",
            diff_dir / "golden.diff",
            rules_dir / "rules_positive.yml",
            rules_dir / "rules_negative.yml",
            baseline_dir / "golden_agent.jsonl",
            baseline_dir / "null_agent.jsonl",
        )
        for required_file in required_files:
            require_path(required_file, missing)
            entries.append(ArchiveEntry(required_file, required_file.relative_to(repo_root)))

        for required_dir in (instance_image_dir, pseudo_output_dir):
            require_path(required_dir, missing)
            entries.append(ArchiveEntry(required_dir, required_dir.relative_to(repo_root)))

    if missing:
        raise ReleaseError("Missing benchmark release inputs:\n" + "\n".join(f"  - {path}" for path in missing[:50]))

    return entries


def output_agent_dir(repo_root: Path, setting: tuple[str, str], instance: Instance, agent: str) -> Path:
    description_type, mode = setting
    return repo_root.joinpath("outputs", description_type, mode, *instance.path_parts, agent)


def has_evaluation_result(agent_dir: Path) -> bool:
    return (agent_dir / "evaluation" / "evaluation_result.json").is_file()


def discover_agents(repo_root: Path, settings: Sequence[tuple[str, str]], instances: Sequence[Instance]) -> list[str]:
    discovered: set[str] | None = None

    for setting in settings:
        for instance in instances:
            instance_dir = repo_root.joinpath("outputs", setting[0], setting[1], *instance.path_parts)
            if not instance_dir.is_dir():
                raise ReleaseError(f"Missing output instance directory: {instance_dir}")

            agents_here = {
                child.name
                for child in instance_dir.iterdir()
                if child.is_dir() and child.name not in EXCLUDED_DISCOVERY_AGENTS and has_evaluation_result(child)
            }
            discovered = agents_here if discovered is None else discovered & agents_here

    return sorted(discovered or set())


def validate_agents(agents: Sequence[str], expected_agents: int) -> list[str]:
    unique_agents = sorted(set(agents))
    if len(unique_agents) != len(agents):
        raise ReleaseError("Agent list contains duplicates.")
    if len(unique_agents) != expected_agents:
        raise ReleaseError(
            f"Selected {len(unique_agents)} agents; expected {expected_agents}. "
            "Use --agent or --expected-agents if this release intentionally differs."
        )
    return unique_agents


def collect_output_dirs(
    repo_root: Path,
    settings: Sequence[tuple[str, str]],
    instances: Sequence[Instance],
    agents: Sequence[str],
) -> list[Path]:
    missing: list[str] = []
    output_dirs: list[Path] = []

    for setting in settings:
        for instance in instances:
            for agent in agents:
                agent_dir = output_agent_dir(repo_root, setting, instance, agent)
                if not has_evaluation_result(agent_dir):
                    missing.append(str(agent_dir / "evaluation" / "evaluation_result.json"))
                output_dirs.append(agent_dir)

    if missing:
        raise ReleaseError("Missing selected output evaluations:\n" + "\n".join(f"  - {path}" for path in missing[:50]))

    return sorted(output_dirs)


def iter_entry_files(entry: ArchiveEntry) -> list[tuple[Path, Path]]:
    if entry.source.is_file():
        return [(entry.source, entry.arcname)]

    files: list[tuple[Path, Path]] = []
    for source_file in sorted(path for path in entry.source.rglob("*") if path.is_file()):
        files.append((source_file, entry.arcname / source_file.relative_to(entry.source)))
    return files


def create_benchmark_zip(archive_path: Path, entries: Sequence[ArchiveEntry]) -> None:
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in entries:
            for source_file, arcname in iter_entry_files(entry):
                archive.write(source_file, arcname.as_posix())


def existing_output_archives(release_dir: Path) -> list[Path]:
    existing = []
    for candidate in [release_dir / OUTPUTS_ARCHIVE_NAME, *sorted(release_dir.glob("outputs.z[0-9][0-9]"))]:
        if candidate.exists():
            existing.append(candidate)
    return existing


def existing_archives(release_dir: Path) -> list[Path]:
    existing = []
    benchmark_archive = release_dir / BENCHMARK_ARCHIVE_NAME
    if benchmark_archive.exists():
        existing.append(benchmark_archive)
    existing.extend(existing_output_archives(release_dir))
    return existing


def selected_existing_archives(release_dir: Path, archive: str) -> list[Path]:
    existing = []
    benchmark_archive = release_dir / BENCHMARK_ARCHIVE_NAME
    if archive in {"all", "benchmark"} and benchmark_archive.exists():
        existing.append(benchmark_archive)
    if archive in {"all", "outputs"}:
        existing.extend(existing_output_archives(release_dir))
    return existing


def confirm(prompt: str, yes: bool) -> None:
    if yes:
        print(f"[confirmed by --yes] {prompt}")
        return

    answer = input(f"{prompt} Type 'yes' to continue: ")
    if answer != "yes":
        raise ReleaseError("Aborted by user.")


def create_outputs_zip(repo_root: Path, release_dir: Path, output_dirs: Sequence[Path], split_size: str) -> None:
    zip_binary = shutil.which("zip")
    if zip_binary is None:
        raise ReleaseError("The `zip` utility is required to create split outputs archives.")

    zip_input = "".join(f"{output_dir.relative_to(repo_root).as_posix()}\n" for output_dir in output_dirs)
    command = [zip_binary, "-r", "-s", split_size, str(release_dir / OUTPUTS_ARCHIVE_NAME), "-@"]
    subprocess.run(command, cwd=repo_root, check=True, input=zip_input, text=True)


def print_plan(
    release_dir: Path,
    dry_run: bool,
    archive: str,
    settings: Sequence[tuple[str, str]],
    agents: Sequence[str],
    instances: Sequence[Instance],
    benchmark_entries: Sequence[ArchiveEntry] | None,
    output_dirs: Sequence[Path] | None,
) -> None:
    mode = "DRY RUN" if dry_run else "LIVE"
    print("-------------------------------------------------------")
    print("CodeTaste release archive builder")
    print(f"Mode: {mode}")
    print(f"Release directory: {release_dir}")
    print(f"Archive selection: {archive}")
    print(f"Instances: {len(instances)}")
    if benchmark_entries is not None:
        print(f"Benchmark archive: {release_dir / BENCHMARK_ARCHIVE_NAME}")
        benchmark_file_count = sum(len(iter_entry_files(entry)) for entry in benchmark_entries)
        print(f"Benchmark archive input roots: {len(benchmark_entries)}")
        print(f"Benchmark archive files after directory expansion: {benchmark_file_count}")
    if output_dirs is not None:
        print(f"Outputs archive: {release_dir / OUTPUTS_ARCHIVE_NAME}")
        print(f"Output agent directories: {len(output_dirs)}")
        print("Settings:")
        for description_type, mode_name in settings:
            print(f"  - {description_type}/{mode_name}")
        print("Agents:")
        for agent in agents:
            print(f"  - {agent}")
    print("-------------------------------------------------------")


def remove_existing(paths: Sequence[Path]) -> None:
    for path in paths:
        path.unlink()


def main(argv: Sequence[str]) -> int:
    repo_root = Path(__file__).resolve().parents[1]
    args = parse_args(argv, repo_root)
    repo_root = args.repo_root.resolve()
    instances_csv = resolve_under_repo(repo_root, args.instances_csv)
    release_dir = resolve_under_repo(repo_root, args.release_dir)

    try:
        settings = parse_settings(args.settings)
        instances = load_instances(instances_csv, args.expected_instances)
        benchmark_entries = (
            collect_benchmark_entries(repo_root, instances_csv, instances)
            if args.archive in {"all", "benchmark"}
            else None
        )
        agents = (
            validate_agents(args.agents or discover_agents(repo_root, settings, instances), args.expected_agents)
            if args.archive in {"all", "outputs"}
            else []
        )
        output_dirs = (
            collect_output_dirs(repo_root, settings, instances, agents) if args.archive in {"all", "outputs"} else None
        )

        print_plan(release_dir, args.dry_run, args.archive, settings, agents, instances, benchmark_entries, output_dirs)

        if args.dry_run:
            print("Dry run only. Re-run with --live to create archives.")
            return 0

        confirm("Confirm the settings above are the intended release settings.", args.yes)
        confirm("Confirm the agent list above is complete and correct.", args.yes)

        existing = selected_existing_archives(release_dir, args.archive)
        if existing and not args.overwrite:
            raise ReleaseError(
                "Release archive files already exist:\n"
                + "\n".join(f"  - {path}" for path in existing)
                + "\nUse --overwrite to replace them."
            )
        if existing:
            confirm(f"Confirm replacement of {len(existing)} existing release archive file(s).", args.yes)

        confirm(f"Create selected release zip(s) in {release_dir}.", args.yes)

        release_dir.mkdir(parents=True, exist_ok=True)
        remove_existing(existing)
        if benchmark_entries is not None:
            create_benchmark_zip(release_dir / BENCHMARK_ARCHIVE_NAME, benchmark_entries)
        if output_dirs is not None:
            create_outputs_zip(repo_root, release_dir, output_dirs, args.split_size)

        print("Done.")
        return 0
    except ReleaseError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
