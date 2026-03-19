---
created: '2026-03-19T07:49:46+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-073848-2fdb44
run_id: rc-20260319-073848-2fdb44
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

ablations:
  curriculum_without_cycles:
    description: 'Ablation that uses a single noise-to-clean transition (monotone
      ramp) but matches the marginal mixture over time to the cyclic curriculum.

      '
    expected_effect: 'If Hypothesis C is correct, this ablation should underperform
      cyclic curricula by ~0.01 val_bpb despite identical marginal exposure.

      '
    how_it_differs: 'Replace get_cycle_phase with a single ramp phase; compute mixture
      as a monotone function of global training progress but re-weight to match the
      marginal exposure of each data tier in the cyclic schedule.

      '
    linked_method: cyclic_noise_denoise_curriculum_trainer
    what_is_removed: 'Repeated alternation between noise and denoise phases; only
      one pass from noisy to clean.

      '
  curriculum_without_high_quality_code:
    description: 'Ablation that removes high_quality_code from both cyclic and baseline
      curricula to test whether observed gains are driven purely by code data.

      '
    expected_effect: 'If gains persist on web_general validation, they are not solely
      due to code data; if they vanish, code-heavy phases may be the main driver.

      '
    how_it_differs: 'Set high_quality_code_fraction to 0 in all phases and re-normalize
      mixture over remaining sources.

      '
    linked_method: cyclic_noise_denoise_curriculum_trainer
    what_is_removed: 'All batches from codeparrot_small_lm; only noisy_web and curated_web
      are used.

      '
  latent_search_without_diffusion_updates:
    description: 'Ablation that keeps latent representation and decoder but replaces
      diffusion-style updates with independent latent sampling.

      '
    expected_effect: 'Behavior should approximate random search in latent space, testing
      whether diffusion-style exploration is critical for improvements.

      '
    how_it_differs: 'propose_latent_candidates samples z from prior p(z) each iteration
      without using the denoiser; update_latent_posterior becomes a no-op.

      '
    linked_method: latent_diffusion_multifidelity_config_search
    what_is_removed: 'Noise/denoise diffusion steps and gradient-based latent refinement.

      '
  latent_search_without_multifidelity:
    description: 'Ablation of LatentDiffusionConfigSearcher that uses only single-fidelity
      (short-run) val_bpb signals for search, ignoring medium and long runs.

      '
    expected_effect: 'Increased susceptibility to early-final inversions and reduced
      final val_bpb gains over random/TPE, directly probing Hypothesis B’s multi-fidelity
      requirement.

      '
    how_it_differs: 'Fix allocate_fidelity to always assign short runs; remove fidelity
      conditioning from the denoiser; select best configs solely by short-run val_bpb.

      '
    linked_method: latent_diffusion_multifidelity_config_search
    what_is_removed: 'Medium and long fidelity evaluations and their conditioning
      in the latent denoiser/acquisition model.

      '
  surrogate_large_capacity_overfit:
    description: 'Ablation that increases surrogate capacity (~5–10MB) to test for
      overfitting and instability in gating decisions.

      '
    expected_effect: 'Potentially improved in-sample R^2 but worse generalization
      and higher miss-rate on top configs, validating the design choice of a tiny
      surrogate.

      '
    how_it_differs: 'Increase surrogate_hidden_dim and layers (e.g., 256 units, 4
      layers); keep training protocol identical.

      '
    linked_method: early_bpb_surrogate_gated_search
    what_is_removed: 'The strict <1MB capacity constraint on the surrogate model.

      '
  surrogate_without_static_features:
    description: 'Ablation of EarlyBPBSurrogateGate that uses only early val_bpb time
      series as input, removing static configuration features.

      '
    expected_effect: 'Reduced R^2 and higher MAE in final val_bpb prediction, especially
      across regimes with differing training dynamics, testing the importance of static
      features in Hypothesis A.

      '
    how_it_differs: 'Modify featurize_run to return only concatenated early val_bpb
      values; adjust input layer size accordingly, leaving model capacity unchanged.

      '
    linked_method: early_bpb_surrogate_gated_search
    what_is_removed: 'All static config features (architecture knobs, LR scale, schedule
      type, compression ratios) from surrogate inputs.

      '
baselines:
  early_bpb_direct_gating:
    description: 'Uses raw early val_bpb from quick-harness runs as a direct proxy
      for final val_bpb, with a simple threshold-based early-stop rule and no learned
      surrogate.

      '
    implementation_spec:
      algorithm_steps:
      - Initialize thresholds on early val_bpb percentiles from a warmup set.
      - For each new config, run quick-harness to a fixed early step budget.
      - Compute early val_bpb and compare to dynamic percentile threshold.
      - 

... (truncated, see full artifact)
