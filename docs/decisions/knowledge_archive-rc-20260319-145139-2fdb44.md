---
created: '2026-03-19T15:13:00+00:00'
evidence:
- stage-21/archive.md
- stage-21/bundle_index.json
id: knowledge_archive-rc-20260319-145139-2fdb44
run_id: rc-20260319-145139-2fdb44
stage: 21-knowledge_archive
tags:
- knowledge_archive
- stage-21
- run-rc-20260
title: 'Stage 21: Knowledge Archive'
---

# Stage 21: Knowledge Archive

# Retrospective Archive — parameter-golf-autorc (autoRC)
Status: REFINE  
Date: 2026-03-19  
Authors: project team

This archive summarizes the failed quick-harness run, the root causes identified, lessons learned, concrete reproducibility notes and tests, and a prioritized plan of follow-up work required before the project can PROCEED.

---

## 1) Executive summary

- Run verdict: REFINE. The idea (jointly optimizing val_bpb + artifact size ≤16MB under a quick-harness gate) remains plausible, but the executed run is a plumbing/debug snapshot and not scientifically valid.
- Primary failures:
  - Crash in secondary-metrics path caused by a signature mismatch: `GlobalValBPBCompressor.infer_logits()` vs. `evaluate_secondary_metrics`.
  - Several ablations are functionally identical to their parents (flags not wired).
  - Missing / unlogged critical metrics: artifact size, parameter counts, wall-clock, token counts, and safety/robustness metrics.
  - n=1 per condition, no variance, undocumented meaning of indices 0–19.
- Immediate recommended action: fix infra and tests, make ablations functional and unit-tested, instrument metrics aligned with hypotheses, and re-run a small, multi-seed experimental pass.

---

## 2) Primary lessons learned

1. Small engineering bugs can silently invalidate whole experimental claims.
   - Example: a TypeError in the secondary metrics path prevented safety/robustness metrics from running, leaving only val_bpb.
2. Ablation flags must be unit-tested to assert they change behavior.
   - Without tests, “ablation” can be a no-op and lead to false negatives/positives in analysis.
3. Core hypotheses must be matched to logged, verifiable metrics:
   - If your claim is “joint objective: val_bpb + artifact size + harness latency”, you must log val_bpb, artifact size, parameter count, wall-clock and token counts for every candidate.
4. Single-run results (n=1) are only useful for debugging; they cannot support inferential claims.
5. Quick-harness constraints (tight wall-time) require automated, fast CI tests to catch integration regressions early.

---

## 3) Reproducibility checklist (minimal, required for re-run)

For any future run intended to provide evidence, ensure the following are satisfied and recorded in the records-folder.

A. Environment and code
- Provide reproducible environment artifacts:
  - requirements.txt (pinned versions), or a minimal Dockerfile, and a small environment test script.
  - Example: requirements.txt snippet
    - python==3.10.12
    - torch==2.2.0
    - transformers==4.35.0
    - numpy==1.26.0
  - Remove invalid entries (e.g., stray `__future__` lines).
- Include: git commit hash, submodule SHAs, and a one-line reproducible invocation.
- Containerization: provide Dockerfile (optional but recommended) and an entrypoint script that runs a tiny harness.

B. Data
- Versioned datasets and splits, with checksums:
  - Train/val/test/safety-eval separation must be explicit.
  - Record dataset name, version, and SHA256 of the files used (e.g., synthetic wikitext103_quick_harn v1.0).
- Synthetic datasets: provide generator script and seed used to create them.

C. Seeds & sample sizes
- For every reported condition: run K ≥ 3 independent seeds (ideally K = 5 for final claims).
- Seeds must be logged in the record: seed value, RNG state snapshots (if feasible), and exact randomization points (data shuffle, init, augmentation).
- Define meaning of indices 0–19 explicitly (if used still): e.g., 20 checkpoints per seed or 20 random restarts.

D. Metrics (mandatory per-run)
- val_bpb (primary)
- artifact_size_bytes (final serialized artifact size)
- parameter_count (final model parameters)
- quick_harness_wall_clock_seconds
- tokens_processed_training / evaluation
- GPU_hours (or equivalent)
- success_rate (binary promotion gate)
- safety/robustness metrics:
  - Jailbreak/violation rate on held-out prompts
  - Boundary-local robustness proxy (distance-to-threshold stratified metric)
  - RBE or other chosen entropy/resilience metric
- Log mean ± std across seeds for each metric.

E. Records-folder layout (required)
- /records/{run_id}/
  - config.yaml (all hyperparameters)
  - git-commit.txt
  - dataset_manifest.json (filenames + checksums)
  - seed_manifest.json
  - metrics.csv (per-seed, per-checkpoint)
  - model_artifact.tar.gz (if ≤16MB) or model_artifact_info.json if large
  - unit_test_results.log
  - quick_harness_log.txt
  - secondary_metrics.log

F. Artifact-size enforcement
- Implement deterministic artifact building that includes:
  - exact serialization command (e.g., torch.save with pickled optimizer/state? No — only model state dict).
  - strip out non-essential metadata.
- Example check (command line):
  - python -c "import os; print(os.path.getsize('artifact.pth'))"
- Failure mode: runs that exceed 16,000,000 bytes must be rejected by the promotion gate, and this event must be logged.

---

## 4) Immediate engineering fixes (high priority, actionable)

1. F

... (truncated, see full artifact)


{
  "run_id": "rc-20260319-125447-2fdb44",
  "generated": "2026-03-19T15:13:00+00:00",
  "artifact_count": 198,
  "artifacts": [
    "stage-01/decision.json",
    "stage-01/goal.md",
    "stage-01/hardware_profile.json",
    "stage-01/stage_health.json",
    "stage-02/decision.json",
    "stage-02/problem_tree.md",
    "stage-02/stage_health.json",
    "stage-02/topic_evaluation.json",
    "stage-03/decision.json",
    "stage-03/queries.json",
    "stage-03/search_plan.yaml",
    "stage-03/sources.json",
    "stage-03/stage_health.json",
    "stage-04/candidates.jsonl",
    "stage-04/decision.json",
    "stage-04/references.bib",
    "stage-04/search_meta.json",
    "stage-04/stage_health.json",
    "stage-05/decision.json",
    "stage-05/shortlist.jsonl",
    "stage-05/stage_health.json",
    "stage-06/cards/eldin2025artifacts_eeg_embodied_resonance.md",
    "stage-06/cards/fang2025privacy_pact_embedding_graph.md",
    "stage-06/cards/heverin2026prompt_refusal_boundary_instability.md",
    "stage-06/cards/john2025adoption_ai_fraud_detection_nigeria.md",
    "stage-06/cards/shah2025explainability_regulated_re_requirements.md",
    "stage-06/cards/verma2025mpace_mother_child_mllm_compliance.md",
    "stage-06/decision.json",
    "stage-06/stage_health.json",
    "stage-07/decision.json",
    "stage-07/stage_health.json",
    "stage-07/synthesis.md",
    "stage-08/decision.json",
    "stage-08/hypotheses.md",
    "stage-08/novelty_report.json",
    "stage-08/perspectives/contrarian.md",
    "stage-08/perspectives/innovator.md",
    "stage-08/perspectives/pragmatist.md",
    "stage-08/stage_health.json",
    "stage-09/benchmark_agent/acquisition_0.json",
    "stage-09/benchmark_agent/acquisition_1.json",
    "stage-09/benchmark_agent/benchmark_plan.json",
    "stage-09/benchmark_agent/selection_results.json",
    "stage-09/benchmark_agent/survey_results.json",
    "stage-09/benchmark_agent/validation_0.json",
    "stage-09/benchmark_agent/validation_1.json",
    "stage-09/benchmark_plan.json",
    "stage-09/decision.json",
    "stage-09/exp_plan.yaml",
    "stage-09/stage_health.json",
    "stage-10/agent_runs/attempt_001/main.py",
    "stage-10/agent_runs/attempt_001/optimizers.py",
    "stage-10/agent_runs/attempt_002/main.py",
    "stage-10/agent_runs/attempt_002/optimizers.py",
    "stage-10/agent_runs/attempt_003/main.py",
    "stage-10/agent_runs/attempt_003/optimizers.py",
    "stage-10/agent_sandbox/_docker_project_1/experiment_harness.py",
    "stage-10/agent_sandbox/_docker_project_1/main.py",
    "stage-10/agent_sandbox/_docker_project_1/optimizers.py",
    "stage-10/agent_sandbox/_docker_project_1/requirements.txt",
    "stage-10/agent_sandbox/_docker_project_2/__pycache__/optimizers.cpython-310.pyc",
    "stage-10/agent_sandbox/_docker_project_2/experiment_harness.py",
    "stage-10/agent_sandbox/_docker_project_2/main.py",
    "stage-10/agent_sandbox/_docker_project_2/optimizers.py",
    "stage-10/agent_sandbox/_docker_project_2/requirements.txt",
    "stage-10/agent_sandbox/_docker_project_3/__pycache__/optimizers.cpython-310.pyc",
    "stage-10/agent_sandbox/_docker_project_3/experiment_harness.py",
    "stage-10/agent_sandbox/_docker_project_3/main.py",
    "stage-10/agent_sandbox/_docker_project_3/optimizers.py",
    "stage-10/agent_sandbox/_docker_project_3/requirements.txt",
    "stage-10/agent_sandbox/_docker_project_3/results.json",
    "stage-10/architecture_spec.yaml",
    "stage-10/code_agent_log.json",
    "stage-10/decision.json",
    "stage-10/experiment/main.py",
    "stage-10/experiment/optimizers.py",
    "stage-10/experiment_spec.md",
    "stage-10/stage_health.json",
    "stage-11/decision.json",
    "stage-11/schedule.json",
    "stage-11/stage_health.json",
    "stage-12/decision.json",
    "stage-12/runs/run-1.json",
    "stage-12/runs/sandbox/_docker_project_1/__pycache__/optimizers.cpython-310.pyc",
    "stage-12/runs/sandbox/_docker_project_1/experiment_harness.py",
    "stage-12/runs/sandbox/_docker_project_1/main.py",
    "stage-12/runs/sandbox/_docker_project_1/optimizers.py",
    "stage-12/runs/sandbox/_docker_project_1/requirements.txt",
    "stage-12/stage_health.json",
    "stage-13/experiment_v1/main.py",
    "stage-13/experiment_v1/optimizers.py",
    "stage-13/experiment_v2/main.py",
    "stage-13/experiment_v3/main.py",
    "stage-13/experiment_v4/main.py",
    "stage-13/refine_sandbox_v1/_docker_project_1/__pycache__/optimizers.cpython-310.pyc",
    "stage-13/refine_sandbox_v1/_docker_project_1/experiment_harness.py",
    "stage-13/refine_sandbox_v1/_docker_project_1/main.py",
    "stage-13/refine_sandbox_v1/_docker_project_1/optimizers.py",
    "stage-13/refine_sandbox_v1/_docker_project_1/requirements.txt",
    "stage-13/refine_sandbox_v1/_docker_project_1/results.json",
    "stage-13/refine_sandbox_v1_fix/_docker_project_1/__pycache__/optimizers.cpython-310.pyc",
    "stage-13/refine_sandbox_v1_fix/_docker_project_1/experiment_harness.py",
    "stage-13/ref

... (truncated, see full artifact)
