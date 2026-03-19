---
created: '2026-03-19T20:37:39+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260319-203605-3afc3f
run_id: rc-20260319-203605-3afc3f
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

## Source

Research problem:  
Parameter Golf val_bpb minimization — lane_6: Byte‑grouped serialization for artifact compression in quantized LMs.

Hypothesis:  
If we serialize quantized weights with byte‑grouped packing, artifact bytes will decrease (≤ 16 MB compressed) without hurting post‑roundtrip val_bpb (Δ ≤ 0.01) or runtime (> baseline but ≤ 1.10×).


## Sub-questions

1. **How should byte‑grouped packing schemes be designed and parameterized to maximize compressibility under fixed quantization, while preserving exact numerical roundtrip of weights?**  
   - Define concrete layout families: e.g., significance‑grouped (all low bits together, high bits together), block‑wise bit‑slicing, channel/statistics‑grouped layouts.  
   - Specify packing granularity (per‑tensor, per‑block, per‑channel) and how metadata (scales/zero‑points, indices) is serialized.  
   - Ensure that serialization→compression→decompression→deserialization is numerically lossless at the integer level so that any val_bpb change is due to quantization/layout interaction, not representation error.

2. **To what extent do different byte‑grouped layouts improve compressed artifact size versus a strong baseline layout, and can they reliably meet the 16 MB cap across target models/precisions?**  
   - Baseline: standard tensor‑major / row‑major packing for the chosen quantizer.  
   - Compare artifact sizes after a fixed compressor (e.g., zstd at fixed level) across: baseline, significance‑grouped, statistics‑grouped, and at least one control layout (e.g., random byte shuffling).  
   - Analyze which structural properties (e.g., bit‑plane homogeneity, local entropy) correlate with compression gains, and whether those gains are consistent across (a) at least two model sizes or (b) two quantization bit‑widths (e.g., 4‑bit and 8‑bit).  
   - Determine if any layout consistently yields ≥20–30% size reduction over baseline and satisfies the ≤16 MB requirement.

3. **How do byte‑grouped layouts affect val_bpb after full roundtrip, and what mechanisms (if any) cause degradation relative to the baseline quantized model?**  
   - Measure val_bpb on the validation set for:  
     1) original FP model (reference),  
     2) quantized baseline layout,  
     3) each byte‑grouped layout after roundtrip.  
   - Verify that weight values after deserialization match the pre‑serialization quantized integers; if they do, explain any observed val_bpb drift (e.g., nondeterminism, ordering differences affecting kernels, altered cache behaviors).  
   - Establish whether all candidate layouts keep Δ val_bpb ≤ 0.01 absolute vs. the baseline quantized model, and identify any pathological layers/layouts that violate this.

4. **What is the runtime impact of byte‑grouped layouts relative to baseline, and which implementation strategies keep overhead within the ≤1.10× quick‑gate?**  
   - Implement inference kernels or unpacking routines for each layout, measuring tokens/sec (or wall‑clock per fixed validation run) over ≥3 runs.  
   - Decompose overhead into (a) one‑time deserialization/unpacking cost and (b) steady‑state inference cost (cache locality, memory bandwidth).  
   - Explore micro‑optimizations (e.g., streaming unpack to native tensor format at load time vs. on‑the‑fly bit unpacking) and determine the minimal set of changes that preserve baseline‑like runtime while retaining the compression benefit.  
   - Identify which layouts fail the quick‑gate and why (e.g., too much per‑token bit manipulation, poor memory coalescing).

5. **How general and robust are the observed artifact‑val_bpb‑runtime tradeoffs across models, quantization settings, and compressors, and what simple design rule emerges?**  
   - Replicate the best and a near‑best layout on at least:  
     - two model sizes or architectures, and/or  
     - two quantization precisions.  
   - Test at least one alternative compressor (e.g., gzip vs zstd) to see if gains are codec‑specific or structural.  
   - From ablations (including a negative/control layout), derive a compact guideline such as: “bit‑plane grouping within N×N blocks with pre‑grouped scales yields X% artifact reduction at ≤1.05× runtime in most settings.”  
   - Assess whether the same rule plausibly scales beyond the small‑to‑medium models in scope.


## Priority Ranking

1. **Sub-question 1 – Design & correctness of byte‑grouped layouts**  
   Dependency: foundation for all other experiments; must ensure exact roundtrip and clean isolation of the “layout” variable.

2. **Sub-question 4 – Runtime impact and passing the quick‑gate**  
   Reason: many plausible layouts may be dead on arrival if they violate the ≤1.10× runtime constraint; quick elimination saves time.

3. **Sub-question 2 – Artifact size reduction and 16 MB feasibility**  
   Reason: once a few runtimely‑feasible layouts exist, artifact size improvement vs. baseline and the 16 MB cap are the central hypothesis tests.

4. **Sub-question 3 – val_bpb stability afte

... (truncated, see full artifact)
