#!/usr/bin/env python3
"""Fast Aura/Karma Confluence ADF extractor.

Usage:
  extract_macros.py page-adf.json             # markdown
  extract_macros.py --json page-adf.json      # normalized JSON
  cat page-adf.json | extract_macros.py -

Input may be the full getConfluencePage response or the body ADF doc itself.
"""
from __future__ import annotations

import argparse, base64, datetime as dt, html, json, re, sys, urllib.parse
from typing import Any

EXT_TYPES = {"extension", "inlineExtension", "bodiedExtension"}


def get_doc(data: Any) -> dict[str, Any]:
    if isinstance(data, dict) and data.get("type") == "doc":
        return data
    body = data.get("body") if isinstance(data, dict) else None
    if isinstance(body, dict) and body.get("type") == "doc":
        return body
    raise SystemExit("Input must be a Confluence ADF doc or getConfluencePage response with body.type=doc")


def get_title(data: Any) -> str | None:
    return data.get("title") if isinstance(data, dict) else None


def attrs(node: dict[str, Any]) -> dict[str, Any]:
    return node.get("attrs") or {}


def macro_title(node: dict[str, Any]) -> str:
    a = attrs(node)
    p = a.get("parameters") or {}
    md = p.get("macroMetadata") or {}
    md_title = md.get("title") if isinstance(md, dict) else None
    if isinstance(md_title, dict):
        md_title = md_title.get("value")
    title = a.get("extensionTitle") or a.get("text") or md_title
    if title:
        return str(title)
    key = a.get("extensionKey", "")
    if isinstance(key, str):
        if key.startswith("aura-"):
            return key
        if key.startswith("appanvil-karma-"):
            return "Karma - Page Builder"
        if "/static/latex-math-anchor" in key:
            return "Aura LaTeX Reference"
        if "/static/latex-math" in key:
            return "Aura LaTeX Math"
    return str(key or "Unknown macro")


def is_ours(title: str, node: dict[str, Any]) -> bool:
    key = attrs(node).get("extensionKey", "")
    return title.startswith(("Aura ", "Aura -", "Karma ", "Karma -")) or str(key).startswith(("aura-", "appanvil-karma-"))


def get_param(node: dict[str, Any], key: str) -> Any:
    p = attrs(node).get("parameters") or {}
    if "guestParams" in p:
        return (p.get("guestParams") or {}).get(key)
    wrapper = (p.get("macroParams") or {}).get(key)
    return wrapper.get("value") if isinstance(wrapper, dict) else None


def decode_params(raw: Any) -> Any:
    if not raw:
        return None
    if not isinstance(raw, str):
        return raw
    try:
        return json.loads(urllib.parse.unquote(base64.b64decode(raw).decode("utf-8")))
    except Exception:
        try:
            return json.loads(raw)
        except Exception:
            return {"_decode_error": True, "raw": raw[:120]}


def text_from_adf(node: Any) -> str:
    out: list[str] = []
    def walk(n: Any):
        if isinstance(n, list):
            for x in n: walk(x)
        elif isinstance(n, dict):
            if n.get("type") in EXT_TYPES:
                return
            if "text" in n and isinstance(n["text"], str):
                out.append(n["text"])
            for c in n.get("content") or []:
                walk(c)
            if n.get("type") in {"paragraph", "heading", "listItem"} and out and out[-1] != "\n":
                out.append("\n")
    walk(node)
    return re.sub(r"\n{3,}", "\n\n", "".join(out)).strip()


def text_from_tree(v: Any) -> str:
    out: list[str] = []
    def walk(n: Any):
        if isinstance(n, list):
            for x in n: walk(x)
        elif isinstance(n, dict):
            if isinstance(n.get("text"), str) and n["text"]:
                out.append(n["text"])
            for key in ("children", "content", "value"):
                if key in n: walk(n[key])
    walk(v)
    return " ".join("".join(out).split())


def strip_html(s: str) -> str:
    s = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", s or "")
    s = re.sub(r"(?is)<a\b[^>]*href=['\"]([^'\"]+)['\"][^>]*>(.*?)</a>", lambda m: f"{strip_html(m.group(2))} ({m.group(1)})", s)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?is)</(p|div|li|tr|h[1-6])>", "\n", s)
    s = re.sub(r"(?is)<[^>]+>", "", s)
    return re.sub(r"\n{3,}", "\n\n", html.unescape(s)).strip()


def link_value(link: Any) -> str | None:
    if isinstance(link, dict):
        v = link.get("value") or link.get("url") or link.get("href")
        t = link.get("type")
        return f"{v} ({t})" if v and t else v
    return str(link) if link else None


def render_macro(node: dict[str, Any]) -> dict[str, Any]:
    title = macro_title(node)
    summary = get_param(node, "summary")
    cfg = decode_params(get_param(node, "params"))
    body_text = text_from_adf(node.get("content") or [])
    block: dict[str, Any] = {"type": title, "summary": summary, "text": None, "items": [], "link": None, "needs_api": False}
    c = cfg if isinstance(cfg, dict) else {}

    if title in {"Aura - Button", "Link"} or str(attrs(node).get("extensionKey")) in {"aura-inline-button", "aura-button"}:
        block.update(text=c.get("label") or summary, link=link_value(c.get("link")))
    elif title == "Aura - Cards" or attrs(node).get("extensionKey") == "aura-cards":
        typ = c.get("type") or "classic"
        source = c.get(f"{typ}Cards", {}) if typ in {"classic", "hover", "flip"} else c.get("classicCards", {})
        for card in source.get("cards", []) if isinstance(source, dict) else []:
            if typ == "flip":
                f, b = card.get("front", {}), card.get("back", {})
                block["items"].append({"title": f.get("title"), "body": f.get("body"), "backTitle": b.get("title"), "backBody": b.get("body"), "link": link_value(card.get("link") or f.get("link") or b.get("link"))})
            else:
                block["items"].append({"title": card.get("title"), "body": card.get("body"), "link": link_value(card.get("link"))})
        block["text"] = summary
    elif title == "Aura - Progress":
        for b in c.get("bars", []):
            block["items"].append({"label": b.get("labelText"), "progress": b.get("progress"), "value": b.get("valueProps")})
    elif title == "Aura - Countdown":
        exp = c.get("expires")
        when = None
        if isinstance(exp, (int, float)):
            when = dt.datetime.fromtimestamp(exp/1000, tz=dt.timezone.utc).isoformat()
        block["text"] = when or str(exp or "")
    elif title == "Aura - Title":
        block["text"] = c.get("cloudText") or summary
    elif title == "Aura - Status":
        rows = c.get("rows") or []
        active = next((r for r in rows if r.get("active")), rows[0] if rows else {})
        block["text"] = active.get("name") or summary
    elif title == "Aura - Panel":
        headline = (((c.get("headline") or {}).get("text") or {}).get("text"))
        block["text"] = "\n".join(x for x in [headline, body_text or (((c.get("body") or {}).get("text") or {}).get("text"))] if x)
        block["link"] = link_value((c.get("header") or {}).get("link"))
    elif title in {"Aura LaTeX Math", "Aura LaTeX Reference"}:
        block["text"] = c.get("expression") or c.get("displayName") or c.get("id")
    elif title in {"Aura - Tab Group", "Aura - Expand Group"}:
        block["items"] = grouped_children(node, "Tab" if "Tab" in title else "Expand")
    elif title.startswith("Aura - Tab") or title.startswith("Aura - Expand"):
        block["text"] = c.get("title") or summary
    elif title == "Aura - Background Content":
        block["text"] = body_text or ((c.get("text") or {}).get("text"))
    elif title == "Aura - Dynamic Content (Cards & Lists)":
        block["text"] = f"Dynamic content: {c.get('type') or 'unknown'}"
        block["needs_api"] = True
    elif title == "Aura - Divider":
        block["text"] = (((c.get("style") or {}).get("text") or {}).get("text")) or summary
    elif title == "Aura - HTML (iframe)":
        block["text"] = strip_html(c.get("htmlCode") or c.get("html") or "")
    elif title == "Aura - Embed":
        block.update(text=c.get("embedType"), link=c.get("inputUrl"))
    elif title == "Aura - User Profile":
        for card in c.get("cards", []):
            block["items"].append({k: card.get(k) for k in ("user", "name", "info", "email") if card.get(k)})
        block["text"] = summary
    elif title == "Karma - Page Builder" or attrs(node).get("extensionKey") == "appanvil-karma-designer":
        page = decode_params(get_param(node, "page")) or get_param(node, "page")
        block["text"] = summary or text_from_karma(page)
    else:
        block["text"] = summary or body_text or text_from_tree(c)
    return block


def grouped_children(node: dict[str, Any], kind: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for child in node.get("content") or []:
        if isinstance(child, dict) and child.get("type") in EXT_TYPES and kind in macro_title(child):
            cfg = decode_params(get_param(child, "params"))
            title = (cfg or {}).get("title") if isinstance(cfg, dict) else None
            current = {"title": title or get_param(child, "summary") or macro_title(child), "body": ""}
            items.append(current)
        else:
            txt = text_from_adf(child)
            if txt and current is not None:
                current["body"] = (current["body"] + "\n" + txt).strip()
    return items


def text_from_karma(page: Any) -> str:
    if isinstance(page, str):
        try: page = json.loads(page)
        except Exception: return ""
    out: list[str] = []
    def walk(n: Any):
        if isinstance(n, list):
            for x in n: walk(x)
        elif isinstance(n, dict):
            name, params = n.get("name"), n.get("params") or {}
            if name == "text":
                t = text_from_tree(params.get("value"))
                if t: out.append(t)
            elif name == "button":
                label = params.get("label")
                link = link_value(params.get("link"))
                if label or link: out.append(f"Button: {label or ''} -> {link or ''}".strip())
            for child in n.get("children") or []: walk(child)
    walk(page)
    return "\n".join(out)


def collect(doc: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    def walk(n: Any):
        if isinstance(n, list):
            for x in n: walk(x)
        elif isinstance(n, dict):
            if n.get("type") in EXT_TYPES:
                title = macro_title(n)
                if is_ours(title, n):
                    blocks.append(render_macro(n))
                # Still walk bodied macro content for nested macros only if parent is not a grouping macro.
                if title not in {"Aura - Tab Group", "Aura - Expand Group"}:
                    walk(n.get("content") or [])
                return
            walk(n.get("content") or [])
    walk(doc.get("content") or [])
    return blocks


def markdown(title: str | None, blocks: list[dict[str, Any]]) -> str:
    lines = [f"# {title}" if title else "# Extracted Aura/Karma content", ""]
    for b in blocks:
        lines.append(f"## {b['type']}")
        if b.get("text"):
            lines.append(str(b["text"]))
        if b.get("link"):
            lines.append(f"Link: {b['link']}")
        for it in b.get("items") or []:
            if isinstance(it, dict):
                head = it.get("title") or it.get("label") or it.get("name") or it.get("user") or "Item"
                tail = "; ".join(f"{k}: {v}" for k, v in it.items() if k != "title" and v not in (None, "", {}))
                lines.append(f"- {head}" + (f" — {tail}" if tail else ""))
            else:
                lines.append(f"- {it}")
        if b.get("needs_api"):
            lines.append("_Requires follow-up Confluence/API calls for rendered dynamic results._")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("input", nargs="?", default="-")
    args = ap.parse_args()
    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    data = json.loads(raw)
    blocks = collect(get_doc(data))
    result = {"title": get_title(data), "blocks": blocks}
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(markdown(result["title"], blocks), end="")

if __name__ == "__main__":
    main()
