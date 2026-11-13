# Upstream attribution and dependency provenance

Maivoc is an independent community configuration/experience layer, **not** an official LibreChat project or endorsement.

## Incorporated

1. **LibreChat** — https://github.com/LibreChat-AI/LibreChat — MIT; official project and copyright notice retained verbatim in `third_party/LibreChat-LICENSE`. Pinned source tag `v0.8.8` (release 2026-09-30); `scripts/bootstrap.sh` fetches this repository into ignored `upstream/LibreChat`. Features used: chat/DB/history, provider endpoints, BYOK credential UI, model switching and comparisons.
2. **Ollama** — https://github.com/ollama/ollama — optional separate runtime container `ollama/ollama:0.40.16`; no source vendored. Review Ollama's repository license and image notices as part of distribution audit.
3. **Qwen3 model weights** — https://ollama.com/library/qwen3 — **not vendored**; users explicitly pull `qwen3:4b`. Review model license and acceptable deployment conditions before commercial distribution.

## Evaluated, not incorporated
- https://github.com/andrepul/LibreChat-PWA — possible PWA reference only. No source/assets copied.
- Hosted provider APIs OpenRouter, Groq, Google, OpenAI, Anthropic — integration points, no provider code vendored.

## Rule for every future copied repo or asset
Record original author, source URL, license, commit/tag, files reused, modifications, notice location, and attribution destination. Retain required copyright/license text in distributed copies, verify transitive assets independently, and give upstream authors appropriate credit. Maivoc-authored code licensing remains undecided; LibreChat's MIT license does not automatically assign Maivoc's own license.
