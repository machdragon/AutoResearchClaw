---
created: '2026-03-19T22:42:46+00:00'
evidence:
- stage-21/archive.md
- stage-21/bundle_index.json
id: knowledge_archive-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 21-knowledge_archive
tags:
- knowledge_archive
- stage-21
- run-rc-20260
title: 'Stage 21: Knowledge Archive'
---

# Stage 21: Knowledge Archive

```markdown
# RLG Lane_1 Retrospective Archive

Status: **REFINE** (infrastructure + methodology)  
Lane: **Parameter Golf lane_1** — recurrence + LoRA + lightweight gating under:
- artifact cap: **≤ 16 MB**
- runtime cap: **≤ 1.10×** baseline
- objective: **val_bpb** (post–round-trip)

---

## 1. What We Tried

### 1.1 Concept & Configuration Ladder

Targeted design: a *composite* small model under a hard artifact cap:

1. **Backbone**: tiny recurrent LM (RNN/RWKV‑style) as the core.
2. **LoRA specialization**: low‑rank adapters on selected recurrent projections.
3. **Lightweight gating**: a global residual gate that scales LoRA contribution per sequence (no token‑wise routing).

Intended ladder of conditions:

- **Baseline (challenge reference)**  
  Large(‑ish) model used only as an external point of comparison for val_bpb and runtime.

- **R‑only**: `recurrence_only`  
  Minimal recurrent LM tuned to fit under 16 MB without LoRA/gating.

- **R+LoRA**: `recurrence_lora`  
  Same backbone, with LoRA modules enabled on chosen matrices.

- **R+LoRA+Gate (RLG)**: `recurrence_lora_gated`  
  As above, plus a small global gate that rescales LoRA outputs at the residual level.

Hypothesis for lane_1:

- As we move: **R‑only → R+LoRA → RLG**, we should see:
  - **Monotone improvement in val_bpb**,  
  - **Runtime still below 1.10× baseline**, ideally much lower,
  - **Total artifact ≤ 16 MB** (backbone + LoRA + gate).

### 1.2 What Actually Ran

We obtained one “full” run artefact with:

- One seed per condition (**n = 1**).
- Per‑condition metrics (single values; no variance):
  - Baseline  
  - `recurrence_only`  
  - `recurrence_lora`  
  - `recurrence_lora_gated`
- Reported numbers showed a *nice, monotone* val_bpb improvement along the ladder and extremely small recorded latencies for the recurrence‑based models.
- The run was nevertheless tagged **failed**, due to:
  - `ModuleNotFoundError: No module named 'harness'` in the main script.
  - Broken runtime instrumentation (`runtime_ratio = 0.0` everywhere).
  - Ablation checker claiming all `recurrence_*` conditions are **behaviorally identical**.

The core lesson: this run is **not** a valid test of the scientific hypothesis; it is a **pipeline diagnostic**.

---

## 2. Key Lessons Learned

### 2.1 Conceptual: The Design Still Makes Sense

- The *idea* of RLG — recurrence + LoRA + lightweight gating under a shared tight budget — remains coherent and under‑explored in the literature.
- The configuration ladder (R‑only → R+LoRA → RLG) is a good scaffold for systematic ablations once the wiring is correct.
- Nothing observed so far contradicts feasibility in principle; the problems are entirely *methodological* and *infrastructure‑level*.

### 2.2 Ablations: Label ≠ Behavior

- The ablation checker reported:  
  > all three “recurrence_*” conditions produce identical outputs across all metrics.

Implication:

- Config flags for `recurrence_only`, `recurrence_lora`, `recurrence_lora_gated` are **not actually changing**:
  - the constructed computation graph, or
  - the loaded checkpoint, or both.

Lesson:

- **You cannot trust condition names.**  
  Until you have explicit tests showing that `recurrence_only` vs `recurrence_lora` produce different logits on a fixed batch, you are not running true ablations.
- A good ablation harness is *critical*; here, it correctly exposed that our variants were effectively the same model.

### 2.3 Runtime: Instrumentation Before Claims

- Recorded runtimes:
  - Baseline: ~62,992 ms
  - Recurrence variants: ~0.004–0.014 ms
  - `runtime_ratio`: **0.0** for all non‑baseline models

Problems:

- Orders‑of‑magnitude discrepancy with nonsensical ratios.
- No explicit control of:
  - batch size,
  - sequence length,
  - warmup iterations,
  - device synchronization (e.g., `cuda.synchronize()`).

Lesson:

- **Runtime metrics were broken.** Any “gating is cheap” story is currently speculation, not evidence.
- A lane with a hard quick‑gate is *all about* reliable latency measurement; this must be a first‑class, tested subsystem.

### 2.4 Artifact Size: Missing the Core Constraint

- The run **does not** log:
  - full on‑disk artifact size per condition, or
  - decomposition into backbone vs LoRA vs gate.

Given lane_1’s 16 MB cap, this is a major gap.

Lesson:

- Without precise artifact accounting, the “parameter golf” angle is untested. You cannot say the design meets the deployment spec without byte‑accurate size measurements.

### 2.5 Statistics: n = 1 is Not Enough

- Each condition has **n = 1** measurement.
- No variance, no confidence intervals, no seed‑to‑seed variability.
- With such tiny differences (e.g. ~0.015 in val_bpb), we need at least 3–5 seeds to know if differences are real vs noise.

Lesson:

- Any reported “monotone improvement” is **purely anecdotal** given the broken ablations and n = 1.  
- For a serious claim, **multi‑seed replication** is mandatory.

### 2.6 Meta: The “Result” of This Run is a To‑Do List

- 

... (truncated, see full artifact)


{
  "run_id": "rc-20260319-220921-d02b4b",
  "generated": "2026-03-19T22:42:46+00:00",
  "artifact_count": 199,
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
    "stage-04/web_search_result.json",
    "stage-05/decision.json",
    "stage-05/shortlist.jsonl",
    "stage-05/stage_health.json",
    "stage-06/cards/chan2020maturation-main.md",
    "stage-06/cards/christensendalsgaard2021solar-main.md",
    "stage-06/cards/gea2022interactive-main.md",
    "stage-06/cards/hong2020house-main.md",
    "stage-06/cards/hosang2022effects-main.md",
    "stage-06/cards/mogadala2021trends-main.md",
    "stage-06/cards/mohammadi2021functionally-main.md",
    "stage-06/cards/murad2023weed-main.md",
    "stage-06/cards/patel2020artificial-main.md",
    "stage-06/cards/rathnayake2023rssi-main.md",
    "stage-06/cards/trzepiecinski2024current-main.md",
    "stage-06/cards/verheul2020measuring-main.md",
    "stage-06/cards/woody2024electric-main.md",
    "stage-06/cards/zhang2020training-main.md",
    "stage-06/cards/zhou2023research-main.md",
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
    "stage-09/decision.json",
    "stage-09/domain_profile.json",
    "stage-09/exp_plan.yaml",
    "stage-09/stage_health.json",
    "stage-10/ablation_warning.json",
    "stage-10/code_review.json",
    "stage-10/decision.json",
    "stage-10/experiment/main.py",
    "stage-10/experiment_spec.md",
    "stage-10/stage_health.json",
    "stage-10/validation_report.md",
    "stage-11/decision.json",
    "stage-11/schedule.json",
    "stage-11/stage_health.json",
    "stage-12/decision.json",
    "stage-12/runs/run-1.json",
    "stage-12/runs/sandbox/_project/experiment_harness.py",
    "stage-12/runs/sandbox/_project/main.py",
    "stage-12/stage_health.json",
    "stage-13/decision.json",
    "stage-13/experiment_final/main.py",
    "stage-13/experiment_final.py",
    "stage-13/experiment_v1/main.py",
    "stage-13/experiment_v2/main.py",
    "stage-13/refine_sandbox_v1/_project/experiment_harness.py",
    "stage-13/refine_sandbox_v1/_project/main.py",
    "stage-13/refine_sandbox_v2/_project/experiment_harness.py",
    "stage-13/refine_sandbox_v2/_project/main.py",
    "stage-13/refinement_log.json",
    "stage-13/stage_health.json",
    "stage-13_v1/decision.json",
    "stage-13_v1/experiment_final/main.py",
    "stage-13_v1/experiment_final.py",
    "stage-13_v1/experiment_v1/main.py",
    "stage-13_v1/experiment_v2/main.py",
    "stage-13_v1/refine_sandbox_v1/_project/experiment_harness.py",
    "stage-13_v1/refine_sandbox_v1/_project/main.py",
    "stage-13_v1/refine_sandbox_v2/_project/experiment_harness.py",
    "stage-13_v1/refine_sandbox_v2/_project/main.py",
    "stage-13_v1/refinement_log.json",
    "stage-13_v1/stage_health.json",
    "stage-13_v2/decision.json",
    "stage-13_v2/experiment_final/main.py",
    "stage-13_v2/experiment_final.py",
    "stage-13_v2/experiment_v1/main.py",
    "stage-13_v2/experiment_v2/main.py",
    "stage-13_v2/refine_sandbox_v1/_project/experiment_harness.py",
    "stage-13_v2/refine_sandbox_v1/_project/main.py",
    "stage-13_v2/refine_sandbox_v2/_project/experiment_harness.py",
    "stage-13_v2/refine_sandbox_v2/_project/main.py",
    "stage-13_v2/refinement_log.json",
    "stage-13_v2/stage_health.json",
    "stage-14/analysis.md",
    "stage-14/charts/architecture_diagram_2.png",
    "stage-14/charts/figure_manifest.json",
    "stage-14/charts/pipeline_overview_1.png",
    "stage-14/charts/scripts/fig_main_val_bpb.py",
    "stage-14/charts/scripts/fig_pareto_valbpb_runtime.py",
    "stage-14/charts/scripts/fig_runtime_quickgate.py",
    "stage-14/decision.json",
    "stage-14/experiment_summary.json",
    "stage-14/figure_decisions.json",
    "stage-14/figure_plan.json",
    "stage-14/figure_plan_code.json",
    "stage-14/figure_plan_final.json",
    "stage-14/nano_banana_results.json",
    "stage-14/perspectives/methodologist.md",
    "stage-14/perspectives/optimist.md",
    "stage-14/perspectives/skeptic.md",
    "stage-14/results_table.tex",
    "stage-14/scripts_0.json",
    "stage-14/scripts_

... (truncated, see full artifact)
