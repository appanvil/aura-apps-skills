# Aura Apps Skills

This repository is the public skill collection for Aura Apps.

It contains agent skills and supporting reference material for working with Aura and Karma content, especially Confluence pages that use Aura/Karma macros.

## Skills

### `aura-apps-macro-reader`

Located in `skills/aura-apps-macro-reader/`.

Use this skill to read Confluence pages that contain Aura or Karma macros. These macros often store visible page content inside macro parameters rather than normal Confluence prose, so default Markdown extraction can miss important content.

The skill provides:

- Aura/Karma macro detection
- Forge vs Connect parameter handling
- per-macro reference files for deep parsing
- Aura parameter decoding guidance and a deterministic decode helper script
- Confluence link/page ID resolution guidance
- safe handling instructions for embedded HTML macros

## Structure

```text
skills/
└── aura-apps-macro-reader/
    ├── SKILL.md
    └── references/
        ├── aura-content-formatting/
        ├── karma/
        └── shared/

.claude-plugin/
├── marketplace.json
└── plugin.json

.codex-plugin/
└── plugin.json

.agents/
└── plugins/
    └── marketplace.json
```

## Helper scripts

Decode Aura `params` values without asking the model to manually perform Base64/URL/JSON decoding:

```bash
python3 skills/aura-apps-macro-reader/scripts/decode_aura_params.py '<raw-params-value>'
python3 skills/aura-apps-macro-reader/scripts/decode_aura_params.py --adf page-adf.json --macro-title 'Aura - Button'
python3 skills/aura-apps-macro-reader/scripts/decode_aura_params.py --adf page-adf.json --all
```

The script only deserializes `params`; macro matching remains title/context based in the skill instructions.

## Usage

### Pi

Symlink or copy this repository into a Pi skill location, for example:

```bash
ln -s /path/to/aura-apps-skills ~/.pi/agent/skills/aura-apps-skills
```

Invoke the skill where supported:

```text
/skill:aura-apps-macro-reader
```

### Claude Code

This repository includes a Claude plugin marketplace at `.claude-plugin/marketplace.json`.

Add the marketplace and install the plugin:

```text
/plugin marketplace add appanvil/aura-apps-skills
/plugin install aura-apps@aura-apps-skills
```

Claude plugin skills are namespaced by plugin name:

```text
/aura-apps:aura-apps-macro-reader
```

For local/personal installation without marketplace, copy the skill folder to:

```text
~/.claude/skills/aura-apps-macro-reader/
```

Then invoke:

```text
/aura-apps-macro-reader
```

### OpenAI Codex

This repository includes a Codex plugin manifest at `.codex-plugin/plugin.json` and a repo marketplace at `.agents/plugins/marketplace.json`.

For local skill installation without plugins, copy or symlink the skill folder to:

```text
~/.agents/skills/aura-apps-macro-reader/
```

Codex can also install it through the included marketplace/plugin metadata where plugin marketplaces are supported.
