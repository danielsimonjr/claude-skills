---
name: skill-validator
description: Validates Claude Code skill directories for correct structure. Use automatically when creating or editing skills in this repository to ensure SKILL.md has valid YAML frontmatter (name, description), references resolve, and directory conventions are followed.
user-invocable: false
---

# Skill Validator

Validates that skills in this repository follow the required structure and conventions.

## Validation Checks

When a skill directory is created or modified, run these checks:

### 1. SKILL.md Exists and Has Valid Frontmatter

Every skill directory MUST contain a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name-here
description: One-line description of what the skill does and when to use it.
---
```

**Required fields:**
- `name` — lowercase, hyphenated identifier (must match or relate to directory name)
- `description` — non-empty string that tells Claude Code when to activate the skill

**Validation rules:**
- Frontmatter must be delimited by `---` on its own line
- `name` must not be empty
- `description` must not be empty and should be at least 20 characters
- `description` should start with an action verb or "Use when..." pattern for effective triggering

### 2. Directory Structure

Recommended layout (only SKILL.md is required):

```
skill-name/
├── SKILL.md          # REQUIRED - skill definition
├── README.md         # Recommended - human-readable docs
├── references/       # Optional - supporting materials
└── examples/         # Optional - worked examples
```

### 3. Internal References Resolve

If SKILL.md contains references to other files using `<filename.md>` syntax or `[text](path)` links, verify the referenced files exist relative to the skill directory.

### 4. No Duplicate Skill Names

The `name` field in SKILL.md frontmatter must be unique across all skills in the repository. Check all sibling skill directories for conflicts.

## How to Validate

To validate a single skill:

1. Read `SKILL.md` in the skill directory
2. Parse YAML frontmatter between the first two `---` lines
3. Check `name` and `description` exist and are non-empty
4. Scan for internal file references and verify they resolve
5. Check no other skill in the repo uses the same `name`

To validate all skills:

1. List all directories in the repository root (excluding `.git`, `__pycache__`, `node_modules`)
2. For each directory containing a `SKILL.md`, run the single-skill validation
3. Report any issues found

## Common Issues

| Issue | Fix |
|-------|-----|
| Missing `---` delimiters | Add YAML frontmatter block at top of SKILL.md |
| Empty `name` | Add a lowercase, hyphenated name |
| Empty `description` | Add a description starting with what the skill does |
| Broken reference link | Update the path or remove the reference |
| Duplicate skill name | Rename one of the conflicting skills |
| Directory name mismatch | Rename directory to match `name` field (with `-skill` suffix if desired) |
