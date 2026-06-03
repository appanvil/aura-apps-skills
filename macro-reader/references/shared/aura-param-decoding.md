# Shared Aura parameter decoding

Use this for Aura content-formatting macros and Aura LaTeX macros after title-based detection.

## Outer ADF shape

```ts
interface AuraConnectExtension {
  type: "extension" | "inlineExtension" | "bodiedExtension";
  attrs: {
    extensionType: "com.atlassian.confluence.macro.core";
    extensionTitle?: string; // match title first
    text?: string;
    extensionKey: `aura-${string}`;
    parameters: { macroParams: Record<string, { value: string }> };
  };
}

interface AuraForgeExtension {
  type: "extension" | "inlineExtension" | "bodiedExtension";
  attrs: {
    extensionType: "com.atlassian.ecosystem";
    extensionTitle?: string; // match title first
    text?: string;
    extensionKey: `${string}/${string}/static/${string}`;
    parameters: { guestParams: Record<string, string> };
  };
}
```

## Access params

```ts
function getParam(ext: any, key: string): string | undefined {
  const p = ext.attrs?.parameters ?? {};
  if (p.guestParams) return p.guestParams[key]; // Forge
  const wrapper = p.macroParams?.[key];          // Connect
  return wrapper && typeof wrapper === "object" ? wrapper.value : undefined;
}
```

## Decode `params`

```ts
interface AuraMacroParamEnvelope<T> {
  summary?: string;
  params: string; // Base64(decodeURIComponent(JSON.stringify(T))) inverse below
}

function decodeAuraParams<T>(raw: string): T {
  return JSON.parse(decodeURIComponent(atob(raw))) as T;
}
```

Python:

```python
import base64, json, urllib.parse

def decode_aura_params(raw: str):
    return json.loads(urllib.parse.unquote(base64.b64decode(raw).decode("utf-8")))
```

## Shared style/data aliases

Many macro interfaces reference these shared Aura style types from `formatting-utils` / style controls. Treat them as structured style metadata; preserve only fields relevant to content questions.

```ts
type AuraColor = string | { light: string; dark?: string };
type Alignment = { horizontal?: "start" | "center" | "end" | "left" | "right"; vertical?: string };
type Size = { width?: string | number; height?: string | number; minWidth?: string | number; minHeight?: string | number };
type Border = { top?: boolean; right?: boolean; bottom?: boolean; left?: boolean; style?: string; width?: number; color?: AuraColor };
type BoxShadow = string | { name?: string; value?: string; color?: AuraColor } | Record<string, unknown>;
type BorderRadius = { radius?: number; topLeft?: number; topRight?: number; bottomLeft?: number; bottomRight?: number };
type BackgroundColor = { color?: AuraColor } | AuraColor;
type Padding = { top?: number; right?: number; bottom?: number; left?: number };
type Icon = { name?: string; icon?: string | { id: string }; id?: string; color?: AuraColor; size?: number };
type Text = { text?: string; color?: AuraColor; fontSize?: number; textAlign?: string; fontWeight?: string | number; [key: string]: unknown };
type LinkMeta = { type?: string; value?: string; target?: string; [key: string]: unknown };
type HyperLinkMeta = LinkMeta;
```
