# Provider integration matrix — 2026-11-13

**Free-first does not mean unmetered, anonymous, or private.** Users must create a provider account and BYOK credentials for cloud endpoints; plan eligibility varies by region.

| Connector | MVP | Credential | Free usage | Default model | Privacy / caveat |
|---|---|---|---|---|---|
| Ollama (Qwen) | Configured, opt-in local profile | None; internal placeholder | No per-call provider charges, local compute costs | `qwen3:4b` | No cloud submission if truly local |
| OpenRouter | Configured | User API key | `openrouter/free` routes to free models, rate limited | `openrouter/free` | Third-party model providers see requests |
| Google Gemini API | Built-in configured | User API key | Eligible models have a free tier | `gemini-2.5-flash-lite` / `gemini-2.5-flash` | Free-tier prompts/responses may be used to improve products |
| GroqCloud | Configured | User API key | Limited developer free plan, model-dependent | `openai/gpt-oss-20b` | Usage ceilings and deprecations can change |
| OpenAI | Optional | User API key | Do not assume free inference | User-selected | API billed separately from ChatGPT subscriptions |
| Anthropic | Optional | User API key | Do not assume free inference | User-selected | API billed separately from Claude subscriptions |

## Why we are NOT integrating everything yet

- **Hugging Face Inference Providers:** monthly free credits for free accounts are very small (currently $0.10) and account/provider routing differs. Keep as optional post-validation.
- **Cloudflare Workers AI:** includes a free daily allocation, but needs an account, configured account/model-specific endpoint, and extra gateway security. Evaluate in Stage 2.
- **Cerebras and other rapidly changing tiers:** candidates; verify stable free entitlement, model catalog, and endpoint format before adding.

## Key behavior

LibreChat custom endpoints use `apiKey: "user_provided"`. Built-in endpoints use `OPENAI_API_KEY=user_provided`, `ANTHROPIC_API_KEY=user_provided`, `GOOGLE_KEY=user_provided` in the **runtime** .env. Keys are entered in the chat UI and encrypted server-side with persistent `CREDS_KEY` and `CREDS_IV`. Losing those secrets can make encrypted keys unrecoverable. The UI may offer time-limited credential retention; test the "never expire" option instead of assuming keys always persist.

For cost safety, OpenRouter's initial model list is intentionally **free only** (`fetch:false`). Paid models require an explicit future config change. Groq may bill only on a funded/paid organization plan; verify account-level quotas before promising any spend cap.

## Official sources

- https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints
- https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/openrouter
- https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/groq
- https://www.librechat.ai/docs/configuration/librechat_yaml/ai_endpoints/ollama
- https://www.librechat.ai/docs/configuration/pre_configured_ai/google
- https://openrouter.ai/collections/free-models
- https://ai.google.dev/gemini-api/docs/pricing
- https://console.groq.com/docs/rate-limits
- https://console.groq.com/docs/deprecations
- https://huggingface.co/docs/inference-providers/pricing
- https://developers.cloudflare.com/workers-ai/platform/pricing/
- https://ollama.com/library/qwen3
