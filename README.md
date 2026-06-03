# Aura Apps Skills

This repository is the public skill collection for Aura Apps.

It contains agent skills and supporting reference material for working with Aura and Karma content, especially Confluence pages that use Aura/Karma macros.

## Skills

### `aura-apps-macro-reader`

Located in `macro-reader/`.

Use this skill to read Confluence pages that contain Aura or Karma macros. These macros often store visible page content inside macro parameters rather than normal Confluence prose, so default Markdown extraction can miss important content.

The skill provides:

- Aura/Karma macro detection
- Forge vs Connect parameter handling
- per-macro reference files
- Aura parameter decoding guidance
- Confluence link/page ID resolution guidance
- safe handling instructions for embedded HTML macros

## Structure

```text
macro-reader/
├── SKILL.md
└── references/
    ├── aura-content-formatting/
    ├── karma/
    └── shared/
```

## Usage

Install or symlink this repository into an agent skills directory, then invoke the skill by name where supported:

```text
/skill:aura-apps-macro-reader
```
# aura-apps-skills
