## Decision

REFINE

## Justification

The current results fail multiple minimum criteria for “PROCEED” and do not constitute a fundamental negative result against the hypothesis; they show an engineering/pathology issue, not a conceptual dead end.

Specifically:

- The experiment is effectively a single smoke-test run (n=1) with a broken ablation, so there is no valid scientific evidence for or against the codec-aware, staged-QAT hypothesis.
- Several mandatory quality criteria for “PROCEED” are not met: no ≥2 proper baselines with results, no ≥3 seeds per condition, explicit ablation failure, and an analysis-quality rating below 4/10 (3/10).
- The method runs end-to-end and does not catastrophically degrade performance, so there is no strong signal that the underlying idea is flawed enough to warrant a pivot.

Given this, the correct path is to refine the experimental design, wiring, and metrics to produce scientifically valid evidence.

## Evidence

- **Minimum quality criteria failures for PROCEED:**
  1. At least 2 baselines + proposed method with results:  
     - Only one baseline (unspecified regime) and one candidate-like config are observed; no clear B0/B1 baselines with multiple seeds.
  2. Primary metric definition:  
     - val_bpb is defined and direction is clear (lower is better) — this *passes*.
  3. ≥3 seeds per condition:  
     - n=1 for baseline and candidate — this *fails*.
  4. No identical per-seed values across conditions:  
     - Ablation tooling explicitly reports **ABLATION FAILURE** (conditions not differentiating), implying invalid contrasts — this *fails*.
  5. Analysis quality rating ≥4/10:  
     - Rating is **3/10** — this *fails*.

- **Observed performance:**
  - Baseline: `val_bpb ≈ 3.3794`, runtime ≈ 62,992 ms.
  - Candidate: `val_bpb ≈ 3.3919` (worse by ~0.37%), runtime ≈ 80,894 ms (≈1.28× slower, over the 1.10× gate).

- **Missing key metrics:**
  - No artifact size / compression ratio logged, despite a 16 MB cap being central to the problem.

- **Interpretation:**
  - The run demonstrates that the staged QAT + compression-regularization pipeline can execute, but provides no valid inferential evidence on effectiveness.

## Next Actions

1. **Fix ablation and wiring (blocking).**
   - Ensure `qat_enabled`, `compression_reg_enabled`, and `compression_reg_lambda` actually affect the computation graph.
   - Add explicit logs:
     - Compression loss term magnitude when enabled versus exactly zero when disabled.
   - Re-run a minimal sanity check:
     - Same base config with compression reg off vs on; verify that:
       - Ablation tool no longer reports failure.
       - Logged compression loss and training behavior differ across conditions.

2. **Establish clean baselines with replication.**
   - Define and run at least:
     - **B0**: Float-only training, no QAT, no compression regularizer.
     - **B1**: Staged QAT + teacher distillation, no compression regularizer (this is the true reference for the hypothesis).
   - For **each** baseline and any candidate: run ≥3 seeds and report mean ± std for:
     - Post-roundtrip val_bpb.
     - Runtime (and runtime ratio vs B1).

3. **Add compression-focused metrics.**
   - Log:
     - `artifact_size_bytes` for the final int8+zlib artifact (full model).
     - Optionally per-module artifact sizes (e.g., embeddings, output projection).
   - Treat:
     - `artifact_size_bytes ≤ 16 MB` and
     - `runtime_ratio ≤ 1.10`
     as explicit gates, same status as the val_bpb goal.

4. **Reduce runtime overhead before wide sweeps.**
   - Decrease zlib evaluation frequency (e.g., every N steps, use last value otherwise).
   - Consider sampling rows/blocks from large tensors for the compression loss instead of full-matrix roundtrips.
   - Batch or cache zlib operations where possible.

5. **Run a minimal, proper ablation grid.**
   - Once wiring and metrics are fixed, run:
     - **B1**: Staged QAT baseline, λ = 0.
     - **C1**: B1 + compression regularizer with small λ (e.g., 1e-5).
     - **C2**: B1 + compression regularizer at target λ (e.g., 1e-4).
   - For each condition:
     - Use ≥3 seeds.
     - Record val_bpb, artifact_size_bytes, runtime_ratio, compression-loss magnitude.
     - Check all gates (runtime, artifact size).

6. **Reassess go/no-go after refined runs.**
   - If at least one candidate meets:
     - Compression and runtime gates, and
     - Shows ≥0.5–1.5% val_bpb *improvement* over B1 with solid variance estimates,
   - Then re-evaluate for **PROCEED**. If multiple clean, negative results accumulate despite correct wiring and metrics, then reconsider a **PIVOT**.