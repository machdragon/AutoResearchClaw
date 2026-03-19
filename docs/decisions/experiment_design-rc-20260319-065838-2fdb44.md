---
created: '2026-03-19T07:09:52+00:00'
evidence:
- stage-09/exp_plan.yaml
id: experiment_design-rc-20260319-065838-2fdb44
run_id: rc-20260319-065838-2fdb44
stage: 09-experiment_design
tags:
- experiment_design
- stage-09
- run-rc-20260
title: 'Stage 09: Experiment Design'
---

# Stage 09: Experiment Design

ablations:
- expected_effect: 'Tests whether targeted micro-dosed data is necessary for local
    refusal robustness gains; expectation is a noticeable drop in high-risk neighborhood
    RBE/flip-rate improvements at similar val_bpb.

    '
  how_it_differs: 'In MicrodoseDomainWeightedSafetyGolf, set microdose_fraction =
    0 and exclude adversarial_safety_microdose from D_mix; all other hyperparameters
    and domain weights remain unchanged.

    '
  name: no_microdose_data_ablation
  related_hypotheses:
  - HypothesisA
  what_is_removed: 'Remove the adversarial safety micro-dose data from training while
    keeping the domain-weighted loss and parameter-golf procedure intact.

    '
- expected_effect: 'Tests whether domain weighting is crucial for both micro-dose
    safety gains (Hypothesis A) and decoupling val_bpb from harmful capability (Hypothesis
    D); expect reduced safety benefits and stronger positive correlation between val_bpb
    and harmful capability.

    '
  how_it_differs: 'Replace domain-weighted loss in MicrodoseDomainWeightedSafetyGolf
    and DomainWeightedValbpbMitigator with plain cross-entropy over all tokens.

    '
  name: no_domain_weighting_ablation
  related_hypotheses:
  - HypothesisA
  - HypothesisD
  what_is_removed: 'Remove domain-weighted loss and loss floors; revert to standard
    global val_bpb objective while keeping micro-dosed data and parameter-golf search.

    '
- expected_effect: 'Tests whether multi-profile search is necessary for Pareto improvements;
    expect that some profiles cannot be simultaneously optimized, leading to dominated
    points on profile-specific frontiers.

    '
  how_it_differs: 'In MultiCityProfileSpecificGolf, disable per-profile search and
    instead optimize a single shared configuration on a mixed-profile objective, then
    evaluate it on each profile separately.

    '
  name: single_profile_only_ablation
  related_hypotheses:
  - HypothesisB
  what_is_removed: 'Remove multi-profile optimization; enforce a single global configuration
    for all profiles while still using domain-weighted objectives.

    '
- expected_effect: 'Tests Hypothesis C’s claim that co-evolution is required for predictive
    harness metrics; expect lower correlation with large suite L and more overfitting
    to the static harness.

    '
  how_it_differs: 'In CoevolvingAdversarialQuickHarnessGate, disable generate_adversarial_prompts
    and update_harness; replace H_t with a static harness identical to FixedHarnessNonAdversarialGate.

    '
  name: fixed_non_adversarial_harness_ablation
  related_hypotheses:
  - HypothesisC
  what_is_removed: 'Remove the co-evolution and adversarial generation in the quick-harness
    gate; use a fixed non-adversarial harness instead.

    '
- expected_effect: 'Tests how much the size cap shapes trade-offs; expect lower val_bpb
    and higher safety performance when unconstrained, but loss of relevance to deployment
    constraints and possible changes in val_bpb–harm correlation.

    '
  how_it_differs: 'In all proposed methods, skip artifact size checks and compression
    constraints during selection; still record model sizes but do not enforce ≤16MB
    gating.

    '
  name: no_16mb_constraint_ablation
  related_hypotheses:
  - HypothesisA
  - HypothesisB
  - HypothesisD
  what_is_removed: 'Remove the hard 16MB artifact cap from parameter-golf selection
    and compression; allow arbitrarily large models.

    '
baselines:
- LSTM LM
- DANN
- description: 'Strong macro-safety fine-tuning baseline that uses 5–10% generic safety
    data (Safe-RLHF or similar) with a standard global val_bpb objective and no domain
    weighting. Represents widely adopted safety-FT practice.

    '
  hypotheses_compared:
  - HypothesisA
  - HypothesisD
  implementation_spec:
    algorithm_steps:
    - Initialize base transformer LM (e.g., 350M–1B params) with standard tokenizer.
    - Load generic safety dataset (safe_rlhf) and benign corpus (wikitext-103, pile_subset_1B).
    - Construct training batches mixing base data and generic safety data at 5–10%
      proportion.
    - Optimize standard cross-entropy loss over all tokens to minimize global val_bpb.
    - Periodically evaluate val_bpb on validation splits and safety metrics on fixed
      harness.
    - Apply light post-training quantization (e.g., 8-bit weights/activations) to
      meet 16MB where possible.
    - Export final model checkpoint and tokenizer ensuring artifact ≤16MB or record
      failure.
    class_name: MacroSafetyValbpbFinetune
    differentiator: 'Uses only generic macro-safety data and a standard global val_bpb
      objective without domain weighting or micro-dosed safety data.

      '
    key_hyperparameters:
      batch_size: 64
      grad_clip_norm: 1.0
      learning_rate: 2e-5
      max_steps: 5000
      quantization_bits: 8
      safety_data_fraction: 0.1
      weight_decay: 0.01
    key_methods:
    - __init__
    - build_model
    - forward

... (truncated, see full artifact)
