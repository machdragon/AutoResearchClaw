"""Build lightweight leaderboard snapshots from pipeline runs.

Inspired by AGI's snapshot pattern: keep a stable `latest.json` and
timestamped archives so progress can be inspected without opening each run.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class RunScore:
    """Normalized scoring view for one pipeline run."""

    run_id: str
    run_dir: str
    generated: str
    stages_done: int
    stages_executed: int
    stages_failed: int
    final_status: str
    citation_verify_score: float
    template_ratio: float
    score: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "run_dir": self.run_dir,
            "generated": self.generated,
            "stages_done": self.stages_done,
            "stages_executed": self.stages_executed,
            "stages_failed": self.stages_failed,
            "final_status": self.final_status,
            "citation_verify_score": round(self.citation_verify_score, 4),
            "template_ratio": round(self.template_ratio, 4),
            "score": round(self.score, 4),
        }


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _score_run(summary: dict[str, Any], run_dir: Path) -> RunScore:
    run_id = str(summary.get("run_id") or run_dir.name)
    generated = str(summary.get("generated") or "")
    stages_done = _safe_int(summary.get("stages_done"), 0)
    stages_executed = _safe_int(summary.get("stages_executed"), 0)
    stages_failed = _safe_int(summary.get("stages_failed"), 0)
    final_status = str(summary.get("final_status") or "unknown")

    content_metrics = summary.get("content_metrics", {})
    if not isinstance(content_metrics, dict):
        content_metrics = {}
    citation_verify = _safe_float(content_metrics.get("citation_verify_score"), 0.0)
    template_ratio = _safe_float(content_metrics.get("template_ratio"), 1.0)

    done_ratio = stages_done / stages_executed if stages_executed > 0 else 0.0
    template_quality = max(0.0, 1.0 - template_ratio)
    failure_penalty = min(0.25, stages_failed * 0.03)
    status_bonus = 0.05 if final_status == "done" else 0.0
    raw_score = (
        (0.55 * done_ratio)
        + (0.30 * citation_verify)
        + (0.15 * template_quality)
        + status_bonus
        - failure_penalty
    )
    score = max(0.0, min(1.0, raw_score))

    return RunScore(
        run_id=run_id,
        run_dir=str(run_dir),
        generated=generated,
        stages_done=stages_done,
        stages_executed=stages_executed,
        stages_failed=stages_failed,
        final_status=final_status,
        citation_verify_score=citation_verify,
        template_ratio=template_ratio,
        score=score,
    )


def _parse_generated_ts(value: str) -> datetime:
    if not value:
        return datetime.fromtimestamp(0, tz=UTC)
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return datetime.fromtimestamp(0, tz=UTC)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


def collect_run_scores(artifacts_root: Path) -> list[RunScore]:
    """Load and score all runs under `artifacts_root`."""
    if not artifacts_root.exists():
        return []

    scores: list[RunScore] = []
    for run_dir in sorted(artifacts_root.iterdir()):
        if not run_dir.is_dir():
            continue
        summary_path = run_dir / "pipeline_summary.json"
        if not summary_path.exists():
            continue
        try:
            loaded = json.loads(summary_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if not isinstance(loaded, dict):
            continue
        scores.append(_score_run(loaded, run_dir))

    scores.sort(
        key=lambda item: (
            item.score,
            _parse_generated_ts(item.generated),
            item.stages_done,
        ),
        reverse=True,
    )
    return scores


def build_snapshot(scores: list[RunScore], *, top: int = 10) -> dict[str, Any]:
    now = datetime.now(tz=UTC)
    top_n = max(1, top)
    top_runs = [item.to_dict() for item in scores[:top_n]]
    successful = sum(1 for item in scores if item.final_status == "done")
    failed = sum(1 for item in scores if item.stages_failed > 0)
    avg_score = (sum(item.score for item in scores) / len(scores)) if scores else 0.0

    snapshot: dict[str, Any] = {
        "version": 1,
        "timestamp": now.isoformat(timespec="seconds"),
        "summary": (
            f"{len(scores)} runs indexed, {successful} successful, "
            f"{failed} with stage failures"
        ),
        "leaderboard": {
            "top_runs": top_runs,
            "global_best": top_runs[0] if top_runs else None,
            "average_score": round(avg_score, 4),
        },
        "run_counts": {
            "total_runs": len(scores),
            "successful_runs": successful,
            "runs_with_failures": failed,
        },
    }
    return snapshot


def write_snapshot_files(snapshot: dict[str, Any], output_root: Path) -> tuple[Path, Path]:
    """Write `latest.json` and hourly archive JSON. Returns both paths."""
    timestamp_raw = snapshot.get("timestamp", "")
    if not isinstance(timestamp_raw, str):
        timestamp_raw = ""
    ts = _parse_generated_ts(timestamp_raw)

    dated_dir = output_root / ts.strftime("%Y-%m-%d")
    dated_dir.mkdir(parents=True, exist_ok=True)
    latest_path = output_root / "latest.json"
    hour_path = dated_dir / f"{ts.strftime('%H')}.json"

    payload = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.write_text(payload, encoding="utf-8")
    hour_path.write_text(payload, encoding="utf-8")
    return latest_path, hour_path
