# Aura - User Profile

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Collection of user profile cards.

## Decoded `params` interface

```ts
type CardStyle = "filled" | "diagonal" | "title" | "title-up" | "title-down";
type CardSize = "small" | "medium" | "large";
type CardHover = "none" | "elevate" | "shrink";
interface UserCardProps { accountId?: string; name?: string; title?: string; department?: string; location?: string; email?: string; phone?: string; avatarUrl?: string; [key: string]: unknown; }
interface UserProfileCollectionProps { cardSize: CardSize; cardStyle: CardStyle; hover?: CardHover; cards: UserCardProps[]; fullWidth?: boolean; shapeColor: AuraColor; fontColor: AuraColor; nameColor: AuraColor; }
```

## Reading guidance

Output each card user name and populated profile fields. Account IDs may require user API lookup.
