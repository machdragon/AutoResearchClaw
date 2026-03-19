---
created: '2026-03-19T13:19:05+00:00'
evidence:
- stage-11/schedule.json
id: resource_planning-rc-20260319-125447-2fdb44
run_id: rc-20260319-125447-2fdb44
stage: 11-resource_planning
tags:
- resource_planning
- stage-11
- run-rc-20260
title: 'Stage 11: Resource Planning'
---

# Stage 11: Resource Planning

{
  "tasks": [
    {
      "id": "setup_env_and_data",
      "name": "Environment setup, dataset download, caching, and common dataloader harness (CIFAR-10/100, Tiny-ImageNet, wikitext103_quick_harness)",
      "depends_on": [],
      "gpu_count": 0,
      "estimated_minutes": 240,
      "priority": 10
    },
    {
      "id": "shared_attack_and_audit_sims",
      "name": "Implement shared adversarial attack suite and audit_sim/human_review simulators",
      "depends_on": [
        "setup_env_and_data"
      ],
      "gpu_count": 0,
      "estimated_minutes": 360,
      "priority": 9
    },
    {
      "id": "baseline_global_valbpb_impl",
      "name": "Implement GlobalValBPBCompressor baseline (model, search space, quick-harness gate)",
      "depends_on": [
        "setup_env_and_data"
      ],
      "gpu_count": 1,
      "estimated_minutes": 360,
      "priority": 9
    },
    {
      "id": "baseline_model_heavy_impl",
      "name": "Implement ModelHeavyLogLightGate baseline (RAG-style compliance gate)",
      "depends_on": [
        "setup_env_and_data"
      ],
      "gpu_count": 1,
      "estimated_minutes": 360,
      "priority": 8
    },
    {
      "id": "baseline_artifact_maximal_impl",
      "name": "Implement ArtifactMaximalRAG baseline (artifact_maximal_retrieval_llm)",
      "depends_on": [
        "setup_env_and_data"
      ],
      "gpu_count": 1,
      "estimated_minutes": 360,
      "priority": 8
    },
    {
      "id": "proposed_boundary_weighted_controller_impl",
      "name": "Implement BoundaryWeightedAutoRC (boundary_weighted_robustness_controller)",
      "depends_on": [
        "shared_attack_and_audit_sims",
        "baseline_global_valbpb_impl"
      ],
      "gpu_count": 1,
      "estimated_minutes": 480,
      "priority": 9
    },
    {
      "id": "proposed_trace_heavy_allocator_impl",
      "name": "Implement TraceHeavyBoundaryAllocator (trace_heavy_boundary_weighted_evidence_allocator)",
      "depends_on": [
        "shared_attack_and_audit_sims"
      ],
      "gpu_count": 1,
      "estimated_minutes": 480,
      "priority": 8
    },
    {
      "id": "proposed_adversarial_core_selector_impl",
      "name": "Implement AdversarialCoreArtifactSelector (adversarially_pruned_core_artifact_selector)",
      "depends_on": [
        "shared_attack_and_audit_sims",
        "baseline_artifact_maximal_impl"
      ],
      "gpu_count": 1,
      "estimated_minutes": 480,
      "priority": 8
    },
    {
      "id": "baseline_global_valbpb_runs",
      "name": "Run globally_compressed_valbpb_minimizer across seeds and regimes",
      "depends_on": [
        "baseline_global_valbpb_impl",
        "shared_attack_and_audit_sims"
      ],
      "gpu_count": 8,
      "estimated_minutes": 112500,
      "priority": 10
    },
    {
      "id": "baseline_model_heavy_runs",
      "name": "Run model_heavy_log_light_compliance_gate across seeds and regimes",
      "depends_on": [
        "baseline_model_heavy_impl",
        "shared_attack_and_audit_sims"
      ],
      "gpu_count": 8,
      "estimated_minutes": 112500,
      "priority": 9
    },
    {
      "id": "baseline_artifact_maximal_runs",
      "name": "Run artifact_maximal_retrieval_llm across seeds and regimes",
      "depends_on": [
        "baseline_artifact_maximal_impl",
        "shared_attack_and_audit_sims"
      ],
      "gpu_count": 8,
      "estimated_minutes": 112500,
      "priority": 9
    },
    {
      "id": "proposed_boundary_weighted_controller_runs",
      "name": "Run boundary_weighted_robustness_controller across seeds and regimes",
      "depends_on": [
        "proposed_boundary_weighted_controller_impl"
      ],
      "gpu_count": 8,
      "estimated_minutes": 112500,
      "priority": 10
    },
    {
      "id": "proposed_trace_heavy_allocator_runs",
      "name": "Run trace_heavy_boundary_weighted_evidence_allocator across seeds and regimes",
      "depends_on": [
        "proposed_trace_heavy_allocator_impl"
      ],
      "gpu_count": 8,
      "estimated_minutes": 112500,
      "priority": 9
    },
    {
      "id": "proposed_adversarial_core_selector_runs",
      "name": "Run adversarially_pruned_core_artifact_selector across seeds and regimes",
      "depends_on": [
        "proposed_adversarial_core_selector_impl"
      ],
      "gpu_count": 8,
      "estimated_minutes": 112500,
      "priority": 9
    },
    {
      "id": "ablation_no_boundary_conditioning_impl",
      "name": "Implement no_boundary_conditioning_compression_ablation variant",
      "depends_on": [
        "proposed_boundary_weighted_controller_impl"
      ],
      "gpu_count": 1,
      "estimated_minutes": 240,
      "priority": 7
    },
    {
      "id": "ablation_uniform_trace_density_impl",
      "name": "Implement uniform_trace_density_ablation variant",
      "depends_on": [
        "proposed_trace_heavy_allocator_impl"
      ],
      "gpu_count": 1,
      "estimated_minutes": 240,
      "priority": 7
    },
    {
      "id": "ablation

... (truncated, see full artifact)
