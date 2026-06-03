# Aura - Panel

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Bodied panel for highlighting info/note/error/success/warning style content with optional headline/header/link.

## Decoded `params` interface

```ts
interface AuraPanelProps { showMacroBody?: boolean; base?: { backgroundColor?: BackgroundColor; size?: Size; border?: Border; boxShadow?: BoxShadow; borderRadius?: BorderRadius }; header?: { backgroundColor?: BackgroundColor; icon?: Icon; link?: LinkMeta }; body?: { text?: Text }; headline?: { text?: Text; border?: Border; alignment?: Alignment }; }
```

## Reading guidance

Output headline text, header link if present, and bodied content. `body.text` may contain visible text in non-bodied/migrated cases.
