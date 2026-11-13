#!/usr/bin/env bash
# Prepare a PRIVATE local LibreChat checkout; never deploy from this script.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$ROOT/upstream/LibreChat"
TAG="v0.8.8"

for cmd in git python3 docker; do
  command -v "$cmd" >/dev/null || { echo "Missing dependency: $cmd" >&2; exit 1; }
done
docker compose version >/dev/null || { echo "Docker Compose plugin is required" >&2; exit 1; }
python3 "$ROOT/scripts/validate.py"
if [[ -e "$DEST" ]]; then
  echo "Refusing to overwrite existing runtime: $DEST" >&2
  exit 1
fi
mkdir -p "$ROOT/upstream"
git clone --branch "$TAG" --depth 1 https://github.com/LibreChat-AI/LibreChat.git "$DEST"
cp "$DEST/.env.example" "$DEST/.env"
cp "$ROOT/config/librechat.yaml" "$DEST/librechat.yaml"
cp "$ROOT/config/docker-compose.override.yml" "$DEST/docker-compose.override.yml"

python3 - "$DEST/.env" "$(id -u)" "$(id -g)" <<'PYENV'
import pathlib, re, secrets, sys
p=pathlib.Path(sys.argv[1])
content=p.read_text()
values={
    "APP_TITLE":"Maivoc",
    "CUSTOM_FOOTER":"[Powered by LibreChat](https://github.com/LibreChat-AI/LibreChat)",
    "ALLOW_EMAIL_LOGIN":"true",
    "ALLOW_REGISTRATION":"true", # ONLY for first local signup, disable immediately
    "ALLOW_SOCIAL_LOGIN":"false",
    "ALLOW_SOCIAL_REGISTRATION":"false",
    "OPENAI_API_KEY":"user_provided",
    "ANTHROPIC_API_KEY":"user_provided",
    "GOOGLE_KEY":"user_provided",
    "GOOGLE_MODELS":"gemini-2.5-flash-lite,gemini-2.5-flash",
    "CREDS_KEY":secrets.token_hex(32),
    "CREDS_IV":secrets.token_hex(16),
    "JWT_SECRET":secrets.token_hex(32),
    "JWT_REFRESH_SECRET":secrets.token_hex(32),
    "MEILI_MASTER_KEY":secrets.token_hex(32),
    "ADMIN_PANEL_SESSION_SECRET":secrets.token_hex(32),
    "UID":sys.argv[2],
    "GID":sys.argv[3],
}
for k,v in values.items():
    pattern=re.compile(rf"^{re.escape(k)}=.*$",re.MULTILINE)
    if pattern.search(content):
        content=pattern.sub(lambda m, k=k,v=v: f"{k}={v}",content)
    else:
        content+=f"\n{k}={v}\n"
p.write_text(content)
p.chmod(0o600)
PYENV

(cd "$DEST" && docker compose config -q)
echo "Prepared at $DEST"
echo "Run: cd upstream/LibreChat && docker compose up -d"
echo "Open http://localhost:3080, create first account, then disable ALLOW_REGISTRATION."
echo "No cloud API keys, public ports, or production deployment were configured."
