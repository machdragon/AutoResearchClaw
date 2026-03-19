---
created: '2026-03-19T22:41:54+00:00'
evidence:
- stage-19/paper_revised.md
id: paper_revision-rc-20260319-220921-d02b4b
run_id: rc-20260319-220921-d02b4b
stage: 19-paper_revision
tags:
- paper_revision
- stage-19
- run-rc-20260
title: 'Stage 19: Paper Revision'
---

# Stage 19: Paper Revision

# RLG: Recurrent LoRA Gating for Budgeted Language Modeling

# Abstract

Severely resource‑constrained language modeling, as instantiated in the Parameter Golf challenge, requires optimizing compression quality under explicit caps on artifact size and runtime rather than under open‑ended training budgets. Existing work on parameter‑efficient fine‑tuning and conditional computation largely targets large transformer backbones and rarely foregrounds strict byte‑level artifact limits or quick‑gate‑style latency constraints. This paper studies RLG, a recurrent architecture that augments a tiny backbone with low‑rank LoRA adapters and a lightweight global residual gate, designed conceptually for a 16 MB artifact budget and a runtime ratio no greater than 1.10 relative to a challenge baseline. We implement a minimal instantiation of this design and obtain a single recorded run with three configurations—recurrence‑only, recurrence+LoRA, and recurrence+LoRA+gating—yielding validation bits‑per‑byte of 3.34944261, 3.33444261, and 3.32444261 respectively, compared to 3.37944261 for the challenge baseline, with all variants passing the quick‑gate predicate and recorded runtimes below 0.014 ms. These measurements indicate a monotone improvement in compression quality along the RLG configuration ladder at effectively unchanged latency in this run. While restricted to a single seed and a single benchmark environment, the study clarifies how recurrence, low‑rank adaptation, and global gating can be composed into a budget‑aware design and identifies concrete experimental practices for future, more extensive evaluations.

# Introduction

Language models have rapidly progressed in capability, yet many deployment scenarios require models that operate under rigid resource constraints rather than in data‑center regimes. Embedded devices, on‑device assistants, and constrained benchmarks such as Parameter Golf mandate tight upper bounds on model artifact size, end‑to‑end runtime, and often on training duration as well. In these environments, a model’s usefulness depends not only on its raw predictive quality but also on whether it fits within a specific byte budget and passes strict “quick‑gate” latency checks. Bits‑per‑byte on a held‑out validation set provides a natural objective and evaluation metric in this context, since it directly quantifies compression quality at the byte level and aligns with the artifact limits that deployment infrastructure enforces. Designing architectures that navigate this joint space of compression quality, artifact footprint, and latency therefore becomes a central challenge for small‑scale language modeling.

A growing body of work addresses efficient deep learning through pruning, distillation, and quantization, as well as through parameter‑efficient fine‑tuning (PEFT) mechanisms such as LoRA and adapters [houlsby2019parameter, hu2022lora, prottasha2025peft, bian2025survey]. These techniques have demonstrated that large pretrained transformers can be adapted to new tasks with a small fraction of their parameters updated, often with minimal loss in downstream performance. Other studies have examined the deployment side of efficiency, highlighting the discrepancy between training‑time proxies like FLOPs and real inference‑time costs, and arguing for metrics that better capture energy, latency, and memory usage [desislavov2021compute, frantar2023quipt]. Benchmarks such as MLPerf Tiny [banbury2021mlperf] and performance‑per‑resource proposals [selvan2024pepr] similarly foreground constraints that go beyond accuracy alone. However, most of this literature assumes that the backbone itself is relatively large and fixed, and that adapter or compression modules are small perturbations on top, rather than part of a globally budgeted design that must satisfy artifact caps like 16 MB.

Recurrent architectures, including modern variants such as RWKV [peng2023rwkv], S4‑style state‑space models [gu2021hyena, gupta2022simple], and gated RNNs, offer an alternative path to efficiency by replacing quadratic‑time attention with linear‑time sequence processing. Theoretical and empirical analyses alike emphasize that architectural bias can substitute for scale in many settings [berner2021modern, orvieto2023resurrecting], and recurrent or state‑space models have recently matched or exceeded transformers on some long‑context benchmarks at comparable parameter counts. At the same time, extensive experience with transformers shows that conditional computation via routing and gating, including mixture‑of‑experts designs [shazeer2017outrageously, fedus2021switch, zhu2025foldmoe], can deliver favorable quality‑throughput trade‑offs when implemented carefully. Yet, most mixture‑of‑experts and routing work targets server‑class environments and multi‑billion parameter models [zhu2023runtime, wen2023variational], making it less directly applicable to small, strictly budgeted settings.

Building on these strands, this paper studie

... (truncated, see full artifact)
