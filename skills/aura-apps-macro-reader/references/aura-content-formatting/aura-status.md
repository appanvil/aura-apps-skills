# Aura - Status

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Inline status label with a selected row/template.

## Decoded `params` interface

```ts
type StatusSize = "small" | "medium" | "large";
type StatusRow = { id: number; fontColor: AuraColor; backgroundColor: AuraColor; name: string; active: boolean };
interface StatusMeta { size: StatusSize; fitSize: boolean; uppercase: boolean; }
interface StatusProps { meta: StatusMeta; rows: StatusRow[]; isLocked?: boolean; }
```

## Reading guidance

Visible value is the row where `active === true`; otherwise first row/name.
