---
created: '2026-03-19T07:00:19+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-065838-2fdb44
run_id: rc-20260319-065838-2fdb44
stage: 03-search_strategy
tags:
- search_strategy
- stage-03
- run-rc-20260
title: 'Stage 03: Search Strategy'
---

# Stage 03: Search Strategy

objective:
  primary: Design and evaluate an automatic, compute-efficient compression/architecture
    search framework for small LMs that minimizes validation bits-per-byte (val_bpb)
    subject to a hard 16MB artifact size constraint, using a quick-harness as a low-fidelity
    gate.
  secondary:
  - Characterize and calibrate quick-harness metrics as predictors of full val_bpb
    across compression patterns.
  - Define a tractable joint search space over quantization, pruning, and adapters
    with fast, accurate size estimation.
  - Compare AutoRC-style controllers against fixed recipes and simpler auto-compression
    baselines under equal size and compute budgets.
overall_strategy:
  phases:
  - goals:
    - Clarify existing practices in quick/low-fidelity evaluation for LM compression
      and NAS.
    - Survey compression search spaces and constraint handling in model compression
      literature.
    methods:
    - Targeted keyword searches in arXiv, ACL Anthology, and major ML conferences
      (NeurIPS, ICML, ICLR).
    - Backward and forward citation chaining from a small set of anchor papers.
    name: Scoping_and_background
  - goals:
    - Identify methods for constructing small validation/eval harnesses that correlate
      strongly with full validation metrics.
    - Collect techniques for multi-fidelity evaluation, surrogate modeling, and calibration
      (mapping quick scores to full val_bpb).
    methods:
    - Search for multi-fidelity Bayesian optimization, early-stopping predictors,
      and low-fidelity proxies in NAS and HPO.
    - Look for LM-specific work on bits-per-byte / bits-per-character evaluation and
      data subsampling strategies.
    name: Harness_design_and_calibration_Q1
  - goals:
    - Define parameterization of quantization, pruning, and adapters suitable for
      automated search.
    - Gather formulas and empirical practices for computing compressed artifact size,
      including metadata and embeddings.
    methods:
    - Survey quantization (post-training and QAT), pruning (structured/unstructured),
      and low-rank adaptation literature.
    - Search for work that explicitly models or constrains model size, memory footprint,
      or on-device artifacts.
    name: Compression_search_space_and_constraints_Q2
  - goals:
    - Compare multi-fidelity BO, ASHA-style bandits, evolutionary search, and PBT
      for compression/NAS under constraints.
    - Identify best practices for handling hard constraints (like 16MB) and budget
      allocation between cheap and full evaluations.
    methods:
    - Search NAS and AutoML literature for constrained and multi-fidelity optimization.
    - Review AutoML frameworks (Ray Tune, Vizier, BOHB) for applicable algorithms.
    name: Controller_and_search_algorithm_Q3
  - goals:
    - 'Find baselines: strong fixed compression recipes and quantization-only auto-compression.'
    - Collect methods for constructing and analyzing Pareto frontiers (quality vs.
      size/latency).
    methods:
    - Search for LM compression benchmarks and studies that report performance vs.
      model size.
    - Identify open-source tools like AutoAWQ, AWQ, GPTQ, and their evaluation protocols.
    name: Empirical_comparison_and_Pareto_analysis_Q4
  - goals:
    - Understand transferability of quick-harness calibrations across datasets, models,
      and constraints.
    - Identify known failure modes of low-fidelity proxies and compressed models.
    methods:
    - Search for cross-dataset/model transfer in NAS and HPO.
    - Look for robustness analyses in compression and quantization papers.
    name: Generalization_and_robustness_Q5
practical_notes:
- Give special attention to works using Enwik8 or similar byte/character-level corpora
  with bits-per-byte/character metrics.
- Track any explicit 8MB–32MB deployment targets in mobile/edge LM papers as analogs
  to the 16MB cap.
- Maintain a small curated list of candidate quick-harness designs (dataset subsets,
  context lengths, vocab restrictions) found in the literature.
- Document any open-source AutoML/compression frameworks that could be adapted for
  AutoRC-style controllers.
priority_subquestions:
- id: Q1
  rationale: Everything else depends on having a reliable, cheap proxy for val_bpb.
  title: Quick-harness design and calibration
- id: Q2
  rationale: Need precise, efficiently computable size model and well-structured search
    space.
  title: Search space and constraint modeling under a 16MB artifact cap
- id: Q3
  rationale: Main algorithmic contribution once Q1 and Q2 are in place.
  title: AutoRC controller / search algorithm for parameter golf
- id: Q4
  rationale: Downstream but essential for demonstrating value.
  title: Empirical effectiveness and comparison to baselines
- id: Q5
  rationale: Important but can be partially deferred if resources are tight.
  title: Generalization, robustness, and transferability
risk_alignment:
- mitigation_via_search:
  - Prioritize

... (truncated, see full artifact)


{
  "sources": [
    {
      "id": "arxiv",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"language model\" OR \"transformer\") AND (\"low-fidelity\" OR \"proxy\" OR \"early stopping\" OR \"subsampled\" OR \"partial training\") AND (\"validation loss\" OR \"bits per byte\" OR \"bits-per-character\" OR \"bpc\") AND (\"multi-fidelity\" OR \"surrogate model\" OR \"calibration\" OR \"correlation\")",
      "verified_at": null
    },
    {
      "id": "scholar",
      "name": "Google Scholar",
      "type": "scholarly_search_engine",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "\"early stopping\" predictor neural network validation loss correlation multi-fidelity Bayesian optimization",
      "verified_at": null
    },
    {
      "id": "acl_anthology",
      "name": "ACL Anthology",
      "type": "digital_library",
      "url": "https://aclanthology.org",
      "status": "planned",
      "query": "(\"language model\" OR \"LM\") AND (\"validation loss\" OR perplexity) AND (\"subset\" OR \"subsampled\" OR \"small dev set\" OR \"few-shot evaluation\")",
      "verified_at": null
    },
    {
      "id": "arxiv_Q2_space",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"model compression\" OR \"neural network compression\") AND (\"quantization\" OR \"pruning\" OR \"sparsity\" OR \"low-rank\" OR \"LoRA\") AND (\"search\" OR \"automatic\" OR \"AutoML\" OR \"NAS\") AND (\"model size\" OR \"memory footprint\" OR \"on-device\" OR \"edge device\")",
      "verified_at": null
    },
    {
      "id": "arxiv_Q2_mixed_precision",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"mixed precision\" OR \"mixed-precision\" OR \"per-channel quantization\" OR \"per-tensor quantization\") AND (\"search space\" OR \"configuration space\") AND (\"Bayesian optimization\" OR \"evolutionary\" OR \"reinforcement learning\")",
      "verified_at": null
    },
    {
      "id": "scholar_Q2_constraints",
      "name": "Google Scholar",
      "type": "scholarly_search_engine",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "\"model size constraint\" \"neural network\" quantization pruning",
      "verified_at": null
    },
    {
      "id": "arxiv_Q3_multifidelity",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"multi-fidelity\" OR \"multi fidelity\" OR \"successive halving\" OR \"ASHA\" OR \"Hyperband\") AND (\"Bayesian optimization\" OR \"bandit\" OR \"evolutionary\" OR \"population based training\" OR \"PBT\") AND (\"neural architecture search\" OR \"NAS\" OR \"hyperparameter optimization\")",
      "verified_at": null
    },
    {
      "id": "arxiv_Q3_constrainedBO",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"constrained\" OR \"budgeted\" OR \"resource-aware\") AND (\"Bayesian optimization\" OR \"black-box optimization\") AND (\"model compression\" OR \"quantization\" OR \"pruning\")",
      "verified_at": null
    },
    {
      "id": "arxiv_Q4_LMcompression",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"language model\" OR \"transformer\") AND (\"quantization\" OR \"pruning\" OR \"compression\") AND (\"bits per byte\" OR \"bpc\" OR \"perplexity\") AND (\"model size\" OR \"parameter budget\" OR \"on-device\")",
      "verified_at": null
    },
    {
      "id": "arxiv_Q4_AWQ",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"AWQ\" OR \"AutoAWQ\" OR \"GPTQ\" OR \"bitsandbytes\") AND (\"quantization\" OR \"compression\")",
      "verified_at": null
    },
    {
      "id": "scholar_Q4_Pareto",
      "name": "Google Scholar",
      "type": "scholarly_search_engine",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "\"Pareto frontier\" model compression accuracy size",
      "verified_at": null
    },
    {
      "id": "arxiv_Q5_transferNAS",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"transferability\" OR \"generalization\" OR \"cross-dataset\" OR \"cross-domain\") AND (\"neural architecture search\" OR \"hyperparameter optimization\")",
      "verified_at": null
    },
    {
      "id": "arxiv_Q5_robustness_compression",
      "name": "arXiv",
      "type": "preprint",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "(\"robustness\" OR \"stability\") AND (\"quantization\" OR \"pruning\" OR \"sparsity\") AND (\"failure mode\" OR \"pathology\" OR \"degr

... (truncated, see full artifact)


{
  "queries": [
    "Parameter Golf val bpb minimization under",
    "Parameter Golf val bpb benchmark",
    "Parameter Golf val bpb survey",
    "Golf val bpb minimization",
    "Parameter Golf val comparison",
    "Parameter Golf val deep learning",
    "val bpb minimization under"
  ],
  "year_min": 2020
}