## Decision

REFINE

## Justification

- The core hypotheses (roundtrip-aware QAT + compression regularization) are still **plausible** and not falsified by the current data; we simply have **no reliable causal evidence** yet.
- Multiple MINIMUM QUALITY CRITERIA for PROCEED are violated:
  - Only **one candidate run**; no ≥3 seeds per condition.
  - Only **one baseline** is effectively present, and even that is not a clearly separate, controlled run.
  - Ablation tool reports **“ABALATION FAILURE”**, and the overall analysis quality is self‑rated at **3/10 (<4/10)**.
- The current configuration is **numerically stable** and near-baseline in quality, so there is **no strong negative signal** to justify a PIVOT.
- The main blockers are **experimental design and instrumentation**, not the underlying idea; that points to **REFINE**, not PROCEED or PIVOT.

## Evidence

- **Insufficient baselines and seeds**
  - One candidate configuration (full_staged_QAT + compression_reg) vs a baked-in “baseline” scalar.
  - **n = 1** for candidate; baseline not run as a separate condition.
  - Violates criteria: ≥2 baselines, ≥3 seeds per condition.

- **Primary metric and direction are clear, but results are negative and underpowered**
  - Primary metric: `val_bpb` (lower is better).
  - Candidate vs baseline:
    - Baseline: `val_bpb ≈ 3.3794`
    - Candidate: `val_bpb ≈ 3.3919`
    - Δ ≈ +0.0125 bpb (≈ **+0.37% worse**), below the 0.5% “worth caring about” threshold even if it were an improvement.
  - Runtime:
    - `runtime_ratio ≈ 1.284` → **~28% slower**, violating the ≤1.10× quick-gate.

- **Ablation integrity is currently broken**
  - “ABALATION FAILURE”: metrics identical across supposed conditions.
  - Indicates toggles or hyperparameters are not actually changing the executed code path, or only one condition truly ran.
  - This directly violates the ablation integrity requirement (no identical per‑seed values across different conditions).

- **Analysis quality too low for PROCEED**
  - Self-assessed rating: **3/10** (<4/10 threshold).
  - Single run, unclear baseline provenance, no variance estimates, no codec-level metrics.

- **No strong evidence against the hypothesis**
  - Configuration is **stable** and close to baseline performance.
  - The modest degradation and slower runtime look like tuning/instrumentation issues, not a conceptual failure.

## Next Actions

### 1. Fix ablation & configuration wiring (highest priority)

- Ensure that core flags actually change behavior:
  - `qat_enabled`
  - `compression_reg_enabled`
  - `compression_reg_lambda`
  - QAT schedule parameters (`qat_start_frac`, etc.)
- Add “unit-test” style checks:
  - Tiny toy model + 100 steps:
    - Run with `compression_reg_enabled=false` vs `true`.
    - Confirm:
      - Loss terms differ as expected.
      - Gradients on targeted parameters (e.g., `final_proj`, `embed`) change magnitude/structure.
  - Same for `qat_enabled` toggles:
    - Confirm different quantization observers / fake-quant modules are present/absent.
- Re-run the ablation harness until the “ABALATION FAILURE” warning disappears and metrics differ across conditions.

### 2. Establish clean, explicit baselines

Run under the same harness, with **≥3 seeds each**:

1. **Float-only baseline**
   - No QAT, no compression_reg.
   - Evaluate via the *deployment roundtrip* (int8 + zlib) at the end only.
   - Log:
     - `val_bpb` (post-roundtrip),
     - runtime,
     - model size pre- and post-zlib.

2. **QAT-only baseline**
   - QAT enabled.
   - `compression_reg_enabled = false`.
   - Same metrics as above.

3. (Optional but useful) **KD-only / teacher baseline**
   - Distillation or teacher guidance without compression_reg.
   - Helps disentangle “teacher” vs “codec-aware” benefits.

### 3. Add codec-level metrics

For each condition:

- Log at minimum:
  - Serialized model size before compression (bytes).
  - Serialized model size after zlib (bytes).
- If feasible:
  - Per-layer or per-parameter-block zlib sizes.
  - Simple entropy or sparsity proxies (e.g., histogram of weight values).
- This will directly test whether the compression regularizer actually improves zlib compressibility.

### 4. Run a minimal but sound experimental grid

Once wiring and baselines are correct:

- For each of **3–5 seeds**, run:
  1. Float-only baseline.
  2. QAT-only.
  3. QAT + compression_reg with 1–2 λ values (e.g., “mild” and “strong”).
- For each run, record:
  - `val_bpb` post‑roundtrip (primary metric).
  - Runtime and `runtime_ratio` vs float-only baseline.
  - Codec metrics (pre/post-zlib sizes).
- Compute:
  - Mean ± std of `val_bpb` and runtime per condition.
  - Relative % change vs float-only and QAT-only baselines.
- Use these to assess:
  - Does QAT alone help post-roundtrip bpb?
  - Does adding compression_reg improve either bpb or zlib size at acceptable runtime?

### 5. Address runtime overhead

- Profile the current candidate configuration:
  - Attribute the ~28% overhead:
    - QAT overhead (fake-quant, observers).
    - Compression regularizer computation (extra forward passes, teacher calls, zlib calls if any during training).
    - Python/IO overhead.
- Design quick adjustments:
  - Reduce frequency or scope of compression regularizer (e.g., subset of layers, less frequent evaluation).
  - Ensure zlib is not called inside tight per-batch loops unless necessary.
- Target a **runtime_ratio ≤ 1.10** for at least one QAT and one QAT+compression_reg configuration.

### 6. Only then reassess PROCEED vs PIVOT

After the above:

- If QAT+compression_reg:
  - Consistently improves post-roundtrip `val_bpb` or zlib size by ≥0.5% at ≤1.10× runtime, with clean ablations and variance estimates,
  - And the analysis quality is ≥4/10,
  - Then move to **PROCEED** (paper writing and broader sweeps).

- If, even with proper wiring and tuning, QAT+compression_reg is consistently neutral or worse vs QAT-only across seeds and settings:
  - Then consider a **PIVOT** away from codec-guided regularization as currently designed (e.g., alternative objectives, different teachers, or abandoning codec alignment).

For now, the path is clearly **REFINE**: repair experimental control, establish robust baselines, and generate interpretable evidence before any go/no-go call on the underlying ideas.