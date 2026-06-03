# Aura - Child Tabs

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough.


## What it does

Dynamic macro that displays child pages of a parent page as tabs.

## Decoded `params` interface

```ts
interface TabsInteractiveState { backgroundColor?: BackgroundColor; text?: Text; border?: Border; }
interface DynamicTabsProps { parentPage?: string; tabWidth: number; tabHeight: number; tabSpacing: number; direction: "vertical" | "horizontal"; height: number; states: { active: TabsInteractiveState; inactive: TabsInteractiveState; hover: TabsInteractiveState }; content: { padding?: Padding; border?: Border; boxShadow?: BoxShadow; backgroundColor?: BackgroundColor; size?: Size; text?: Text }; }
```

## Reading guidance

To know displayed tab labels/content, fetch descendants of `parentPage` or current page.
