"""Offline collector tests: no external credentials, no invented traffic."""
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from tools.github_traffic_snapshot import collect, retrieve, REPOSITORIES


class TrafficCollectorTests(unittest.TestCase):
    def test_requires_token(self):
        with self.assertRaises(ValueError):
            collect("")

    def test_rejects_non_allowlisted_repo(self):
        with self.assertRaises(ValueError):
            retrieve("../other", "views", "dummy")

    def test_rejects_unsupported_endpoint(self):
        with self.assertRaises(ValueError):
            retrieve(REPOSITORIES[0], "users", "dummy")

    @patch("tools.github_traffic_snapshot.retrieve")
    def test_records_source_time_and_all_endpoints(self, mocked):
        mocked.return_value = {"count": 1, "uniques": 1}
        data = collect("dummy", "2026-10-26T12:00:00+00:00")
        self.assertEqual(data["window"], "rolling_last_14_days")
        self.assertEqual(data["collected_at_utc"], "2026-10-26T12:00:00+00:00")
        self.assertEqual(len(data["repositories"]), len(REPOSITORIES))
        self.assertEqual(mocked.call_count, 4 * len(REPOSITORIES))
        for r in data["repositories"].values():
            self.assertIn("views_14d", r)
            self.assertIn("clones_14d", r)


if __name__ == "__main__":
    unittest.main()
