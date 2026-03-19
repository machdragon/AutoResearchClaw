---
created: '2026-03-19T12:58:09+00:00'
evidence:
- stage-04/candidates.jsonl
- stage-04/references.bib
- stage-04/search_meta.json
id: literature_collect-rc-20260319-125447-2fdb44
run_id: rc-20260319-125447-2fdb44
stage: 04-literature_collect
tags:
- literature_collect
- stage-04
- run-rc-20260
title: 'Stage 04: Literature Collect'
---

# Stage 04: Literature Collect

{"paper_id": "arxiv-2602.11674", "title": "Benchmark Health Index: A Systematic Framework for Benchmarking the Benchmarks of LLMs", "authors": [{"name": "Longyuan Zhu", "affiliation": ""}, {"name": "Hairan Hua", "affiliation": ""}, {"name": "Linlin Miao", "affiliation": ""}, {"name": "Bing Zhao", "affiliation": ""}], "year": 2026, "abstract": "Large Language Models (LLMs) are advancing rapidly, yet the benchmarks used to measure this progress are becoming increasingly unreliable. Score inflation and selective reporting have eroded the authority of standard benchmarks, leaving the community uncertain about which evaluation results remain trustworthy. We introduce the Benchmark Health Index (BHI), a pure data-driven framework for auditing evaluation sets along three orthogonal and complementary axes: (1) Capability Discrimination, measuring how sharply a benchmark separates model performance beyond noise; (2) Anti-Saturation, estimating remaining headroom before ceiling effects erode resolution and thus the benchmark's expected longevity; and (3) Impact, quantifying influence across academic and industrial ecosystems via adoption breadth and practice-shaping power. By distilling 106 validated benchmarks from the technical reports of 91 representative models in 2025, we systematically characterize the evaluation landscape. BHI is the first framework to quantify benchmark health at a macro level, providing a principled basis for benchmark selection and enabling dynamic lifecycle management for next-generation evaluation protocols.", "venue": "cs.AI", "citation_count": 0, "doi": "", "arxiv_id": "2602.11674", "url": "https://arxiv.org/abs/2602.11674v1", "source": "arxiv", "cite_key": "zhu2026benchmark", "collected_at": "2026-03-19T12:58:09+00:00"}
{"paper_id": "arxiv-2603.00913", "title": "Minimalist Compliance Control", "authors": [{"name": "Haochen Shi", "affiliation": ""}, {"name": "Songbo Hu", "affiliation": ""}, {"name": "Yifan Hou", "affiliation": ""}, {"name": "Weizhuo Wang", "affiliation": ""}, {"name": "Karen Liu", "affiliation": ""}, {"name": "Shuran Song", "affiliation": ""}], "year": 2026, "abstract": "Compliance control is essential for safe physical interaction, yet its adoption is limited by hardware requirements such as force torque sensors. While recent reinforcement learning approaches aim to bypass these constraints, they often suffer from sim-to-real gaps, lack safety guarantees, and add system complexity. We propose Minimalist Compliance Control, which enables compliant behavior using only motor current or voltage signals readily available in modern servos and quasi-direct-drive motors, without force sensors, current control, or learning. External wrenches are estimated from actuator signals and Jacobians and incorporated into a task-space admittance controller, preserving sufficient force measurement accuracy for stable and responsive compliance control. Our method is embodiment-agnostic and plug-and-play with diverse high-level planners. We validate our approach on a robot arm, a dexterous hand, and two humanoid robots across multiple contact-rich tasks, using vision-language models, imitation learning, and model-based planning. The results demonstrate robust, safe, and compliant interaction across embodiments and planning paradigms.", "venue": "cs.RO", "citation_count": 0, "doi": "", "arxiv_id": "2603.00913", "url": "https://arxiv.org/abs/2603.00913v1", "source": "arxiv", "cite_key": "shi2026minimalist", "collected_at": "2026-03-19T12:58:09+00:00"}
{"paper_id": "arxiv-2601.17911", "title": "Prompt Injection Evaluations: Refusal Boundary Instability and Artifact-Dependent Compliance in GPT-4-Series Models", "authors": [{"name": "Thomas Heverin", "affiliation": ""}], "year": 2026, "abstract": "Prompt injection evaluations typically treat refusal as a stable, binary indicator of safety. This study challenges that paradigm by modeling refusal as a local decision boundary and examining its stability under structured perturbations. We evaluated two models, GPT-4.1 and GPT-4o, using 3,274 perturbation runs derived from refusal-inducing prompt injection attempts. Each base prompt was subjected to 25 perturbations across five structured families, with outcomes manually coded as Refusal, Partial Compliance, or Full Compliance. Using chi-square tests, logistic regression, mixed-effects modeling, and a novel Refusal Boundary Entropy (RBE) metric, we demonstrate that while both models refuse >94% of attempts, refusal instability is persistent and non-uniform. Approximately one-third of initial refusal-inducing prompts exhibited at least one \"refusal escape,\" a transition to compliance under perturbation. We find that artifact type is a stronger predictor of refusal failure than perturbation style. Textual artifacts, such as ransomware notes, exhibited significantly higher instability, with flip rates exceeding 20%. Conversely, executable malware artifacts showed zero refusal escapes in both models. W

... (truncated, see full artifact)


@article{zhu2026benchmark,
  title = {Benchmark Health Index: A Systematic Framework for Benchmarking the Benchmarks of LLMs},
  author = {Longyuan Zhu and Hairan Hua and Linlin Miao and Bing Zhao},
  year = {2026},
  journal = {cs.AI},
  eprint = {2602.11674},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2602.11674v1},
}

@article{shi2026minimalist,
  title = {Minimalist Compliance Control},
  author = {Haochen Shi and Songbo Hu and Yifan Hou and Weizhuo Wang and Karen Liu and Shuran Song},
  year = {2026},
  journal = {cs.RO},
  eprint = {2603.00913},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2603.00913v1},
}

@article{heverin2026prompt,
  title = {Prompt Injection Evaluations: Refusal Boundary Instability and Artifact-Dependent Compliance in GPT-4-Series Models},
  author = {Thomas Heverin},
  year = {2026},
  journal = {cs.CR},
  eprint = {2601.17911},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2601.17911v1},
}

@article{jung2025caddieset,
  title = {CaddieSet: A Golf Swing Dataset with Human Joint Features and Ball Information},
  author = {Seunghyeon Jung and Seoyoung Hong and Jiwoo Jeong and Seungwon Jeong and Jaerim Choi and Hoki Kim and Woojin Lee},
  year = {2025},
  journal = {cs.CV},
  eprint = {2508.20491},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2508.20491v1},
}

@article{nadler2025complexity,
  title = {Complexity of del Pezzo surfaces with du Val singularities},
  author = {Valentine Nadler},
  year = {2025},
  journal = {math.AG},
  eprint = {2504.12904},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2504.12904v1},
}

@article{mace2025vidore,
  title = {ViDoRe Benchmark V2: Raising the Bar for Visual Retrieval},
  author = {Quentin Macé and António Loison and Manuel Faysse},
  year = {2025},
  journal = {cs.IR},
  eprint = {2505.17166},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2505.17166v2},
}

@article{noda2025benchmark,
  title = {A Benchmark and Evaluation for Real-World Out-of-Distribution Detection Using Vision-Language Models},
  author = {Shiho Noda and Atsuyuki Miyai and Qing Yu and Go Irie and Kiyoharu Aizawa},
  year = {2025},
  journal = {cs.CV},
  eprint = {2501.18463},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2501.18463v3},
}

@article{li2025overlaybench,
  title = {OverLayBench: A Benchmark for Layout-to-Image Generation with Dense Overlaps},
  author = {Bingnan Li and Chen-Yu Wang and Haiyang Xu and Xiang Zhang and Ethan Armand and Divyansh Srivastava and Xiaojun Shan and Zeyuan Chen and Jianwen Xie and Zhuowen Tu},
  year = {2025},
  journal = {cs.CV},
  eprint = {2509.19282},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2509.19282v1},
}

@article{committee2025roman,
  title = {Roman Galactic Plane Survey Definition Committee Report},
  author = {Roman Galactic Plane Survey Definition Committee},
  year = {2025},
  journal = {astro-ph.GA},
  eprint = {2511.07494},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2511.07494v1},
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

@article{he2025membership,
  title = {Membership Inference Attacks on Recommender System: A Survey},
  author = {Jiajie He and Xintong Chen and Xinyang Fang and Min-Chun Chen and Yuechun Gu and Keke Chen},
  year = {2025},
  journal = {cs.IR},
  eprint = {2509.11080},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2509.11080v3},
}

@article{heyde2025aint,
  title = {AIn't Nothing But a Survey? Using Large Language Models for Coding German Open-Ended Survey Responses on Survey Motivation},
  author = {Leah von der Heyde and Anna-Carolina Haensch and Bernd Weiß and Jessica Daikeler},
  year = {2025},
  journal = {cs.CL},
  eprint = {2506.14634},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2506.14634v3},
}

@article{li2025articulated,
  title = {ART: Articulated Reconstruction Transformer},
  author = {Zizhang Li and Cheng Zhang and Zhengqin Li and Henry Howard-Jenkins and Zhaoyang Lv and Chen Geng and Jiajun Wu and Richard Newcombe and Jakob Engel and Zhao Dong},
  year = {2025},
  journal = {cs.CV},
  eprint = {2512.14671},
  archiveprefix = {arXiv},
  url = {https://arxiv.org/abs/2512.14671v2},
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

@article{fang2025privacy,
  title 

... (truncated, see full artifact)


{
  "real_search": true,
  "queries_used": [
    "Parameter Golf val bpb minimization under",
    "Parameter Golf val bpb minimization under benchmark",
    "Parameter Golf val bpb minimization under survey",
    "Parameter Golf val bpb minimization under seminal",
    "Parameter Golf val bpb minimization under state of the art"
  ],
  "year_min": 2020,
  "total_candidates": 178,
  "bibtex_entries": 178,
  "ts": "2026-03-19T12:58:09+00:00"
}