"""Generate a guessable description markdown file for a given agent.

This script creates a comprehensive markdown file containing:
- True descriptions from assets/descriptions/
- Best plans selected by the judge
- Last 4 lines of judge output

For each instance in instances.csv.
"""

import argparse
import csv
import json
from pathlib import Path


def get_instance_identifier(owner: str, repo: str, commit_hash: str) -> str:
    """Get the instance identifier in format: owner/repo/commit_hash[:8]"""
    return f"{owner}/{repo}/{commit_hash[:8]}"


def read_true_description(owner: str, repo: str, commit_hash: str, base_dir: Path) -> str:
    """Read the true description from assets/descriptions/"""
    desc_path = base_dir / "assets" / "descriptions" / owner / repo / commit_hash[:8] / "description.md"

    if not desc_path.exists():
        return f"**[Missing]** Description file not found at: {desc_path}"

    try:
        return desc_path.read_text(encoding="utf-8")
    except Exception as e:
        return f"**[Error]** Failed to read description: {e}"


def read_open_description(owner: str, repo: str, commit_hash: str, base_dir: Path) -> str:
    """Read the open description from assets/descriptions/ with newlines removed"""
    desc_path = base_dir / "assets" / "descriptions" / owner / repo / commit_hash[:8] / "open_description.md"

    if not desc_path.exists():
        return "[Missing open_description.md]"

    try:
        content = desc_path.read_text(encoding="utf-8")
        # Remove all newlines and extra whitespace
        return " ".join(content.split())
    except Exception as e:
        return f"[Error reading open_description.md: {e}]"


def read_best_plan(owner: str, repo: str, commit_hash: str, agent_id: str, output_dir: Path) -> str:
    """Read the best plan according to the judge output"""
    agent_output_dir = output_dir / owner / repo / commit_hash[:8] / agent_id

    # Check if agent output directory exists
    if not agent_output_dir.exists():
        return f"**[Missing]** Agent output directory not found at: {agent_output_dir}"

    # Read multiplan_metadata.json to get selected plan index
    metadata_path = agent_output_dir / "multiplan_metadata.json"
    if not metadata_path.exists():
        return f"**[Missing]** multiplan_metadata.json not found at: {metadata_path}"

    try:
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        selected_index = metadata.get("selected_plan_index")
        if selected_index is None:
            return "**[Error]** No selected_plan_index found in multiplan_metadata.json"

        # Read the corresponding plan file
        plan_path = agent_output_dir / "refactoring_plans" / f"refactoring_plan{selected_index}.md"
        if not plan_path.exists():
            return f"**[Missing]** Plan file not found at: {plan_path}"

        plan_content = plan_path.read_text(encoding="utf-8")
        return f"**Selected Plan {selected_index}:**\n\n{plan_content}"

    except json.JSONDecodeError as e:
        return f"**[Error]** Failed to parse multiplan_metadata.json: {e}"
    except Exception as e:
        return f"**[Error]** Failed to read best plan: {e}"


def read_last_4_lines_judge_out(owner: str, repo: str, commit_hash: str, agent_id: str, output_dir: Path) -> str:
    """Read the last 4 lines of judge.out"""
    judge_path = output_dir / owner / repo / commit_hash[:8] / agent_id / "judge.out"

    if not judge_path.exists():
        return f"**[Missing]** judge.out not found at: {judge_path}"

    try:
        with open(judge_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Get last 4 lines
        last_lines = lines[-4:] if len(lines) >= 4 else lines
        return "".join(last_lines).rstrip()

    except Exception as e:
        return f"**[Error]** Failed to read judge.out: {e}"


def generate_guessable_description(agent_id: str, base_dir: Path, output_dir: Path, instances_csv: Path) -> Path:
    """Generate the guessable description markdown file for the given agent.

    Args:
        agent_id: The agent identifier (e.g., "codex-v0.77.0-gpt-5.2")
        base_dir: Base directory of the repo
        output_dir: Output directory containing agent results (e.g., outputs/open/multiplan)
        instances_csv: Path to instances.csv

    Returns:
        Path to the generated markdown file
    """
    output_file = base_dir / f"guessable_description_{agent_id}.md"

    print(f"Generating guessable description for agent: {agent_id}")
    print(f"Output file: {output_file}")

    with open(instances_csv, "r", encoding="utf-8") as csvfile, open(output_file, "w", encoding="utf-8") as outfile:

        reader = csv.DictReader(csvfile)
        instance_count = 0

        for row in reader:
            owner = row["owner"]
            repo = row["repo"]
            commit_hash = row["commit_hash"]

            instance_id = get_instance_identifier(owner, repo, commit_hash)
            instance_count += 1

            print(f"Processing instance {instance_count}: {instance_id}")

            # Write instance separator
            outfile.write("=" * 80 + "\n")
            outfile.write(f"{instance_id}\n")
            outfile.write("=" * 80 + "\n\n")

            # Part 1: True Description
            outfile.write("# Part 1: True Description\n\n")
            true_desc = read_true_description(owner, repo, commit_hash, base_dir)
            outfile.write(true_desc)
            outfile.write("\n\n")

            # Part 2: Best Plan according to judge (with open description in heading)
            open_desc = read_open_description(owner, repo, commit_hash, base_dir)
            outfile.write(
                f"# Part 2: Best Plan according to the judge output : (derived from Open Description : {open_desc})\n\n"
            )
            best_plan = read_best_plan(owner, repo, commit_hash, agent_id, output_dir)
            outfile.write(best_plan)
            outfile.write("\n\n")

            # Part 3: Last 4 lines of judge.out
            outfile.write("# Part 3: Last 4 lines of judge.out\n\n")
            outfile.write("```\n")
            last_lines = read_last_4_lines_judge_out(owner, repo, commit_hash, agent_id, output_dir)
            outfile.write(last_lines)
            outfile.write("\n```\n\n")

    print(f"\nSuccessfully generated guessable description for {instance_count} instances")
    print(f"Output written to: {output_file}")

    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Generate guessable description markdown for a given agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python -m refactoring_benchmark.tools.generate_guessable_description --agent codex-v0.77.0-gpt-5.2
    python -m refactoring_benchmark.tools.generate_guessable_description --agent claude-code-v2.0.76-sonnet45 --output-dir outputs/open/multiplan
        """,
    )

    parser.add_argument("--agent", required=True, help="Agent ID (e.g., 'codex-v0.77.0-gpt-5.2')")

    parser.add_argument(
        "--output-dir",
        default="outputs/open/multiplan",
        help="Output directory containing agent results (default: outputs/open/multiplan)",
    )

    parser.add_argument(
        "--instances-csv", default="instances.csv", help="Path to instances.csv (default: instances.csv in repo root)"
    )

    parser.add_argument("--base-dir", default=".", help="Base directory of the repository (default: current directory)")

    args = parser.parse_args()

    base_dir = Path(args.base_dir).resolve()
    output_dir = base_dir / args.output_dir
    instances_csv = base_dir / args.instances_csv

    # Validate paths
    if not instances_csv.exists():
        print(f"Error: instances.csv not found at: {instances_csv}")
        return 1

    if not output_dir.exists():
        print(f"Warning: Output directory not found at: {output_dir}")
        print("Proceeding anyway - missing data will be noted in the output")

    # Generate the file
    try:
        generate_guessable_description(args.agent, base_dir, output_dir, instances_csv)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
