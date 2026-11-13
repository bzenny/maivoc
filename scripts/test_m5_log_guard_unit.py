#!/usr/bin/env python3
"""Isolated tests so changes to log parser can never silently disable M5."""
import unittest

from test_m5_runtime import assert_clean_api_logs


class LogGuardTests(unittest.TestCase):
    def assert_rejected(self, sample: str) -> None:
        with self.assertRaises(AssertionError):
            assert_clean_api_logs(sample)

    def test_real_scheduler_not_started(self) -> None:
        self.assert_rejected(
            "LibreChat | [schedules] scheduler NOT started; scheduling features off"
        )

    def test_real_scheduler_permanently_unavailable(self) -> None:
        self.assert_rejected(
            "LibreChat | [schedules] scheduling service PERMANENTLY unavailable"
        )

    def test_error_severity_line(self) -> None:
        self.assert_rejected("LibreChat | 2026-11-13 ERROR: unknown background failure")

    def test_fatal_severity_line(self) -> None:
        self.assert_rejected("LibreChat | FATAL: database connection lost")

    def test_clean_logs(self) -> None:
        assert_clean_api_logs(
            "LibreChat | INFO: Server listening on 3080\n"
            "LibreChat | [schedules] scheduler running"
        )


if __name__ == "__main__":
    unittest.main()
