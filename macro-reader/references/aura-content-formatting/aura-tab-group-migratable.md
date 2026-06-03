# Migrated Tab Group

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Legacy/migrated tab group container.

## Decoded `params` interface

```ts
interface MigratedTabGroupProps extends AuraTabCollectionProps {}
```

## Reading guidance

Treat like Aura Tab Group; nested migrated tabs may have rich-text body.
