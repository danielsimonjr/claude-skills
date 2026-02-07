#!/usr/bin/env python3
"""
sync_skills_table.py - Regenerate the skills inventory table in CLAUDE.md.

Scans all skill directories for SKILL.md files, parses their YAML frontmatter,
and updates the skills table in CLAUDE.md to match.

Usage:
    python scripts/sync_skills_table.py              # dry-run (print table)
    python scripts/sync_skills_table.py --write      # update CLAUDE.md in place
"""

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"

# Directories to skip when scanning
SKIP_DIRS = {".git", "__pycache__", "node_modules", "scripts", ".venv", "venv"}


def parse_frontmatter(skill_md_path: Path) -> dict:
    """Parse YAML frontmatter from a SKILL.md file."""
    text = skill_md_path.read_text(encoding="utf-8")

    # Match --- delimited frontmatter
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}

    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


def discover_skills() -> list[dict]:
    """Discover all skills and return their metadata."""
    skills = []

    for entry in sorted(REPO_ROOT.iterdir()):
        if not entry.is_dir() or entry.name in SKIP_DIRS or entry.name.startswith("."):
            continue

        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(skill_md)
        if not fm.get("name"):
            continue

        skills.append({
            "directory": entry.name,
            "name": fm.get("name", ""),
            "description": fm.get("description", ""),
        })

    return skills


def generate_table(skills: list[dict]) -> str:
    """Generate a markdown table from skill metadata."""
    lines = [
        "| Directory | Skill Name | Description |",
        "|-----------|-----------|-------------|",
    ]

    for s in skills:
        desc = s["description"]
        # Truncate long descriptions for table readability
        if len(desc) > 120:
            desc = desc[:117] + "..."
        lines.append(f"| `{s['directory']}/` | {s['name']} | {desc} |")

    return "\n".join(lines)


def update_claude_md(table: str) -> bool:
    """Replace the skills table in CLAUDE.md. Returns True if changed."""
    if not CLAUDE_MD.exists():
        print(f"CLAUDE.md not found at {CLAUDE_MD}", file=sys.stderr)
        return False

    content = CLAUDE_MD.read_text(encoding="utf-8")

    # Find the skills table between markers or between the header and next section
    # Look for a markdown table after "## Skills Inventory" or similar header
    pattern = re.compile(
        r"(##\s+Skills\s+Inventory[^\n]*\n\n)"  # Header
        r"(\|.*?\|(?:\n\|.*?\|)*)",               # Table
        re.IGNORECASE,
    )

    match = pattern.search(content)
    if not match:
        print("Could not find skills inventory table in CLAUDE.md", file=sys.stderr)
        return False

    old_table = match.group(2)
    if old_table.strip() == table.strip():
        print("Skills table is already up to date.", file=sys.stderr)
        return False

    new_content = content[: match.start(2)] + table + content[match.end(2) :]
    CLAUDE_MD.write_text(new_content, encoding="utf-8")
    return True


def main():
    write_mode = "--write" in sys.argv

    skills = discover_skills()
    if not skills:
        print("No skills found.", file=sys.stderr)
        sys.exit(1)

    table = generate_table(skills)

    if write_mode:
        if update_claude_md(table):
            print(f"Updated CLAUDE.md with {len(skills)} skills.")
        else:
            print("No changes needed.")
    else:
        print(f"Found {len(skills)} skills:\n")
        print(table)
        print(f"\nRun with --write to update CLAUDE.md")


if __name__ == "__main__":
    main()
