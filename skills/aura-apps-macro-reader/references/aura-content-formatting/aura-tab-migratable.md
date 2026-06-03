# Migrated Tab

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Legacy/migrated tab shape; same semantic role as Aura Tab but body type may be rich-text.

## Decoded `params` interface

```ts
interface MigratedTabProps { title?: string; icon?: string | { id: string }; }
```

## Reading guidance

Treat like Aura Tab; read body rich text directly.
