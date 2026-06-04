#!/usr/bin/env python3
"""Decode Aura macro `params` values.

This script intentionally does not identify or classify macros. The LLM should
choose the right reference file from the ADF title/context. This helper only
performs the deterministic decoding pipeline used by Aura params:

  JSON.stringify(config) -> encodeURIComponent -> base64

Usage:
  decode_aura_params.py '<base64-param-value>'
  decode_aura_params.py --input params.txt
  decode_aura_params.py --adf page.json --macro-title 'Aura - Button'
  decode_aura_params.py --adf page.json --all
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.parse
from typing import Any

EXT_TYPES = {"extension", "inlineExtension", "bodiedExtension"}


def decode_aura_params(raw: str) -> Any:
    """Return decoded Aura params JSON from a base64/urlencoded JSON string."""
    decoded = base64.b64decode(raw).decode("utf-8")
    unquoted = urllib.parse.unquote(decoded)
    return json.loads(unquoted)


def macro_title(node: dict[str, Any]) -> str:
    attrs = node.get("attrs") or {}
    params = attrs.get("parameters") or {}
    metadata = params.get("macroMetadata") or {}
    md_title = metadata.get("title") if isinstance(metadata, dict) else None
    if isinstance(md_title, dict):
        md_title = md_title.get("value")
    return str(attrs.get("extensionTitle") or attrs.get("text") or md_title or "")


def get_param(node: dict[str, Any], key: str) -> Any:
    attrs = node.get("attrs") or {}
    params = attrs.get("parameters") or {}
    if "guestParams" in params:
        return (params.get("guestParams") or {}).get(key)
    wrapper = (params.get("macroParams") or {}).get(key)
    return wrapper.get("value") if isinstance(wrapper, dict) else None


def iter_extensions(node: Any):
    if isinstance(node, list):
        for item in node:
            yield from iter_extensions(item)
    elif isinstance(node, dict):
        if node.get("type") in EXT_TYPES:
            yield node
        for child in node.get("content") or []:
            yield from iter_extensions(child)


def get_doc(data: Any) -> Any:
    if isinstance(data, dict) and data.get("type") == "doc":
        return data
    if isinstance(data, dict) and isinstance(data.get("body"), dict):
        return data["body"]
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw", nargs="?", help="Raw Aura params value")
    parser.add_argument("--input", "-i", help="File containing one raw params value")
    parser.add_argument("--adf", help="ADF JSON file or full getConfluencePage JSON response")
    parser.add_argument("--macro-title", help="Decode first macro whose displayed title contains this text")
    parser.add_argument("--all", action="store_true", help="Decode all extension nodes with a params value")
    args = parser.parse_args()

    if args.adf:
        with open(args.adf, encoding="utf-8") as f:
            data = json.load(f)
        results = []
        for ext in iter_extensions(get_doc(data)):
            raw = get_param(ext, "params")
            if not raw:
                continue
            title = macro_title(ext)
            if args.macro_title and args.macro_title.lower() not in title.lower():
                continue
            try:
                decoded = decode_aura_params(raw)
            except Exception as exc:
                decoded = {"_decode_error": str(exc)}
            results.append({"title": title, "params": decoded})
            if args.macro_title and not args.all:
                break
        print(json.dumps(results if args.all or not args.macro_title else (results[0] if results else None), ensure_ascii=False, indent=2))
        return

    if args.input:
        with open(args.input, encoding="utf-8") as f:
            raw = f.read().strip()
    elif args.raw:
        raw = args.raw.strip()
    else:
        raw = sys.stdin.read().strip()

    print(json.dumps(decode_aura_params(raw), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
