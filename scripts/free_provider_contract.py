#!/usr/bin/env python3
"""Opt-in real streaming checks for free-tier provider APIs.

Tests the external provider and its configured model, NOT the Maivoc UI path.
Never prints credentials, request bodies, response bodies, or error payloads.
No network call occurs without an explicit --provider and its environment key.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Iterator

MODELS = {
    "openrouter": "openrouter/free",
    "groq": "openai/gpt-oss-20b",
    "gemini": "gemini-3.5-flash-lite",
}
ENV_KEYS = {
    "openrouter": "MAIVOC_OPENROUTER_API_KEY",
    "groq": "MAIVOC_GROQ_API_KEY",
    "gemini": "MAIVOC_GEMINI_API_KEY",
}
URLS = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions",
    "gemini": "https://generativelanguage.googleapis.com/v1beta/models/"
              "gemini-3.5-flash-lite:streamGenerateContent?alt=sse",
}


def sse_data_lines(response) -> Iterator[str]:
    """Read standards-compatible SSE 'data:' lines, ignoring comments/events."""
    for raw in response:
        line = raw.decode("utf-8", errors="replace").strip()
        if line.startswith("data:"):
            yield line[5:].strip()


def extract_text(provider: str, item: dict) -> str:
    if provider == "gemini":
        chunks = [
            part.get("text", "")
            for candidate in item.get("candidates", [])
            for part in (candidate.get("content") or {}).get("parts", [])
            if isinstance(part, dict)
        ]
        return "".join(x for x in chunks if isinstance(x, str))
    chunks = [
        (choice.get("delta") or {}).get("content")
        for choice in item.get("choices", [])
        if isinstance(choice, dict)
    ]
    return "".join(x for x in chunks if isinstance(x, str))


def probe(provider: str, key: str) -> None:
    prompt = "Reply with one friendly sentence; this is an API smoke test."
    url = URLS[provider]
    if provider == "gemini":
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 80},
        }
        headers = {"Content-Type": "application/json",
                   "Accept": "text/event-stream", "x-goog-api-key": key}
    else:
        payload = {"model": MODELS[provider], "stream": True,
                   "max_tokens": 80, "messages": [{"role": "user", "content": prompt}]}
        headers = {"Content-Type": "application/json",
                   "Accept": "text/event-stream",
                   "Authorization": "Bearer " + key}
    req = urllib.request.Request(url, method="POST",
                                 data=json.dumps(payload).encode("utf-8"),
                                 headers=headers)
    print("CHECK:", provider, MODELS[provider], "(response text and key hidden)", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=45) as response:
            if response.status != 200:
                raise RuntimeError(f"unexpected HTTP status {response.status}")
            event_count = 0
            text_chunks = 0
            for data in sse_data_lines(response):
                if data == "[DONE]":
                    break
                try:
                    event = json.loads(data)
                except ValueError:
                    continue
                if not isinstance(event, dict):
                    continue
                if event.get("error"):
                    raise RuntimeError("provider returned a streaming error")
                event_count += 1
                if extract_text(provider, event):
                    text_chunks += 1
            if event_count == 0 or text_chunks == 0:
                raise RuntimeError("stream did not contain a text completion")
            print(f"PASS: {provider} delivered streamed text ({event_count} SSE events)")
    except urllib.error.HTTPError as exc:
        # Never print exc, its headers, URL, body, or any provider data.
        raise RuntimeError(f"{provider} returned HTTP {exc.code}; check access, model and quota") from None
    except urllib.error.URLError:
        raise RuntimeError(f"{provider} connection failed; check connectivity") from None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=tuple(MODELS), action="append",
                        required=True, help="Provider to test; may repeat")
    args = parser.parse_args()
    providers = list(dict.fromkeys(args.provider))
    missing = [ENV_KEYS[p] for p in providers if not os.environ.get(ENV_KEYS[p])]
    if missing:
        for name in missing:
            print(f"Missing environment variable: {name}", file=sys.stderr)
        print("No requests sent. Provide keys privately, never in GitHub.", file=sys.stderr)
        return 2
    passed = 0
    for provider in providers:
        try:
            probe(provider, os.environ[ENV_KEYS[provider]])
        except RuntimeError as err:
            print(f"FAIL: {err}", file=sys.stderr)
        else:
            passed += 1
    print(f"Provider API streams verified: {passed}/{len(providers)}")
    if passed != len(providers):
        return 1
    print("External provider success is NOT proof that Maivoc's chat UI/key vault works.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
