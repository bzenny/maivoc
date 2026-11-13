# Maivoc MVP acceptance — pending actual integration testing

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
- [ ] Transparent mark and lockup PNG files in GitHub (generated via brand workflow)
- [ ] Generated 192/512 icons, maskable icon and browser/iOS icons have correct sizes
- [ ] Maivoc manifest is served as `/manifest.webmanifest` from live image, `short_name=Maivoc`
- [ ] Custom endpoint model picker labels communicate Local/Free accurately
- [ ] Install on Android and iOS displays Maivoc name + correct connected-M icon (test clean install and existing SW cache)
- [ ] Existing LibreChat instance receives updated compose overlay and restarts with no errors
- [ ] Upstream attribution and brand/media documentation are visible
