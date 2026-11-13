# Maivoc — Claude Code standing instructions

Mission: ship a simple, personal-first, free-first AI workspace based on LibreChat. One browser/PWA frontend, self-hosted MVP, managed-tenant option only after explicit redesign.

## Operating principles
1. Read `README.md`, `docs/ARCHITECTURE.md`, `docs/PROVIDERS.md` and `docs/UPSTREAM.md` before editing.
2. Keep LibreChat outside this repo: fetch **v0.8.8** to ignored `upstream/LibreChat`; preserve its MIT license. Configuration before code; no unrelated dependencies.
3. One change per reviewable commit. Explain the pain point, minimal delta, test commands, rollback, and risks.
4. Never paste, log, commit, expose or rotate API keys and persistent secrets. Never commit a generated `.env`, database, chat export or model weight.
5. Free-first is a **default UX**, not an assertion that all models are costless or private. Explicitly label limits and data-sharing risks; do not silently select paid models.
6. Keep local dev ports bound to loopback; never publicly expose Ollama, MongoDB, Meilisearch, admin dashboard or vector DB. Stop before any VPS/domain/cloud deployment.
7. Native mobile app-store publication and managed tenant isolation are **post-MVP**. Do not add a second app or payment system now.
8. Do not claim tests passed unless you ran them. If Docker, credentials or devices are unavailable, mark acceptance tests pending.
9. Record every incorporated GitHub repo, original copyright, license, exact tag/commit and modifications in `docs/UPSTREAM.md`.
10. Before upstream upgrades, compare migration notes, keep images version-pinned, test with a backup and rollback plan.

## Iteration loop
Read docs and code → smallest change → lint `python3 scripts/validate.py` → `bash -n scripts/bootstrap.sh` → inspect diff → test actual Compose where available → review → commit.

Initial UX target: Connect → Converse → Switch → Compare → Search. No unnecessary features or speculative framework rewrites.
