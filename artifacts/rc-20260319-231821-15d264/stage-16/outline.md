```markdown
# Candidate Method Name

**Method name (2–5 chars):** `GOLF`  
(“Gate-Optimized Learned Factors”; mnemonic tie-in to Parameter Golf)

---

# Candidate Titles

1. **GOLF: Roundtrip-Aware Quantization for Compression-Efficient Parameter Golf**
   - Memorability: 5/5 (short, matches challenge name)
   - Specificity: 4/5 (mentions roundtrip + compression + context)
   - Novelty signal: 4/5 (codec-aware QAT framing is uncommon)

2. **GOLF: Staged Quantization-Aware Training for Codec-Aligned Language Models**
   - Memorability: 4/5
   - Specificity: 5/5 (staged QAT, codec alignment, LM)
   - Novelty signal: 4/5

3. **GOLF: Teaching Models to Survive Int8+Zlib Roundtrips**
   - Memorability: 5/5 (vivid, informal but catchy)
   - Specificity: 4/5 (deployment path explicit)
   - Novelty signal: 5/5 (very strong “this is new” signal)

Preferred for a NeurIPS/ICLR-style paper: **Title 2** (best trade-off of rigor and catchiness).  
For now, the outline will assume **Title 2**.

---

# Paper Outline (with Goals, Word Counts, and Evidence Links)

> Throughout, “evidence links” indicate which existing results you can already cite vs. where you must add new experiments (REFINE step).

---

## 1. Introduction (800–1000 words)

### Section Goals
- Motivate deployment-aligned training for compressed models under strict artifact and runtime gates (Parameter Golf context).
- Argue that current quantization and compression schemes are largely disconnected at training time.
- Introduce **GOLF** as staged QAT explicitly aligned to an **int8+zlib roundtrip**, with an emphasis on *post-roundtrip* `val_bpb` under a gate budget.
- Make clear that current evidence is preliminary and infrastructure-focused, motivating a careful methodology.

### Substructure

1. **Motivation: Deployment-constrained language models**
   - Describe practical setting: Parameter Golf challenge, 16 MB artifact limit, ≤1.10× runtime quick-gate.
   - Explain why bits-per-byte (`val_bpb`) after a full deployment pipeline matters more than float validation loss.
   - Evidence links:
     - Parameter Golf docs / rules (external).
     - Existing work on deployment-centric metrics (e.g., model size, latency) in compression/QAT literature.

2. **Gap: Disconnection between quantization, compression, and training objectives**
   - Summarize state of play:
     - QAT is usually calibrated to minimize float-domain loss, not codec behavior.
     - Compression (e.g., zlib) is fully post-hoc, with no learning signal.
     - Prior work focuses on static weight distributions (e.g., entropy coding) but rarely on *codec-aligned* training.
   - Highlight absence of methods that explicitly minimize *post int8+zlib* `val_bpb` under runtime gates.
   - Evidence links:
     - QAT methods (e.g., Jacob et al., 2018; Esser et al., 2019; recent LLM quantization work).
     - Model compression via pruning, quantization, and entropy coding (Han et al., 2016; Choi et al., etc.).
     - Works on deployment metrics (latency/footprint) as first-class objectives.

3. **Our approach: GOLF for lane_3 Parameter Golf**
   - Introduce **GOLF** by name and core idea:
     - Staged QAT schedule.
     - Compression-aware regularizer approximating zlib behavior.
     - Training and evaluation explicitly tied to the int8+zlib roundtrip.
   - Emphasize lane_3 hypothesis:
     - “Staged QAT aligned to int8+zlib improves post-roundtrip `val_bpb` over float-only training under the same gate budget.”
   - Clarify the Parameter Golf constraints:
     - 16,000,000-byte artifact limit; records-folder submission path; 10-minute-ish training/eval runs; no rewrites of canonical entrypoints.

4. **Contributions**
   - Bullet list (3–4 points), each 2–3 sentences:
     - A deployment-aligned evaluation harness for lane_3: post-roundtrip `val_bpb`, runtime gates, and artifact size tracking.
       - Evidence: Current working pipeline, single-run metrics (baseline vs staged QAT + compression_reg).
     - The **GOLF** framework: staged QAT with a codec-aligned compression regularizer targeting int8+zlib, designed for Parameter Golf constraints.
       - Evidence: Method design (this paper); current implementation sketch.
     - A methodology for causal evaluation under strict compute and artifact limits, including ablation tooling and gate-aware comparisons.
       - Evidence: Ablation tooling, “ABALATION FAILURE” diagnostics; planned refinement experiments.
     - A first empirical study showing that a naïve GOLF instantiation is numerically stable but not yet superior, and what this reveals about aligning QAT with real codecs.
       - Evidence: Current single-run results and detailed methodological audit.

---

## 2. Related Work (600–800 words)

### Section Goals
- Position GOLF within three strands: QAT, model compression/coding, and deployment-constrained evaluation.
- Highlight absence of **codec-aware, roundtrip-aligned** QAT in existing literature.
- Emphasize how Parameter Golf’s constraints differ from usual compression settings.

### Subsections

2.1 **Quantization-Aware Training and Low-Precision Models**
- Review classic QAT for CNNs and transformers; discuss fake quantization, per-channel scaling, etc.
- Mention recent int8/4-bit LLM work; note focus on pretraining/fine-tuning metrics, not codec roundtrip.
- Contrast with GOLF’s emphasis on *zlib-aligned* signals and post-roundtrip `val_bpb`.
- Evidence links:
  - QAT for CNNs and transformers (Jacob et al.; Esser et al.; Nagel et al.; Dettmers et al.).
  - LLM quantization baselines (e.g., GPTQ, AWQ, SmoothQuant).

2.2 **Model Compression, Entropy Coding, and Learned Compressibility**
- Cover pruning + quantization + Huffman/entropy coding (e.g., Deep Compression).
- Discuss works that shape weight distributions for entropy coding or compression-aware regularization.
- Argue that most such work models idealized entropy, not specific real-world codecs like zlib.
- Evidence links:
  - Deep Compression and follow-ups.
  - Learned entropy models (e.g., variational compression, hyperpriors).
  - Any prior “codec-aware” training methods, if they exist (even outside NLP).

2.3 **Deployment-Centric Metrics and Benchmarking**
- Survey papers and benchmarks that include latency, footprint, or energy as first-class metrics.
- Explain how Parameter Golf extends this by imposing artifact sizes and strict runtime gates, and prioritizing post-roundtrip metrics.
- Position GOLF as explicitly tuned for such constraints, not for bulk pretraining.
- Evidence links:
  - Mobile/embedded ML benchmarks (MLPerf Tiny, etc.).
  - Efficient training & inference frameworks focusing on wall-clock budgets.

---

## 3. Method (1000–1500 words)

### Section Goals
- Formally define the problem: minimize post-roundtrip `val_bpb` under (artifact, runtime) constraints.
- Detail GOLF architecture: staged QAT schedule and compression regularizer approximating zlib behavior.
- Clearly describe the lane_3 Parameter Golf setting and how GOLF respects the constraints.
- Provide enough detail that an expert reader could reimplement without the original repo.

### Subsections

3.1 **Problem Formulation: Compression-Gated Language Modeling**
- Define:
  - Base language model \( f_\theta \).
  - Deployment transform \( \mathcal{D} \): float → int8 quantization → serialization → zlib compress/decompress → int8 → float or int8 inference.
  - Post-roundtrip validation metric `val_bpb` as \( \mathcal{L}_{\text{deploy}}(\theta) \).
- Formulate objective:
  \[
  \min_\theta \mathbb{E}_{(x,y)\sim \mathcal{D}_\text{train}}[\ell(f_{\mathcal{D}(\theta)}(x), y)]
  \]
  subject to:
  - Artifact size \( \leq 16\text{MB} \),
  - Expected runtime \( T(\theta) \leq 1.10 \times T_{\text{baseline}} \).
- Discuss how constraints are enforced via gating in experiments (quick gate, records-folder submissions).
- Evidence links:
  - Parameter Golf specs (artifact limit, quick-gate).
  - Current metrics (baseline vs candidate runtime, artifact size estimates).

3.2 **Staged Quantization-Aware Training in GOLF**
- Describe QAT setup:
  - Fake-quant modules inserted at chosen layers (e.g., embeddings, final projection).
  - Staged schedule:
    - Early training: float-only, no QAT.
    - Mid training: partial QAT (subset of layers).
    - Late training: full QAT, approximating deployment quantizer.
  - Hyperparameters: `qat_start_frac`, `qat_ramp_length`, etc.
- Clarify how QAT is wired to respect the do-not-modify root script constraint:
  - GOLF adds new experiment configs and QAT modules, leaving canonical entrypoints intact.
- Evidence links:
  - Existing QAT theory and schedules from related work.
  - Current implementation choices (scope: `final_proj`, `embed`; staged schedule).
  - Single-run stability result (no NaNs, near-baseline `val_bpb`).

3.3 **Codec-Aligned Compression Regularization**
- Describe the compression regularizer:
  - A differentiable proxy for zlib’s coding cost (e.g., weight distribution penalties, local entropy approximations).
  - Applied selectively (e.g., to `final_proj` and embeddings) to limit overhead.
- Formalize the augmented loss:
  \[
  \mathcal{L}_{\text{train}} = \mathcal{L}_{\text{LM}} + \lambda_{\text{comp}} \, \mathcal{R}_{\text{zlib-proxy}}(\theta)
  \]
- Discuss:
  - Why direct zlib in-loop is too slow / non-differentiable.
  - How GOLF’s regularizer is tuned to correlate with zlib-compressed size while respecting runtime gate.
- Evidence links:
  - Current implementation flags (`compression_reg_enabled`, `compression_reg_lambda`).
  - Methodology audit showing these flags must be wired properly (ablation failure).

3.4 **Roundtrip-Aware Evaluation and Gate Enforcement**
- Explain evaluation protocol:
  - At evaluation, apply full `int8+zlib` roundtrip to model artifacts produced under each configuration.
  - Compute `val_bpb` from the roundtrip model; log `runtime_ratio` vs canonical float baseline.
  - Use “quick-gate” to flag configurations exceeding 1.10× runtime as non-deployable.
- Detail recording and artifact handling:
  - records-folder submissions only.
  - Track serialized size before and after zlib; verify 16MB limit.
- Evidence links:
  - Existing pipeline: baseline and candidate `val_bpb`, `runtime_ratio`, quick-gate flag.
  - Logging outputs: delta_bpb, runtime, ABALATION FAILURE, etc.

3.5 **Implementation within the Parameter Golf Framework**
- Describe how GOLF is integrated while respecting constraints:
  - No modification of root training script; new configs/experiment files only.
  - Training/eval time capped to leaderboard-style 10-minute runs; extended sweeps treated as non-record experiments.
- Highlight ablation infrastructure:
  - Auto-detection of controlled differences.
  - “ABALATION FAILURE” diagnostic as a safeguard.
- Evidence links:
  - Current ablation tool behavior and logs.
  - Planned fixes to ensure toggles affect execution paths.

---

## 4. Experiments (800–1200 words)

### Section Goals
- Present experimental design tailored to Parameter Golf lane_3.
- Describe baselines and GOLF variants under the same harness.
- Clarify hardware, datasets, and hyperparameters.
- Emphasize methodological refinements prompted by the negative first result.

### Subsections

4.1 **Experimental Setup**
- Datasets and tasks:
  - Describe corpus used, train/val split, and metric definition (bits-per-byte on validation text).
  - Clarify that validation is not used to tune zlib directly (avoid leakage).
- Models:
  - Base architecture (parameter count, depth, vocab).
  - Quantization scheme (int8 format, per-channel/per-tensor, calibration).
- Hardware and runtime measurement:
  - NVIDIA RTX 5070 Ti, 16GB VRAM.
  - Describe how runtime is measured (wall-clock training + eval; n=1 per current run; plan for multiple seeds).
- Hyperparameters:
  - Learning rate, batch size, training steps/epochs.
  - QAT schedule params and compression_reg λ values.
  - Include **Table 1: Hyperparameters**.
- Evidence links:
  - Current recorded metrics (single run) and environment config.
  - Planned refined configurations (float-only, QAT-only, QAT+compression_reg, 3+ seeds).

4.2 **Baselines and GOLF Variants**
- Baselines (to be run/refined):
  - Float-only baseline: training without QAT or compression_reg; post-hoc int8+zlib roundtrip at evaluation.
  - QAT-only baseline: staged QAT without compression regularizer.
- GOLF variants:
  - GOLF-λ0: QAT-only (compression_reg disabled).
  - GOLF-λmild, GOLF-λstrong: QAT + compression_reg at different λ.
- Explain that current presented metrics come from a single GOLF-λcandidate run against a cached baseline scalar; future experiments will add proper baselines and seeds.
- Evidence links:
  - Present single-run metrics and their limitations (n=1, ambiguous baseline).
  - Design for upcoming ablation runs under REFINE decision.

4.3 **Training and Evaluation Protocol**
- Outline:
  - For each configuration, run training for N steps within time budget.
  - After training, export the model, run int8 quantization + zlib compress/decompress, then evaluate `val_bpb`.
  - Measure runtime and artifact size, enforce quick-gate.
- Clarify that any run exceeding 10-minute constraints is treated as non-record and not counted toward leaderboard-style claims.
- Evidence links:
  - Current runtime numbers (62992 ms baseline vs 80894 ms candidate).
  - Parameter Golf rules about runtime and artifact limits.

---

## 5. Results (600–800 words)

### Section Goals
- Present quantitative outcomes: `val_bpb`, runtime, artifact size, and codec metrics.
- Interpret the initial negative result as a diagnostic, not as a final verdict.
- Use ablation results (once fixed) to isolate contributions of QAT vs compression regularization.

### Subsections

5.1 **Main Quantitative Results**
- Introduce **Table 2: Main Results** (float-only, QAT-only, GOLF variants) with:
  - Mean ± std `val_bpb` post-roundtrip.
  - Runtime ratio vs float baseline.
  - Zlib-compressed model size.
- For now, describe the preliminary single-run result as an illustrative row:
  - Baseline_val_bpb ≈ 3.3794; candidate_val_bpb ≈ 3.3919 (+0.37% worse).
  - Runtime_ratio ≈ 1.284 (fails ≤1.10 gate).
- Emphasize that this run is **not** statistically interpretable and will be replaced by multi-seed averages in final version.
- Evidence links:
  - Provided LaTeX table and metric summary.

5.2 **Ablation Studies: QAT vs Compression Regularization**
- Present **Table 3: Ablation Results**:
  - Float-only vs QAT-only vs QAT+compression_reg with varying λ.
- Discuss:
  - Whether QAT alone improves or degrades post-roundtrip `val_bpb`.
  - Whether compression_reg materially changes codec metrics (zlib size), and at what runtime cost.
- Connect to ablation integrity:
  - Explain earlier “ABALATION FAILURE” and how fixing toggles changed the picture.
- Evidence links:
  - Planned ablation runs (once wiring is fixed).
  - Current ablation failure logs as a cautionary case study.

5.3 **Codec- and Gate-Aware Performance Tradeoffs**
- Use at least one figure (e.g., **Figure 1: Quality–Runtime–Size Pareto**):
  - X-axis: runtime_ratio.
  - Y-axis: post-roundtrip `val_bpb`.
  - Bubble size: zlib-compressed model size.
- Analyze:
  - Where GOLF variants fall vs baselines under ≤1.10 × runtime.
  - Whether any configuration offers a consistent improvement without violating gates.
- Evidence links:
  - Future multi-configuration runs.
  - Current preliminary point as “numerically stable but not yet competitive.”

---

## 6. Discussion (400–600 words)

### Section Goals
- Interpret findings in light of prior literature.
- Explain why the first GOLF instantiation underperforms and what that says about codec-aligned QAT.
- Reflect on the role of tooling (ablation framework, quick-gate) in reliable compression research.

### Subsections

6.1 **What Does the Negative First Result Tell Us?**
- Discuss how the slight degradation in `val_bpb` (+0.37%) and 28% runtime overhead indicate:
  - QAT+compression_reg is not trivially beneficial.
  - A naïve implementation can easily violate runtime gates.
- Argue that such early failures are expected when aligning to a non-differentiable codec.
- Evidence links:
  - Current single-run data and methodology audit.

6.2 **Codec-Aware Training vs Post-Hoc Compression**
- Compare to prior methods that compress post-hoc:
  - Many achieve good size reductions but do not optimize post-roundtrip quality explicitly.
- Argue that GOLF remains promising conceptually:
  - If properly tuned, it might shift models into zlib-friendly regimes without sacrificing `val_bpb`.
- Evidence links:
  - Related work on entropy modeling and coding-aware objectives.
  - The potential of learned weight distributions for better compressibility.

6.3 **Designing Reliable Experiments Under Strict Gates**
- Reflect on the importance of:
  - Multi-seed baselines,
  - Explicit gate-aware evaluation (runtime, artifact size),
  - Strong ablation tooling to avoid mis-wired experiments.
- Position the Parameter Golf challenge as an ideal testbed for such methodologies.
- Evidence links:
  - “ABALATION FAILURE” as a concrete example.
  - Parameter Golf constraints enforcing rigor.

---

## 7. Limitations (200–300 words)

### Section Goals
- Explicitly list concrete limitations, quarantining caveats from other sections.
- Clarify that current results are infrastructure- and methodology-focused rather than conclusive performance claims.

### Key Limitations (to elaborate in prose)
- **Underpowered experiments so far**:
  - Only one candidate GOLF run and a cached baseline scalar; no multi-seed variance or multiple baselines yet.
  - Evidence: n=1 in current results; explicit analysis rating of 3/10.

- **Broken ablation control in the current snapshot**:
  - “ABALATION FAILURE” shows that early ablations are invalid; some toggles did not affect code paths.
  - This undermines causal attribution for early observations.

- **Ambiguous and under-documented baseline**:
  - Current baseline is not a separate float-only run in the same harness; provenance unclear.

- **Incomplete codec metrics**:
  - Presently missing layerwise zlib size and entropy estimates; only global artifact size is tracked.

- **Runtime profiling incomplete**:
  - Exact breakdown of the 28% overhead (QAT vs compression_reg vs infrastructure) not yet characterized.

---

## 8. Conclusion (200–300 words)

### Section Goals
- Summarize the conceptual proposal and the current empirical status.
- Emphasize infrastructure contributions and the REFINE decision.
- Point to specific next steps.

### Content Plan
- Brief recap:
  - Introduce GOLF: staged QAT plus codec-aware regularization aligned to int8+zlib roundtrip for Parameter Golf lane_3.
  - Stress that the hypothesis remains plausible but unconfirmed.

- Current status:
  - End-to-end measurement stack is operational.
  - Preliminary run: numerically stable, slight degradation in post-roundtrip `val_bpb`, runtime gate violation.

- Future work:
  - Fix ablation wiring and re-run baselines and GOLF variants with ≥3 seeds.
  - Add rich codec metrics and runtime profiling.
  - Explore alternative regularizers and schedules that might satisfy both the 16MB artifact limit and ≤1.10× runtime while improving post-roundtrip `val_bpb`.

- Close with broader takeaway:
  - Argue that truly deployment-aligned training for compressed models requires integrating codecs, quantization, and rigorous, gate-aware evaluation—precisely the space GOLF aims to explore.

---
```