#!/usr/bin/env python3
"""Read GitHub's 14-day traffic windows; write dated, source-attributed JSON."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OWNER = "dokarpov"
REPOSITORIES = (
    "dokarpov", "decision-systems", "intake-integrity-lab",
    "intake-integrity-site", "rolehint", "policy-kit", "oido-site",
    "daria-exe", "rilatu", "planriva-site",
)
ENDPOINTS = ("views", "clones", "popular/referrers", "popular/paths")
API_VERSION = "2026-03-10"


def retrieve(repo: str, endpoint: str, token: str):
    if repo not in REPOSITORIES or endpoint not in ENDPOINTS:
        raise ValueError("Only allowlisted repositories and traffic endpoints are permitted")
    url = f"https://api.github.com/repos/{OWNER}/{repo}/traffic/{endpoint}"
    req = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "portfolio-traffic-snapshot/1.0",
    })
    try:
        with urlopen(req, timeout=25) as response:
            return json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"GitHub HTTP {exc.code} for {repo}/{endpoint}; check repository token scope and Administration: read") from exc
    except URLError as exc:
        raise RuntimeError(f"GitHub request failed for {repo}/{endpoint}: {exc.reason}") from exc


def collect(token: str, observed_at: str = None) -> dict:
    if not token:
        raise ValueError("PORTFOLIO_TRAFFIC_TOKEN is required; no snapshot was collected")
    observed_at = observed_at or datetime.now(timezone.utc).isoformat(timespec="seconds")
    results = {}
    for repo in REPOSITORIES:
        results[repo] = {
            "views_14d": retrieve(repo, "views", token),
            "clones_14d": retrieve(repo, "clones", token),
            "referrers_14d_top10": retrieve(repo, "popular/referrers", token),
            "paths_14d_top10": retrieve(repo, "popular/paths", token),
        }
    return {
        "source": "GitHub REST Traffic API",
        "api_version": API_VERSION,
        "collected_at_utc": observed_at,
        "window": "rolling_last_14_days",
        "interpretation": "Do not sum overlapping windows or unique counts across repositories",
        "repositories": results,
    }


def main():
    token = os.environ.get("PORTFOLIO_TRAFFIC_TOKEN", "")
    if not token:
        raise SystemExit("Missing PORTFOLIO_TRAFFIC_TOKEN — no analytics data collected")
    result = collect(token)
    date = result["collected_at_utc"][:10]
    destination = Path("reports") / f"github-traffic-{date}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Saved GitHub traffic snapshot: {destination}")


if __name__ == "__main__":
    main()
