**Hypothesis 1 – “Compression-Teacher Distillation”: zlib as an *oracle* for better codes**

**Bold claim**

Training a model to *imitate the zlib coder itself*—via a learned “compression-teacher distillation” loss—will reduce **post-roundtrip val_bpb by at least 1.5%** compared to standard staged QAT that only matches float logits, under the same architecture, int8 inference, 16MB artifact limit, and ≤1.10× runtime.

If the best val_bpb improvement over a strong QAT+logit-distillation baseline is **<0.5%**, this hypothesis is rejected.

---

**Cross-domain inspiration**

- From **data compression** and **program analysis**:
  - Tools like profile-guided optimization don’t just optimize source code; they optimize *for the behavior of the compiler and CPU pipeline*.
  - Here, zlib is the “compiler/CPU.” Instead of only making the model robust to quantization noise, we explicitly train it to produce weight/activation statistics that zlib compresses efficiently.
- From **imitation learning**:
  - Rather than only distilling from a float teacher’s predictions, we “distill from the codec” by teaching the model how to behave in ways that zlib rewards (shorter code lengths).

---

**Rationale & novelty**

Existing QAT + distillation setups:

- Align student to a float teacher via:
  - Logit matching (KL divergence).
  - Possibly feature matching.
- At most, they inject quantization noise or fake quantization and hope zlib “likes” the resulting tensors.

Key missing ingredient:

- None explicitly *query the codec* during training and feed that signal back as a supervised objective.

New idea:

1. **Freeze a float teacher.**
2. **Introduce an auxiliary “compression-teacher” objective** during QAT:
   - For a given minibatch, run:
     - Teacher float32 forward → logits_t, activations_t.
     - Student int8 forward → quantized weights/activations.
   - Select a target tensor for compression (e.g., final layer weights or a critical activation tensor snapshot).
3. **Compute an approximate codelength signal from zlib**:
   - Quantized tensor → raw bytes → `zlib.compress` → record compressed length in bytes.
   - Normalize per-element or per-byte: `L_zlib = compressed_bits / num_raw_bytes`.
4. **Distillation-style “compression teacher” loss**:
   - Let `L_task` = standard task loss (e.g., NLL/log-likelihood).
   - Let `L_kd` = logit distillation from float teacher.
   - Let `L_comp = (L_zlib - α)^2` where α is a moving baseline or a target compressibility level from the teacher’s own quantized snapshot.
   - Total: `L_total = L_task + λ_kd L_kd + λ_comp L_comp`.

Why this is *not* just “compression regularization”:

- We do **teacher-relative** compression distillation:
  - Teacher defines not only what predictions are; it also defines *where compressibility matters* (e.g., which layers/tensors you track).
  - Student learns to meet or beat the teacher’s compressibility on those tensors, while staying close in prediction space.
- This explicitly **models the codec as a target behavior**, rather than just punishing entropy or L2 norms.

Feasibility vs. runtime:

- One GPU, ≤30 min:
  - Compute zlib cost on **small, representative tensors** only (e.g., last layer weights after quantization, or a downsampled activation map).
  - Evaluate `L_zlib` on **a fraction of minibatches** (e.g., every Nth batch).
  - All extra costs are CPU-side zlib calls + minor host-device transfers, easily within ≤1.10× if carefully profiled:
    - Use batched compressions and caching of tensor layouts.
    - Only do it on the student model; teacher is float-only.

---

**Measurable prediction**

- Setup:
  - Baseline A: your best staged-QAT with float-teacher logit distillation, no codec-aware loss.
  - Proposed B: same architecture, training epochs, gate budget, but with added `L_comp` as above.
  - Deployment: identical int8 quantization scheme, identical zlib settings, 16MB artifact limit enforced by pruning/prior hyperparams.
- Metric:
  - `val_bpb` = bits per byte after full int8+zlib roundtrip on validation artifact(s).
- Prediction:
  - Best B’s post-roundtrip `val_bpb` will be **≤ 0.985 ×** best A’s `val_bpb` (≥1.5% relative reduction), while:
    - Not degrading core task metric (e.g., val NLL or accuracy) by more than 0.3% relative.

**Failure condition (falsifiability)**

- If under identical training time and early stopping budget:
  - `val_bpb(B) > 0.995 × val_bpb(A)` (less than 0.5% improvement),  
  - or task performance degrades by >0.5% absolute,
- then this hypothesis is considered falsified.

---

**Estimated risk level**

- **Risk: Medium–High**
  - Medium: Technically simple; codec API is trivial; loss is differentiable w.r.t. model via straight-through or proxy (the gradient doesn’t go through zlib, only through correlation with model parameters).
  - High: zlib is quirky; its LZ77/Huffman heuristics may not line up nicely with simple per-layer compression surrogates, so gains may be small without careful choice of tensors and scaling of λ_comp.


---

---

**Hypothesis 2 – “Quantization-Vaccinated Gates”: stochastic gate dropout that *anti-correlates* with zlib entropy**

**Bold claim**

Injecting a **compression-biased stochastic gating process** during QAT—where gates are *more likely to drop units that inflate zlib entropy*—will create a model whose fixed, deterministic int8 deployment (no gates, same FLOPs) attains **≥2.0% lower post-roundtrip val_bpb** than standard QAT with uniform dropout, under the same gate budget and runtime constraints.

If the improvement is **<0.75%**, this hypothesis is rejected.

---

**Cross-domain inspiration**

- From **vaccination in epidemiology**:
  - Controlled, targeted exposure to a pathogen builds immunity more effectively than random exposure.
- From **Monte Carlo methods in physics**:
  - Importance sampling: inject stochasticity where it matters most for the quantity you care about.
- Here:
  - Random dropout ≈ uniform noise inoculation.
  - Compression-biased gate dropout ≈ *importance-weighted vaccination* against those features most likely to cause high-entropy, hard-to-compress representations.

---

**Rationale & novelty**

Standard practice:

- Dropout, stochastic depth, etc., are uniform or layerwise—agnostic to what the downstream codec sees.
- QAT may add uniform activation noise or fake quantization, but does not:
  - Dynamically identify which activations systematically hurt zlib.
  - Bias training-time stochasticity to “attack” those problematic units.

New idea:

1. During training only, maintain a **running estimate of per-channel (or per-head) compressibility**:
   - For a chosen layer or small subset of layers (to keep cost low), periodically:
     - Take the quantized activation tensor `A_q` (e.g., per-channel).
     - For each channel `c` in a random subset:
       - Extract bytes for that channel and zlib-compress → get `bpb_c`.
   - Maintain an exponential moving average (EMA) `h_c` of `bpb_c`:
     - Higher `h_c` = channel tends to produce zlib-unfriendly patterns (high entropy or poor match to zlib’s dictionary patterns).

2. **Compression-biased gate dropout**:
   - Introduce training-only multiplicative gates `g_c ∈ {0,1}` for channels (or heads).
   - For each minibatch:
     - Compute gating probability:
       - `p_drop(c) = clip(β * (h_c - μ), 0, p_max)`  
         where μ is mean of `h_c` over channels, β is a temperature.
     - Sample `g_c ~ Bernoulli(1 - p_drop(c))`.
   - This ensures:
     - Channels that historically inflate zlib entropy are more frequently dropped during training.
     - The model is repeatedly forced to reroute information through more compressible channels.

3. At inference:

   - **No gates, no extra ops.**
   - You freeze the final weights after QAT; gating and `h_c` are discarded.
   - Model is deterministic int8, identical FLOPs, artifact ≤16MB.

Why this is conceptually distinct:

- It’s not just L1/L2 regularization or uniform dropout; it’s a **feedback loop from the codec into the stochastic structure of the network during training**.
- Duplex effect:
  - Reduces reliance on “spiky,” hard-to-compress features.
  - Encourages features that are naturally more structured (e.g., longer runs, lower entropy), which zlib encodes efficiently.

Feasibility vs. compute:

- To respect ≤1.10× runtime:
  - Estimate `h_c` only:
    - Every N steps (e.g., once per epoch or every few hundred minibatches).
    - On a small fixed subset of channels and a smaller batch slice.
  - Compress on CPU asynchronously; update `h_c` via a queue / callback.
  - Gating itself is trivial: elementwise multiply with a precomputed binary mask.

---

**Measurable prediction**

- Baseline C:
  - Best staged QAT model with:
    - Standard dropout / stochastic depth (if any).
    - No compression-biased gating; trained to same epochs, same hyper-schedule.
- Proposed D:
  - Same architecture, quantization scheme, zlib settings, and gate budget.
  - Add compression-biased gate dropout during QAT as described.
  - Inference-time: identical compute graph to C.

- Metric:
  - `val_bpb` after full int8+zlib roundtrip.

- Prediction:
  - `val_bpb(D) ≤ 0.98 × val_bpb(C)` (≥2.0% improvement),
  - with task metric degradation ≤0.5% relative (or equal, if early stopping is tuned).

**Failure condition (falsifiability)**

- If, under comparable training time and careful tuning:
  - `val_bpb(D) > 0.9925 × val_bpb(C)` (less than 0.75% relative improvement),
  - or accuracy/NLL drops by >0.7% absolute,
- the hypothesis is falsified.

---

**Estimated risk level**

- **Risk: High**
  - The mechanism is quite unconventional:
    - Channels that are “bad for zlib” might also be highly informative for the task; aggressively dropping them could hurt task performance.
  - The mapping from per-channel zlib-friendliness to whole-model val_bpb is indirect.
  - However, even if per-channel signals are noisy, the importance-weighted dropout can act as a strong regularizer that reduces pathological, unstructured codes.

---

If you want to run a very quick test pass, Hypothesis 1 is lower engineering effort and more robust; Hypothesis 2 is more radical but could reveal interesting structure in which features are inherently “compressible specialists” versus “entropy bombs.”