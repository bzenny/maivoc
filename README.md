# Maivoc — every model, one workspace

**Status:** integration foundation proposed; not yet deployed or validated against running containers.
**Upstream:** [LibreChat](https://github.com/LibreChat-AI/LibreChat) v0.8.8 (MIT).
**Strategy:** personal self-hosting first, managed multi-user service only after a separate security/tenant-isolation design.

Maivoc offers cloud and local AI models in one browser/PWA workspace. Start free-first: Ollama on your own hardware, OpenRouter's free router, Google Gemini's eligible free API tier, and Groq's limited free tier. Optional OpenAI and Anthropic use **separate API billing**, not personal ChatGPT/Claude subscriptions. All cloud providers require their own free account/API key, subject to regional availability and rate limits.

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
