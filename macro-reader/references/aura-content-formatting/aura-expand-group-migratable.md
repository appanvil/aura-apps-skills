# Migrated Expand Group

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Legacy/migrated expand group container.

## Decoded `params` interface

```ts
interface MigratedExpandGroupProps extends ExpandGroupProps {}
```

## Reading guidance

Treat like Aura Expand Group; nested migrated expands may have rich-text body.
