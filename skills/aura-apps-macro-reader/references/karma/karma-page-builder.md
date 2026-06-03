# Karma - Page Builder

Match by title `Karma - Page Builder` first; then determine Forge vs Connect. Read `summary` first. If structure is needed, parse `page` as JSON. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.

## What it does

Karma Page Builder stores a full page layout tree in one macro. It contains sections, rows, columns, and nested elements such as text, images, buttons, dividers, spacers, cards, icons, videos, embeds, and search bars.

## Outer macro params

```ts
interface KarmaMacroParams {
  summary?: string;
  page: string; // JSON.stringify(KarmaPageTree); Connect: macroParams.page.value, Forge: guestParams.page
}

type KarmaPageTree = Section[] | Section;
```

## Layout tree interfaces

```ts
type AuraColor = string | { light: string; dark?: string };
type LinkMeta = { type?: string; value?: string; target?: string; [key: string]: unknown };
type HyperLinkMeta = LinkMeta;
type ImagePosition = "top left" | "top center" | "top right" | "center left" | "center center" | "center right" | "bottom left" | "bottom center" | "bottom right";

type Section = { id: string; name: "section"; children: Row[]; params: { background?: AuraColor; image?: HyperLinkMeta; imagePosition?: ImagePosition; backgroundSize?: string; padding?: number; gap?: number; borderRadius?: unknown } };
type Row = { id: string; name: "row"; children: Column[]; params: { layout: number[]; gap?: number; minHeight?: number; padding?: number; borderRadius?: number; backgroundColor?: AuraColor; backgroundImage?: HyperLinkMeta; backgroundSize?: string; imagePosition?: ImagePosition; size?: "small" | "medium" | "large" } };
type Column = { id: string; name: "column"; children: KarmaElement[]; params: { background?: string; padding?: number; borderRadius: unknown; verticalAlignment?: "top" | "center" | "bottom" | string; gap?: number } };

type KarmaElement =
  | { id?: string; name: "text"; params: TextProps }
  | { id?: string; name: "button"; params: ButtonProps }
  | { id?: string; name: "divider"; params: DividerProps }
  | { id?: string; name: "image"; params: ImageProps }
  | { id?: string; name: "spacer"; params: SpacerProps }
  | { id?: string; name: "card"; params: CardProps; children?: KarmaElement[] }
  | { id?: string; name: "icon" | "video" | "embed" | "confluence-embed" | "search-bar"; params: Record<string, unknown>; children?: KarmaElement[] };
```

## Element interfaces for visible content

```ts
interface TextProps { value: SlateNode[]; }
type SlateNode = { type?: string; text?: string; children?: SlateNode[]; [markOrStyle: string]: unknown };

type ButtonShadow = "none" | "grounded" | "elevated";
type ButtonSize = "small" | "medium" | "large";
type IconPosition = "left" | "right";
interface ButtonInteractiveState { colors: { background?: AuraColor; label?: AuraColor; outline?: AuraColor }; shadow?: ButtonShadow; }
interface ButtonProps { label: string; size: ButtonSize; link?: LinkMeta; icon?: string | { id: string }; iconPosition?: IconPosition; width?: number; states: { idle: ButtonInteractiveState; hover: ButtonInteractiveState }; shape: string; alignment: "start" | "center" | "end"; }

interface DividerProps { color: AuraColor; fontColor: AuraColor; width?: number; alignment: "start" | "center" | "end"; icon?: string | { id: string }; text?: string; fontSize: number; borderStyle: string; height: number; }
interface ImageProps { width?: number; height?: number; image?: HyperLinkMeta; link?: LinkMeta; boxShadows?: unknown[]; alignment: "start" | "center" | "end"; borderRadius: unknown; position: ImagePosition; shouldOpenDialog?: boolean; overlayColor?: AuraColor; }
interface SpacerProps { space?: number; grow?: boolean; }
interface CardProps { children: KarmaElement[]; background?: AuraColor; boxShadows?: unknown[]; image?: HyperLinkMeta; imagePosition?: ImagePosition; backgroundSize?: string; padding?: number; gap?: number; link?: LinkMeta; borderRadius?: unknown; isMediaFullSize?: boolean; hover?: "none" | "elevate" | "shrink"; }
```

## Reading guidance

Walk `children` recursively in order. For `text`, walk the Slate tree and collect every non-empty `text` leaf, preserving paragraphs/lists when possible. For `button`, output `label` and `link.value`. For `image`, output `image.value`, `link.value`, and alt-like metadata if present. For `card`, output its link/background metadata and recurse into children. Ignore spacers and purely visual divider fields unless the user asks about layout/styling.
