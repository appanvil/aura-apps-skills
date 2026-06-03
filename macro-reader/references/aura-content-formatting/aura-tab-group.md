# Aura - Tab Group

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Container for Aura Tab child macros; controls tab styling and reads nested tab bodies.

## Decoded `params` interface

```ts
type TabDirection = "vertical" | "horizontal";
interface AuraTabCollectionProps { general?: { tabHeight?: number; tabWidth?: number; tabSpacing?: number; direction?: TabDirection; sticky?: boolean }; active?: { border?: Border; backgroundColor?: BackgroundColor; text?: Text }; hover?: { backgroundColor?: BackgroundColor; text?: Text; border?: Border }; inactive?: { backgroundColor?: BackgroundColor; text?: Text; border?: Border }; content?: { padding?: Padding; border?: Border; boxShadow?: BoxShadow; backgroundColor?: BackgroundColor; size?: Size; text?: Text }; body?: unknown; }
```

## Reading guidance

Walk bodied content for nested Aura Tab macros in document order; pair each TabProps with its body.
