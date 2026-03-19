---
created: '2026-03-19T08:02:13+00:00'
evidence:
- stage-11/schedule.json
id: resource_planning-rc-20260319-073848-2fdb44
run_id: rc-20260319-073848-2fdb44
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
      "id": "HYP_A_00_warmup_full_runs",
      "name": "Hypothesis A warmup: 80 full tiny-model runs for surrogate & direct gate calibration",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 4800,
      "priority": "high"
    },
    {
      "id": "HYP_A_01_early_bpb_direct_gating",
      "name": "Hypothesis A: EarlyBPBDirectGate baseline (320 gated runs, 400 configs)",
      "depends_on": [
        "HYP_A_00_warmup_full_runs"
      ],
      "gpu_count": 4,
      "estimated_minutes": 7200,
      "priority": "high"
    },
    {
      "id": "HYP_A_02_surrogate_main",
      "name": "Hypothesis A: EarlyBPBSurrogateGate main experiment (320 gated runs, 400 configs)",
      "depends_on": [
        "HYP_A_00_warmup_full_runs"
      ],
      "gpu_count": 4,
      "estimated_minutes": 7200,
      "priority": "high"
    },
    {
      "id": "HYP_A_10_ablation_surrogate_large_capacity_overfit",
      "name": "Ablation: large-capacity surrogate overfit test",
      "depends_on": [
        "HYP_A_02_surrogate_main"
      ],
      "gpu_count": 4,
      "estimated_minutes": 2400,
      "priority": "medium"
    },
    {
      "id": "HYP_A_11_ablation_surrogate_without_static_features",
      "name": "Ablation: surrogate without static configuration features",
      "depends_on": [
        "HYP_A_02_surrogate_main"
      ],
      "gpu_count": 4,
      "estimated_minutes": 2400,
      "priority": "medium"
    },
    {
      "id": "HYP_B_00_latent_diffusion_multifidelity_search",
      "name": "Hypothesis B: LatentDiffusionConfigSearcher multi-fidelity search (200 configs)",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 7200,
      "priority": "high"
    },
    {
      "id": "HYP_B_01_multifidelity_random_config_search",
      "name": "Hypothesis B baseline: MultiFidelityRandomSearcher (200 configs)",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 7200,
      "priority": "high"
    },
    {
      "id": "HYP_B_02_explicit_space_tpe_bpb_optimizer",
      "name": "Hypothesis B baseline: ExplicitSpaceTPEOptimizer (TPE, 200 configs)",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 7200,
      "priority": "high"
    },
    {
      "id": "HYP_B_10_ablation_latent_search_without_diffusion_updates",
      "name": "Ablation: latent search without diffusion-style updates",
      "depends_on": [
        "HYP_B_00_latent_diffusion_multifidelity_search"
      ],
      "gpu_count": 4,
      "estimated_minutes": 3600,
      "priority": "medium"
    },
    {
      "id": "HYP_B_11_ablation_latent_search_without_multifidelity",
      "name": "Ablation: latent search without multi-fidelity signals (short-only)",
      "depends_on": [
        "HYP_B_00_latent_diffusion_multifidelity_search"
      ],
      "gpu_count": 4,
      "estimated_minutes": 3600,
      "priority": "medium"
    },
    {
      "id": "HYP_C_00_static_data_mixture_curriculum",
      "name": "Hypothesis C baseline: StaticMixtureCurriculumTrainer (3 curricula x 2 domains x 2 LR schedules, static condition)",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 6000,
      "priority": "high"
    },
    {
      "id": "HYP_C_01_monotone_quality_ramp_curriculum",
      "name": "Hypothesis C baseline: MonotoneQualityRampTrainer (3 curricula x 2 domains x 2 LR schedules, monotone condition)",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 6000,
      "priority": "high"
    },
    {
      "id": "HYP_C_02_cyclic_noise_denoise_curriculum",
      "name": "Hypothesis C main: CyclicNoiseDenoiseTrainer (3 curricula x 2 domains x 2 LR schedules, cyclic condition)",
      "depends_on": [],
      "gpu_count": 4,
      "estimated_minutes": 6000,
      "priority": "high"
    },
    {
      "id": "HYP_C_10_ablation_curriculum_without_cycles",
      "name": "Ablation: curriculum without cycles (monotone ramp matched to cyclic marginal exposure)",
      "depends_on": [
        "HYP_C_02_cyclic_noise_denoise_curriculum"
      ],
      "gpu_count": 4,
      "estimated_minutes": 3000,
      "priority": "medium"
    },
    {
      "id": "HYP_C_11_ablation_curriculum_without_high_quality_code",
      "name": "Ablation: cyclic & baselines without high-quality code data",
      "depends_on": [
        "HYP_C_00_static_data_mixture_curriculum",
        "HYP_C_01_monotone_quality_ramp_curriculum",
        "HYP_C_02_cyclic_noise_denoise_curriculum"
      ],
      "gpu_count": 4,
      "estimated_minutes": 3000,
      "priority": "medium"
    },
    {
      "id": "ANALYSIS_00_metrics_and_statistics",
      "name": "Global statistical analysis and metric computation across all hypotheses",
      "depends_on": [
        "HYP_A_01_early_bpb_direct_gating",
        "HYP_A_02_surrogate_main",
        "HYP_B_00_latent_diffusion_multifidelity_search",
        "HYP_B_01_multifidelity_random_config_search",
        "HYP_B_02_explicit_space_tpe_bpb_opti

... (truncated, see full artifact)
