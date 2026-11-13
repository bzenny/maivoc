#!/usr/bin/env python3
"""M5 negative E2E: prove live scheduler failure is rejected by check_logs().

Only run on the disposable GitHub CI runner whose bootstrap script has had
SCHEDULES_SINGLE_PROCESS intentionally removed before startup.
"""
from __future__ import annotations

import re
import time

from test_m5_runtime import ready, compose, check_logs

OBSERVED_FAILURE = re.compile(
    r"\\[schedules\\][^\\n]*scheduler\\s+NOT\\s+started|PERMANENTLY\\s+unavailable",
    re.IGNORECASE,
)


def main() -> None:
    ready()
    deadline = time.monotonic() + 90
    while time.monotonic() < deadline:
        # Never print the raw logs: they may contain secrets.
        logs = compose("logs", "--no-color", "api").stdout
        if OBSERVED_FAILURE.search(logs):
            print("PASS: deliberately disabled scheduler emitted expected failure signal")
            break
        time.sleep(3)
    else:
        raise AssertionError("Negative E2E invalid: no real scheduler failure observed")

    # A successful guard MUST reject this instance. The negative test succeeds
    # only if the real production check_logs() function raises.
    try:
        check_logs()
    except AssertionError as exc:
        reason = str(exc)
        if "scheduler" not in reason.lower():
            raise AssertionError("Log guard failed for an unrelated reason") from exc
        print("PASS: check_logs() correctly rejects real scheduler failure")
    else:
        raise AssertionError(
            "REGRESSION: check_logs() passed despite the real scheduler failure"
        )


if __name__ == "__main__":
    main()
