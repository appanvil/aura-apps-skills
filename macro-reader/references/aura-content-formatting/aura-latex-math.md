# Aura LaTeX Math

Read `../shared/aura-param-decoding.md` first. Match by title `Aura LaTeX Math` before key; then determine Forge vs Connect for param access. Decode `params`.

## What it does

Renders a LaTeX expression inline or as a block image/SVG. It has no useful text `summary`; decode params directly.

## Decoded `params` interface

```ts
interface LatexMath {
  expression: string;
  isInline: boolean;
  anchor?: string;
  showAnchor: boolean;
  fontSize?: number; // default 1
}
```

## Reading guidance

Visible content is `expression`. Best-effort render simple LaTeX to Unicode; if the expression is complex, include raw LaTeX in a fenced block. If `showAnchor`/`anchor` are set, mention the reference anchor if relevant.
