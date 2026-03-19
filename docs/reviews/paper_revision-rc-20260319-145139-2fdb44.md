---
created: '2026-03-19T15:11:19+00:00'
evidence:
- stage-19/paper_revised.md
id: paper_revision-rc-20260319-145139-2fdb44
run_id: rc-20260319-145139-2fdb44
stage: 19-paper_revision
tags:
- paper_revision
- stage-19
- run-rc-20260
title: 'Stage 19: Paper Revision'
---

# Stage 19: Paper Revision

# GOLF: Boundary-Aware Compression under a 16MB Artifact Cap

# Abstract

Strict deployment budgets in parameter‑golf settings require models to satisfy hard artifact‑size caps while remaining compatible with fast quick‑harness evaluations that gate promotion. Existing compression and parameter‑efficient fine‑tuning methods typically optimize global accuracy or parameter counts, but they do not treat promotion‑boundary behavior and artifact‑size verification as coupled first‑class constraints [prottasha2025peft, bian2025survey]. This paper studies GOLF, a lightweight controller that applies boundary‑aware loss weighting and importance‑conditioned compression to jointly shape validation bits‑per‑byte (val_bpb) and serialized artifact size under a 16,000,000‑byte cap. GOLF defines a promotion score over validation examples, constructs a distance to a decision threshold, and uses this distance to re‑weight the training loss and to guide selective redundancy for boundary‑adjacent examples. In a single recorded quick‑harness run with three fully logged conditions, GOLF’s configurations achieved identical aggregated val_bpb of 0.134155 with success_rate = 1.0 across globally compressed, model‑heavy, and artifact‑retrieval variants, and per‑seed val_bpb values for one condition spanned a range of 0.002158. These empirical observations show that the current boundary‑aware mechanisms do not yet yield measurable aggregate val_bpb gains over a globally compressed baseline, but they do produce tightly clustered performance under strict artifact‑cap enforcement. The study therefore provides a negative yet informative result: under the present synthetic setup, simple global compression remains competitive with boundary‑aware allocation, highlighting the need for richer metrics and more realistic workloads when evaluating boundary‑focused controllers.

# Introduction

Deployment pipelines that rely on promotion gates increasingly demand models that are not only accurate but also small, auditable, and fast to evaluate. Parameter‑golf scenarios crystallize this requirement by imposing strict artifact‑size caps—such as a 16MB serialized model budget—alongside quick‑harness checks that must complete within tight wall‑time limits before a candidate can be deployed. In such settings, practitioners cannot simply maximize predictive performance; they must jointly manage compression, verification, and promotion‑boundary behavior so that compact models remain reliable on the edge cases that determine whether an artifact is accepted or rejected. This tension between compactness and robustness motivates methods that reason explicitly about where representational bits are most valuable under operational constraints.

Existing work on parameter‑efficient fine‑tuning and model compression offers many techniques to reduce memory and computation, including adapter layers, low‑rank updates, pruning, and quantization [prottasha2025peft, bian2025survey]. Surveys of small‑model design for resource‑constrained environments show that careful architectural choices can make compact models surprisingly effective [song2025small], while iterative reasoning and energy‑based approaches provide theoretical perspectives on how representations can be reshaped under constraints [du2022iterative]. At the same time, research on parameter‑free and performative optimization points out that optimization objectives must be aligned with the downstream decision environment, especially when past deployment choices influence future data [park2024parameterfree]. Despite this rich landscape, most methods still treat artifact size as a soft target or a proxy such as parameter count, and they rarely integrate promotion‑boundary or quick‑harness constraints directly into the optimization loop. This gap becomes salient in operational workflows where artifact size and wall‑time limits are hard gates rather than preferences.

Concerns about safety and robustness under compression further sharpen the need for artifact‑aware controllers. Studies of adversarial robustness and universal perturbations document how compression can reshape decision boundaries in unanticipated ways [zhang2021survey, hingun2022reap], while analyses of refusal boundary instability in large language models show that subtle changes in artifacts or runtime configurations can alter compliance behavior on sensitive inputs [heverin2026prompt]. Work on safety compliance frameworks and automated compliance cards emphasizes that safety verification must account for the exact deployment artifact and its operational environment [hu2025safety, marino2024compliance]. In parallel, systems and benchmarking communities have proposed quick‑harness style evaluations, such as MLPerf Tiny, to enable fast, reproducible checks for embedded and edge models [banbury2021mlperf]. Research on preparing scientific artifacts and defining compliance for time‑bounded execution underlines the importance of records‑folder conventio

... (truncated, see full artifact)
