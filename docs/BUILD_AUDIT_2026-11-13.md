# Maivoc — Full-build technical audit
**Review date:** 2026-11-13 · **Basis:** GitHub `main` after PR #15 and its successful CI run · **Decision:** NO-GO for full `v0.1.0` release.

## What has been genuinely verified
- Maivoc is a small config-and-branding overlay for [LibreChat](https://github.com/LibreChat-AI/LibreChat) v0.8.8, not a fork or separate mobile application.
- Disposable real Docker CI boots API, MongoDB and Meilisearch; the only published host port is `127.0.0.1:3080`. The optional Ollama model server has no published port.
- CI checks app title, manifest/favicon/logo byte-identity, custom provider labels, provider sorting as implemented by LibreChat's frontend, registration enabled temporarily, login, 403 signup restriction after lockdown, and owner login after stopping/restarting API+Mongo+Meilisearch.
- PR #15's *real negative test* removes `SCHEDULES_SINGLE_PROCESS` and confirms `[schedules] scheduler NOT started` is detected by the same log guard used in the normal runtime test. Both jobs passed: [M5 run](https://github.com/bzenny/maivoc/actions/runs/43368515424). Its [merged main-branch CI](https://github.com/bzenny/maivoc/actions/runs/43368917829) also passed.
- Connected-M branding, reversed lockup, transparent PNGs and PWA icons are present. Upstream MIT license notice in `third_party/` matches LibreChat's exact copyright/license.
- Config and credentials live under a Git-ignored runtime tree. The bootstrap generates nondefault secrets and uses chmod 0600 for runtime `.env`; actual secret restore remains untested.

## Release blockers (source-verified)

| ID | Severity | Finding / evidence | Resolution |
|---|---|---|---|
| F01 | **P0** | Upstream `v0.8.8/.env.example` sets **`SEARCH=false`**; Maivoc bootstrap sets `MEILI_MASTER_KEY` but never enables `SEARCH=true`. A running Meilisearch container does not prove searchable history. | [#16](https://github.com/bzenny/maivoc/issues/16): enable it; create/save/find messages and repeat after restart |
| F02 | **P0** | OpenRouter/Groq/Gemini have config and picker checks, **not live AI replies**. Gemini 2.5 is not yet shut down but new-account access is restricted; newer free-tier models need testing. | [#2](https://github.com/bzenny/maivoc/issues/2), [#7](https://github.com/bzenny/maivoc/issues/7): test eligible model, streaming, rate limits, privacy warning |
| F03 | **P0** | Mid-thread model switching, side-by-side compare, credential rotation, Ollama Qwen and history persistence are advertised upstream abilities but not tested in Maivoc. | [#2](https://github.com/bzenny/maivoc/issues/2): user-level E2E tests |
| F04 | **P1** | The `bootstrap.sh` script copies config files to ignored `upstream/LibreChat` only once. `git pull` does **not** sync changed YAML/Compose into the running app. | [#18](https://github.com/bzenny/maivoc/issues/18): safe diff/backup/sync/upgrade/rollback |
| F05 | **P1** | Loopback-only app is inaccessible from another phone; secure PWA install testing requires HTTPS or device-local localhost. Old icons may remain in the service-worker cache. | [#3](https://github.com/bzenny/maivoc/issues/3): privately authenticated HTTPS test access; Android/iOS new and returning browser tests |
| F06 | **P1** | Public Maivoc repository has **no root LICENSE** for its original code/art. The third-party LibreChat MIT license does not automatically license Maivoc-authored files. | [#17](https://github.com/bzenny/maivoc/issues/17): owner-approved code license and clear trademark/art terms |
| F07 | **P1** | GitHub's branch API reports `main.protected=false`, even though review and CI are currently performed. Independent repository rulesets were not audited. | [#19](https://github.com/bzenny/maivoc/issues/19): required PR checks/review, restrict writes/force-pushes |
| F08 | **P1** | Production HTTPS, 2FA, key/DB backup and restore, upgrades and network isolation for managed use are not implemented. MongoDB uses `--noauth` inside the private Compose network. | [#4](https://github.com/bzenny/maivoc/issues/4): private HTTPS, restore/rollback and hardening before remote use |
| F09 | **P1** | RAG/vector services are off by default, yet file upload UX may still imply unsupported document capabilities. | [#11](https://github.com/bzenny/maivoc/issues/11): test image upload separately and hide/label unavailable document features |

## Other findings
- Cloud **free** is not **private**. Current custom endpoint trust labels are good; built-in Google does not show the equivalent data-use warning. Google's official pricing page says free-tier content may be used to improve products.
- `SCHEDULES_SINGLE_PROCESS=true` removes a startup failure in a one-process deployment; it does **not** enable LibreChat Scheduled Chats UI on its own. That requires `interface.schedules` and additional opt-in setup.
- `qwen3:4b` is an optional ~2.5 GB model download and local inference requires available RAM/CPU; not a zero-hardware feature.
- The base LibreChat Compose includes optional admin/RAG image tags still set to `latest`; these are normally disabled by Maivoc profiles but must be pinned/hardened before enabling them.
- CI tests provider **order contract** from server-supplied `order` fields rather than opening the model-picker DOM. Add a real browser smoke test before promising complete UI test coverage.
- Maivoc has manifest branding but lacks distinctive first-run provider onboarding and an automatic update interface. A PWA icon/manifest alone does not prove mobile installability.
- For released software, consider immutable image digest pins and a lockfile/dependency audit. Root licensing and documentation should precede broad redistribution.

## Go / no-go
**GO:** personal developer preview on Linux Mint, owner-only, localhost, with manual model-provider testing and no public exposure.

**NO-GO:** completed free-first/multi-model experience, verified searchable chats, normal-consumer PWA install, public HTTPS instance, managed multi-user service, or `v0.1.0` official release.

## Order of execution
1. Enable and end-to-end test search including restart (#16).
2. Validate free provider responses and Ollama, switch/compare, key persistence (#2/#7).
3. Private HTTPS phone access, mobile and service-worker update tests (#3).
4. Clarify file upload (#11); then upgrade/backup/restore (#18/#4).
5. Approve root license and protect main (#17/#19), then run release checklist and explicitly authorize `v0.1.0`.

**Authoritative references:**
- [LibreChat v0.8.8 .env defaults](https://github.com/LibreChat-AI/LibreChat/blob/v0.8.8/.env.example), [Meilisearch search setup](https://www.librechat.ai/docs/configuration/meilisearch)
- [Google Gemini model list and 2.5 access](https://ai.google.dev/gemini-api/docs/models), [Gemini pricing/data handling](https://ai.google.dev/gemini-api/docs/pricing)
- [OpenRouter free router](https://openrouter.ai/collections/free-models/)
- [MDN PWA installability](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)
- [LibreChat scheduling configuration](https://www.librechat.ai/docs/configuration/scheduled_chats)

No secrets, account data or private logs were used or committed for this review.
