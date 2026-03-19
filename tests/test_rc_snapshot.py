# pyright: basic
from __future__ import annotations

import json
from pathlib import Path

from researchclaw.snapshot import build_snapshot, collect_run_scores, write_snapshot_files


def _write_summary(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_collect_run_scores_orders_by_score(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts"
    _write_summary(
        artifacts / "run-a" / "pipeline_summary.json",
        {
            "run_id": "run-a",
            "generated": "2026-03-18T10:00:00Z",
            "stages_done": 23,
            "stages_executed": 23,
            "stages_failed": 0,
            "final_status": "done",
            "content_metrics": {"citation_verify_score": 0.95, "template_ratio": 0.02},
        },
    )
    _write_summary(
        artifacts / "run-b" / "pipeline_summary.json",
        {
            "run_id": "run-b",
            "generated": "2026-03-18T11:00:00Z",
            "stages_done": 12,
            "stages_executed": 23,
            "stages_failed": 3,
            "final_status": "failed",
            "content_metrics": {"citation_verify_score": 0.4, "template_ratio": 0.3},
        },
    )

    scores = collect_run_scores(artifacts)
    assert [item.run_id for item in scores] == ["run-a", "run-b"]
    assert scores[0].score > scores[1].score


def test_build_snapshot_shapes_leaderboard_and_counts(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts"
    _write_summary(
        artifacts / "run-1" / "pipeline_summary.json",
        {
            "run_id": "run-1",
            "generated": "2026-03-18T12:00:00Z",
            "stages_done": 23,
            "stages_executed": 23,
            "stages_failed": 0,
            "final_status": "done",
        },
    )
    _write_summary(
        artifacts / "run-2" / "pipeline_summary.json",
        {
            "run_id": "run-2",
            "generated": "2026-03-18T13:00:00Z",
            "stages_done": 20,
            "stages_executed": 23,
            "stages_failed": 1,
            "final_status": "failed",
        },
    )

    scores = collect_run_scores(artifacts)
    snapshot = build_snapshot(scores, top=1)

    assert snapshot["version"] == 1
    assert snapshot["run_counts"]["total_runs"] == 2
    assert snapshot["run_counts"]["successful_runs"] == 1
    assert len(snapshot["leaderboard"]["top_runs"]) == 1
    assert snapshot["leaderboard"]["global_best"]["run_id"] == "run-1"


def test_write_snapshot_files_writes_latest_and_hourly_archive(tmp_path: Path) -> None:
    snapshot = {
        "version": 1,
        "timestamp": "2026-03-18T15:14:00+00:00",
        "summary": "x",
        "leaderboard": {"top_runs": [], "global_best": None, "average_score": 0.0},
        "run_counts": {"total_runs": 0, "successful_runs": 0, "runs_with_failures": 0},
    }
    latest_path, hourly_path = write_snapshot_files(snapshot, tmp_path / "snapshots")

    assert latest_path.exists()
    assert latest_path.name == "latest.json"
    assert hourly_path.exists()
    assert "2026-03-18" in str(hourly_path)
    assert hourly_path.name == "15.json"
