# Aura - Divider

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Horizontal separator, optionally with icon or text.

## Decoded `params` interface

```ts
type DividerType = "regular" | "icon" | "text";
interface DividerStyle { size?: Size; alignment?: Alignment; icon?: Icon; text?: Text; border?: Border; }
interface AuraDividerProps { type: DividerType; style: DividerStyle; }
```

## Reading guidance

Usually ignore regular dividers; for `text`, output `style.text.text`; for `icon`, mention icon only if relevant.
