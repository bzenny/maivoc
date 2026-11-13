# Maivoc free-provider integration tests (BYOK)

## What is tested
The **automated** free-first integration checks confirm that current LibreChat v0.8.8 can start, the model picker advertises the intended providers in free-first order, and real message search works after cold restart. No third-party API key is stored in GitHub, so these checks do **not** prove the cloud inference path.

The **optional** script `scripts/free_provider_contract.py` sends a short harmless prompt straight to each provider's **official API**, checks that the response is valid streamed SSE text, and reports **only** PASS/FAIL and HTTP status. It does not print keys or returned text. This is an upstream connectivity/entitlement test, **not** Maivoc UI end-to-end integration.

| Provider | Model | Credentials |
|---|---|---|
| OpenRouter | `openrouter/free` | Your free OpenRouter API key |
| Groq | `openai/gpt-oss-20b` | Your Groq API key on a free-enabled account |
| Google | `gemini-3.5-flash-lite` | Your Gemini API key with eligible free tier |

Cloud models are not private. Google states that free-tier prompts/responses may be used to improve its products. Never send confidential content to these test endpoints. Free eligibility, usage limits and model names can change.

## Run from a private Linux Mint terminal

Do not paste keys into a chat or commit them to `.env` in the Maivoc repository.

```bash
cd maivoc
read -r -s -p "OpenRouter test key: " MAIVOC_OPENROUTER_API_KEY; echo
read -r -s -p "Groq test key: " MAIVOC_GROQ_API_KEY; echo
read -r -s -p "Gemini test key: " MAIVOC_GEMINI_API_KEY; echo
export MAIVOC_OPENROUTER_API_KEY MAIVOC_GROQ_API_KEY MAIVOC_GEMINI_API_KEY
python3 scripts/free_provider_contract.py --provider openrouter --provider groq --provider gemini
unset MAIVOC_OPENROUTER_API_KEY MAIVOC_GROQ_API_KEY MAIVOC_GEMINI_API_KEY
```

You may test only one provider by specifying one `--provider` and its environment key. Errors (401, 403, 404, 429) should be investigated against the account model list, quotas, or region; do not silently route to paid models.

## Final in-app acceptance (manual until scripted)
1. Log into the **private** Maivoc instance as the owner.
2. For each provider enter the same personal key through LibreChat's model-key dialog (do not paste into chat history).
3. Send a short prompt and confirm streaming output, completion and any rate-limit notices.
4. Switch models during a conversation; confirm previous context remains visible.
5. Run side-by-side compare between two configured free models and check both results.
6. Restart the whole stack, log in again, verify conversations still exist and are searchable.
7. Revoke/replace a key through the UI and confirm old access does not persist unexpectedly.
8. Check provider activity/billing dashboard for **zero charge** on the free requests.

Record only sanitized pass/fail/date/account tier, never API keys, private conversation text, request/response payloads or unredacted logs.

## Primary references
- https://ai.google.dev/gemini-api/docs/pricing
- https://openrouter.ai/collections/free-models/
- https://console.groq.com/docs/models
- https://www.librechat.ai/docs/configuration/meilisearch
