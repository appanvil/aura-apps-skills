# Aura - Embed

Read `../shared/aura-param-decoding.md` first. Match by title before key; then determine Forge vs Connect for param access. Decode `getParam(ext, "params")` unless `summary` is enough. If link targets matter or the user wants to follow links, also read `../shared/confluence-link-resolution.md`.


## What it does

Embeds external content such as Figma, Miro, Loom, Google Docs/Sheets/Slides/Forms/Maps, Office, Released, or raw URL.

## Decoded `params` interface

```ts
type EmbedType = "url" | "figma" | "miro" | "trello" | "loom" | "google-docs" | "google-sheets" | "google-slides" | "google-forms" | "google-maps" | "office-word" | "office-pp" | "office-excel" | "office-forms" | "released";
type ReleasedColorScheme = "system" | "light" | "dark";
interface EmbedProps { inputUrl: string; embedType: EmbedType; width: string | number; height: string | number; alignment: Alignment; metadata?: { released?: { colorScheme?: ReleasedColorScheme } }; }
```

## Reading guidance

Output embed type and URL. Do not infer embedded document content without fetching the URL separately.
