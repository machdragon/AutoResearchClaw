## Decision
REFINE

## Justification

The work is not ready to move to paper-writing, but it also does not justify abandoning the core hypothesis.

- The **minimum quality criteria for PROCEED are not met**:
  - Only **one baseline** is present, not ≥2.
  - **Seeds per condition = 1**, not ≥3.
  - **Ablation integrity is explicitly broken** (identical outputs across conditions).
  - **Analysis quality rating is 3/10**, below the ≥4/10 threshold.
- The results show:
  - The candidate is **worse in val_bpb** and **substantially slower**, failing the runtime gate.
  - The **infrastructure is functioning** and numerically stable.
- The main hypothesis (codec-guided QAT + compression-aware reg helps under size+runtime constraints) is **not actually tested** yet:
  - No artifact-size metrics.
  - No validated ablations.
  - No statistical robustness.

This argues for **improving the experimental setup and metrics**, not discarding the idea.

## Evidence

- **Metrics & constraints**
  - Candidate val_bpb: **3.3919**
  - Baseline val_bpb: **3.3794** → Δ ≈ **+0.0125** bpb (~+0.37%, in the wrong direction).
  - Candidate runtime_ms: **80,894**
  - Baseline runtime_ms: **62,992** → runtime_ratio ≈ **1.284** (>1.10 gate; `quick_gate_passed = 0`).

- **Experimental integrity**
  - Seeds: **n=1** per condition.
  - Ablation system: **“ABLATION FAILURE: Conditions produce identical outputs.”**
  - No `artifact_size_bytes` or post-roundtrip size metrics.
  - Overall analysis quality score: **3/10** (<4/10 requirement).

All of these violate the explicit PROCEED criteria and indicate methodology, not hypothesis, is the bottleneck.

## Next Actions

### 1. Fix Wiring and Ablation Integrity (Blocker)

- Verify that key flags **actually change behavior**:
  - `qat_enabled`
  - `compression_reg_enabled`
  - `compression_reg_scope`
  - `compression_reg_lambda`
- Implement and log internal metrics per step or per batch:
  - `compression_loss` (or equivalent extra loss term).
  - `quantization_error` / per-layer clipping stats.
  - On/off differences when toggling each flag.
- Add quick tests:
  - Run a **tiny subset training** (e.g., a few hundred steps) for:
    1. QAT off, compression_reg off
    2. QAT on, compression_reg off
    3. QAT on, compression_reg on
  - Confirm:
    - Loss components differ across conditions.
    - Final outputs / checkpoints differ (no more “identical outputs” alerts).

### 2. Define and Run a Minimal, Clean Baseline Suite

Under identical training budgets, data splits, and deployment pipeline, run at least:

1. **Float-only baseline**  
   - No QAT  
   - No compression_reg

2. **QAT-only baseline**  
   - QAT enabled  
   - `compression_reg_enabled = false`

3. **QAT + compression_reg (candidate)**  
   - QAT enabled  
   - compression_reg enabled with a reasonable λ

For each condition:

- Use **≥3 random seeds**.
- Log:
  - Mean ± std of val_bpb
  - Mean ± std of runtime (or runtime_ratio)
  - Mean ± std of artifact size (see next step).

### 3. Add Deployment-Critical Metrics

Integrate explicit size and deployment-path metrics into the pipeline:

- For each run, after full roundtrip (int8 + zlib or whatever actual stack is):
  - `artifact_size_bytes`
  - `artifact_gate_passed` (≤16MB).
  - Clarify and log explicitly whether `val_bpb` is measured on this final artifact.
- Ensure **runtime** is measured in a consistent way:
  - Same hardware and batch size.
  - Multiple iterations or runs if feasible, to estimate variance.

### 4. Re-run with Proper Statistics

After wiring and metrics are fixed:

- For the 3 core conditions, run **≥3 seeds** each.
- Compute and record:
  - Mean ± std for val_bpb, runtime_ratio, artifact_size.
  - Whether each condition passes:
    - Runtime gate (≤1.10×).
    - Size gate (≤16MB).
- Interpret any deltas only in light of this variability. For small differences (~0.3–1%), check if they are outside typical run-to-run noise.

### 5. Tighten Alignment with the Main Hypothesis

Once the above is in place:

- Define explicit success criteria, e.g.:
  - Among configurations that pass size + runtime gates, **QAT + compression_reg** must improve post-roundtrip val_bpb by at least X% over:
    - Float-only
    - QAT-only
- Run a **small, principled sweep** over:
  - `compression_reg_lambda`
  - `qat_start_frac`
  - Potentially `qat_group_size`
- Use the improved infrastructure to:
  - Identify whether there is any regime where QAT + compression_reg is strictly better under constraints.
  - If **all** reasonable regimes fail, then revisit the core hypothesis (potential PIVOT).

Only after these refinements and a second analysis pass meets all PROCEED criteria (≥2 baselines, defined primary metric, ≥3 seeds, ablation integrity, analysis quality ≥4/10) should you move to paper-writing.