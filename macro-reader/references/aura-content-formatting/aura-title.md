# Aura - Title

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Styled headline/title text.

## Decoded `params` interface

```ts
interface TitleProps { fontSize?: string | number; lineHeight?: string | number; cloudText?: string; color?: AuraColor; isManualLineHeight?: boolean; fontWeight?: string | number; textAlign?: "left" | "center" | "right" | string; }
```

## Reading guidance

Visible text is `cloudText`.
