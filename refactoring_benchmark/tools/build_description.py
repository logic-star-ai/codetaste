#!/usr/bin/env python3
"""
Build filtered task descriptions from existing descriptions.

Extracts specific sections from source descriptions and generates
new description files with only the requested sections in a standardized format.

Output Format:
    # <Title>
    <Summary content - no header>

    ## Why
    <Why content>

    ## Scope
    <Scope content>

Usage:
    python build_description.py --include title --include summary --include why
    python build_description.py --include title --include summary --output-dir custom_dir
"""

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Supported sections (normalized lowercase for matching)
SUPPORTED_SECTIONS = ["title", "summary", "why", "scope"]


def parse_markdown_sections(content: str) -> Dict[str, Tuple[str, int]]:
    """
    Parse markdown content into sections handling both ATX (#) and Setext (underline) headers.

    Returns dict mapping normalized section names to (content, start_position) tuples.
    The start_position allows us to maintain the original order of sections.

    Special handling for "title":
    - If a section explicitly named "Title" exists, use it
    - Otherwise, the first header (if it's level 1) becomes the title
    """
    sections = {}
    lines = content.split("\n")
    current_section = None
    current_content = []
    position = 0
    first_header = None

    # Special case: Check if first line is plain text title (no header marker)
    # Pattern: "Title text\n\nSummary\n---"
    if (
        len(lines) >= 3
        and lines[0].strip()
        and not lines[0].startswith("#")
        and not lines[0].startswith("**")
        and (lines[1].strip() == "" or lines[1].strip() == "")
        and (
            lines[2].strip().lower() in ["summary", "why", "scope"]
            or (len(lines) >= 4 and re.match(r"^[=-]+\s*$", lines[3]))
        )
    ):
        # Line 0 is an implicit title
        first_header = lines[0].strip()
        # Don't set current_section yet, let normal parsing handle the rest

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check for ATX-style header (# Header)
        atx_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if atx_match:
            # Save previous section
            if current_section is not None:
                sections[current_section] = ("\n".join(current_content).strip(), position)
                position += 1

            # Start new section
            level = len(atx_match.group(1))
            section_name = atx_match.group(2).strip()
            current_section = normalize_section_name(section_name)
            current_content = []

            # Track first level-1 header for implicit title
            if first_header is None and level == 1:
                first_header = section_name

            # Check if next line is decorative dashes/equals (mixed format)
            # Skip them if they exist
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                if re.match(r"^[=-]+\s*$", next_line) and len(next_line.strip()) >= 3:
                    i += 2  # Skip both the header and decorative underline
                    continue

            i += 1
            continue

        # Check for Setext-style header (underlined with = or -)
        # Also handle **Bold** headers with underlines
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            # Check if next line is all = or all -
            if re.match(r"^=+\s*$", next_line):
                # Save previous section
                if current_section is not None:
                    sections[current_section] = ("\n".join(current_content).strip(), position)
                    position += 1

                # Level 1 header (=)
                # Handle both regular text and **Bold** text
                section_name = line.strip()
                # Remove bold markers if present
                section_name = re.sub(r"^\*\*(.*?)\*\*$", r"\1", section_name)
                current_section = normalize_section_name(section_name)
                current_content = []

                # Track first level-1 header for implicit title
                if first_header is None:
                    first_header = section_name

                i += 2  # Skip both the header and underline
                continue
            elif re.match(r"^-+\s*$", next_line) and len(next_line.strip()) >= 3:
                # Save previous section
                if current_section is not None:
                    sections[current_section] = ("\n".join(current_content).strip(), position)
                    position += 1

                # Level 2 header (-)
                # Handle both regular text and **Bold** text
                section_name = line.strip()
                # Remove bold markers if present
                section_name = re.sub(r"^\*\*(.*?)\*\*$", r"\1", section_name)
                current_section = normalize_section_name(section_name)
                current_content = []

                i += 2  # Skip both the header and underline
                continue

        # Regular content line
        if current_section is not None:
            current_content.append(line)
        else:
            # Content before any header (treat as preamble)
            if "preamble" not in sections:
                sections["preamble"] = (line, -1)  # -1 to sort before everything
            else:
                old_content, pos = sections["preamble"]
                sections["preamble"] = (old_content + "\n" + line, pos)

        i += 1

    # Save final section
    if current_section is not None:
        sections[current_section] = ("\n".join(current_content).strip(), position)

    # Handle implicit title: if no explicit "title" section exists,
    # use the first level-1 header as the title
    if "title" not in sections and first_header is not None:
        # The first header has no content, just the header itself
        sections["title"] = (first_header, -2)  # -2 to sort before everything

    return sections


def normalize_section_name(name: str) -> str:
    """
    Normalize section name for matching.
    Converts to lowercase for case-insensitive matching.
    """
    return name.lower().strip()


def get_section_title_from_original(content: str, section_key: str) -> Optional[str]:
    """
    Extract the original formatting of a section header from the content.
    Returns the header in its original case and format.
    """
    lines = content.split("\n")
    section_lower = section_key.lower()

    i = 0
    while i < len(lines):
        line = lines[i]

        # Check ATX-style header
        atx_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if atx_match:
            header_text = atx_match.group(2).strip()
            if header_text.lower() == section_lower:
                # Return just the # header, skip any decorative underlines
                return line
            i += 1
            continue

        # Check Setext-style header (but not if previous line was ATX)
        if i + 1 < len(lines):
            next_line = lines[i + 1]
            if re.match(r"^[=-]+\s*$", next_line) and len(next_line.strip()) >= 3:
                # Make sure this isn't a decorative underline after ATX header
                if i > 0:
                    prev_line = lines[i - 1]
                    if re.match(r"^#{1,6}\s+", prev_line):
                        # Skip - this is decorative
                        i += 1
                        continue

                header_text = line.strip()
                if header_text.lower() == section_lower:
                    # Return both the text and underline
                    return f"{line}\n{next_line}"

        i += 1

    # Fallback: use canonical name with # header
    canonical = section_key.capitalize()
    return f"# {canonical}"


def has_explicit_title_section(content: str) -> bool:
    """Check if the content has an explicit 'Title' section header."""
    lines = content.split("\n")
    for i, line in enumerate(lines):
        # Check ATX-style "# Title"
        if re.match(r"^#\s+Title\s*$", line, re.IGNORECASE):
            return True
        # Check Setext-style "Title\n----"
        if i + 1 < len(lines):
            if re.match(r"^Title\s*$", line, re.IGNORECASE) and re.match(r"^[=-]+\s*$", lines[i + 1]):
                return True
    return False


def build_filtered_description(included_sections: List[str], original_content: str) -> str:
    """
    Build a new description with standardized formatting:
    - Title: # <title text>
    - Summary: <content> (no header)
    - Why: ## Why
    - Scope: ## Scope
    """
    sections = parse_markdown_sections(original_content)

    # Build output in standardized format
    output_parts = []

    # Define the standard order and format
    section_formats = {
        "title": ("# {content}", 0),  # Level 1, no label
        "summary": ("{content}", 1),  # No header at all
        "why": ("## Why\n\n{content}", 2),  # Level 2
        "scope": ("## Scope\n\n{content}", 3),  # Level 2
    }

    # Sort by defined order
    for section_name in ["title", "summary", "why", "scope"]:
        if section_name in included_sections and section_name in sections:
            content, _ = sections[section_name]
            format_str, _ = section_formats[section_name]
            if len(included_sections) == 1:
                format_str = format_str.lstrip("# ")

            if content:  # Only add if content exists
                output_parts.append(format_str.format(content=content))

    return "\n\n".join(output_parts)


def process_instances(
    instances_csv: Path,
    descriptions_dir: Path,
    description_name: str,
    output_base_dir: Path,
    included_sections: List[str],
) -> Tuple[int, int, List[str]]:
    """
    Process all instances from CSV and generate filtered descriptions.

    Returns (success_count, error_count, error_messages).
    """
    success_count = 0
    error_count = 0
    errors = []

    with open(instances_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            owner = row["owner"]
            repo = row["repo"]
            commit_hash = row["commit_hash"]
            short_hash = commit_hash[:8]

            # Source path
            source_desc = descriptions_dir / owner / repo / short_hash / "description.md"

            if not source_desc.exists():
                errors.append(f"Missing description: {source_desc}")
                error_count += 1
                continue

            try:
                # Read source description
                original_content = source_desc.read_text(encoding="utf-8")

                # Build filtered description
                filtered_content = build_filtered_description(included_sections, original_content)

                # Create output directory
                output_dir = output_base_dir / owner / repo / short_hash
                output_dir.mkdir(parents=True, exist_ok=True)

                # Write filtered description
                output_file = output_dir / description_name
                output_file.write_text(filtered_content, encoding="utf-8")

                success_count += 1

            except Exception as e:
                errors.append(f"Error processing {source_desc}: {str(e)}")
                error_count += 1

    return success_count, error_count, errors


def main():
    parser = argparse.ArgumentParser(
        description="Build filtered task descriptions with selected sections in standardized format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Output Format:
  # <Title>
  <Summary content - no header>

  ## Why
  <Why content>

  ## Scope
  <Scope content>

Examples:
  %(prog)s --include title --include summary --include why
  %(prog)s --include title --include summary --output-dir custom_descriptions

Supported sections:
  title, summary, why, scope
        """,
    )

    parser.add_argument(
        "--include",
        action="append",
        dest="sections",
        required=True,
        help="Section to include (can be specified multiple times)",
    )

    parser.add_argument(
        "--output-dir", type=Path, help="Custom output directory name (default: descriptions_{section1}_{section2}_...)"
    )

    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path(__file__).parent.parent.parent / "instances.csv",
        help="Path to instances.csv (default: ./instances.csv)",
    )

    parser.add_argument(
        "--descriptions-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent / "assets" / "descriptions",
        help="Path to source descriptions (default: ./assets/descriptions)",
    )
    parser.add_argument(
        "--description-name",
        type=str,
        default="description.md",
        help="Name of the description file in each instance directory (default: description.md)",
    )

    args = parser.parse_args()

    # Normalize and validate section names
    included_sections = []
    for section in args.sections:
        normalized = normalize_section_name(section)
        if normalized not in SUPPORTED_SECTIONS:
            print(f"Error: Unsupported section '{section}'")
            print(f"Supported sections: {', '.join(SUPPORTED_SECTIONS)}")
            return 1
        included_sections.append(normalized)

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        sections_str = "_".join(included_sections)
        output_dir = Path(__file__).parent.parent.parent / f"descriptions_{sections_str}"

    # Validate inputs
    if not args.instances_csv.exists():
        print(f"Error: instances.csv not found at {args.instances_csv}")
        return 1

    if not args.descriptions_dir.exists():
        print(f"Error: descriptions directory not found at {args.descriptions_dir}")
        return 1

    print("Building filtered descriptions...")
    print(f"  Sections: {', '.join(included_sections)}")
    print(f"  Output: {output_dir}")
    print()

    # Process instances
    success, errors, error_msgs = process_instances(
        args.instances_csv, args.descriptions_dir, args.description_name, output_dir, included_sections
    )

    # Report results
    print(f"Processed {success + errors} instances:")
    print(f"  ✓ Success: {success}")
    if errors > 0:
        print(f"  ✗ Errors: {errors}")
        print()
        print("Error details:")
        for msg in error_msgs[:10]:  # Show first 10 errors
            print(f"  - {msg}")
        if len(error_msgs) > 10:
            print(f"  ... and {len(error_msgs) - 10} more errors")

    print()
    print(f"Filtered descriptions written to: {output_dir}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    exit(main())
