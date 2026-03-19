## Source

User-provided problem statement and goal context on:
- Parameter Golf for val_bpb minimization
- lane_3: staged QAT aligned to int8+zlib roundtrip
- Under strict artifact (≤16MB) and runtime (≤1.10×) gates

---

## Sub-questions

1. **Objective & Measurement Design (Core Scientific Question)**  
   *How do we precisely define, measure, and operationalize “post-roundtrip val_bpb” and the runtime / artifact gates so that staged, roundtrip-aware QAT can be compared fairly to float-only and naive QAT baselines?*  
   - Define the exact evaluation protocol:
     - training data split and validation setup on enwik8,
     - computation of val_bpb from validation NLL for each model variant.
   - Specify the exact “roundtrip”:
     - float model → (QAT / post-hoc) int8 model → serialize → zlib compress → store artifact,
     - then: zlib decompress → load int8 weights → run validation.
   - Define what counts toward:
     - artifact size (weights, quantization metadata, tokenizer/config, any scaffolding),
     - runtime overhead (how to measure ≤1.10×: per-step training time? total wall-clock to a fixed val_bpb?).
   - Decide granularity of measurement:
     - how frequently to run full roundtrips during training,
     - which checkpoints or epochs are used for the final comparison.

2. **Staged QAT & Proxy Loss Design (Algorithmic Question)**  
   *What staged QAT schedule and which differentiable proxies best approximate int8+zlib behavior, improving post-roundtrip val_bpb without violating the quick-gate?*  
   - Design stages (e.g., 3-phase schedule):
     - Stage 1: mostly float32, light compressibility regularizers (e.g., L1, structured sparsity, zero-run-friendly patterns).
     - Stage 2: mixed-precision / “soft” int8 simulation with smooth quantization and proxy losses approximating zlib (e.g., entropy of weight histograms, run-length statistics, per-tensor variance control).
     - Stage 3: hard int8 QAT with realistic quantization operators and periodic true zlib roundtrip checks.
   - Choose proxy objectives that correlate with zlib compressibility:
     - encourage longer zero or repeated-value runs,
     - reduce “noisy” weight distributions that break Deflate blocks,
     - maybe re-order or block-structure weights to favor local redundancy.
   - Integrate these into the loss with tunable coefficients and schedules without destabilizing training.
   - Ensure the additional computations for proxies and quantization simulation fit within ≤1.10× runtime.

3. **Gate-Feasible Baseline & Architecture Search (Feasibility & Comparison Question)**  
   *Given the ≤16MB artifact limit and ≤1.10× runtime gate, what model architecture(s) and baseline training setups are viable, and how do float-only and naive QAT perform under the same constraints?*  
   - Choose candidate architectures (e.g., compact Transformer LM) whose:
     - int8 parameter count + minimal metadata can compress via zlib to ≤16MB.
   - Empirically determine:
     - float-only baseline val_bpb and artifact size after int8+zlib post-hoc quantization,
     - naive int8 QAT baseline (standard QAT recipe) + zlib artifact size and val_bpb.
   - Confirm both baselines:
     - respect the artifact limit or document necessary adjustments (smaller width/depth, pruning, etc.),
     - meet or serve as reference for the runtime gate.
   - Use these baselines to define realistic target gains (e.g., 1.5–3% val_bpb reduction).

4. **Roundtrip Frequency & Overhead Control (Systems/Optimization Question)**  
   *How often can we afford to do full int8+zlib roundtrips during training, and what hybrid strategy (proxy vs exact feedback) yields the best val_bpb gains under the 1.10× runtime constraint?*  
   - Empirically sweep roundtrip frequencies:
     - e.g., every 500, 1k, 5k, 10k steps, or only per-epoch / at milestones.
   - Quantify added wall-clock cost vs information value:
     - correlation between intermediate proxy metrics and true post-roundtrip val_bpb.
   - Design a control policy for roundtrips:
     - e.g., more frequent near convergence, or adaptive (increase frequency when proxy metrics plateau).
   - Decide how roundtrip feedback influences training:
     - early stopping,
     - adjusting regularization strengths,
     - switching stages or quantization aggressiveness.
   - Ensure the final chosen configuration satisfies ≤1.10× total runtime while still giving sufficient signal to improve compressibility.

5. **Ablations, Generalization, and Failure Modes (Validation Question)**  
   *Which components of staged, roundtrip-aware QAT are actually responsible for any val_bpb improvements, and how robust are the findings across seeds and small setting variations?*  
   - Ablate:
     - staged vs single-stage QAT (all quantization from the start),
     - with vs without compressibility proxies,
     - with vs without real zlib roundtrip feedback (proxies only).
   - Test sensitivity:
     - different random seeds,
     - slight architecture changes within the artifact budget (e.g., depth vs width),
     - small variations in proxy loss weights or stage durations.
   - Check for degenerate solutions:
     - models that compress extremely well (low artifact size) but severely degrade val_bpb or perplexity,
     - models gaming proxies while real zlib behavior does not improve.
   - Evaluate whether insights plausibly extend:
     - to other codecs (gzip/brotli) or data distributions, at least in small pilots.

---

## Priority Ranking

1. **(Highest)** Sub-question 1 – Objective & Measurement Design  
   - Without precise, reproducible definitions of val_bpb, roundtrip, and gates, all subsequent results risk being invalid or incomparable.

2. **Sub-question 3 – Gate-Feasible Baseline & Architecture Search**  
   - Establishing viable baselines and a model that fits ≤16MB is foundational; it also informs what is realistically achievable and which trade-offs matter.

3. **Sub-question 2 – Staged QAT & Proxy Loss Design**  
   - Core of the novelty; once the evaluation and baselines are solid, most effort should go into designing and iterating on this.

4. **Sub-question 4 – Roundtrip Frequency & Overhead Control**  
   - Critical for meeting the 1.10× runtime gate and making the method practical; can be tuned after an initial staged QAT design exists.

5. **(Lower, but necessary for publishability)** Sub-question 5 – Ablations, Generalization, and Failure Modes  
   - Comes after an initial “best” configuration is identified; essential for a convincing scientific story but not the first-order blocker.

---

## Risks

1. **Proxy Loss–zlib Mismatch**  
   - Risk: Differentiable proxies (sparsity, entropy, run-length stats) may correlate weakly with actual zlib compression, yielding little or no val_bpb improvement.  
   - Mitigation: Early, small-scale experiments to measure proxy–zlib correlation; consider light-weight approximate Deflate simulators if correlation is too low.

2. **Artifact Budget Incompatibility**  
   - Risk: Even aggressive quantization and compression may not push a reasonably performant model below 16MB, forcing too small a model to see clear val_bpb differences.  
   - Mitigation: Careful model-size planning (parameter count × 1 byte + metadata), optional structured sparsity or pruning, and iterative adjustment of architecture.

3. **Runtime Gate Violation (≥1.10×)**  
   - Risk: Frequent roundtrips or heavy proxy computations push training well beyond 1.10× baseline runtime.  
   - Mitigation: Profile early; treat gate as a hard constraint and bias toward cheap proxies and infrequent roundtrips with adaptive scheduling.

4. **Instability in Staged QAT**  
   - Risk: Transition between stages (especially when switching to hard int8 simulation) can destabilize training and hurt both perplexity and val_bpb.  
   - Mitigation: Gradual transitions (e.g., smooth quantization annealing), warm-up periods, and conservative quantization parameters in earlier stages.

5. **Weak or Non-Robust Gains**  
   - Risk: Observed val_bpb improvements are small (<1%) or inconsistent across seeds, making the result unconvincing.  
   - Mitigation: Reserve enough runs (seeds) in the compute budget; focus on the most promising proxy designs; if needed, relax some secondary constraints (e.g., slightly longer training) while still honoring the quick-gate in the main comparison.

6. **Overfitting to enwik8 & Codec Specificity**  
   - Risk: Learned compressibility patterns are idiosyncratic to enwik8 or to zlib’s particular heuristics, limiting generality.  
   - Mitigation: Include at least lightweight tests on another codec or small secondary dataset; frame contributions honestly as “codec-aware training” with discussion of portability.