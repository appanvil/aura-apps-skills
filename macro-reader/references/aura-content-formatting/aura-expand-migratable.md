# Migrated Expand

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Legacy/migrated expand child.

## Decoded `params` interface

```ts
interface MigratedExpandProps { title: string; icon?: string | { id: string }; }
```

## Reading guidance

Treat like Aura Expand; read rich-text body directly.
