# Aura - Expand (Must be used in Aura - Expand Group)

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

A single expandable child used inside Aura Expand Group.

## Decoded `params` interface

```ts
interface ExpandProps { title: string; icon?: string | { id: string }; }
```

## Reading guidance

Output title and body content when available.
