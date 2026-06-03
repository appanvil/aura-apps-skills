# Aura - Dynamic Content (Cards & Lists)

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Child pages, blogs, spaces, label-filtered content, user lists, manual org charts, and Mantra events. Config describes what to fetch/render; it is not the rendered result.

## Decoded `params` interface

```ts
type SortBy = "title" | "created" | "lastmodified" | "default";
type SortDirection = "asc" | "desc";
type ViewType = "backgroundCard" | "list" | "simpleCard";
type ImageCategory = "nature" | "business" | "architecture" | "gradient" | "abstract" | "watercolor" | "aura";
type SpaceType = "global" | "personal" | "all";
type BasicViewType = "card" | "list";
type UserViewType = BasicViewType | "compact";
type PageType = "page" | "whiteboard" | "embed" | "database";
interface Toggles { author: boolean; owner: boolean; labels: boolean; date: boolean; comments: boolean; likes: boolean; space: boolean; description: boolean; image: boolean; }
interface SpaceToggles { author: boolean; categories: boolean; icon: boolean; description: boolean; }
interface DynamicContent { labels?: string[]; spaces?: string[]; users?: string[]; sortBy?: SortBy; defaultImageCategory: ImageCategory; sortDirection: SortDirection; elementsPerPage: number; viewType: ViewType; toggles: Toggles; }
interface DynamicContentPage extends DynamicContent { parentPage?: string; isAllChildrenEnabled: boolean; pageTypes?: PageType[]; }
interface DynamicContentSpaces { categories?: string[]; elementsPerPage: number; type?: SpaceType; viewType: BasicViewType; toggles: SpaceToggles; }
type ContentSource = "confluence" | "mantra" | "users";
interface DynamicContentUsers { group?: string; users?: string[]; viewType: UserViewType; defaultImageCategory: ImageCategory | "SYNC_MANTRA"; mantraProperties?: string[]; contentSource?: ContentSource; mantraFilters?: unknown[]; }
interface DynamicContentProps { type?: "pages" | "blogposts" | "spaces" | "users" | "manual-org-chart" | "mantra-events"; blogs: DynamicContent; pages: DynamicContentPage; spaces: DynamicContentSpaces; users: DynamicContentUsers; manualOrgChart: { tree: unknown }; mantraEvents: { amount: number; byFilter: { workspaceId?: string; categories?: string[]; creator?: string; from?: number | null; to?: number | null; hidePastEvents?: boolean } }; }
```

## Reading guidance

If type is pages/blogposts/spaces/users/mantra-events, make follow-up Confluence/Mantra/user API calls when the user needs actual rendered items. If `parentPage` is `CURRENT_PAGE`, use current page descendants.
