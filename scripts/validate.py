#!/usr/bin/env python3
"""Static validation of Maivoc's free-first overlay (no provider calls)."""
from pathlib import Path
import sys
try:
    import yaml
except ImportError:
    print("Install PyYAML for static validation: python3 -m pip install PyYAML==6.0.3", file=sys.stderr)
    sys.exit(2)

root=Path(__file__).resolve().parents[1]
class ComposeLoader(yaml.SafeLoader): pass
ComposeLoader.add_constructor("!override", lambda loader,node: loader.construct_sequence(node))

config=yaml.safe_load((root/"config/librechat.yaml").read_text())
compose=yaml.load((root/"config/docker-compose.override.yml").read_text(), Loader=ComposeLoader)
assert config["version"]=="1.3.17"
custom={item["name"]:item for item in config["endpoints"]["custom"]}
assert {"OpenRouter","Groq","Ollama"} <= set(custom)
assert custom["OpenRouter"]["models"]["default"]==["openrouter/free"]
assert custom["OpenRouter"]["models"]["fetch"] is False
assert custom["Groq"]["apiKey"]=="user_provided"
assert custom["OpenRouter"]["apiKey"]=="user_provided"
assert custom["Ollama"]["baseURL"]=="http://ollama:11434/v1/"
assert compose["services"]["api"]["image"]=="ghcr.io/librechat-ai/librechat:v0.8.8"
assert all(p.startswith("127.0.0.1:") for p in compose["services"]["api"]["ports"])
assert not compose["services"]["ollama"].get("ports")
assert "local-model" in compose["services"]["ollama"]["profiles"]
assert "rag" in compose["services"]["rag_api"]["profiles"]
assert "admin" in compose["services"]["admin-panel"]["profiles"]
assert (root/"scripts/bootstrap.sh").is_file()
# Ensure the bootstrap writes the two tested LibreChat runtime settings.
bootstrap=(root/"scripts/bootstrap.sh").read_text()
assert '"ENDPOINTS":"custom,google,agents,anthropic,openAI"' in bootstrap
assert '"SCHEDULES_SINGLE_PROCESS":"true"' in bootstrap
# M4 manifest, SVG sources, Compose overlay, trust labels.
import json
manifest=json.loads((root/"assets/branding/pwa/manifest.webmanifest").read_text())
assert manifest["short_name"]=="Maivoc" and manifest["display"]=="standalone"
assert manifest["theme_color"]=="#0B0F17"
assert len(manifest["icons"])>=3
assert (root/"assets/branding/maivoc-mark.svg").is_file()
assert (root/"assets/branding/maivoc-lockup.svg").is_file()
api=compose["services"]["api"]
mounts=[v["target"] for v in api["volumes"] if isinstance(v,dict)]
assert "/app/client/dist/manifest.webmanifest" in mounts
assert "/app/client/dist/assets/maskable-icon.png" in mounts
assert custom["Ollama"]["modelDisplayLabel"].endswith("Local · Private")
assert "Free · Limits apply" in custom["OpenRouter"]["modelDisplayLabel"]
assert "Free · Limits apply" in custom["Groq"]["modelDisplayLabel"]
print("Static Maivoc config and branding checks passed; Docker/mobile integration still unverified.")
