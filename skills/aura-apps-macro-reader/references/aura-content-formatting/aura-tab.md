# Aura - Tab (Must be used in Aura - Tab Group)

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

A single tab child used inside Aura Tab Group; body content lives in the bodied macro content, while params give label/icon.

## Decoded `params` interface

```ts
interface TabProps { title?: string; icon?: string | { id: string }; }
```

## Reading guidance

Extract title/icon from params. Extract tab body from the enclosing Tab Group body/order when structure is needed.
