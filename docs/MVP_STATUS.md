# Maivoc — MVP readiness ledger

**As of 2026-11-13 (Review #4).** Target: **v0.1.0**, not yet tagged.
**Foundation:** LibreChat `v0.8.8` (MIT), Docker Compose, one browser/PWA codebase, free-first BYOK, private personal instance first.

| Capability | Implementation | Actual verification | Release impact |
|---|---|---|---|
| Pinned upstream, private loopback app, MongoDB and Meilisearch | Implemented | Fresh Docker test and [runtime CI](https://github.com/bzenny/maivoc/actions/runs/43350676814) | Baseline passed |
| First owner account, login, registration lock | Implemented | Runtime CI registers/logs in, disables registration, rejects 403, owner re-login passes | Baseline passed |
| Endpoint order and custom trust labels | Implemented | Runtime CI follows LibreChat's actual frontend `order` sorting and confirms labels; no Assistants | Baseline passed |
| Connected-M branding, asset mounting and dark-mode reversed lockup | Implemented | PR #12 asset workflow, static PNG checks; original logo assets byte-verified by real runtime CI | Need mobile visual test |
| Web manifest and install icons | Implemented | Runtime CI serves correct manifest, icons and SVG bytes | Actual PWA installation pending |
| Free cloud connectors OpenRouter, Groq, Gemini | Configured | **No real model replies**; keys not provided to CI | Blocking |
| Optional Ollama/Qwen local model | Configured | Qwen image/model download and generation not verified | Blocking |
| Mid-conversation switching and side-by-side comparison | Upstream capability | Not exercised with live models | Blocking |
| Persistent chat history and search | Search enabled | Real authenticated message-save/search verified before and after full Docker stop/start; user-facing history/search UI still needs validation | API search verified, UI pending |
| API-key persistence and rotation | Upstream capability | Not tested with real credentials | Blocking |
| File/image upload with RAG disabled | Partially available upstream | UX behavior undecided (#11) | Blocking for clear MVP UX |
| Android/iOS phone installation | Brand manifest/assets configured | Clean and returning-client tests not performed (#3) | Blocking |
| Remote HTTPS, 2FA, recovery/backup/restore | Not implemented | Not verified (#4) | Blocking for remote self-hosted release |
| GitHub versioning and change validation | Implemented | PR CI passed; live runtime CI implemented | Baseline passed |
| One-click updates / release deployment | Not implemented | No production site or deployment checks | Future release gate |
| Managed multi-tenant product | Deliberately deferred | Not implemented (#10) | Post-MVP |

## Confirmed changes

- [PR #1](https://github.com/bzenny/maivoc/pull/1): free-first self-hosted configuration baseline.
- [PR #8](https://github.com/bzenny/maivoc/pull/8): Maivoc branding, PWA overlays and trust labels.
- [PR #9](https://github.com/bzenny/maivoc/pull/9): remove ignored Gemini YAML.
- [PR #12](https://github.com/bzenny/maivoc/pull/12): reversed light/dark lockup, font-independent outlines and branch-safe assets.
- [PR #13](https://github.com/bzenny/maivoc/pull/13): actual pinned Docker integration and auth/UI-order contract checks.
- [PR #13 passing runtime CI](https://github.com/bzenny/maivoc/actions/runs/43350676814): proves live app startup on a disposable runner, **not** real provider inference.

## Remaining work in recommended order

1. [#7 Gemini modernization](https://github.com/bzenny/maivoc/issues/7): verify supported free-tier model; consider custom endpoint with explicit data-use warning, but only after streaming and title behavior are confirmed.
2. [#2 Real provider and model tests](https://github.com/bzenny/maivoc/issues/2): cloud replies, Ollama model pull, mid-thread switching, comparison, key persistence and history across restart.
3. [#3 Android/iOS testing](https://github.com/bzenny/maivoc/issues/3): clean and cached installations, navigation, key entry, narrow-screen compare.
4. [#11 File-upload UX](https://github.com/bzenny/maivoc/issues/11): distinguish image upload from RAG document upload, hide or label unsupported paths.
5. [#4 Secure remote hosting](https://github.com/bzenny/maivoc/issues/4): HTTPS, auth, backups, restore and rollback.
6. Only after the release gates pass: tag `v0.1.0`.

**Out of scope:** [#10 managed architecture](https://github.com/bzenny/maivoc/issues/10) until the personal MVP passes. The same application may later be hosted as a managed service after tenant-isolation and security design.

## Hard boundary

Do not put real model keys, cloud credentials, private chat content, database volumes or encryption secrets in GitHub or CI logs. An API free tier is not the same as private inference. The project is a LibreChat-based independent application; preserve MIT notices and upstream credit.

## Review #5 — M5 scheduler regression hardening
The original M5 test passed despite LibreChat's `[schedules] scheduler NOT started` error when `SCHEDULES_SINGLE_PROCESS` was removed. The new regression suite tests that real failure path, disallows unallowlisted API ERROR/FATAL lines, and tests MongoDB-backed login persistence after a full Compose stop/start. See `scripts/test_m5_log_guard_unit.py`, `scripts/test_m5_scheduler_regression.py`, and `.github/workflows/runtime-smoke.yml`. Mark these completed only after the latest GitHub Actions jobs pass.

## Search and provider remediation (search API verified; live provider calls pending)
New installs explicitly enable LibreChat full-text search with Meilisearch telemetry disabled and a unique master key. Runtime CI writes a real message through LibreChat and searches it before and after a cold restart. Gemini's new bootstrap default is `gemini-3.5-flash-lite` (officially documented free-tier model), with actual live account response tests pending. Existing installations are not overwritten by `git pull`; follow README instructions and preserve existing secrets.
