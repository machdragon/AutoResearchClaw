---
created: '2026-03-19T15:15:58+00:00'
evidence:
- stage-22/paper_final.md
- stage-22/paper_final_latex.md
- stage-22/references.bib
- stage-22/paper.tex
- stage-22/code//
id: export_publish-rc-20260319-145139-2fdb44
run_id: rc-20260319-145139-2fdb44
stage: 22-export_publish
tags:
- export_publish
- stage-22
- run-rc-20260
title: 'Stage 22: Export Publish'
---

# Stage 22: Export Publish

# GOLF: Boundary-Aware Compression under a 16MB Artifact Cap

## Abstract

Strict deployment budgets in parameter‑golf settings require models to satisfy hard artifact‑size caps while remaining compatible with fast quick‑harness evaluations that gate promotion. Existing compression and parameter‑efficient fine‑tuning methods typically optimize global accuracy or parameter counts, but they do not treat promotion‑boundary behavior and artifact‑size verification as coupled first‑class constraints [prottasha2025peft, bian2025survey]. This paper studies GOLF, a lightweight controller that applies boundary‑aware loss weighting and importance‑conditioned compression to jointly shape validation bits‑per‑byte (val_bpb) and serialized artifact size under a 16,000,000‑byte cap. GOLF defines a promotion score over validation examples, constructs a distance to a decision threshold, and uses this distance to re‑weight the training loss and to guide selective redundancy for boundary‑adjacent examples. In a single recorded quick‑harness run with three fully logged conditions, GOLF’s configurations achieved identical aggregated val_bpb of 0.134155 with success_rate = 1.0 across globally compressed, model‑heavy, and artifact‑retrieval variants, and per‑seed val_bpb values for one condition spanned a range of 0.002158. These empirical observations show that the current boundary‑aware mechanisms do not yet yield measurable aggregate val_bpb gains over a globally compressed baseline, but they do produce tightly clustered performance under strict artifact‑cap enforcement. The study therefore provides a negative yet informative result: under the present synthetic setup, simple global compression remains competitive with boundary‑aware allocation, highlighting the need for richer metrics and more realistic workloads when evaluating boundary‑focused controllers.

---


> **Note:** This paper was produced in degraded mode. Quality gate score (2/4.5) was below threshold. Unverified numerical results in tables have been replaced with `---` and require independent verification.


## 1 Introduction

Deployment pipelines that rely on promotion gates increasingly demand models that are not only accurate but also small, auditable, and fast to evaluate. Parameter‑golf scenarios crystallize this requirement by imposing strict artifact‑size caps—such as a 16MB serialized model budget—alongside quick‑harness checks that must complete within tight wall‑time limits before a candidate can be deployed. In such settings, practitioners cannot simply maximize predictive performance; they must jointly manage compression, verification, and promotion‑boundary behavior so that compact models remain reliable on the edge cases that determine whether an artifact is accepted or rejected. This tension between compactness and robustness motivates methods that reason explicitly about where representational bits are most valuable under operational constraints.

Existing work on parameter‑efficient fine‑tuning and model compression offers many techniques to reduce memory and computation, including adapter layers, low‑rank updates, pruning, and quantization [prottasha2025peft, bian2025survey]. Surveys of small‑model design for resource‑constrained environments show that careful architectural choices can make compact models surprisingly effective [song2025small], while iterative reasoning and energy‑based approaches provide theoretical perspectives on how representations can be reshaped under constraints [du2022iterative]. At the same time, research on parameter‑free and performative optimization points out that optimization objectives must be aligned with the downstream decision environment, especially when past deployment choices influence future data [park2024parameterfree]. Despite this rich landscape, most methods still treat artifact size as a soft target or a proxy such as parameter count, and they rarely integrate promotion‑boundary or quick‑harness constraints directly into the optimization loop. This gap becomes salient in operational workflows where artifact size and wall‑time limits are hard gates rather than preferences.

Concerns about safety and robustness under compression further sharpen the need for artifact‑aware controllers. Studies of adversarial robustness and universal perturbations document how compression can reshape decision boundaries in unanticipated ways [zhang2021survey, hingun2022reap], while analyses of refusal boundary instability in large language models show that subtle changes in artifacts or runtime configurations can alter compliance behavior on sensitive inputs [heverin2026prompt]. Work on safety compliance frameworks and automated compliance cards emphasizes that safety verification must account for the exact deployment artifact and its operational environment [hu2025safety, marino2024compliance]. In parallel, systems and benchmarking communities have proposed quick‑harness style evaluations, such as MLPerf Tiny, to enable fa

... (truncated, see full artifact)


# GOLF: Boundary-Aware Compression under a 16MB Artifact Cap

## Abstract

Strict deployment budgets in parameter‑golf settings require models to satisfy hard artifact‑size caps while remaining compatible with fast quick‑harness evaluations that gate promotion. Existing compression and parameter‑efficient fine‑tuning methods typically optimize global accuracy or parameter counts, but they do not treat promotion‑boundary behavior and artifact‑size verification as coupled first‑class constraints \cite{prottasha2025peft, bian2025survey}. This paper studies GOLF, a lightweight controller that applies boundary‑aware loss weighting and importance‑conditioned compression to jointly shape validation bits‑per‑byte (val_bpb) and serialized artifact size under a 16,000,000‑byte cap. GOLF defines a promotion score over validation examples, constructs a distance to a decision threshold, and uses this distance to re‑weight the training loss and to guide selective redundancy for boundary‑adjacent examples. In a single recorded quick‑harness run with three fully logged conditions, GOLF’s configurations achieved identical aggregated val_bpb of 0.134155 with success_rate = 1.0 across globally compressed, model‑heavy, and artifact‑retrieval variants, and per‑seed val_bpb values for one condition spanned a range of 0.002158. These empirical observations show that the current boundary‑aware mechanisms do not yet yield measurable aggregate val_bpb gains over a globally compressed baseline, but they do produce tightly clustered performance under strict artifact‑cap enforcement. The study therefore provides a negative yet informative result: under the present synthetic setup, simple global compression remains competitive with boundary‑aware allocation, highlighting the need for richer metrics and more realistic workloads when evaluating boundary‑focused controllers.

---


> **Note:** This paper was produced in degraded mode. Quality gate score (2/4.5) was below threshold. Unverified numerical results in tables have been replaced with `---` and require independent verification.


## 1 Introduction

Deployment pipelines that rely on promotion gates increasingly demand models that are not only accurate but also small, auditable, and fast to evaluate. Parameter‑golf scenarios crystallize this requirement by imposing strict artifact‑size caps—such as a 16MB serialized model budget—alongside quick‑harness checks that must complete within tight wall‑time limits before a candidate can be deployed. In such settings, practitioners cannot simply maximize predictive performance; they must jointly manage compression, verification, and promotion‑boundary behavior so that compact models remain reliable on the edge cases that determine whether an artifact is accepted or rejected. This tension between compactness and robustness motivates methods that reason explicitly about where representational bits are most valuable under operational constraints.

Existing work on parameter‑efficient fine‑tuning and model compression offers many techniques to reduce memory and computation, including adapter layers, low‑rank updates, pruning, and quantization \cite{prottasha2025peft, bian2025survey}. Surveys of small‑model design for resource‑constrained environments show that careful architectural choices can make compact models surprisingly effective \cite{song2025small}, while iterative reasoning and energy‑based approaches provide theoretical perspectives on how representations can be reshaped under constraints \cite{du2022iterative}. At the same time, research on parameter‑free and performative optimization points out that optimization objectives must be aligned with the downstream decision environment, especially when past deployment choices influence future data \cite{park2024parameterfree}. Despite this rich landscape, most methods still treat artifact size as a soft target or a proxy such as parameter count, and they rarely integrate promotion‑boundary or quick‑harness constraints directly into the optimization loop. This gap becomes salient in operational workflows where artifact size and wall‑time limits are hard gates rather than preferences.

Concerns about safety and robustness under compression further sharpen the need for artifact‑aware controllers. Studies of adversarial robustness and universal perturbations document how compression can reshape decision boundaries in unanticipated ways \cite{zhang2021survey, hingun2022reap}, while analyses of refusal boundary instability in large language models show that subtle changes in artifacts or runtime configurations can alter compliance behavior on sensitive inputs \cite{heverin2026prompt}. Work on safety compliance frameworks and automated compliance cards emphasizes that safety verification must account for the exact deployment artifact and its operational environment \cite{hu2025safety, marino2024compliance}. In parallel, systems and benchmarking communities have proposed quick‑harness style evalua

... (truncated, see full artifact)


@article{heverin2026prompt,
  title = {Prompt Injection Evaluations: Refusal Boundary Instability and Artifact-Dependent Compliance in GPT-4-Series Models},
  author = {Thomas Heverin},
  year = {2026},
  journal = {cs.CR},
  eprint = {2601.17911},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2601.17911v1},
}

@article{bian2025survey,
  title = {A Survey on Parameter-Efficient Fine-Tuning for Foundation Models in Federated Learning},
  author = {Jieming Bian and Yuanzhe Peng and Lei Wang and Yin Huang and Jie Xu},
  year = {2025},
  journal = {cs.LG},
  eprint = {2504.21099},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2504.21099v1},
}

@article{song2025small,
  title = {Is Small Language Model the Silver Bullet to Low-Resource Languages Machine Translation?},
  author = {Yewei Song and Lujun Li and Cedric Lothritz and Saad Ezzini and Lama Sleem and Niccolo Gentile and Radu State and Tegawendé F. Bissyandé and Jacques Klein},
  year = {2025},
  journal = {cs.CL},
  eprint = {2503.24102},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2503.24102v3},
}

@article{hu2025safety,
  title = {Safety Compliance: Rethinking LLM Safety Reasoning through the Lens of Compliance},
  author = {Wenbin Hu and Huihao Jing and Haochen Shi and Haoran Li and Yangqiu Song},
  year = {2025},
  journal = {cs.CL},
  eprint = {2509.22250},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2509.22250v1},
}

@article{chen2025beyond,
  title = {Beyond Yes or No: Predictive Compliance Monitoring Approaches for Quantifying the Magnitude of Compliance Violations},
  author = {Qian Chen and Stefanie Rinderle-Ma and Lijie Wen},
  year = {2025},
  journal = {cs.LG},
  eprint = {2502.01141},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2502.01141v1},
}

@article{prottasha2025peft,
  title = {PEFT A2Z: Parameter-Efficient Fine-Tuning Survey for Large Language and Vision Models},
  author = {Nusrat Jahan Prottasha and Upama Roy Chowdhury and Shetu Mohanto and Tasfia Nuzhat and Abdullah As Sami and Md Shamol Ali and Md Shohanur Islam Sobuj and Hafijur Raman and Md Kowsher and Ozlem Ozmen Garibay},
  year = {2025},
  journal = {cs.CL},
  eprint = {2504.14117},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2504.14117v1},
}

@article{park2024parameterfree,
  title = {Parameter-Free Algorithms for Performative Regret Minimization under Decision-Dependent Distributions},
  author = {Sungwoo Park and Junyeop Kwon and Byeongnoh Kim and Suhyun Chae and Jeeyong Lee and Dabeen Lee},
  year = {2024},
  journal = {cs.LG},
  eprint = {2402.15188},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2402.15188v1},
}

@article{marino2024compliance,
  title = {Compliance Cards: Automated EU AI Act Compliance Analyses amidst a Complex AI Supply Chain},
  author = {Bill Marino and Yaqub Chaudhary and Yulu Pi and Rui-Jie Yew and Preslav Aleksandrov and Carwyn Rahman and William F. Shen and Isaac Robinson and Nicholas D. Lane},
  year = {2024},
  journal = {cs.AI},
  eprint = {2406.14758},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2406.14758v2},
}

@article{hou2024adaptive,
  title = {Adaptive Compliance Policy: Learning Approximate Compliance for Diffusion Guided Control},
  author = {Yifan Hou and Zeyi Liu and Cheng Chi and Eric Cousineau and Naveen Kuppuswamy and Siyuan Feng and Benjamin Burchfiel and Shuran Song},
  year = {2024},
  journal = {cs.RO},
  eprint = {2410.09309},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2410.09309v2},
}

@article{angermeir2024automated,
  title = {Towards Automated Continuous Security Compliance},
  author = {Florian Angermeir and Jannik Fischbach and Fabiola Moyón and Daniel Mendez},
  year = {2024},
  journal = {cs.SE},
  eprint = {2407.21494},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2407.21494v2},
}

@article{canesche2023preparing,
  title = {Preparing Reproducible Scientific Artifacts using Docker},
  author = {Michael Canesche and Roland Leissa and Fernando Magno Quintão Pereira},
  year = {2023},
  journal = {cs.DL},
  eprint = {2308.14122},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2308.14122v1},
}

@article{ratiu2023defining,
  title = {Defining and executing temporal constraints for evaluating engineering artifact compliance},
  author = {Cosmina-Cristina Ratiu and Christoph Mayr-Dorn and Alexander Egyed},
  year = {2023},
  journal = {cs.SE},
  eprint = {2312.13012},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2312.13012v1},
}

@article{du2022iterative,
  title = {Learning Iterative Reasoning through Energy Minimization},
  author = {Yilun Du and Shuang Li and Joshua B. Tenenbaum and Igor Mordatch},
  year = {2022},
  journal = {cs.LG},
  eprint = {2206.15448},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2206.15448v1},
}

@article{hingun2022reap,
  title = {REAP: A Large-Scale Realistic Adversarial Patch Benchmark},
  author = {Nabeel Hingun and Chawin 

... (truncated, see full artifact)


% WARNING: Compilation failed. Errors:
% ! LaTeX Error: Unicode character ∈ (U+2208)
% !  ==> Fatal error occurred, no output PDF file produced!
% Style file: https://media.neurips.cc/Conferences/NeurIPS2025/Styles.zip
\documentclass{article}
\usepackage[preprint]{neurips_2025}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{nicefrac}
\usepackage{microtype}
\usepackage{graphicx}
\usepackage{natbib}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{adjustbox}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}

\title{GOLF: Boundary-Aware Compression under a 16MB Artifact Cap}

\author{Anonymous}

\begin{document}
\maketitle

\begin{abstract}
Strict deployment budgets in parameter‑golf settings require models to satisfy hard artifact‑size caps while remaining compatible with fast quick‑harness evaluations that gate promotion. Existing compression and parameter‑efficient fine‑tuning methods typically optimize global accuracy or parameter counts, but they do not treat promotion‑boundary behavior and artifact‑size verification as coupled first‑class constraints \cite{prottasha2025peft, bian2025survey}. This paper studies GOLF, a lightweight controller that applies boundary‑aware loss weighting and importance‑conditioned compression to jointly shape validation bits‑per‑byte (val\_bpb) and serialized artifact size under a 16,000,000‑byte cap. GOLF defines a promotion score over validation examples, constructs a distance to a decision threshold, and uses this distance to re‑weight the training loss and to guide selective redundancy for boundary‑adjacent examples. In a single recorded quick‑harness run with three fully logged conditions, GOLF's configurations achieved identical aggregated val\_bpb of 0.1342 with success\_rate = 1.0 across globally compressed, model‑heavy, and artifact‑retrieval variants, and per‑seed val\_bpb values for one condition spanned a range of 0.0022. These empirical observations show that the current boundary‑aware mechanisms do not yet yield measurable aggregate val\_bpb gains over a globally compressed baseline, but they do produce tightly clustered performance under strict artifact‑cap enforcement. The study therefore provides a negative yet informative result: under the present synthetic setup, simple global compression remains competitive with boundary‑aware allocation, highlighting the need for richer metrics and more realistic workloads when evaluating boundary‑focused controllers.

\begin{quote}
\textbf{Note:} This paper was produced in degraded mode. Quality gate score (2/4.5) was below threshold. Unverified numerical results in tables have been replaced with \texttt{---} and require independent verification.
\end{quote}
\end{abstract}

\section{Introduction}

\label{sec:introduction}

Deployment pipelines that rely on promotion gates increasingly demand models that are not only accurate but also small, auditable, and fast to evaluate. Parameter‑golf scenarios crystallize this requirement by imposing strict artifact‑size caps---such as a 16MB serialized model budget---alongside quick‑harness checks that must complete within tight wall‑time limits before a candidate can be deployed. In such settings, practitioners cannot simply maximize predictive performance; they must jointly manage compression, verification, and promotion‑boundary behavior so that compact models remain reliable on the edge cases that determine whether an artifact is accepted or rejected. This tension between compactness and robustness motivates methods that reason explicitly about where representational bits are most valuable under operational constraints.

Existing work on parameter‑efficient fine‑tuning and model compression offers many techniques to reduce memory and computation, including adapter layers, low‑rank updates, pruning, and quantization \cite{prottasha2025peft, bian2025survey}. Surveys of small‑model design for resource‑constrained environments show that careful architectural choices can make compact models surprisingly effective \cite{song2025small}, while iterative reasoning and energy‑based approaches provide theoretical perspectives on how representations can be reshaped under constraints \cite{du2022iterative}. At the same time, research on parameter‑free and performative optimization points out that optimization objectives must be aligned with the downstream decision environment, especially when past deployment choices influence future data \cite{park2024parameterfree}. Despite this rich landscape, most methods still treat artifact size as a soft target or a proxy such as parameter count, and they rarely integrate promotion‑boundary or quick‑harness constraints directly into the optimization loop. This gap becomes salient in operational workflows where artifact size and wall‑time limits are hard gates rather than preferences.

Concerns about safety and robustness under compression further sha

... (truncated, see full artifact)


Directory with 3 files: README.md, main.py, requirements.txt