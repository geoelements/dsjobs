import unittest
from unittest.mock import Mock, patch
from io import StringIO
import sys
from datetime import datetime, timedelta

import dsjobs as ds


class TestRuntimeSummary(unittest.TestCase):
    def test_runtime_summary(self):
        # Create a mock for the `ag` object
        ag_mock = Mock()

        # Mock the return value for getHistory on the mock object
        start_time = datetime.now() - timedelta(minutes=10)

        ag_mock.jobs.getHistory.return_value = [
            {"status": "PENDING", "created": start_time},
            {
                "status": "PROCESSING_INPUTS",
                "created": start_time + timedelta(seconds=3),
            },
            {
                "status": "STAGING_INPUTS",
                "created": start_time + timedelta(seconds=7),
            },  # 3 + 4
            {
                "status": "STAGED",
                "created": start_time + timedelta(seconds=11),
            },  # 7 + 4
            {
                "status": "STAGING_JOB",
                "created": start_time + timedelta(seconds=18),
            },  # 11 + 7
            {
                "status": "SUBMITTING",
                "created": start_time + timedelta(seconds=30),
            },  # 18 + 12
            {
                "status": "QUEUED",
                "created": start_time + timedelta(seconds=48),
            },  # 30 + 18
            {
                "status": "RUNNING",
                "created": start_time + timedelta(minutes=1, seconds=14),
            },  # 48 seconds + 26 seconds
            {
                "status": "CLEANING_UP",
                "created": start_time + timedelta(minutes=1, seconds=22),
            },  # 74 seconds + 22 seconds
            {
                "status": "ARCHIVING",
                "created": start_time + timedelta(minutes=1, seconds=22),
            },  # no change
            {"status": "FINISHED", "created": start_time + timedelta(minutes=11)},
        ]

        # Capture the printed output
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            ds.runtime_summary(
                ag_mock, "mock_id"
            )  # Passing the mock object to your function
            output = out.getvalue().strip()
        finally:
            sys.stdout = saved_stdout

        # Expected output based on the mock data
        expected_output = """
Runtime Summary
---------------
PENDING             time: 0:00:03
PROCESSING_INPUTS   time: 0:00:04
STAGING_INPUTS      time: 0:00:04
STAGED              time: 0:00:07
STAGING_JOB         time: 0:00:12
SUBMITTING          time: 0:00:18
QUEUED              time: 0:00:26
RUNNING             time: 0:00:08
CLEANING_UP         time: 0:00:00
ARCHIVING           time: 0:09:38
TOTAL               time: 0:11:00
---------------
""".strip()

        self.maxDiff = None
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()
