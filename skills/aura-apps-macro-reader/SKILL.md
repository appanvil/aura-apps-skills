---
name: aura-apps-macro-reader
description: Use when reading Confluence pages built with Aura or Karma macro apps. Trigger when Confluence markdown is empty, when ADF/html contains extension/inlineExtension/bodiedExtension nodes with macro titles starting with "Aura ", "Aura -", or "Karma -", or when asked to extract content from Aura/Karma macros. Always identify our macros by extensionTitle/text first, then determine Forge vs Connect shape and dispatch to the macro-specific reference file under references/.
---

# Reading Aura and Karma Macros in Confluence

Pages built with Aura and Karma store visible content inside macro extension parameters. Default `markdown` often loses the content. Use ADF and dispatch progressively.

## Fast path first

Use the bundled extractor before reading per-macro references. It decodes common Aura/Karma macros deterministically and avoids loading large reference files into context.

1. Fetch the page with ADF (`contentFormat: "adf"` or Confluence v2 `body-format=atlas_doc_format`). Avoid `markdown`; avoid `html` unless ADF is impossible.
2. Save the full JSON response to a temp file, then run:

```bash
python3 ${CLAUDE_SKILL_DIR:-skills/aura-apps-macro-reader}/scripts/extract_macros.py /tmp/page-adf.json
```

For machine-readable output:

```bash
python3 ${CLAUDE_SKILL_DIR:-skills/aura-apps-macro-reader}/scripts/extract_macros.py --json /tmp/page-adf.json
```

3. Answer from the extractor output when possible.
4. Only read per-macro reference files when the user asks for structure/details the extractor did not provide, when extraction looks wrong, or when implementing/debugging parser behavior.
5. Do not resolve Confluence links, fetch descendants, fetch users, or inspect dynamic macro targets unless the user explicitly asks to follow/expand those targets.

## Manual workflow when the extractor is insufficient

1. Walk all `extension`, `inlineExtension`, and `bodiedExtension` nodes recursively.
2. Identify macros by title first:
   - Aura if `attrs.extensionTitle` or `attrs.text` starts with `Aura ` or `Aura -`.
   - Karma if `attrs.extensionTitle` or `attrs.text` starts with `Karma ` or `Karma -`.
   - Use `extensionKey` only as fallback when title is missing.
3. After title/vendor detection, determine shape per node:
   - Forge: `attrs.extensionType == "com.atlassian.ecosystem"`, params in `parameters.guestParams`, bare values.
   - Connect: `attrs.extensionType == "com.atlassian.confluence.macro.core"`, params in `parameters.macroParams`, values wrapped as `{ value }`.
4. Read `summary` first when present. If it answers the question, stop. Otherwise dispatch to the exact reference file below.

```python
def get_param(ext, key):
    p = ext.get("attrs", {}).get("parameters", {})
    if "guestParams" in p:
        return p["guestParams"].get(key)
    wrapper = p.get("macroParams", {}).get(key)
    return wrapper.get("value") if isinstance(wrapper, dict) else None
```

## Aura parameter decoding

Most Aura content-formatting macros store structured config in `params`, encoded as JSON stringify → URL encode → Base64. Read `references/shared/aura-param-decoding.md` before parsing Aura `params`.

## Link/page resolution

Aura/Karma link fields often store Confluence page/content IDs instead of URLs. When the user asks to follow links, inspect linked content, or identify link targets, read `references/shared/confluence-link-resolution.md`, resolve IDs through the Confluence API/MCP, then fetch linked pages in ADF and re-run this workflow.

## Dispatch table

Match normalized macro title (prefer `extensionTitle`, then `text`). Then read exactly one macro reference unless nested/body content requires more.

### Aura content formatting

- `Aura - Dynamic Content (Cards & Lists)` → `references/aura-content-formatting/aura-dynamic-content.md`
- `Aura - Tab (Must be used in Aura - Tab Group)` → `references/aura-content-formatting/aura-tab.md`
- `Aura - Tab Group` → `references/aura-content-formatting/aura-tab-group.md`
- `Aura - Title` → `references/aura-content-formatting/aura-title.md`
- `Aura - Button` → `references/aura-content-formatting/aura-button.md`
- hidden `Link` → `references/aura-content-formatting/aura-link.md`
- `Aura - Divider` → `references/aura-content-formatting/aura-divider.md`
- `Aura - Cards` → `references/aura-content-formatting/aura-cards.md`
- `Aura - Background Content` → `references/aura-content-formatting/aura-background-content.md`
- `Aura - Panel` → `references/aura-content-formatting/aura-panel.md`
- `Aura - Expand Group` → `references/aura-content-formatting/aura-expand-group.md`
- `Aura - Expand (Must be used in Aura - Expand Group)` → `references/aura-content-formatting/aura-expand.md`
- `Aura - Status` → `references/aura-content-formatting/aura-status.md`
- `Aura - Countdown` → `references/aura-content-formatting/aura-countdown.md`
- `Aura - Progress` → `references/aura-content-formatting/aura-progress.md`
- `Aura - HTML (iframe)` → `references/aura-content-formatting/aura-html.md`
- `Aura - Embed` → `references/aura-content-formatting/aura-embed.md`
- `Aura - Child Tabs` → `references/aura-content-formatting/aura-child-tabs.md`
- `Aura - User Profile` → `references/aura-content-formatting/aura-user-profile.md`
- `Migrated Tab` (tab) → `references/aura-content-formatting/aura-tab-migratable.md`
- `Migrated Tab Group` → `references/aura-content-formatting/aura-tab-group-migratable.md`
- `Migrated Expand` → `references/aura-content-formatting/aura-expand-migratable.md`
- `Migrated Expand Group` → `references/aura-content-formatting/aura-expand-group-migratable.md`

### Aura LaTeX

- `Aura LaTeX Math` → `references/aura-content-formatting/aura-latex-math.md`
- `Aura LaTeX Reference` → `references/aura-content-formatting/aura-latex-reference.md`

### Karma

- `Karma - Page Builder` → `references/karma/karma-page-builder.md`

## Limits

Be explicit when macro data alone cannot provide resolved attachment URLs, dynamic query results, visual column ordering, rendered iframe behavior, or Confluence inline-comment anchors.
