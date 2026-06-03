# Aura - Background Content

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Bodied macro that renders nested content over an image/color background.

## Decoded `params` interface

```ts
type BackgroundSize = "cover" | "auto" | "contain" | "pattern";
type ContentPosition = "flex-start" | "center" | "flex-end";
interface BackgroundProps { isEditor?: boolean; containerMinHeight: string; contentPosition: ContentPosition; alignment?: Alignment; padding: string; backgroundSize: BackgroundSize; backgroundPosition: string; backgroundImageHref?: string; backgroundImageHrefType?: LinkMeta["type"]; backgroundColor?: AuraColor; text?: Text; }
```

## Reading guidance

Visible prose is primarily in the bodied macro content; params are styling/background metadata.
