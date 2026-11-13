# Architecture decisions — self-hosted now, managed later

## M0: personal instance (approved)
Browser and mobile browsers access the **same LibreChat application**. A PWA installation is a frontend shortcut/client, not an on-device copy of the backend or MongoDB. Use the official pinned LibreChat release and a config-only overlay. Datastore = MongoDB; history search = Meilisearch. RAG/vector and Admin Panel are opt-in and disabled for the minimal default runtime.

Local default: Docker Compose API, MongoDB, Meilisearch. API image `ghcr.io/librechat-ai/librechat:v0.8.8`; only HTTP `127.0.0.1:3080` is published. This prevents accidental LAN/public exposure but does **not** make the app HTTPS-ready for a VPS. The default upstream Compose file pointed the main API at a floating development image and exposed public ports; Maivoc's overlay deliberately corrects both.

Ollama is a separate opt-in Compose service and stores weights in a persistent named volume; no Ollama host port is published. The local model does not automatically follow you to mobile when your own machine is off.

## M1: private remote instance (not built yet)
Separate production Compose overlay with an authenticated HTTPS edge/tunnel, access control, backups/restores, operating-system hardening, 2FA, reverse-proxy correctness, no public internal services, and reviewed registration/SSRF settings. Do NOT reuse the development bind as the entire production network configuration.

## M2: managed multi-user product (not built yet)
Single-instance multi-user login is not by itself adequate tenant isolation. Needs architectural review for tenant-scoped accounts, data and query boundaries, API key encryption/rotation, quota and cost enforcement, cross-tenant tests, deletion/export, abuse controls, observability, incident response, privacy disclosures, billing consent, and migration from personal instances.

## Decisions postponed
True installable PWA support is unverified against pinned release; test Android/iOS first. Native mobile wrappers and app stores only after usability and policy review. No separate frontend codebase, speculative orchestration service, auto-model routing, or paid subscription layer for the MVP.
