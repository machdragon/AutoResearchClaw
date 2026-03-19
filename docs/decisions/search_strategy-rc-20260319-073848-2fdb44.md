---
created: '2026-03-19T07:41:07+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-073848-2fdb44
run_id: rc-20260319-073848-2fdb44
stage: 03-search_strategy
tags:
- search_strategy
- stage-03
- run-rc-20260
title: 'Stage 03: Search Strategy'
---

# Stage 03: Search Strategy

context:
  domain: small language models, compression, AutoRC-style automated recipe/architecture
    search
  key_metrics:
  - description: Bits-per-byte on a small, fast evaluation harness (≤10 minutes on
      a single GPU).
    name: val_bpb_harness
  - description: Bits-per-byte on the full validation benchmark, used for final model
      selection.
    name: val_bpb_full
  - description: Total serialized artifact size in megabytes (weights + tokenizer
      + minimal runtime metadata).
    name: artifact_size_mb
  - description: Wall-clock time to run the quick-harness evaluation on a single GPU.
    name: harness_runtime
  - description: Total compute spent in search (GPU-days).
    name: gpu_days
  primary_objective: Minimize validation bits-per-byte (val_bpb) under a quick-harness
    gate while enforcing a hard 16MB artifact size constraint at promotion time.
output_expectations:
  artifacts:
  - Survey-style notes on quick-harness design patterns and their empirical predictiveness.
  - Analytic and empirically calibrated formulas for predicting artifact_size_mb from
    architecture and compression parameters.
  - Shortlist of AutoRC/HPO algorithms suitable for parameter golf under hard size
    constraints, with pros/cons.
  - Table of compression and recipe knobs ranked by val_bpb gain per MB at ≤16MB.
  - Guidelines document summarizing reusable heuristics for low-footprint LM design.
  coverage_depth:
    compression_and_recipe_knob_importance: medium
    generalization_and_robustness: medium
    param_golf_autorc_algorithm_design: medium_high
    quick_harness_design_and_predictiveness: high
    search_space_and_16mb_constraint_modeling: high
priority_order:
- quick_harness_design_and_predictiveness
- search_space_and_16mb_constraint_modeling
- param_golf_autorc_algorithm_design
- compression_and_recipe_knob_importance
- generalization_and_robustness
retrieval_plan:
  phases:
  - description: Establish baseline knowledge on small LMs, bits-per-byte metrics,
      quick evaluation harnesses, and model compression under tight size constraints.
    focus_questions:
    - 1.1
    - 1.2
    - 2.1
    - 2.3
    name: phase_1_foundation_and_background
    strategies:
    - queries:
      - '"bits per byte" language model evaluation small models'
      - small language models 10MB 20MB compression quantization pruning
      - fast validation harness language models correlation full validation
      - quick evaluation protocol single GPU <10 minutes perplexity
      - AutoML architecture search under model size constraints
      tools:
      - Semantic Scholar
      - Google Scholar
      - arXiv
      type: scholarly_search
    - description: From highly cited compression and tiny-LM papers, follow references
        on evaluation protocols and size-constrained search.
      type: snowballing
  - description: Targeted search on designing predictive quick-harnesses for LM evaluation.
    focus_questions:
    - 1.1
    - 1.2
    - 1.3
    - 1.4
    name: phase_2_quick_harness_design
    strategies:
    - queries:
      - '"proxy tasks" for language model evaluation correlation with full benchmark'
      - multi-fidelity evaluation language models quick proxy metrics
      - subset selection for validation set language models domain mix
      - overfitting to validation subset language models detection
      - early stopping proxy perplexity correlation study
      tools:
      - arXiv
      - Google Scholar
      type: scholarly_search
    - queries:
      - multi-fidelity hyperparameter optimization language models
      - cheap proxies for neural architecture search NLP
      tools:
      - OpenReview
      - NeurIPS proceedings
      - ICLR proceedings
      type: domain_search
  - description: Model artifact size components and define a search space that respects
      16MB.
    focus_questions:
    - 2.1
    - 2.2
    - 2.3
    - 2.4
    name: phase_3_size_constraint_and_artifact_modeling
    strategies:
    - queries:
      - tiny transformer language models <20MB
      - parameter-efficient language models quantization 4-bit 8-bit
      - predicting model size from architecture and quantization
      - tokenizer size impact on model footprint
      - Pareto frontier model size vs accuracy NLP
      tools:
      - arXiv
      - Google Scholar
      type: scholarly_search
    - queries:
      - Hugging Face model file size calculation
      - tokenizer serialization size
      - state_dict size vs parameter count
      tools:
      - Hugging Face docs
      - PyTorch docs
      type: implementation_docs
  - description: Investigate AutoML and multi-fidelity HPO methods suitable for parameter
      golf under hard size constraints.
    focus_questions:
    - 3.1
    - 3.2
    - 3.3
    - 3.4
    name: phase_4_autorc_and_search_algorithm_design
    strategies:
    - queries:
      - multi-fidelity Bayesian optimization neural networks
      - Hyperband ASHA language models
      - evolutionary arch

... (truncated, see full artifact)


{
  "sources": [
    {
      "id": "s1",
      "name": "arXiv",
      "type": "scholarly_repository",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"bits per byte\" language model evaluation small models OR \"tiny transformer\" compression",
      "verified_at": null
    },
    {
      "id": "s2",
      "name": "Google Scholar",
      "type": "scholarly_search_engine",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "\"fast validation\" OR \"quick harness\" language models multi-fidelity perplexity",
      "verified_at": null
    },
    {
      "id": "s3",
      "name": "Semantic Scholar",
      "type": "scholarly_search_engine",
      "url": "https://www.semanticscholar.org",
      "status": "planned",
      "query": "\"small language models\" compression quantization pruning \"model size\"",
      "verified_at": null
    },
    {
      "id": "s4",
      "name": "OpenReview",
      "type": "conference_repository",
      "url": "https://openreview.net",
      "status": "planned",
      "query": "\"multi-fidelity\" hyperparameter optimization \"language models\" OR \"NLP\"",
      "verified_at": null
    },
    {
      "id": "s5",
      "name": "NeurIPS Proceedings",
      "type": "conference_repository",
      "url": "https://papers.nips.cc",
      "status": "planned",
      "query": "\"proxy tasks\" \"neural architecture search\" constrained OR \"size-constrained\"",
      "verified_at": null
    },
    {
      "id": "s6",
      "name": "ICLR Proceedings",
      "type": "conference_repository",
      "url": "https://iclr.cc/Conferences",
      "status": "planned",
      "query": "\"AutoML\" \"model size constraint\" OR \"feasibility-aware\" Bayesian optimization",
      "verified_at": null
    },
    {
      "id": "s7",
      "name": "Hugging Face Hub",
      "type": "model_repository",
      "url": "https://huggingface.co/models",
      "status": "planned",
      "query": "\"tiny\" transformer OR \"small\" language model size:<50MB",
      "verified_at": null
    },
    {
      "id": "s8",
      "name": "Papers With Code",
      "type": "benchmark_repository",
      "url": "https://paperswithcode.com",
      "status": "planned",
      "query": "\"model compression\" \"transformer\" \"NLP\" bits-per-byte OR perplexity",
      "verified_at": null
    },
    {
      "id": "s9",
      "name": "Ray Tune Documentation",
      "type": "framework_docs",
      "url": "https://docs.ray.io/en/latest/tune/index.html",
      "status": "planned",
      "query": "constrained optimization model size multi-objective HyperBand ASHA",
      "verified_at": null
    },
    {
      "id": "s10",
      "name": "Optuna Documentation",
      "type": "framework_docs",
      "url": "https://optuna.org",
      "status": "planned",
      "query": "multi-objective optimization model_size accuracy constraint",
      "verified_at": null
    },
    {
      "id": "s11",
      "name": "PyTorch Documentation",
      "type": "framework_docs",
      "url": "https://pytorch.org/docs/stable/",
      "status": "planned",
      "query": "state_dict size parameter count serialization bytes",
      "verified_at": null
    },
    {
      "id": "s12",
      "name": "Hugging Face Transformers Documentation",
      "type": "framework_docs",
      "url": "https://huggingface.co/docs/transformers/index",
      "status": "planned",
      "query": "tokenizer serialization file size quantization 4bit 8bit",
      "verified_at": null
    }
  ],
  "count": 12,
  "generated": "2026-03-19T07:41:07+00:00"
}

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