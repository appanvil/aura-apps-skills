# Aura - Expand Group

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Container for Aura Expand child macros; controls expand styling and reads nested expand bodies.

## Decoded `params` interface

```ts
type ExpandIconVariant = "chevron-down" | "chevron-right" | "plus";
type ExpandDesign = "berlin" | "paris" | "seoul" | "new-york";
interface ExpandGroupProps { design: ExpandDesign; shadow?: boolean; iconVariant: ExpandIconVariant; hasNumberedHeadings?: boolean; highlightColor: AuraColor; headerFontColor: AuraColor; text?: Text; }
```

## Reading guidance

Walk bodied content for nested Aura Expand macros in document order; pair each title with its body.
