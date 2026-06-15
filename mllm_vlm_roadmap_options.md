# MLLM/VLM-Centered Roadmap Options for Layer Analysis and Thickness Estimation

## Purpose

This note expands the MLLM/VLM-focused alternatives to `future_research_roadmap.md`. It does not recommend a single roadmap. Instead, it lists several research roadmaps that can all be pursued while keeping MLLMs/VLMs central to the contribution.

The key constraint from the reference review is that an MLLM/VLM should not be described as a direct, standalone pixel ruler for every layer. The strongest faithful claim is:

> MLLMs/VLMs can reason over electron micrographs, ROIs, layer-stack tables, material priors, calibration outputs, and tool results to produce structured layer hypotheses, boundary evidence labels, metrology instructions, anomaly explanations, and auditable reports.

Quantitative thickness values still need calibration, boundary evidence, uncertainty, and expert validation.

## Shared Assumptions Across All Roadmaps

All proposed roadmaps should preserve these assumptions.

1. The VLM is central, but its role is explicit.

   The model may parse layer tables, identify visual anchors, classify boundary evidence, generate tool calls, explain ambiguity, and produce structured reports. It should not be claimed to directly measure invisible interfaces from image contrast.

2. Boundary evidence must be typed.

   Use at least:

   - `observed_boundary`: visible in the image and supported by pixel evidence.
   - `weak_visual_boundary`: faint or noisy visual evidence, needs confidence and review.
   - `design_inferred_boundary`: not visible; inferred from stack order, nominal thickness, process priors, or neighboring anchors.
   - `requires_review`: too ambiguous for reliable automated use.

3. Layer labeling and thickness metrology are separate tasks.

   A VLM may correctly infer that a dark region corresponds to a dielectric or organic layer, but thickness estimation requires pixel-to-length calibration, boundary localization, profile statistics, and uncertainty.

4. Calibration is not optional.

   Prefer microscope metadata when available. Use scale-bar detection/OCR as a fallback. Manual calibration is required when both fail or confidence is low.

5. Human review remains part of the research design.

   The references support human-in-the-loop workflows more strongly than immediate full autonomy, especially for multilayer TEM/STEM metrology and ambiguous interfaces.

## Roadmap 1: Structured VLM Layer-Reasoning Benchmark

### Core Idea

Make the main research question: how well can an MLLM/VLM align an electron micrograph ROI with a layer-stack table and produce structured layer hypotheses?

This roadmap treats layer reasoning as the core VLM capability. Thickness measurement is secondary and used only to evaluate whether the VLM's layer map is useful downstream.

### VLM Role

The VLM receives:

- SEM/TEM/STEM image.
- ROI coordinates.
- Layer stack table with material, sequence, nominal thickness, and expected contrast.
- Optional scale/calibration output.
- Optional few-shot examples.

The VLM outputs:

```yaml
layer_hypotheses:
  - layer_name: GE1
    material: Mo
    y_range_px: [120, 156]
    evidence_type: observed_boundary
    visual_anchor: bright_high_z_metal_band
    confidence: 0.91
boundaries:
  - between: [GI1, GE1]
    y_px: 120
    evidence_type: observed_boundary
    confidence: 0.88
  - between: [PLN2, PLN3]
    y_px: null
    evidence_type: design_inferred_boundary
    confidence: 0.35
    note: "No visible contrast separation; inferred from layer order and nominal thickness."
```

### Work Packages

1. Build a benchmark of ROIs with expert labels.
2. Define strict output schemas for layer order, anchors, and boundary evidence.
3. Run prompt ablations:
   - image only
   - image plus ROI
   - image plus ROI plus layer table
   - image plus ROI plus layer table plus calibration
   - image plus ROI plus layer table plus few-shot examples
4. Measure hallucinations: unsupported layers, overconfident invisible boundaries, wrong material assignments, wrong scale assumptions.
5. Compare generic VLMs with domain-tuned VLMs where available.

### Success Metrics

- Layer sequence accuracy.
- High-contrast anchor identification precision/recall.
- Boundary evidence classification accuracy.
- Unsupported boundary claim rate.
- Structured-output validity rate.
- Cross-stack transfer performance.

### Strong References

- R06: `references/ref06_2408.15305.pdf` supports semiconductor electron micrograph VLM instruction tuning and on-premise small-model motivation.
- R07: `references/ref07_2407.10810.pdf` supports domain-specific multimodal wafer defect knowledge querying.
- R08: `references/ref08_MicroscopyGPT_ACS.pdf` supports microscopy VLM potential while motivating domain-specific data.
- R17: `references/ref17_QuPAINT_CVF.pdf` supports physics-aware instruction tuning and synthetic data for material characterization.

### Main Risk

The VLM may produce plausible labels without evidence. The mitigation is strict evidence typing and expert validation.

## Roadmap 2: Domain-Tuned Semiconductor/Microscopy VLM

### Core Idea

Make the research contribution a domain-adapted MLLM/VLM for semiconductor and microscopy layer reasoning. The key comparison is not "VLM vs deterministic metrology," but "generic VLM vs domain-tuned VLM."

### VLM Role

The VLM is the main model under study. It is trained or adapted to answer structured questions such as:

- What layers are likely present in this ROI?
- Which high-contrast bands are reliable anchors?
- Which boundaries are directly visible?
- Which layers are indistinguishable under this modality?
- What additional metadata or modality would reduce ambiguity?
- Is the proposed layer ordering consistent with the stack table?

### Work Packages

1. Build instruction data from expert annotations.
2. Add synthetic or weakly supervised examples where appropriate.
3. Include question types for:
   - layer sequence reasoning
   - material/contrast interpretation
   - visible vs inferred boundary classification
   - defect description
   - calibration sanity checks
4. Train or fine-tune a small VLM where data privacy and on-premise use matter.
5. Compare against general-purpose VLM baselines.

### Candidate Training Examples

```text
Question:
Given this ROI and layer table, identify the visible metal anchors and explain which dielectric interfaces cannot be directly observed.

Answer:
The bright lower band is consistent with GE1 because it appears after the Poly-Si/GI1 region in the expected stack and has high-Z Mo contrast. The GI1/Buffer and GI2/ILD dielectric boundaries are not visually separable in this image and should be marked design_inferred_boundary unless auxiliary contrast or metadata is available.
```

### Success Metrics

- Improvement over generic VLM on layer reasoning tasks.
- Reduction in hallucinated boundaries.
- Better evidence-type calibration.
- Cross-domain transfer from LTPS/display stacks to HZO/TiN or other multilayer stacks.
- Latency and deployment feasibility for local/on-premise use.

### Strong References

- R06: `references/ref06_2408.15305.pdf` is the closest reference for a small-scale semiconductor electron micrograph vision-language assistant.
- R07: `references/ref07_2407.10810.pdf` supports customized IC fabrication LMMs for defect detection and Q&A.
- R08: `references/ref08_MicroscopyGPT_ACS.pdf` supports microscopy-specific VLM training.
- R17: `references/ref17_QuPAINT_CVF.pdf` supports physics-aware instruction data and synthetic-data design.

### Main Risk

Training data may teach the model to memorize stack patterns instead of grounding in image evidence. The benchmark must separate image-grounded claims from table-derived claims.

## Roadmap 3: Physics-Aware VLM for Boundary Evidence

### Core Idea

Make the VLM explicitly physics-aware. The research goal is not only to label layers, but to teach the model when layer boundaries are physically observable under a given imaging modality and when they must remain inferred.

This roadmap is a good fit if the paper needs stronger scientific novelty than prompt engineering alone.

### VLM Role

The VLM reasons over:

- Material composition.
- Expected electron contrast.
- Imaging modality: SEM, TEM, STEM, HAADF-STEM.
- Resolution and probe effects.
- Nominal film thickness.
- Stack order.
- Auxiliary cues such as EDS/EELS/HAADF availability.

The VLM output should include statements like:

```yaml
boundary_assessment:
  between: [PLN2, PLN3]
  visual_observability: low
  reason: "Adjacent organic layers have similar SEM contrast and no visible intensity discontinuity."
  recommended_status: design_inferred_boundary
  recommended_next_action: "Request expert review or auxiliary modality if this interface matters."
```

### Work Packages

1. Encode contrast and modality priors into instruction data.
2. Generate synthetic or curated examples where boundaries are visible, weakly visible, or invisible.
3. Train the VLM to classify observability before assigning a coordinate.
4. Add uncertainty language and confidence calibration.
5. Validate on HZO/TiN, LTPS/display, HAADF/STEM, and noisy/low-contrast examples.

### Success Metrics

- Boundary observability classification accuracy.
- Reduction in false measured-boundary claims.
- Calibration of confidence vs expert disagreement.
- Correct identification of when auxiliary modalities are needed.
- Generalization across material systems.

### Strong References

- R17: `references/ref17_QuPAINT_CVF.pdf` supports physics-aware instruction tuning and synthetic data for material characterization.
- R14: `references/ref14_orbi_pseudo_haadf.pdf` supports quantitative HAADF/STEM analysis and atomic/interplanar measurement rigor.
- R46: `references/ref46_nist_jmonsel.pdf` supports physics-based SEM model fitting for nanoscale features.
- R47: `references/ref47_probe_profile_pmc.pdf` supports probe broadening and resolution limits in thick STEM specimens.
- R25: `references/ref25_oae_microstructural_hfo2.pdf` and R55: `references/ref55_tin_hzo_texture_pmc.pdf` support HfO2/HZO/TiN domain priors.

### Main Risk

Physics-aware language can sound authoritative even when not experimentally validated. The roadmap should distinguish trained priors from measured evidence.

## Roadmap 4: VLM-Orchestrated Metrology Agent

### Core Idea

Keep the VLM at the center as an orchestrator. It interprets the image and layer table, decides which measurement tools to invoke, checks their outputs, and generates a structured explanation. It does not directly replace metrology algorithms.

This is the most faithful way to combine VLMs with thickness estimation.

### VLM Role

The VLM acts as a tool-using agent:

1. Parse ROI and layer table.
2. Identify likely visual anchors.
3. Decide whether boundaries are visible or inferred.
4. Request calibration from metadata or scale-bar OCR.
5. Call profile/gradient methods for visible interfaces.
6. Suggest segmentation only for visible regions.
7. Request physics-based fitting for ultrathin SEM/CD cases.
8. Produce a report that ties measurements to evidence.

### Example Tool Plan

```yaml
vlm_tool_plan:
  calibration:
    preferred: metadata
    fallback: scale_bar_ocr
    manual_if_confidence_below: 0.8
  visible_boundary_tools:
    - intensity_profile
    - gradient_peak_detection
    - roughness_tracking
  inferred_boundary_policy:
    method: constrained_layer_stack_inference
    requires_uncertainty: true
  physics_extensions:
    - jmonsel_model_fit_for_sub_20_nm_sem_edges
    - probe_broadening_uncertainty_for_stem
```

### Work Packages

1. Define a VLM tool-call schema.
2. Build deterministic tools for calibration and visible-boundary profiles.
3. Let the VLM select tools and audit outputs.
4. Add consistency checks:
   - layer order
   - expected thickness ranges
   - unit plausibility
   - visible/inferred separation
5. Evaluate whether VLM orchestration reduces human correction time and unsupported claims.

### Success Metrics

- Tool-selection accuracy.
- Calibration error detection.
- Boundary evidence classification.
- Visible-boundary thickness error after VLM-guided tool use.
- Unsupported measurement claim rate.
- Expert correction time.

### Strong References

- R05: `references/ref05_2510.11260.pdf` supports automated scale-bar detection, OCR, and LLM verification.
- R33: `references/ref33_simplipytem_plos.pdf` supports metadata, scale-bar handling, and TEM workflow automation.
- R38: `references/ref38_2604.00359.pdf` supports human-AI-assisted layer thickness and interface roughness workflows using gradient-based detection and review.
- R46: `references/ref46_nist_jmonsel.pdf` supports JMONSEL-style SEM model-based metrology.
- R47: `references/ref47_probe_profile_pmc.pdf` supports STEM probe-broadening uncertainty.

### Main Risk

The system may be perceived as less "MLLM/VLM-first" because measurement tools do the numeric work. The framing should emphasize that the VLM contribution is multimodal interpretation, tool selection, evidence arbitration, and report grounding.

## Roadmap 5: Human-in-the-Loop VLM Copilot

### Core Idea

Build a VLM-assisted expert annotation and review system. The research contribution is a VLM copilot that proposes labels, evidence types, and ambiguity explanations, while experts correct the result. The correction logs become training data.

This roadmap is strong when trust, deployment, and dataset creation matter.

### VLM Role

The VLM provides:

- Initial layer labels.
- Boundary evidence classifications.
- Explanations for ambiguous or invisible boundaries.
- Suggestions for additional review or auxiliary data.
- Draft reports from expert-approved annotations.

The expert provides:

- Boundary edits.
- Label corrections.
- Calibration corrections.
- Rejection or approval of inferred boundaries.
- Notes on sample-prep artifacts.

### Work Packages

1. Create an annotation UI or notebook interface.
2. Display VLM proposals with confidence and evidence type.
3. Allow drag-editing boundaries and changing labels.
4. Store every correction as structured training data.
5. Use active learning to prioritize uncertain examples.
6. Retrain or adapt the VLM from correction logs.

### Success Metrics

- Expert time saved per ROI.
- Number of manual edits per image.
- Acceptance rate of VLM-proposed labels.
- Boundary evidence correction rate.
- Improvement after active-learning rounds.
- Expert trust survey or report acceptance rate.

### Strong References

- R38: `references/ref38_2604.00359.pdf` strongly supports human-in-the-loop multilayer TEM/STEM thickness and roughness analysis.
- R06: `references/ref06_2408.15305.pdf` supports domain-tuned VLMs for semiconductor electron micrographs.
- R05: `references/ref05_2510.11260.pdf` supports interactive LLM-assisted scale-bar verification.

### Main Risk

The VLM may mostly accelerate annotation rather than solve metrology end to end. That is acceptable if the contribution is framed as expert-time reduction and data flywheel creation.

## Roadmap 6: VLM Defect and Anomaly Reasoning After Layer Context

### Core Idea

Focus the VLM on anomaly explanation and defect knowledge queries, but condition it on the layer map. The VLM should describe what is abnormal, which layer or interface is affected, and what hypotheses are plausible. Localization can come from anomaly detectors or visible segmentation tools.

### VLM Role

The VLM receives:

- Image and ROI.
- Layer hypotheses.
- Boundary evidence labels.
- Defect/anomaly masks or candidate regions.
- Optional process or historical context.

The VLM outputs:

```yaml
anomaly_report:
  anomaly_type: discontinuity
  affected_layer: SD2
  visual_evidence: "Bright conductive band is interrupted within ROI."
  severity: medium
  confidence: 0.77
  root_cause_hypotheses:
    - hypothesis: "Possible local patterning or etch issue."
      support: "Image morphology only; no telemetry available."
      status: weak_hypothesis
```

### Work Packages

1. Establish layer context before defect reasoning.
2. Add rule-based checks for missing/extra layers and out-of-tolerance thickness.
3. Add self-supervised anomaly detection for novel defects.
4. Use the VLM for description, severity framing, and knowledge queries.
5. Restrict root-cause recommendations unless telemetry or historical cases are available.

### Success Metrics

- Defect description accuracy.
- Affected-layer identification accuracy.
- Known-defect classification F1 or mAP.
- Novel-defect recall.
- Unsupported root-cause claim rate.
- Expert usefulness rating.

### Strong References

- R07: `references/ref07_2407.10810.pdf` supports VLM-based wafer defect detection and defect knowledge querying.
- R10: `references/ref10_2511.03120.pdf` supports image-intrinsic priors and novel class discovery for IC SEM defects.
- R01: `references/ref01_semifa_arxiv.pdf` supports agentic semiconductor failure-analysis reporting with multimodal fusion and telemetry, but should be used as architecture inspiration rather than proof of layer metrology accuracy.

### Main Risk

The VLM may overstate root cause from image-only evidence. The report schema should label root-cause statements as hypotheses and note whether telemetry exists.

## Roadmap 7: Agentic VLM Failure-Analysis Workflow

### Core Idea

Build a multi-agent VLM system for end-to-end failure-analysis assistance, but keep the image-metrology claims auditable. This roadmap is the broadest and should come after smaller VLM reasoning and metrology-validation studies.

### VLM Role

Use multiple VLM/LLM agents:

- `LayerReasoner`: identifies layer order, anchors, and boundary evidence.
- `CalibrationAuditor`: reviews metadata/scale-bar outputs and unit plausibility.
- `MetrologyPlanner`: selects measurement tools and flags invisible interfaces.
- `AnomalyExplainer`: describes defects and affected layers.
- `ReportWriter`: writes a traceable report with evidence links.
- `Reviewer`: checks unsupported claims before export.

### Work Packages

1. Define agent responsibilities and shared state.
2. Enforce structured outputs at every step.
3. Add retrieval over prior expert-approved cases.
4. Optionally integrate equipment telemetry or process logs.
5. Generate reports that preserve measurement provenance.
6. Compare report quality with expert-written reports.

### Success Metrics

- Report completeness.
- Unsupported-claim rate.
- Expert acceptance rate.
- Time-to-report reduction.
- Correct use of telemetry when available.
- Failure recovery when one agent produces low-confidence output.

### Strong References

- R01: `references/ref01_semifa_arxiv.pdf` supports an agentic multimodal semiconductor FA reporting architecture.
- R07: `references/ref07_2407.10810.pdf` supports defect knowledge Q&A.
- R56: `references/ref56_oae_agentic_material_science.html` can be used only as broad agentic materials-science context.
- R05, R38, R46, and R47 should provide the measurement guardrails.

### Main Risk

This roadmap can become fluent report generation without reliable metrology. It should be staged after the VLM layer-reasoning and boundary-evidence tasks are benchmarked.

## Cross-Roadmap Evaluation Matrix

| Capability | Roadmap 1 | Roadmap 2 | Roadmap 3 | Roadmap 4 | Roadmap 5 | Roadmap 6 | Roadmap 7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VLM layer reasoning | Core | Core | Core | Core | Core | Support | Core |
| Domain VLM training | Optional | Core | Strong | Optional | Optional | Optional | Optional |
| Physics-aware reasoning | Optional | Optional | Core | Strong | Optional | Optional | Support |
| Tool orchestration | Low | Low | Medium | Core | Medium | Medium | Core |
| Human review | Medium | Medium | Medium | Medium | Core | Medium | Core |
| Anomaly reasoning | Low | Medium | Low | Medium | Low | Core | Core |
| Report generation | Low | Low | Low | Medium | Medium | Medium | Core |
| Best first milestone | Benchmark | Model adaptation | Evidence taxonomy | Tool-call prototype | Review UI | Defect Q&A | Agent architecture |

## Recommended Reference Discipline

### Core MLLM/VLM References

- R06. `references/ref06_2408.15305.pdf`  
  Use for semiconductor electron micrograph VLM instruction tuning and small/on-premise model motivation.

- R07. `references/ref07_2407.10810.pdf`  
  Use for domain-specific IC/wafer defect multimodal querying and defect Q&A.

- R08. `references/ref08_MicroscopyGPT_ACS.pdf`  
  Use for microscopy VLM framing and the need for domain-specific training.

- R17. `references/ref17_QuPAINT_CVF.pdf`  
  Use for physics-aware instruction tuning and synthetic data in material characterization.

- R01. `references/ref01_semifa_arxiv.pdf`  
  Use for agentic FA report architecture and multimodal/telemetry fusion. Do not use as proof of layer-thickness accuracy.

### Core Metrology and Calibration Guardrails

- R05. `references/ref05_2510.11260.pdf`  
  Use for scale-bar detection, OCR, and LLM-based verification.

- R33. `references/ref33_simplipytem_plos.pdf`  
  Use for TEM metadata, scale bars, contrast enhancement, and workflow automation.

- R38. `references/ref38_2604.00359.pdf`  
  Use for human-in-the-loop multilayer thickness and roughness analysis.

- R46. `references/ref46_nist_jmonsel.pdf`  
  Use for physics-based SEM model fitting in nanoscale metrology.

- R47. `references/ref47_probe_profile_pmc.pdf`  
  Use for STEM probe broadening and resolution limits.

### Domain-Prior References

- R14. `references/ref14_orbi_pseudo_haadf.pdf`  
  Use for quantitative HAADF/STEM rigor.

- R25. `references/ref25_oae_microstructural_hfo2.pdf`  
  Use for HfO2/HZO microstructure and ferroelectric domain priors.

- R55. `references/ref55_tin_hzo_texture_pmc.pdf`  
  Use for HZO/TiN texture and process-microstructure links.

### Use Only as Background

- R11. `references/ref11_nvidia_defect_vfm.html`
- R26. `references/ref26_roboflow_defect_algorithms.html`
- R35/R36/R44. OpenCV/tutorial-style implementation sources.
- R45. `references/ref45_digitalsurf_thickness.html`
- R52. `references/ref52_zenml_samsung_llmops.html`
- R56. `references/ref56_oae_agentic_material_science.html`

These may help frame implementation or industry context, but they should not carry core scientific claims.

### Avoid as Core Evidence

Avoid blocked, incomplete, off-topic, or publisher-shell sources identified in `references/reference_audit.md`, including anti-bot shells, Reddit, unrelated urban/neuroimaging/pasta sources, and malformed citations. If a claim depends on one of those sources, replace it with a primary paper or clearly label it as an unverified hypothesis.

## Practical Choice Guide

Use this guide to choose among the VLM-centered roadmaps.

| If the goal is... | Try this roadmap |
| --- | --- |
| Prove VLMs can reason over image plus layer table | Roadmap 1 |
| Build a publishable model adaptation story | Roadmap 2 |
| Make the scientific novelty stronger and less prompt-only | Roadmap 3 |
| Connect VLMs to real thickness estimation without overclaiming | Roadmap 4 |
| Create a dataset and deployable expert workflow | Roadmap 5 |
| Emphasize failure analysis and defects | Roadmap 6 |
| Build an end-to-end agentic demo | Roadmap 7 |

## Minimal Faithful First Experiment

A compact first experiment that stays VLM-centered and faithful to the references:

1. Collect 20 to 50 ROIs with layer-stack tables.
2. Ask several VLMs to output structured layer hypotheses and boundary evidence labels.
3. Include ablations with and without layer tables and calibration.
4. Compare against expert labels.
5. Penalize unsupported claims about invisible boundaries.
6. Report where the VLM helps: anchor identification, layer-order reasoning, ambiguity explanation, and review prioritization.
7. Report where tools remain necessary: scale calibration, quantitative boundary detection, thickness statistics, and physics-aware metrology.

This experiment keeps the MLLM/VLM as the main research object while avoiding the unsupported claim that it can directly measure invisible layer boundaries from raw pixels.
