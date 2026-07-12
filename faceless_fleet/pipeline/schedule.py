"""Jittered scheduling — the #1 anti-spam control.

Produces a randomized ISO-8601 publishAt so videos drip out at human-plausible
times instead of all firing at the same minute. Mirrors the deterministic-jitter
idea Claude Code's own scheduler uses to avoid thundering-herd posting.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import random


def _seeded_rng(seed_str: str) -> random.Random:
    h = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16)
    return random.Random(h)


LEDGER = None  # resolved lazily: ROOT/output/schedule_ledger.json


def _ledger_path():
    from .config import ROOT
    p = ROOT / "output" / "schedule_ledger.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _load_ledger(now: dt.datetime) -> list[dict]:
    import json
    p = _ledger_path()
    if not p.exists():
        return []
    try:
        entries = json.loads(p.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    # prune anything already published (past)
    return [e for e in entries
            if dt.datetime.fromisoformat(e["when"]) > now - dt.timedelta(hours=1)]


def _save_ledger(entries: list[dict]) -> None:
    import json
    _ledger_path().write_text(json.dumps(entries, indent=2))


def next_publish_at(cfg: dict, seed: str, now: dt.datetime | None = None) -> str:
    """Reserve the next valid publish slot and record it in a FLEET-WIDE ledger
    (output/schedule_ledger.json), so batches and repeated runs respect:
      - min_hours_between_uploads PER CHANNEL (vs other reserved slots of this slug)
      - max_uploads_per_day FLEET-WIDE (all channels share ONE Cloud project's
        hidden Video-Uploads bucket — client IDs share the project number)
    Deterministic minute-jitter per `seed`; the DAY advances as slots fill.
    (2026-07-12: replaces the cursorless version Relay's audit caught — every video
    in a batch used to compute from the same `now` and land ~an hour apart.)"""
    up = cfg["upload"]
    slug = cfg.get("channel", {}).get("slug", "unknown")
    now = now or dt.datetime.now(dt.timezone.utc)
    rng = _seeded_rng(seed)

    ledger = _load_ledger(now)
    min_gap = dt.timedelta(hours=up.get("min_hours_between_uploads", 20))
    max_day = int(up.get("max_uploads_per_day", 5))
    base_hour = up.get("base_publish_hour_utc", 2)
    jitter = up.get("jitter_minutes", 50)
    offset = dt.timedelta(minutes=rng.randint(-jitter, jitter))

    mine = sorted(dt.datetime.fromisoformat(e["when"])
                  for e in ledger if e.get("slug") == slug)
    earliest = now + min_gap
    if mine:
        earliest = max(earliest, mine[-1] + min_gap)

    day = earliest.date()
    for _ in range(120):                                  # bounded search
        when = dt.datetime(day.year, day.month, day.day, base_hour,
                           tzinfo=dt.timezone.utc) + offset
        day_count = sum(1 for e in ledger
                        if dt.datetime.fromisoformat(e["when"]).date() == when.date())
        gap_ok = all(abs((when - m).total_seconds()) >= min_gap.total_seconds()
                     for m in mine)
        if when >= earliest and day_count < max_day and gap_ok:
            ledger.append({"when": when.replace(microsecond=0).isoformat(),
                           "slug": slug, "seed": seed})
            _save_ledger(ledger)
            return when.replace(microsecond=0).isoformat()
        day += dt.timedelta(days=1)
    raise RuntimeError("could not find a publish slot within 120 days — ledger full?")


def _next_publish_at_legacy(cfg: dict, seed: str, now: dt.datetime | None = None) -> str:
    """ISO-8601 UTC publish time at the channel's base hour +/- jitter, at least
    `min_hours_between_uploads` in the future. `seed` (e.g. video filename) makes
    the jitter deterministic per-video so re-runs don't reshuffle the calendar."""
    up = cfg["upload"]
    now = now or dt.datetime.now(dt.timezone.utc)
    rng = _seeded_rng(seed)

    min_gap = dt.timedelta(hours=up.get("min_hours_between_uploads", 20))
    target_day = (now + min_gap).date()

    base_hour = up.get("base_publish_hour_utc", 2)
    jitter = up.get("jitter_minutes", 50)
    offset = rng.randint(-jitter, jitter)

    when = dt.datetime(target_day.year, target_day.month, target_day.day,
                       base_hour, 0, tzinfo=dt.timezone.utc) + dt.timedelta(minutes=offset)
    if when < now + min_gap:
        when += dt.timedelta(days=1)
    return when.replace(microsecond=0).isoformat()


if __name__ == "__main__":
    import sys

    from .config import load_channel
    slug = sys.argv[1] if len(sys.argv) > 1 else "2am_without_her"
    cfg = load_channel(slug)
    for name in ["a.mp4", "b.mp4", "c.mp4"]:
        print(name, "->", next_publish_at(cfg, name))
