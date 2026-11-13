# Maivoc media usage, deployment and provenance

## Canonical source-of-truth
`assets/branding/maivoc-mark.svg` and `assets/branding/maivoc-lockup.svg` are the editable vector master files. The mark has a **truly transparent SVG canvas**. Never start from a screenshot/marketing board or an automatically generated portal/lock image.

## Generated assets (committed in M4)
| Repository file | Alpha / background | Purpose |
|---|---|---|
| `assets/branding/maivoc-mark.png` | Transparent, 1024² | Logo/icon master, press and splash materials |
| `assets/branding/maivoc-lockup.png` | Transparent, 1800×440 | Wordmark + connected-M |
| `assets/branding/pwa/favicon-16x16.png` | Transparent | Browser favicon |
| `assets/branding/pwa/favicon-32x32.png` | Transparent | Browser favicon |
| `assets/branding/pwa/apple-touch-icon-180x180.png` | Opaque charcoal | iOS home screen |
| `assets/branding/pwa/icon-192x192.png` | Opaque charcoal | Web/Android PWA |
| `assets/branding/pwa/icon-512x512.png` | Opaque charcoal | Larger web/PWA icon |
| `assets/branding/pwa/maskable-icon.png` | Opaque charcoal / safe margin | Maskable Android PWA |
| `assets/branding/pwa/manifest.webmanifest` | JSON | App installation name and icon mapping |

## Rebuild / audit
```bash
python3 -m pip install Pillow==11.3.0 CairoSVG==2.8.2
python3 scripts/build_brand_assets.py
python3 scripts/verify_brand_assets.py
```
Assets on `feat/m4-branding` are generated and committed by `.github/workflows/brand-assets.yml` when vector masters change. The production app should consume the committed PNGs; end users do **not** need Python imaging dependencies.

## Runtime mounting: official LibreChat image, not a fork
LibreChat v0.8.8's `client/vite.config.ts` generates `client/dist/manifest.webmanifest` at build-time. The pinned Docker image serves the built assets from `/app/client/dist`. The Maivoc Compose override bind-mounts the custom manifest and icon filenames on those existing paths; `scripts/bootstrap.sh` copies the override into the Git-ignored upstream runtime.

**Existing installations:** copy updated `config/docker-compose.override.yml` to `upstream/LibreChat/docker-compose.override.yml` and run `docker compose up -d --force-recreate api` from the upstream directory. Run `docker compose config -q` before recreating. This preserves the upstream codebase.

**Cached PWA caveat:** LibreChat's built service worker precaches the upstream icon/manifest. An already-installed client may continue to display old icon/name from cache despite runtime bind mounts. Uninstall the prior PWA and clear site data for a first test. For a guaranteed upgrade-safe install experience across versions, M4 should be tested on live Android/iOS and, if stale precaches persist, move manifest/icon overlay into the image **build** process or make a minimal upstream-compatible patch. Do not promise manifest changes are instant on every installed client.

## Provider trust naming
- Ollama: **Local · Private** (private only when actually local and no remote gateway).
- OpenRouter, Groq: **Free · Limits apply** (cloud, provider policies/quotas).
- Google Gemini: eligible free-tier depending on account/model/region (cloud; data-use policies apply).
- Anthropic/OpenAI: **Paid · Billed to your key** for API plans, not consumer subscriptions.
Current custom-endpoint labels come from `modelDisplayLabel` in `config/librechat.yaml`. Built-in Google, Anthropic and OpenAI pickers may not expose matching subtitles without a future tested UI customization; we document these distinctions in onboarding and avoid claiming otherwise.

## Third-party provenance
Maivoc art is project-authored. The engine is LibreChat (MIT) and is separately credited: https://github.com/LibreChat-AI/LibreChat. Do not remove required copyright or license notices and do not use upstream logos as Maivoc logos.
