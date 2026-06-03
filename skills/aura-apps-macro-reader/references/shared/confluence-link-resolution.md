# Shared Confluence link/page resolution

Aura and Karma macro params often reference Confluence content by page/content ID rather than by URL or title. Use this when a user asks to follow a macro link, identify a link target, or dig deeper into linked content.

## Common link shapes

```ts
type LinkMeta = {
  type?: "page" | "blogpost" | "attachment" | "link" | "url" | "email" | "anchor" | string;
  value?: string;   // often a Confluence page/content ID for type "page"/"blogpost"; URL for type "link"/"url"
  target?: "_blank" | "_self" | string;
  title?: string;
  spaceKey?: string;
  [key: string]: unknown;
};
```

Fields vary by macro/version. Treat `value` as the primary target. If `type` indicates Confluence content and `value` is numeric or ID-like, resolve it through Confluence instead of presenting it as a URL.

## Resolution workflow

1. Extract the raw link object from the decoded macro params, e.g. `button.link`, `card.link`, `header.link`, `image.link`, or Karma element `params.link`.
2. If the link is external (`type: "link"`/`"url"`, or `value` starts with `http://`, `https://`, `mailto:`), present/fetch that URL directly.
3. If the link is Confluence content (`type: "page"`, `"blogpost"`, `"content"`, etc., or `value` looks like a Confluence content ID), call Confluence API/MCP to resolve it:
   - `getConfluencePage` / `/wiki/api/v2/pages/{id}` for pages.
   - blogpost endpoint for blogposts.
   - attachments endpoint for attachments.
4. When following the link content, fetch the target page in ADF again and re-run the Aura/Karma macro reader workflow on that target page.
5. If resolution fails, report the raw link object and say the target could not be resolved with available permissions/API data.

## Output guidance

- For summaries: include resolved page title and URL when available.
- For deep traversal: clearly separate source-page content from linked-page content.
- Do not invent page titles from IDs. Resolve via API or show the ID as unresolved.
