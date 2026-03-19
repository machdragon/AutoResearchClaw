---
created: '2026-03-19T20:45:55+00:00'
evidence:
- stage-08/hypotheses.md
- stage-08/novelty_report.json
id: hypothesis_gen-rc-20260319-203605-3afc3f
run_id: rc-20260319-203605-3afc3f
stage: 08-hypothesis_gen
tags:
- hypothesis_gen
- stage-08
- run-rc-20260
title: 'Stage 08: Hypothesis Gen'
---

# Stage 08: Hypothesis Gen

Here’s a synthesized final set of hypotheses that pull the strongest ideas from all three perspectives, explicitly integrate the contrarian’s concerns, and stay within the pragmatist’s feasibility envelope.

I’ll give 3 hypotheses. For each: rationale (including disagreements), measurable prediction, and explicit failure conditions.

---

## Hypothesis 1 – Entropy-Aware, Semantics-Preserving Grouped Serialization Beats Generic Compression by ≥10% Without Behavior Drift

**Claim**

For an already-quantized LLM, we can *reorder and group* weight bytes using entropy-aware, model-specific layout synthesis, then run a standard compressor (zstd) and obtain **≥10% smaller artifacts** than “baseline quantized weights + zstd” while:

- Keeping runtime overhead ≤1.10×, and  
- Preserving **bitwise-identical in-memory weights and outputs**, thus val_bpb within run-to-run noise.

If any of these fail under the specified setup, the hypothesis is rejected.

---

### Rationale

**Core idea (innovator + pragmatist):**

- Treat the quantized weights as a “corpus” with heterogeneous local statistics (per layer/head/channel).
- Learn an **offline permutation** that groups bytes from similar distributions into contiguous blocks (“entropy-homogeneous groups”), then pass this layout through zstd.
- At load time:
  - Decompress to a temporary buffer,
  - Apply the *inverse permutation* to reconstruct the exact original tensor layout,
  - Feed these tensors to the unmodified inference kernels.

This is conservative in that:
- **No new decode kernels** are introduced; all math is identical to the baseline stack.
- Only the disk layout changes; in-memory tensors after load are bit-equal to baseline.

**Why this can still beat generic compression:**

- Default tensor layouts interleave multiple distinct distributions (e.g., different heads, layers) in memory; zstd sees a noisy mixture.
- Grouping by estimated entropy / histograms (per-channel/per-head/per-layer) restores local homogeneity and should improve dictionary/entropy coding.
- This is exactly the kind of structure exploitation that column stores and codecs use, but applied to model weights rather than data.

**Directly addressing contrarian concerns (A + B):**

1. **“Serialization is not inert” (Hyp A)**  
   To ensure serialization is behaviorally inert, this hypothesis **forbids any change to decoding math or quantitative semantics**:
   - No new kernels, no changes in scale/zero-point grouping, no on-the-fly unpacking.
   - Exactly the same tensor strides, dtypes, and alignment as baseline after load.
   - The only operations are: (a) zstd decompression to a temporary buffer, (b) a pure byte-wise permutation back to the baseline format.

   This is explicitly *not* testing “realistic lane_6 with new kernels”; it is testing the boundary case: “does a pure layout/permutation change plus generic compression give us substantive wins and remain numerically inert?”  
   The contrarian’s stronger claim (“any non-trivial packing + kernel changes will affect numerics”) is **left unresolved**; here we test a narrower, safer variant.

2. **“Naive grouping can destroy entropy structure” (Hyp B)**  
   This hypothesis is *entropy-aware*, not naive:
   - Grouping is driven by measured local histograms / entropies.
   - We explicitly compare against:
     - Baseline tensor layout + zstd,
     - A simple, structure-preserving layout (e.g., layer-wise concatenation) to show that the learned grouping is not making things worse.

   If entropy-aware grouping underperforms even baseline + zstd, that directly supports the contrarian’s view that layout has to be co-designed with entropy structure.

**Feasibility (pragmatist):**

- Offline histogram + entropy estimation: linear in number of parameters; trivial for ≤150M params on 1 GPU/CPU.
- Layout synthesis: a graph/cluster/greedy grouping step over channels/blocks → design groups of, say, 4–64 KB.
- Decompression and permutation occur only at load time; inference kernels and runtime remain unchanged.

---

### Measurable prediction

**Setup**

- Pick 2–3 quantized LLMs:
  - At least one small (≤50M params 4-bit) and one medium-small (~100–150M params 4–8-bit).
- Define artifacts:
  1. `Baseline-raw`: standard quantized tensor dump.
  2. `Baseline-zstd`: `Baseline-raw` + zstd -19.
  3. `Entropy-grouped-zstd`:  
     - Analyze per-channel / per-head weight histograms and estimate entropy.  
     - Synthesize a permutation that packs bytes into entropy-homogeneous groups (fixed size G).  
     - Serialize according to this layout and compress with zstd -19.  
     - At load time, decompress and invert the permutation to reconstruct the exact `Baseline-raw` tensor layout.

**Metrics**

1. **Artifact size**  
   - `S_base = size(Baseline-zstd)`  
   - `S_group = size(Entropy-grouped-zstd)`

2. **Behavioral invariance**  
   - Check bitwise equality:
     - After load, for each tensor, compare SHA-256 (or XOR) vs baseline in-memory tensors.
   - E

... (truncated, see full artifact)


{
  "topic": "Parameter Golf val_bpb minimization — lane_6: Byte-grouped serialization for artifact compression. Hypothesis: If we serialize quantized weights with byte-grouped packing, artifact bytes will decrease without hurting post-roundtrip val_bpb. Artifact limit 16MB. Quick-gate: runtime <= 1.10x baseline.",
  "hypotheses_checked": 17,
  "search_queries": [
    "Parameter Golf val_bpb minimization — lane_6: Byte-grouped serialization for artifact compression. Hypothesis: If we serialize quantized weights with byte-grouped packing, artifact bytes will decrease without hurting post-roundtrip val_bpb. Artifact limit 16MB. Quick-gate: runtime <= 1.10x baseline.",
    "here synthesized final set hypotheses"
  ],
  "similar_papers_found": 0,
  "novelty_score": 1.0,
  "assessment": "high",
  "similar_papers": [],
  "recommendation": "proceed",
  "similarity_threshold": 0.25,
  "search_coverage": "full",
  "total_papers_retrieved": 45,
  "generated": "2026-03-19T20:45:55+00:00"
}