---
created: '2026-03-19T06:55:21+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-065325-2fdb44
run_id: rc-20260319-065325-2fdb44
stage: 03-search_strategy
tags:
- search_strategy
- stage-03
- run-rc-20260
title: 'Stage 03: Search Strategy'
---

# Stage 03: Search Strategy

deduplication:
  fuzzy_threshold: 0.9
  method: title_doi_hash
filters:
  language:
  - en
  min_year: 2020
  peer_review_preferred: true
generated: '2026-03-19T06:55:21+00:00'
search_strategies:
- max_results_per_query: 60
  name: keyword_core
  queries:
  - Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact
    compliance on promotion.
  - Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact
    compliance on promotion. benchmark
  - Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact
    compliance on promotion. survey
  sources:
  - arxiv
  - semantic_scholar
  - openreview
- depth: 1
  name: backward_forward_citation
  queries:
  - Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact
    compliance on promotion. seminal
  - Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact
    compliance on promotion. state of the art
  sources:
  - semantic_scholar
  - google_scholar
topic: Parameter Golf val_bpb minimization under quick-harness gate, with 16MB artifact
  compliance on promotion.


{
  "sources": [
    {
      "id": "s1",
      "name": "Google Scholar",
      "type": "academic_search_engine",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "mixed precision bit-width \"model size\" \"language model\" quantization pruning \"perplexity\"",
      "verified_at": null
    },
    {
      "id": "s2",
      "name": "arXiv",
      "type": "preprint_repository",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"language model\" quantization OR pruning \"bits per byte\" OR \"bits per token\" \"model size\"",
      "verified_at": null
    },
    {
      "id": "s3",
      "name": "Semantic Scholar",
      "type": "academic_search_engine",
      "url": "https://www.semanticscholar.org",
      "status": "planned",
      "query": "\"post-training quantization\" transformer \"per-layer\" \"bit allocation\"",
      "verified_at": null
    },
    {
      "id": "s4",
      "name": "MLSys / NeurIPS / ICML proceedings",
      "type": "conference_proceedings_portal",
      "url": "https://proceedings.mlsys.org",
      "status": "planned",
      "query": "\"constrained Bayesian optimization\" \"model compression\" OR quantization",
      "verified_at": null
    },
    {
      "id": "s5",
      "name": "TinyML Foundation resources",
      "type": "community_and_conference_resources",
      "url": "https://tinyml.org",
      "status": "planned",
      "query": "TinyML \"model size\" constraint quantization pruning deployment",
      "verified_at": null
    },
    {
      "id": "s6",
      "name": "TensorFlow Lite documentation",
      "type": "framework_docs",
      "url": "https://www.tensorflow.org/lite",
      "status": "planned",
      "query": "model size file size quantization pruning storage footprint",
      "verified_at": null
    },
    {
      "id": "s7",
      "name": "ONNX Runtime documentation",
      "type": "framework_docs",
      "url": "https://onnxruntime.ai/docs/",
      "status": "planned",
      "query": "quantization model size optimization packaging",
      "verified_at": null
    },
    {
      "id": "s8",
      "name": "GGUF / llama.cpp format docs",
      "type": "format_specification",
      "url": "https://github.com/ggerganov/llama.cpp",
      "status": "planned",
      "query": "GGUF format model file size quantization sparsity",
      "verified_at": null
    },
    {
      "id": "s9",
      "name": "Hugging Face Transformers & Optimum docs",
      "type": "framework_docs",
      "url": "https://huggingface.co/docs",
      "status": "planned",
      "query": "quantization pruning \"model size\" int8 int4 GPTQ AWQ SmoothQuant",
      "verified_at": null
    },
    {
      "id": "s10",
      "name": "Optuna documentation",
      "type": "optimization_framework_docs",
      "url": "https://optuna.org",
      "status": "planned",
      "query": "constrained optimization \"pruner\" \"multi-objective\" model size",
      "verified_at": null
    },
    {
      "id": "s11",
      "name": "BoTorch documentation",
      "type": "optimization_framework_docs",
      "url": "https://botorch.org",
      "status": "planned",
      "query": "constrained Bayesian optimization limited evaluations",
      "verified_at": null
    },
    {
      "id": "s12",
      "name": "Hyperband / BOHB original papers",
      "type": "paper_collection",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "Hyperband BOHB \"multi-fidelity\" \"early stopping\" \"hyperparameter optimization\"",
      "verified_at": null
    },
    {
      "id": "s13",
      "name": "Representative LM quantization papers (e.g., GPTQ, AWQ, SmoothQuant)",
      "type": "paper_collection",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "GPTQ AWQ SmoothQuant \"language model\" quantization perplexity \"model size\"",
      "verified_at": null
    },
    {
      "id": "s14",
      "name": "NeurIPS / ICML model compression challenges",
      "type": "competition_pages",
      "url": "https://neurips.cc/Conferences",
      "status": "planned",
      "query": "\"model compression\" challenge \"model size\" rules",
      "verified_at": null
    },
    {
      "id": "s15",
      "name": "Blogs / engineering posts on LM compression and deployment",
      "type": "technical_blogs",
      "url": "https://www.google.com/search",
      "status": "planned",
      "query": "\"LLM quantization\" \"4-bit\" \"deployment\" \"model size\"",
      "verified_at": null
    }
  ],
  "count": 15,
  "generated": "2026-03-19T06:55:21+00:00"
}

{
  "queries": [
    "Parameter Golf val bpb minimization under",
    "Parameter Golf val bpb minimization under benchmark",
    "Parameter Golf val bpb minimization under survey",
    "Parameter Golf val bpb minimization under seminal",
    "Parameter Golf val bpb minimization under state of the art"
  ],
  "year_min": 2020
}