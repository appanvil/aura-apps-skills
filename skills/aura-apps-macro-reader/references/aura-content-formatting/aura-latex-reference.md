# Aura LaTeX Reference

Read `../shared/aura-param-decoding.md` first. Match by title `Aura LaTeX Reference` before key; then determine Forge vs Connect for param access. Decode `params`.

## What it does

Displays a reference/link to another Aura LaTeX Math macro, optionally with custom display text.

## Decoded `params` interface

```ts
interface LatexMathAnchor {
  id: string;
  displayName?: string;
  page: string; // `CURRENT_PAGE` or a page id
  newTab: boolean;
  showCustomText: boolean;
}
```

## Reading guidance

Visible text is `displayName` when `showCustomText` is true and `displayName` exists; otherwise visible text is `id`. Use `page` to resolve the referenced LaTeX macro only if the user needs the target expression.
