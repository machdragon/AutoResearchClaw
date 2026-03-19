# Framework Diagram Prompt

**Paper**: GOLF: A Negative Result for Codec-Aware QAT in Lane\_3

## Image Generation Prompt

Clean academic vector diagram showing the methodology framework for “GOLF: Negative Result for Codec-Aware QAT in Lane_3”. White or very light grey background (#F7F7F7). Flat design, subtle soft shadows, no gradients, no photorealism.

Left-to-right pipeline with rounded-rectangle modules, high information density but uncluttered. Use muted blues (#4477AA), teals (#44AA99), soft purples (#AA3377), and warm accent (#CCBB44) for key elements; neutral greys (#CCCCCC, #666666) for outlines and text.

Modules (left to right):

1) “Canonical Training Entrypoint” (blue #4477AA)
2) “Lane_3 Objective: val_bpb + Gate Budget” (purple #AA3377), small annotation: “Quick-gate: runtime ≤ 1.10× baseline”
3) “Baseline Float Training (No QAT)” (grey-blue)
4) “Staged QAT Config” (teal #44AA99) with three vertically stacked sub-boxes:
   - “Stage 1: Float Warmup”
   - “Stage 2: QAT Enable (int8 Sim)”
   - “Stage 3: Codec-Aware Fine-Tune”
5) “Int8 Quantization + Gate Constraints” (teal)
6) “Roundtrip Codec Alignment” (accent #CCBB44) with two inner boxes:
   - “int8 Packing”
   - “zlib Compression / Decompression”
7) “Post-Roundtrip Model” (blue)
8) “Official Harness Evaluation” (purple) with two outputs:
   - “val_bpb (Compressed)”
   - “Runtime & Artifact Size (≤16MB)”

Use clear directional arrows between modules; split arrow from “Canonical Training Entrypoint” to both “Baseline Float Training” and “Staged QAT Config” to indicate comparison. Minimal text, sans-serif labels, consistent line weights.

## Usage Instructions

1. Copy the prompt above into an AI image generator (DALL-E 3, Midjourney, Ideogram, etc.)
2. Generate the image at high resolution (2048x1024 or similar landscape)
3. Save as `framework_diagram.png` in the same `charts/` folder
4. Insert into the paper's Method section using:
   - LaTeX: `\includegraphics[width=\textwidth]{charts/framework_diagram.png}`
   - Markdown: `![Framework Overview](charts/framework_diagram.png)`
