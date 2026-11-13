# Maivoc MVP acceptance — verified foundation, release gates pending

- [ ] Free-first: OpenRouter `openrouter/free` responds with BYOK and does not default to a billed model
- [ ] Google Gemini eligible free model responds with BYOK
- [ ] Groq free-tier model responds with BYOK
- [ ] Ollama is unreachable from public network, and `qwen3:4b` responds when opt-in profile started
- [ ] Optional OpenAI and Anthropic credentials work independently
- [ ] Model switch mid-thread retains accessible context; side-by-side comparison works
- [ ] Credential entry, persistence duration, replacement and revocation are tested
- [ ] Search returns previous messages after restart
- [ ] Account signup restricted to owner, 2FA enabled before remote publishing
- [ ] HTTPS via production edge, no leaked internal ports
- [ ] Backup restoration tested including CREDS_KEY/CREDS_IV recovery
- [ ] Android and iOS responsive mobile tests; actual PWA installability established
- [ ] GitHub versioned release, CI passes, reviewed deploy and rollback procedure
- [ ] Privacy: cloud-free-tier warning, data retention/deletion/export documented
- [ ] MIT notice bundled and upstream credits accessible in README/about

Static checks do not count as application or security testing; record dates and evidence.

## M4 brand and PWA tests
- [x] Transparent mark and lockup PNG files in GitHub (generated via brand workflow)
- [x] Generated 192/512 icons, maskable icon and browser/iOS icons have correct sizes
- [x] Maivoc manifest is served as `/manifest.webmanifest` from live image, `short_name=Maivoc`
- [x] Custom endpoint model picker labels communicate Local/Free accurately
- [ ] Install on Android and iOS displays Maivoc name + correct connected-M icon (test clean install and existing SW cache)
- [ ] Existing LibreChat instance receives updated compose overlay and restarts with no errors
- [x] Upstream attribution and brand/media documentation are visible

## M5 actual runtime CI (against disposable real LibreChat)
- [x] GitHub Actions smoke job passes end-to-end on an Ubuntu runner
- [x] Real `/health`, `/readyz`, `/api/config` report ready / title Maivoc
- [x] Manifest, icons, favicon and SVG logo are byte-identical to Git-tracked assets
- [x] Test account registers; login token and ordered `/api/endpoints` work
- [x] Free-first provider names and trust labels match integration contract
- [x] Registration off returns 403 while pre-existing account can login
- [x] No known scheduler/initialization failure signature in startup logs
**Not covered by CI:** real provider responses, local Qwen pull, mid-thread switching, side-by-side compare, history search/persistence, phone installation, production hosting, backups and restore.


## Evidence and interpretation (Review #4)

- [PR #12](https://github.com/bzenny/maivoc/pull/12), merged `9b1cd05`: reversed white-wordmark lockup, SVG wordmark outlines, protected binary generation, media usage instructions.
- [PR #13](https://github.com/bzenny/maivoc/pull/13), merged `0151488`: disposable pinned LibreChat Docker runtime, branding file identity, startup health, endpoint model picker ordering contract, sign-up/login, registration disabled, sanitized startup log assertions.
- [Successful PR runtime CI](https://github.com/bzenny/maivoc/actions/runs/43350676814): passed real Docker startup and auth checks. A successful PR test is not proof of production deployment.
- External Review #4 (2026-11-13): independently reported correct model order, branded assets, owner sign-in and startup. This review is not stored in the repository; the linked GitHub runtime run above is the reproducible evidence.
- All checked entries in **M4** and **M5** above have direct GitHub or runtime evidence. Untested entries remain unchecked.

### Release gate for v0.1.0

**Do not tag yet.** Required before full-MVP sign-off:
1. Connect free cloud BYOK credentials in a private test instance and prove real messages, streaming and error handling for OpenRouter, Groq and an eligible Gemini model (#2, #7).
2. Download, start and invoke Ollama/Qwen on intended hardware; verify it is private and unavailable from public network (#2).
3. Switch models mid-conversation, compare two outputs and verify saved chat search after restart (#2).
4. Test clean and returning-browser PWA installs on Android and iOS, including cached old icons and mobile compare flow (#3).
5. Resolve file-upload behavior without implying unsupported document/RAG features (#11).
6. For remote use: HTTPS, 2FA, backups/restoration and rollback/upgrade validation (#4).
7. Verify distribution compliance and approve a versioned release/tag; do not claim GitHub Actions is a deployment pipeline.

**Post-MVP:** managed multi-user architecture and tenant isolation (#10).
