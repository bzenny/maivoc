#!/usr/bin/env python3
"""M5: exercise a real, freshly booted LibreChat v0.8.8 Docker instance.

No external AI API calls, provider credentials, or test data uploads.
Runs only against http://127.0.0.1:3080 on an ephemeral CI runner.
"""
from __future__ import annotations

import json
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
    expected = ["OpenRouter", "Groq", "ollama", "google", "agents", "anthropic", "openAI"]
    raw_names = list(data.keys())
    # LibreChat v0.8.8's actual frontend mapEndpoints() sorts by each
    # endpoint config's `order` value; raw JSON object key order is NOT UI order:
    # client/src/utils/endpoints.ts (LibreChat-AI/LibreChat, tag v0.8.8).
    def client_order(key: str) -> float:
        entry = data.get(key) or {}
        if not isinstance(entry, dict):
            return 0
        return entry.get("order") or 0

    ordered = [name for name in sorted(raw_names, key=client_order) if name in expected]
    print("Provider order computed from live endpoint order fields:", ordered)
    check(ordered == expected,
          "picker ordering contract matches v0.8.8 mapEndpoints() (free-first)")
    check(not any(x.lower() == "assistants" for x in raw_names),
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

# These are actual failure signatures from LibreChat v0.8.8, not guesses
# about what a scheduler error might say. Regressions are tested by a live
# scheduler-disabled CI boot plus an isolated log parser test.
STARTUP_FAILURE_PATTERNS = {
    "scheduler not started": r"\[schedules\][^\n]*scheduler\s+NOT\s+started",
    "scheduler permanently unavailable": r"PERMANENTLY\s+unavailable",
    "initialization failed": r"Post-listen initialization failed",
    "server failed to start": r"Failed to start server:",
    "startup config error": r"Error in startup config",
    "scheduler single-process error": r"SCHEDULES_SINGLE_PROCESS must",
    "scheduling disabled": r"schedule.*disabled",
}

# No error-level startup lines are allowlisted initially. Add a *specific*
# proven-benign message only with documentation and a regression fixture.
ALLOWED_ERROR_LEVEL_LOGS: tuple[str, ...] = ()
ERROR_LEVEL_RE = re.compile(
    r"(?:^|[\s|])(?:ERROR|FATAL)(?=[:\s\]])",
    flags=re.IGNORECASE,
)


def assert_clean_api_logs(logs: str) -> None:
    """Fail closed on known scheduling/initialization failures and error logs.

    Never reproduce raw log lines in errors: they may contain private data.
    """
    for label, pattern in STARTUP_FAILURE_PATTERNS.items():
        if re.search(pattern, logs, flags=re.IGNORECASE):
            raise AssertionError(f"API log contains forbidden startup condition: {label}")
        print(f"PASS: no API startup failure: {label}")

    for line in logs.splitlines():
        if ERROR_LEVEL_RE.search(line) and not any(
            re.search(allowed, line) for allowed in ALLOWED_ERROR_LEVEL_LOGS
        ):
            raise AssertionError("API log contains an unallowlisted ERROR/FATAL level line")
    print("PASS: no unallowlisted API ERROR/FATAL level lines")


def check_logs() -> None:
    logs = compose("logs", "--no-color", "api").stdout
    assert_clean_api_logs(logs)

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

    # A real cold restart of API + persistence services: the user record must
    # survive, not merely remain in the same running MongoDB process.
    compose("stop", "api", "meilisearch", "mongodb")
    compose("start", "mongodb", "meilisearch", "api")
    ready()
    code, persisted = json_response("/api/auth/login", "POST",
                                    {"email": email, "password": password})
    check(code == 200 and isinstance(persisted, dict) and bool(persisted.get("token")),
          "owner account survives complete service stop/start and can log in")
    code, cfg = json_response("/api/config")
    check(code == 200 and cfg.get("registrationEnabled") is False,
          "registration lock persists after complete service restart")
    check_logs()
    print("M5 RUNTIME SMOKE TEST PASSED — no model-provider calls made.")

if __name__ == "__main__":
    main()
