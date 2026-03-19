---
created: '2026-03-19T22:18:29+00:00'
evidence:
- stage-08/hypotheses.md
- stage-08/novelty_report.json
id: hypothesis_gen-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 08-hypothesis_gen
tags:
- hypothesis_gen
- stage-08
- run-rc-20260
title: 'Stage 08: Hypothesis Gen'
---

# Stage 08: Hypothesis Gen

Here is a synthesized final set of hypotheses that:

- Keep the strongest, most novel ideas (global graded gating; backbone thinning / reallocation; explicit distributional evaluation).
- Build in the pragmatist’s feasibility constraints (16MB, ≤1.10× RTT, simple architectures).
- Directly address the contrarian’s core concerns (backbone under‑optimization; head–tail tradeoffs; “is gating really conditional?”).
- Preserve explicit points of disagreement.

I’ll number them H1–H3.  

---

## H1 – Graded Global Gates vs Token‑wise Gating: How Much Conditional Capacity Do We Really Need?

### Hypothesis

Under a strict small‑model regime (artifact ≤16MB, RTT ≤1.05× baseline), a **sequence‑global graded gate** that modulates shared LoRA adapters recovers **at least 70–80%** of the validation bpb improvement of a richer **token‑wise gated LoRA** system, with:

- Far lower runtime overhead than token‑wise gating, and
- No worse degradation on rare / long‑range regimes than the token‑wise system.

This tests whether cheap, slow‑varying global modulation is “enough” conditional capacity—and whether more complex token‑level routing is overkill in this regime.

### Rationale

From the innovator:

- Strong claim that a single sequence‑level gate, computed from pooled hidden states, might capture most of the benefit of token‑wise routing.
- Cross‑domain analogy: functionally graded materials; a small number of global drivers capturing most variance.

From the pragmatist:

- Focus on mechanisms that are cheap, simple, and fit under 16MB / ≤1.10× RTT.
- LoRA plus very small extra heads are feasible on limited compute.

From the contrarian:

- Skepticism that routing really helps once the backbone is well‑trained.
- Concern that gating may preferentially optimize easy, high‑frequency tokens and harm tails.
- Concern that gating overhead may not be justified under tight RTT caps.

H1 explicitly:

- Puts global gating and token‑wise gating on the same dataset / backbone.
- Measures not just aggregate val_bpb but *distributional* effects (head vs tail; short vs long).
- Uses a stricter runtime cap (≤1.05×) for the global gate variant to directly test “is simple gating enough?”.

### Experimental Setup & Measurable Predictions

Models (all ≤16MB serialized):

1. **Backbone‑only, well‑tuned:**
   - Recurrent LM (e.g., GRU/LSTM or recurrent transformer).
   - Heavily optimized training: schedule, regularization, basic distillation if feasible.
   - Gives baseline bpb: `bpb_rec`.

2. **Token‑wise gated LoRA teacher (reference, can be >16MB if needed):**
   - Same backbone architecture, augmented with:
     - LoRA on selected projections.
     - Token‑wise gating MLPs to choose or mix LoRA experts per token.
   - Gives best bpb: `bpb_tok_gate`.
   - Improvement vs backbone:  
     `Δ_tok = bpb_rec − bpb_tok_gate`.

3. **Global‑gate LoRA (main model, ≤16MB):**
   - Same backbone size as backbone‑only (or slightly thinned to keep ≤16MB).
   - Add 1–few shared LoRA adapters (per layer or per group of layers).
   - Per sequence, compute a global gate vector g from a cheap pooled hidden state (e.g., mean over time from first layer; tiny MLP).
   - Apply same g to all tokens in that sequence:  
     `W_eff = W_base + α(g) · ΔW_LoRA`.
   - No token‑level branching in the gate.
   - bpb: `bpb_global`.

**Core measurable predictions:**

1. **Effectiveness ratio (global vs token‑wise):**

   \[
   \Delta_{\text{global}} = bpb_{\text{rec}} - bpb_{\text{global}}
   \]

   Prediction:

   \[
   \frac{\Delta_{\text{global}}}{\Delta_{\text{tok}}} \ge 0.7 \quad \text{(stretch target 0.8)}
   \]

   i.e., global gate recovers at least 70–80% of the token‑wise gated LoRA improvement.

2. **Runtime:**

   - Measure ms/token (tokens/sec) on:
     - Fixed‑length benchmark (e.g., seq len 512).
     - Mixed “field” workload and a worst‑case long‑sequence workload.

   Let `T_rec` be backbone runtime and `T_global` global‑gate runtime.

   Prediction:

   \[
   \frac{T_{\text{global}}}{T_{\text{rec}}} \le 1.05
   \]

   Token‑wise gated teacher is allowed to exceed this for analysis; we only care that global gate is cheap.

3. **Distributional head–tail behavior:**

   - Stratify validation tokens by:
     - Frequency bands (e.g., top 80%, 80–95%, 95–99%, 99–100%).
     - Sequence length (short / medium / long).
     - Context entropy (e.g., local surprisal quantiles).

   For each band, compute per‑token bpb for:

   - Backbone only
   - Token‑wise gated LoRA
   - Global‑gate LoRA

   Predictions:

   - The global‑gate model’s **relative gains** vs backbone are *not systematically worse* than the token‑wise model’s gains on the rarest tokens and long, high‑entropy sequences.
   - If token‑wise gating improves head but hurts tail, global gate should be at least *no worse* than that on tails.

### Failure Conditions (Falsifiability)

H1 is rejected if any of:

1. **Insufficient effectiveness:**

   \[
   \frac{\Delta_{\text{global}}}{\Delta_{\text{tok}}} 

... (truncated, see full artifact)


{
  "topic": "Parameter Golf val_bpb minimization — lane_1: Recurrence + LoRA + lightweight routing/gating composite. Hypothesis: If we start from recurrence-only and add LoRA specialization plus residual gating, post-roundtrip val_bpb will improve at fixed artifact budget while keeping runtime under 1.10x baseline. Artifact limit 16MB. Quick-gate: runtime <= 1.10x baseline.",
  "hypotheses_checked": 3,
  "search_queries": [
    "Parameter Golf val_bpb minimization — lane_1: Recurrence + LoRA + lightweight routing/gating composite. Hypothesis: If we start from recurrence-only and add LoRA specialization plus residual gating, post-roundtrip val_bpb will improve at fixed artifact budget while keeping runtime under 1.10x baseline. Artifact limit 16MB. Quick-gate: runtime <= 1.10x baseline.",
    "– Graded Global Gates vs Token‑wise Gating: How Much Conditional Capacity Do We Really Need?",
    "– Backbone Thinning + Ungated / Graded LoRA Reallocation Beats Any Pure Backbone at 16MB",
    "– Is Gating Actually Doing Conditional Specialization or Just Static Reparameterization? (Routing & Tail Analysis)",
    "here synthesized final set hypotheses"
  ],
  "similar_papers_found": 0,
  "novelty_score": 1.0,
  "assessment": "high",
  "similar_papers": [],
  "recommendation": "proceed",
  "similarity_threshold": 0.25,
  "search_coverage": "full",
  "total_papers_retrieved": 102,
  "generated": "2026-03-19T22:18:29+00:00"
}