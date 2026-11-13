#!/usr/bin/env python3
"""M5: exercise a real, freshly booted LibreChat v0.8.8 Docker instance.

No external AI API calls, provider credentials, or test data uploads.
Runs only against http://127.0.0.1:3080 on an ephemeral CI runner.
"""
from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream" / "LibreChat"
BASE = "http://127.0.0.1:3080"

def check(value, reason: str) -> None:
    if not value:
        raise AssertionError(reason)
    print(f"PASS: {reason}")

def request(path: str, method: str = "GET", payload: dict | None = None,
            token: str | None = None) -> tuple[int, bytes]:
    headers = {"Accept": "application/json", "Origin": BASE, "Referer": BASE + "/"}
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=18) as res:
            return res.status, res.read()
    except urllib.error.HTTPError as err:
        return err.code, err.read(16384)

def json_response(path: str, method: str = "GET", payload: dict | None = None,
                  token: str | None = None) -> tuple[int, dict | list]:
    code, data = request(path, method, payload, token)
    try:
        return code, json.loads(data)
    except (ValueError, UnicodeDecodeError):
        raise AssertionError(f"{path} returned status {code} and non-JSON response") from None

def compose(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["docker", "compose", *args], cwd=UPSTREAM,
                          capture_output=True, text=True, timeout=150, check=True)

def ready(timeout_sec: int = 210) -> None:
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        try:
            code, body = request("/readyz")
            if code == 200 and body.strip() == b"OK":
                return
        except (OSError, TimeoutError):
            pass
        time.sleep(3)
    raise AssertionError("LibreChat /readyz did not reach 200 within timeout; inspect sanitized container status")

def validate_assets() -> None:
    expected = {
        "/manifest.webmanifest": "assets/branding/pwa/manifest.webmanifest",
        "/assets/favicon-16x16.png": "assets/branding/pwa/favicon-16x16.png",
        "/assets/favicon-32x32.png": "assets/branding/pwa/favicon-32x32.png",
        "/assets/apple-touch-icon-180x180.png": "assets/branding/pwa/apple-touch-icon-180x180.png",
        "/assets/icon-192x192.png": "assets/branding/pwa/icon-192x192.png",
        "/assets/icon-512x512.png": "assets/branding/pwa/icon-512x512.png",
        "/assets/maskable-icon.png": "assets/branding/pwa/maskable-icon.png",
        "/assets/logo.svg": "assets/branding/maivoc-mark.svg",
    }
    for path, relative in expected.items():
        code, bytes_served = request(path)
        check(code == 200, f"HTTP 200 for {path}")
        check(bytes_served == (ROOT / relative).read_bytes(),
              f"deployed {path} matches repository bytes")

def validate_endpoint_order(token: str) -> None:
    code, data = json_response("/api/endpoints", token=token)
    check(code == 200 and isinstance(data, dict), "authenticated endpoints API responds")
    # v0.8.8 returns an insertion-ordered object. Keep only known provider keys;
    # non-provider metadata is allowed but must never be mistaken for a model.
    expected = ["OpenRouter", "Groq", "Ollama", "google", "agents", "anthropic", "openAI"]
    raw_names = list(data.keys())
    print("Endpoint API top-level identifiers (provider names only):", raw_names)
    if isinstance(data.get("endpoints"), (list, dict)):
        container = data["endpoints"]
        print("Endpoint API nested identifiers:", list(container.keys()) if isinstance(container, dict) else
              [x.get("name", x.get("endpoint", "<unnamed>")) if isinstance(x, dict) else x for x in container])
    ordered = [name for name in raw_names if name in expected]
    check(ordered == expected,
          "API returns free-first provider order (OpenRouter → Groq → Ollama → Gemini → Agents → Anthropic → OpenAI)")
    check("assistants" not in [x.lower() for x in raw_names],
          "legacy Assistants endpoint hidden")
    dumped = json.dumps(data, ensure_ascii=False)
    for label in ("OpenRouter · Free · Limits apply", "Groq · Free · Limits apply",
                  "Ollama · Local · Private"):
        check(label in dumped, f"endpoint trust label: {label}")

def disable_registration() -> None:
    dotenv = UPSTREAM / ".env"
    text = dotenv.read_text()
    count = len(re.findall(r"^ALLOW_REGISTRATION=.*$", text, flags=re.MULTILINE))
    check(count == 1, "one runtime registration setting")
    text = re.sub(r"^ALLOW_REGISTRATION=.*$", "ALLOW_REGISTRATION=false", text,
                  count=1, flags=re.MULTILINE)
    dotenv.write_text(text)
    compose("up", "-d", "--no-deps", "--force-recreate", "api")
    ready()

def check_logs() -> None:
    logs = compose("logs", "--no-color", "api").stdout
    bad_patterns = (
        "Post-listen initialization failed",
        "Failed to start server:",
        "Error in startup config",
        "SCHEDULES_SINGLE_PROCESS must",
        "schedule.*disabled",
    )
    for pattern in bad_patterns:
        check(not re.search(pattern, logs, flags=re.IGNORECASE),
              f"no startup log failure matching {pattern!r}")

def main() -> None:
    check((UPSTREAM / "docker-compose.yml").is_file(), "pinned upstream checkout exists")
    compose("config", "-q")
    print("PASS: Docker Compose config is valid; LibreChat live boot validates its own schema")
    ready()
    code, health = request("/health")
    check(code == 200 and health.strip() == b"OK", "/health returns 200")
    config_code, config = json_response("/api/config")
    check(config_code == 200 and isinstance(config, dict), "startup config responds")
    check(config.get("appTitle") == "Maivoc", "LibreChat startup API reports Maivoc")
    check(config.get("registrationEnabled") is True, "temporary local registration enabled")
    validate_assets()

    uid = secrets.token_hex(5)
    email = f"maivoc-ci-{uid}@example.org"
    password = secrets.token_urlsafe(26) + "A9!"
    register = {"name": "Maivoc Test", "username": f"ci{uid}",
                "email": email, "password": password,
                "confirm_password": password}
    code, _ = json_response("/api/auth/register", "POST", register)
    check(code == 200, "first owner test account registered")
    code, signed_in = json_response("/api/auth/login", "POST",
                                    {"email": email, "password": password})
    check(code == 200 and isinstance(signed_in, dict) and
          isinstance(signed_in.get("token"), str), "owner login succeeds")
    validate_endpoint_order(signed_in["token"])

    disable_registration()
    code, locked_config = json_response("/api/config")
    check(code == 200 and locked_config.get("registrationEnabled") is False,
          "public config reports registration disabled")
    register["email"] = f"blocked-{uid}@example.org"
    code, _ = json_response("/api/auth/register", "POST", register)
    check(code == 403, "additional registration rejected with HTTP 403")
    code, signed_in_again = json_response("/api/auth/login", "POST",
                                          {"email": email, "password": password})
    check(code == 200 and bool(signed_in_again.get("token")),
          "existing owner login still succeeds")
    check_logs()
    print("M5 RUNTIME SMOKE TEST PASSED — no model-provider calls made.")

if __name__ == "__main__":
    main()
