# Link

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Hidden legacy block link/button macro (`key: aura-button`) linking to Confluence or external content. Same params as Aura - Button.

## Decoded `params` interface

```ts
type ButtonShadow = "e100" | "e200" | "e300";
interface ButtonInteractiveState { colors: { background?: AuraColor | null; label?: AuraColor | null; outline?: AuraColor | null }; shadow?: ButtonShadow; }
interface ButtonProps { label: string; alignment?: "left" | "center" | "right"; size: "small" | "medium" | "large"; minWidth?: number; shape: "angular" | "rounded" | "circular" | "skewed" | "mixed"; link?: LinkMeta; states: { idle: ButtonInteractiveState; hover: ButtonInteractiveState }; icon?: { position: "left" | "right"; icon: string | { id: string } }; }
```

## Reading guidance

Output label and link target.
