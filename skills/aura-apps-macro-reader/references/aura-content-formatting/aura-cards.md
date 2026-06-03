# Aura - Cards

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Collection of classic, hover, or flip cards with titles, body text, icons/images, and links.

## Decoded `params` interface

```ts
type AuraCardsLayout = "icon-left" | "icon-center" | "icon-right";
type AuraCardsDecoration = "none" | "icon" | "image";
type AuraCardsTheme = "aura" | "fabric" | "aura-accent" | "GET_KARMA_NOW";
type AuraCardsHover = "none" | "elevate" | "shrink";
type AuraCardsImagePosition = "top" | "left" | "right";
type HoverStyle = "elevate" | "zoom" | "highlight" | "background";
type FlipStyle = "box" | "slider" | "3d";
type Roundness = "none" | "slightly" | "rounded";
interface CardContent { icon?: string | { id: string }; title: string; body: string; iconColor?: AuraColor; backgroundColor?: AuraColor; backgroundImage?: HyperLinkMeta; link?: LinkMeta; fontColorTitle?: AuraColor; fontColorBody?: AuraColor; defaultImage?: string; }
interface HoverCardContent { icon?: string | { id: string }; title: string; body: string; backgroundImage?: HyperLinkMeta; accentColor?: AuraColor; link?: LinkMeta; defaultImage?: string; }
interface AuraClassicCardsProps { cards: CardContent[]; maxWidth?: boolean; theme: AuraCardsTheme; columns: number; layout: AuraCardsLayout; decoration: AuraCardsDecoration; gutter: number; padding: number; hover: AuraCardsHover; imageHeight?: number; imagePosition?: AuraCardsImagePosition; roundness?: Roundness; }
interface AuraHoverCardsProps { cards: HoverCardContent[]; style: HoverStyle; columns: number; defaultImageCategory?: string; }
interface AuraFlipCardContent { front: CardContent; back: CardContent; link?: LinkMeta; }
interface AuraFlipCardsProps { cards: AuraFlipCardContent[]; style: FlipStyle; columns: number; height: number; defaultImageCategory?: string; }
interface AuraCardsProps { type?: "classic" | "hover" | "flip"; classicCards: AuraClassicCardsProps; hoverCards: AuraHoverCardsProps; flipCards: AuraFlipCardsProps; }
```

## Reading guidance

For classic/hover cards output title, body, and link for each card. For flip cards output front and back content.
