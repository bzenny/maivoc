# Maivoc — every model, one workspace

**Status:** self-hosted MVP development baseline verified by live, disposable Docker runtime CI; **not released or publicly deployed**. Real provider replies, local Qwen, mobile installation, HTTPS and backups remain to be tested. See [MVP readiness](docs/MVP_STATUS.md).
**Upstream:** [LibreChat](https://github.com/LibreChat-AI/LibreChat) v0.8.8 (MIT).
**Strategy:** personal self-hosting first, managed multi-user service only after a separate security/tenant-isolation design.

Maivoc offers cloud and local AI models in one browser/PWA workspace. Start free-first: Ollama on your own hardware, OpenRouter's free router, Google Gemini's eligible free API tier, and Groq's limited free tier. Optional OpenAI and Anthropic use **separate API billing**, not personal ChatGPT/Claude subscriptions. All cloud providers require their own free account/API key, subject to regional availability and rate limits.

## Maivoc identity (M4)

The canonical icon is the **connected-M** (violet→mint M wings with three white connected nodes), not the portal/lock symbol. [Brand guide](docs/BRANDING.md) · [Media and install guide](docs/MEDIA_GUIDE.md).

![Maivoc connected-M icon](assets/branding/maivoc-mark.svg)

Brand files live in `assets/branding/`. Use the [light lockup](assets/branding/maivoc-lockup.png) on bright backgrounds and the [reversed lockup](assets/branding/maivoc-lockup-reversed.png) on dark backgrounds. Both have a font-independent outlined Inter wordmark. The transparent PNG master and opaque mobile/PWA icons are generated from SVG and committed by GitHub Actions. This repo's Compose overlay mounts the Maivoc web manifest and branded images onto the pinned official LibreChat application. Test an actual phone installation before calling PWA readiness complete.

**Provider trust:** `Local · Private` (Ollama on your hardware); `Free · Limits apply` (rate-limited cloud free tiers); `Paid · Billed to your key` (optional APIs). The custom endpoint labels are set in YAML; not all built-in provider picker subtitles can be changed through configuration. See the guide.

## Automated runtime verification (M5)

GitHub Actions runs `scripts/test_m5_runtime.py` against a **fresh, real pinned LibreChat image** (not only the Maivoc static config). It checks HTTP readiness, byte-for-byte PWA asset overlays, one-time signup/login, ordered provider names and trust labels, blocked registrations after disabling signup, owner re-login, and startup failure signatures. No cloud model calls are made or user keys required. Logs and credentials are not uploaded to CI artifacts.

To run the same test on an empty disposable instance (this registers and locks its throwaway test account):

```bash
bash scripts/bootstrap.sh
cd upstream/LibreChat && docker compose up -d
cd ../..
python3 scripts/test_m5_runtime.py
```

**Important:** Do not run this against your existing personal instance; it sets `ALLOW_REGISTRATION=false` and creates a test account. Runtime CI is not a replacement for provider replies, mobile installation tests, or recovery/backup testing.

## Run locally on Linux Mint

Prerequisites: Git, Python 3, Docker Engine with the Compose **v2.24.4+** plugin, and a Docker-capable Linux user.

```bash
git clone https://github.com/bzenny/maivoc.git
cd maivoc
bash scripts/bootstrap.sh
cd upstream/LibreChat
docker compose config -q
docker compose up -d
```

Open **http://localhost:3080**. The setup binds its HTTP port to **127.0.0.1** only. The free-first picker is ordered by `ENDPOINTS=custom,google,agents,anthropic,openAI`, so custom free endpoints appear before optional paid providers and the old Assistants picker is hidden. `SCHEDULES_SINGLE_PROCESS=true` enables scheduled features in this single-container development setup. Register your first account, then set `ALLOW_REGISTRATION=false` in `upstream/LibreChat/.env` and recreate the API container (`docker compose up -d --force-recreate api`). Do not publish a login before doing this. Secrets are generated in a Git-ignored local runtime; back up the credential encryption key and IV separately.

### Free cloud connectors

On the model selector, enter your **own** credentials:

- **OpenRouter** — select `openrouter/free` to avoid selecting a paid model by accident. [Create key](https://openrouter.ai/settings/keys).
- **Google Gemini** — select `gemini-2.5-flash-lite` or `gemini-2.5-flash` if currently free/available to your account. [Create key](https://aistudio.google.com/apikey).
- **Groq** — select `openai/gpt-oss-20b`. [Create key](https://console.groq.com/keys).
- **OpenAI/Anthropic (optional)** — bring paid API credentials only if desired.

**Important:** A cloud free tier is not a privacy guarantee. Read each provider's data-handling and retention policy; Gemini free-tier content may be used for product improvement. Free limits, models, and eligibility change.

### Local Ollama (optional)

To keep local models private inside the Compose network, start an opt-in Ollama container (no published Ollama port):

```bash
cd upstream/LibreChat
docker compose --profile local-model up -d ollama
docker compose --profile local-model exec ollama ollama pull qwen3:4b
```

Then select **Ollama** → `qwen3:4b` in Maivoc. This uses local CPU/RAM; a GPU-capable deployment can be added later. The default startup does not pull large model weights. Running Ollama on a remote personal computer requires a separate authenticated/private network plan; **never expose port 11434 publicly**.

### Scope and limitations

This first branch includes configuration, validation, and deployment safeguards—not a finished PWA, credential dashboard, SaaS, or verified end-to-end deployment. The tagged LibreChat Compose file includes floating development images: Maivoc pins the main API image and excludes optional development services by default. See `docs/ARCHITECTURE.md`, `docs/PROVIDERS.md`, `docs/ACCEPTANCE.md`, and `docs/UPSTREAM.md`.

**Already bootstrapped?** `scripts/bootstrap.sh` deliberately refuses to overwrite an existing `upstream/LibreChat` folder. Add `ENDPOINTS=custom,google,agents,anthropic,openAI` and `SCHEDULES_SINGLE_PROCESS=true` to your existing `upstream/LibreChat/.env` manually, then recreate the API container with `docker compose up -d --force-recreate api`. These two values are generated automatically only on a **fresh** bootstrap.

No credentials, chat content, or local runtime files belong in Git. Maivoc is independent of, and not endorsed by, the LibreChat project.
