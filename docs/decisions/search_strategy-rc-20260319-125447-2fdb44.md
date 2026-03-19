---
created: '2026-03-19T12:57:08+00:00'
evidence:
- stage-03/search_plan.yaml
- stage-03/sources.json
- stage-03/queries.json
id: search_strategy-rc-20260319-125447-2fdb44
run_id: rc-20260319-125447-2fdb44
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
generated: '2026-03-19T12:57:08+00:00'
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
      "name": "arXiv",
      "type": "preprint_server",
      "url": "https://arxiv.org",
      "status": "planned",
      "query": "\"bits per byte\" OR \"bits-per-byte\" OR \"bits per character\" AND (\"language modeling\" OR \"compression\") AND (\"model size\" OR \"parameter budget\" OR \"compression-aware training\")",
      "verified_at": null
    },
    {
      "id": "s2",
      "name": "OpenReview",
      "type": "preprint_and_conference_submissions",
      "url": "https://openreview.net",
      "status": "planned",
      "query": "\"neural network compression\" AND (quantization OR pruning OR \"low-rank\" OR \"LoRA\") AND (\"language model\" OR transformer)",
      "verified_at": null
    },
    {
      "id": "s3",
      "name": "Google Scholar",
      "type": "academic_search_engine",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "\"constrained Bayesian optimization\" AND (\"model size\" OR \"compression\") AND (\"deep learning\" OR \"neural networks\")",
      "verified_at": null
    },
    {
      "id": "s4",
      "name": "NeurIPS / ICML / ICLR proceedings",
      "type": "conference_proceedings",
      "url": "https://papers.nips.cc",
      "status": "planned",
      "query": "\"multi-objective hyperparameter optimization\" OR \"hardware-aware\" OR \"resource-constrained\" AND (\"neural architecture search\" OR \"HPO\")",
      "verified_at": null
    },
    {
      "id": "s5",
      "name": "ACL / EMNLP / NAACL Anthology",
      "type": "conference_proceedings",
      "url": "https://aclanthology.org",
      "status": "planned",
      "query": "\"efficient\" AND (\"language model\" OR \"transformer\") AND (\"quantization\" OR \"pruning\" OR \"compression\") AND (\"model size\" OR \"on-device\")",
      "verified_at": null
    },
    {
      "id": "s6",
      "name": "Hugging Face documentation",
      "type": "documentation",
      "url": "https://huggingface.co/docs",
      "status": "planned",
      "query": "safetensors artifact size tokenizer inclusion quantization reproducibility",
      "verified_at": null
    },
    {
      "id": "s7",
      "name": "bitsandbytes documentation",
      "type": "documentation",
      "url": "https://github.com/TimDettmers/bitsandbytes",
      "status": "planned",
      "query": "quantization 4-bit 8-bit reproducibility model size measurement",
      "verified_at": null
    },
    {
      "id": "s8",
      "name": "PyTorch documentation",
      "type": "documentation",
      "url": "https://pytorch.org/docs",
      "status": "planned",
      "query": "quantization serialization model size measurement deterministic behavior",
      "verified_at": null
    },
    {
      "id": "s9",
      "name": "MLflow documentation",
      "type": "documentation",
      "url": "https://mlflow.org/docs/latest/index.html",
      "status": "planned",
      "query": "tracking GPU hours model artifacts size CI/CD integration",
      "verified_at": null
    },
    {
      "id": "s10",
      "name": "Survey papers on neural network compression",
      "type": "survey_collection",
      "url": "https://scholar.google.com",
      "status": "planned",
      "query": "\"A survey\" AND (\"neural network compression\" OR \"model compression\" OR \"efficient transformers\")",
      "verified_at": null
    }
  ],
  "count": 10,
  "generated": "2026-03-19T12:57:08+00:00"
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