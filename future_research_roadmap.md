# Roadmap for Future Research: MLLM-Assisted Layer Analysis and Thickness Estimation

## Executive Summary

This roadmap revises the current research plan for automated layer labeling, thickness estimation, and anomaly detection in SEM/TEM cross-section images. The revised direction is a hybrid metrology system:

- Use MLLMs for multimodal reasoning over the image, ROI, layer stack table, material priors, and user instructions.
- Use deterministic image processing, calibrated scale extraction, and physics-aware metrology for quantitative measurements.
- Treat low-contrast or invisible interfaces as constrained inferences with uncertainty, not as directly observed segmentation results.
- Keep a human-in-the-loop review path until the system is validated across devices, imaging conditions, and layer stacks.

The original plan correctly identifies a promising direction, but it overstates the reliability of fully autonomous MLLM/SAM-style segmentation for invisible boundaries and relies on several weak, blocked, or off-topic references. This roadmap shifts the work toward testable research questions, evidence-tiered citations, reproducible benchmarks, and measurable milestones.

## Revised Research Thesis

An MLLM should not be the primary measuring instrument. Its best role is as a reasoning and orchestration layer that parses design tables, identifies visible high-contrast anchors, selects appropriate metrology tools, explains ambiguity, and produces a structured report. Quantitative thickness estimation should be performed by calibrated algorithms and validated against expert annotations, metadata, physical scale bars, and, where relevant, physics-based models such as JMONSEL.

For multilayer stacks where adjacent layers have indistinguishable contrast, the system should output:

- `observed_boundary`: interface visible in the image and measured from pixel evidence.
- `inferred_boundary`: interface not visibly separable; estimated from layer order, nominal thickness, process priors, and neighboring anchors.
- `uncertain_boundary`: interface with ambiguous evidence; requires expert confirmation or auxiliary modalities such as EDS/EELS/STEM.

This boundary taxonomy is the core edit to the research plan.

## Evidence Review and Citation Triage

### Strong Sources for Core Claims

| ID | Local file | Use in roadmap |
| --- | --- | --- |
| R01 | `references/ref01_semifa_arxiv.pdf` | Agentic semiconductor failure-analysis pipeline, multimodal fusion, telemetry-aware report generation. Use as an architecture inspiration, not proof of layer metrology accuracy. |
| R05 | `references/ref05_2510.11260.pdf` and `references/ref32_2510.11260_arxiv_html.html` | Scale-bar detection, OCR, LLM verification, pixel-to-metric calibration. Useful for the calibration module. |
| R06 | `references/ref06_2408.15305.pdf` | Semiconductor electron micrograph VLM instruction tuning and on-premise small-model motivation. |
| R07 | `references/ref07_2407.10810.pdf` | FabGPT for wafer defect knowledge queries and defect reasoning. Useful for domain-specific MLLM direction. |
| R08 | `references/ref08_MicroscopyGPT_ACS.pdf` | Microscopy VLM for image-to-structure captioning; supports potential but also highlights need for domain-specific training and simulated data. |
| R10 | `references/ref10_2511.03120.pdf` | IC defect detection and novel class discovery using image-intrinsic priors; useful for anomaly detection under unseen classes. |
| R14 | `references/ref14_orbi_pseudo_haadf.pdf` | Quantitative HAADF/STEM analysis with precise atomic-column and interplanar-distance measurements; supports quantitative microscopy rigor. |
| R17 | `references/ref17_QuPAINT_CVF.pdf` | Physics-aware instruction tuning and synthetic data for material characterization; useful for physics-informed MLLM training design. |
| R25 | `references/ref25_oae_microstructural_hfo2.pdf` | HfO2 microstructure and ferroelectricity review; useful for HZO/HfO2 stack domain priors. |
| R33 | `references/ref33_simplipytem_plos.pdf` | Open-source TEM processing, metadata, scale bars, contrast, and workflow automation. |
| R38 | `references/ref38_2604.00359.pdf` | Human-in-the-loop TEM/STEM layer thickness and interface roughness workflow; highly relevant for the metrology architecture. |
| R46 | `references/ref46_nist_jmonsel.pdf` | Physics-based SEM model fitting with JMONSEL for 10 nm patterned lines; relevant to sub-20 nm metrology limits. |
| R47 | `references/ref47_probe_profile_pmc.pdf` | Probe broadening and resolution limits in thick STEM specimens; supports uncertainty modeling. |
| R49 | `references/ref49_mdpi_membranes_15_10_288.pdf` | Cross-section preparation challenges; useful as background for sample-prep variability. |
| R55 | `references/ref55_tin_hzo_texture_pmc.pdf` | HZO/TiN texture, thin-film ferroelectric properties, and microstructure-process links. |
| R56 | `references/ref56_oae_agentic_material_science.html` | Agentic materials science review. The file is gzip-compressed despite `.html`; usable as a broad review after decompression, not a metrology-specific source. |

### Sources to Downgrade to Implementation Background

| ID | Local file | Recommended use |
| --- | --- | --- |
| R11 | `references/ref11_nvidia_defect_vfm.html` | Vendor blog on VLM/VFM semiconductor defect classification. Useful for industry framing, not primary scientific evidence. |
| R26 | `references/ref26_roboflow_defect_algorithms.html` | General defect-detection overview. Use only for implementation vocabulary. |
| R35/R36/R44 | OpenCV/PyImageSearch/GitHub/HandMap HTML sources | Useful for pixels-per-metric concepts and prototypes; cite only as tutorials or implementation examples. |
| R45 | `references/ref45_digitalsurf_thickness.html` | Commercial thickness-analysis product background. Useful for feature inspiration, not a scientific validation source. |
| R52 | `references/ref52_zenml_samsung_llmops.html` | LLMOps case-study style page. Use only as industry context; verify before citing as evidence. |

### Sources to Remove or Avoid as Support

The current plan should not rely on blocked pages, incomplete entries, or off-topic sources. Avoid or replace these unless the full primary source is obtained:

- `references/ref02_covalent_tem.html`: anti-bot page, not content.
- `references/ref03_ADA222582.pdf`: DTIC handbook, off-topic.
- `references/ref04_Sekitani_NatureMater_2010.pdf`: valuable paper but not central to SEM/TEM layer metrology here.
- `references/ref15_rochester_research_day_2026.pdf`: abstract collection, weak support.
- `references/ref19_mdpi_lands_15_4_610.pdf`: urban morphology, off-domain.
- `references/ref20_spie_segmentation.html` and `references/ref21_spie_volume_11325.html`: blocked/interstitial pages.
- Ref 24 in the extracted plan: incomplete citation.
- `references/ref27_acs_acsnano_5c15856.html` and `references/ref39_acsami_4c14281.html`: anti-bot shells unless PDF/full text is available elsewhere.
- Ref 31 Reddit: not suitable for the research plan.
- `references/ref41_pasta_kyoto_download_attempt.html`: off-topic.
- `references/ref42_researchgate_ebsd_background.html` and `references/ref50_researchgate_tin_workfunction.html`: blocked 16-byte responses.
- `references/ref43_barbone_neuroimaging.pdf`: off-topic.
- `references/ref54_zeiss_nims_sem*.html`: blocked/redirect pages.

## Key Corrections to the Existing Plan

1. Replace "fully autonomous" with "auditable, staged autonomy."

   The system can automate parts of the workflow, but expert-supervised automation with correction logging should remain the default until quantitative validation supports higher autonomy.

2. Replace "SAM-2 segments invisible boundaries" with "SAM-style models may help visible masks; invisible boundaries require constrained inference."

   A segmentation mask is not evidence when no image contrast exists. For adjacent low-contrast layers, the output should be a model-inferred partition with uncertainty.

3. Separate semantic layer labeling from thickness metrology.

   Layer names can be reasoned from stack order and visible anchors. Thickness values require scale calibration, boundary detection, profile statistics, and error bars.

4. Add uncertainty as a first-class output.

   Every boundary and thickness should carry a confidence score and an evidence type: `visible`, `weak_visual`, `design_inferred`, `metadata_inferred`, or `requires_review`.

5. Replace weak citations with primary or near-primary sources.

   The roadmap should cite R05, R06, R07, R08, R10, R14, R17, R25, R33, R38, R46, R47, and R55 for core technical claims. Vendor/blog sources can remain in a separate implementation-background section.

## Research Questions

### RQ1: Layer Reasoning

How accurately can an MLLM align a user-specified ROI with a structured layer stack table and identify the likely sequence of layers?

Key hypotheses:

- High-Z metal layers can serve as visual anchors in many SEM/TEM cross-sections.
- MLLM performance improves when prompted with material composition, nominal thickness, process order, scale bar, and a few expert-labeled examples.
- The MLLM should output structured reasoning rather than free-form labels.

### RQ2: Boundary Evidence

Which interfaces are actually visible, and which are only inferred from design priors?

Key hypotheses:

- Visible metal/dielectric and high-contrast interfaces can be measured with intensity-profile and gradient methods.
- Organic-organic or dielectric-dielectric boundaries may be invisible in standard SEM contrast and should be inferred only with explicit uncertainty.
- Auxiliary modalities such as HAADF-STEM, EDS, EELS, or metadata can convert some inferred boundaries into observed boundaries.

### RQ3: Thickness Estimation

What is the achievable error for layer thickness estimation under realistic SEM/TEM acquisition conditions?

Key hypotheses:

- For visible interfaces, dense vertical or normal-direction line scans can estimate mean thickness, standard deviation, min/max, and interface roughness.
- For ultrathin layers, probe broadening and sample thickness must be modeled or the system must report reduced confidence.
- Metadata-based calibration should be preferred when available; scale-bar OCR should be the fallback.

### RQ4: Anomaly Detection

Can the system identify structural deviations that matter for failure analysis, including voids, discontinuities, roughness excursions, missing/extra layers, and abnormal contrast?

Key hypotheses:

- Closed-set defect classification is insufficient for new products and process changes.
- Image-intrinsic and self-supervised methods are promising for open-world or novel-class defect discovery.
- MLLMs are useful for explanation and triage, but defect localization should be evaluated with detection and segmentation metrics.

### RQ5: Human-in-the-Loop Deployment

How much expert time can the system save while preserving traceability and metrology confidence?

Key hypotheses:

- A review UI with editable boundaries, layer labels, and uncertainty flags will outperform either manual-only or fully automatic workflows during validation and deployment.
- Correction logs can become supervised data for fine-tuning and active learning.
- Expert trust depends on transparent evidence labels more than on fluent narrative reports.

## Proposed System Architecture

### 1. Input Layer

Inputs:

- SEM/TEM image.
- ROI, such as the red rectangle in the original case study.
- Structured layer stack table with sequence, material, nominal thickness, and optional process step.
- Image metadata if available: pixel size, magnification, instrument, detector, accelerating voltage, acquisition date, and file type.
- Scale bar and scale text if metadata is unavailable.
- Optional examples of expert-labeled images.

Required data schema:

```yaml
sample_id: string
image_path: string
modality: SEM | TEM | STEM | HAADF_STEM | other
roi:
  x: int
  y: int
  width: int
  height: int
calibration:
  source: metadata | scale_bar | manual | unknown
  nm_per_pixel: float
  confidence: float
layer_stack:
  - name: string
    material: string
    nominal_thickness_nm: float
    expected_contrast: bright | dark | variable | unknown
    sequence_index: int
```

### 2. MLLM Reasoning Layer

Responsibilities:

- Parse the layer table and convert it into ordered constraints.
- Identify visually salient anchors such as bright metal bands or distinctive crystalline layers.
- Propose an ordered layer map inside the ROI.
- Mark boundary evidence type for every interface.
- Generate tool calls or instructions for scale extraction, segmentation, intensity profiles, and anomaly checks.

Recommended output schema:

```yaml
layer_hypotheses:
  - layer_name: GE1
    y_range_px: [120, 156]
    evidence_type: visible
    visual_anchor: bright_metal_band
    confidence: 0.91
boundaries:
  - between: [GI1, GE1]
    y_px: 120
    evidence_type: visible
    confidence: 0.88
  - between: [PLN2, PLN3]
    y_px: 620
    evidence_type: design_inferred
    confidence: 0.42
```

### 3. Calibration Layer

Priority order:

1. Use embedded microscope metadata when available, following the SimpliPyTEM-style workflow.
2. Detect scale bar and OCR the scale text when metadata is unavailable.
3. Use an LLM verifier only to detect implausible OCR outputs, unit mismatches, and scale-context inconsistencies.
4. Require manual calibration if both metadata and scale-bar extraction fail.

Metrics:

- Scale-bar localization IoU.
- OCR exact match for value and unit.
- Pixel-to-nm calibration error.
- Failure rate requiring manual review.

### 4. Boundary and Thickness Layer

Recommended baseline:

- Preprocess ROI with denoising and contrast normalization.
- Detect visible interfaces using vertical or normal-direction intensity profiles.
- Smooth profiles, find gradients and derivative extrema, and estimate boundary positions.
- Aggregate many profiles to compute thickness statistics.
- Report interface roughness and confidence.

For visible layers:

```yaml
thickness_result:
  layer_name: PV
  mean_nm: 348.2
  std_nm: 12.7
  min_nm: 321.4
  max_nm: 377.9
  boundary_source: visible_profile
  calibration_source: metadata
  confidence: 0.84
```

For invisible layers:

```yaml
thickness_result:
  layer_name: PLN2
  mean_nm: 1600.0
  std_nm: null
  boundary_source: design_inferred
  calibration_source: scale_bar
  confidence: 0.35
  note: "No visible contrast boundary. Position inferred from nominal thickness ratio between neighboring anchors."
```

Physics-aware extensions:

- Use JMONSEL-style model fitting for SEM critical-dimension or ultrathin feature measurement where beam-sample interaction distorts edge profiles.
- Model probe broadening and sample-thickness effects for thick STEM specimens.
- Use HAADF/STEM intensity and atomic-column methods only when the acquisition modality and resolution support them.

### 5. Anomaly Layer

Targets:

- Missing layer.
- Extra layer.
- Thickness out of tolerance.
- Void or delamination.
- Discontinuity in metal line.
- Abnormal interface roughness.
- Contrast inconsistency suggesting contamination, phase change, oxidation, or sample-prep artifact.

Approach:

- Establish deterministic checks from the measured layer map.
- Add self-supervised or image-intrinsic anomaly detection for localized defects.
- Use MLLMs for defect description, triage, and root-cause hypothesis generation.
- Keep root-cause links to process logs optional until telemetry integration is available.

### 6. Human Review and Audit Layer

The research prototype should include an expert review workflow:

- Overlay layer labels and boundaries on the image.
- Color-code boundary evidence: visible, weak visual, inferred, review required.
- Allow drag-editing of boundaries and label corrections.
- Store correction logs as training data.
- Export a report with all assumptions, calibration source, uncertainty, and unresolved ambiguities.

## Phased Roadmap

### Phase 0: Source Cleanup and Dataset Specification

Goals:

- Finalize the bibliography and remove weak references from the core plan.
- Define the annotation schema for layer labels, visible boundaries, inferred boundaries, and thickness metrics.
- Select initial image categories: LTPS/display stack, HZO/TiN stack, generic multilayer STEM/TEM, and defect/anomaly examples.

Deliverables:

- Cleaned citation list with tiers.
- Dataset schema in YAML/JSON.
- Annotation guide for experts.
- Initial benchmark split plan.

Success criteria:

- Every research claim maps to a strong source or is explicitly labeled as a hypothesis.
- The dataset schema can represent invisible boundaries without pretending they are visual ground truth.

### Phase 1: Deterministic Metrology Baseline

Goals:

- Build a baseline that does not depend on an MLLM.
- Implement ROI extraction, metadata calibration, scale-bar fallback, visible boundary detection, and thickness statistics.
- Add a minimal review interface or notebook visualization.

Deliverables:

- Python pipeline for image loading, ROI crop, calibration, profile extraction, interface detection, and CSV/JSON output.
- Baseline results on at least 20 annotated ROIs.
- Error analysis against expert labels.

Success metrics:

- Scale calibration success rate above 90 percent for images with clean scale bars or metadata.
- Visible-boundary thickness mean absolute error below a target set by expert ground truth and pixel resolution.
- Every output includes confidence and evidence type.

### Phase 2: MLLM Layer Reasoning Prototype

Goals:

- Add MLLM reasoning over image, ROI, and layer stack table.
- Convert free-form responses into strict structured outputs.
- Evaluate whether the MLLM improves layer ordering and anchor assignment over deterministic baselines.

Deliverables:

- Prompt templates for layer-stack reasoning.
- Structured output parser and validator.
- Ablation study: image only, image plus table, image plus table plus examples, image plus table plus calibration.

Success metrics:

- Layer sequence accuracy.
- Anchor identification accuracy.
- Boundary evidence classification accuracy.
- Hallucination rate: nonexistent layers, unsupported boundary claims, or wrong scale units.

### Phase 3: Hybrid Boundary and Thickness Estimation

Goals:

- Combine MLLM layer hypotheses with deterministic metrology.
- Add constrained inference for invisible layers.
- Add uncertainty propagation from calibration, boundary confidence, and design-prior confidence.

Deliverables:

- Hybrid layer map generator.
- Thickness reports with visible/inferred boundary separation.
- Statistical thickness and roughness outputs for visible layers.
- Review UI improvements for expert correction.

Success metrics:

- Reduced expert correction time compared with manual workflow.
- Improved label accuracy compared with deterministic baseline alone.
- Inferred boundary outputs clearly distinguish design priors from visual evidence.

### Phase 4: Defect and Anomaly Detection

Goals:

- Detect deviations from the expected stack after layer mapping.
- Support both known defects and novel/unseen anomaly patterns.
- Add explanatory reports without allowing the narrative to overrule measurement evidence.

Deliverables:

- Rule-based anomaly checks from layer thickness and continuity.
- Self-supervised anomaly prototype for local defect discovery.
- Defect report schema with location, morphology, affected layer, severity, and confidence.

Success metrics:

- Known-defect detection F1 or mAP on annotated data.
- Novel-class recall under held-out defect categories.
- False-positive rate acceptable for expert review workflow.

### Phase 5: Physics-Aware and Cross-Modality Validation

Goals:

- Improve metrology for ultrathin and beam-broadened features.
- Validate against auxiliary measurements and physics-based models.
- Determine when the system should request EDS/EELS/STEM or manual review.

Deliverables:

- JMONSEL-inspired model-fitting experiment for selected SEM edge cases.
- Probe-broadening uncertainty module for STEM/TEM where applicable.
- Cross-modality comparison protocol.

Success metrics:

- Quantified improvement in sub-20 nm feature measurement versus simple edge detection.
- Explicit failure modes for low-resolution, low-contrast, or sample-prep-damaged images.
- Expert-approved review thresholds.

### Phase 6: Agentic Failure-Analysis Workflow

Goals:

- Extend from image metrology to structured FA reporting.
- Integrate historical cases, recipes, and equipment telemetry only after the image-metrology core is reliable.
- Produce traceable, editable reports rather than ungrounded narratives.

Deliverables:

- Multi-agent workflow: image analyst, metrology analyst, anomaly analyst, report writer, reviewer.
- Retrieval layer for historical examples.
- Optional telemetry connector for SECS/GEM or process logs.
- Final FA report template with evidence links.

Success metrics:

- Report completeness.
- Expert acceptance rate.
- Time-to-report reduction.
- Root-cause hypothesis precision when telemetry is available.
- No unsupported corrective-action recommendations.

## Benchmark and Evaluation Plan

### Data Requirements

Each benchmark sample should include:

- Original image.
- ROI.
- Layer stack table.
- Calibration source.
- Expert visible boundary labels.
- Expert inferred boundary labels where applicable.
- Thickness measurements with uncertainty.
- Defect labels if present.
- Notes on sample-prep artifacts and acquisition modality.

### Core Metrics

Layer reasoning:

- Layer sequence accuracy.
- Layer label accuracy.
- Anchor detection precision/recall.
- Evidence-type classification accuracy.

Boundary and thickness:

- Boundary position MAE in pixels and nm.
- Thickness MAE/RMSE in nm.
- Interface roughness error.
- Calibration error.
- Uncertainty calibration: whether confidence matches empirical error.

Anomaly detection:

- Defect localization IoU.
- Defect classification F1.
- Novel-defect recall.
- False-positive rate per ROI.

Workflow:

- Expert correction time.
- Number of manual edits per image.
- Report acceptance rate.
- Hallucination or unsupported-claim rate.

### Required Ablations

- Without layer stack table.
- Without scale-bar or metadata calibration.
- Without MLLM reasoning.
- Without deterministic metrology.
- With visible boundaries only.
- With invisible boundaries included as inferred priors.
- Cross-domain transfer: LTPS to HZO, HZO to generic multilayer TEM, and SEM to STEM.

## Model and Tooling Recommendations

### Baselines

- OpenCV/scikit-image/SciPy for preprocessing, profiles, gradients, contours, and measurements.
- SimpliPyTEM-style metadata and TEM image handling where supported.
- Simple scale-bar detector plus OCR; use LLM verification only as a plausibility check.
- MLLM prompting for structured layer reasoning, not direct final measurement.

### Candidate Models

- Domain-tuned VLM or small on-premise MLLM for semiconductor/microscopy images.
- Self-supervised anomaly detector for IC SEM defects.
- Promptable segmentation for visible regions only, evaluated against deterministic baselines.
- Physics-aware instruction tuning using synthetic stacks and known layer priors.

### Extensions

- JMONSEL-style model fitting for SEM edge profiles.
- Cross-modal fusion with EDS/EELS/HAADF-STEM.
- Active learning from expert corrections.
- Retrieval-augmented FA report generation with historical cases and tool logs.

## Risk Register

| Risk | Impact | Mitigation |
| --- | --- | --- |
| MLLM hallucinates layer labels or boundaries | Incorrect reports and loss of trust | Strict schemas, evidence-type labels, validation rules, expert review. |
| Invisible boundaries are treated as measured | False precision | Separate observed vs inferred outputs and require uncertainty. |
| Scale bar OCR is wrong | Systematic measurement error | Prefer metadata, use OCR validation, require manual calibration on low confidence. |
| SAM-style segmentation fails on low-contrast SEM/TEM | Poor boundary masks | Use deterministic profiles as baseline; restrict segmentation claims to visible interfaces. |
| Domain shift across stacks and instruments | Weak generalization | Cross-domain benchmark, active learning, domain-specific fine-tuning. |
| Weak citations undermine plan credibility | Research plan becomes speculative | Keep evidence tiers and replace blocked/off-topic sources. |
| Lack of expert ground truth | Impossible to validate | Build annotation protocol before model optimization. |
| Overfocus on report generation | Fluent but inaccurate outputs | Prioritize metrology accuracy before agentic reporting. |

## Prioritized Next Steps

1. Create a cleaned bibliography from `references/reference_audit.md`.
2. Convert the extracted plan into a shorter proposal using the revised thesis above.
3. Build the annotation schema and label at least 20 ROIs.
4. Implement the deterministic metrology baseline.
5. Run an MLLM-only pilot to quantify failure modes before adding it to the pipeline.
6. Define acceptance thresholds with domain experts for visible, inferred, and review-required boundaries.

## Recommended Roadmap Figure

Use this flow in the edited proposal:

```text
Image + ROI + Layer Table
          |
          v
Calibration: metadata -> scale bar OCR -> manual
          |
          v
MLLM reasoning: layer order, anchors, evidence types
          |
          v
Boundary engine:
  visible interfaces -> profile/gradient/metrology
  invisible interfaces -> constrained inference + uncertainty
          |
          v
Thickness + roughness + anomaly checks
          |
          v
Expert review and correction log
          |
          v
Validated report and training data feedback
```

## Reference List for the Revised Plan

- R01. SemiFA: An Agentic Multi-Modal Framework for Autonomous Semiconductor Failure Analysis Report Generation. `references/ref01_semifa_arxiv.pdf`
- R05. A Large-Language-Model Assisted Automated Scale Bar Detection and Extraction Framework for Scanning Electron Microscopic Images. `references/ref05_2510.11260.pdf`
- R06. Parameter-Efficient Quantized Mixture-of-Experts Meets Vision-Language Instruction Tuning for Semiconductor Electron Micrograph Analysis. `references/ref06_2408.15305.pdf`
- R07. FabGPT: An Efficient Large Multimodal Model for Complex Wafer Defect Knowledge Queries. `references/ref07_2407.10810.pdf`
- R08. MicroscopyGPT: Generating Atomic-Structure Captions from Microscopy Images of 2D Materials with Vision-Language Transformers. `references/ref08_MicroscopyGPT_ACS.pdf`
- R10. Image-Intrinsic Priors for Integrated Circuit Defect Detection and Novel Class Discovery via Self-Supervised Learning. `references/ref10_2511.03120.pdf`
- R14. Quantitative STEM-HAADF Study of Pseudo-2D Sb2Te3 Films. `references/ref14_orbi_pseudo_haadf.pdf`
- R17. QuPAINT: Physics-Aware Instruction Tuning Approach to Quantum Material Discovery. `references/ref17_QuPAINT_CVF.pdf`
- R25. Microstructural Evolution and Ferroelectricity in HfO2 Films. `references/ref25_oae_microstructural_hfo2.pdf`
- R33. SimpliPyTEM: An Open-Source Python Library and App to Simplify TEM and In Situ TEM Image Analysis. `references/ref33_simplipytem_plos.pdf`
- R38. AI-Assisted Human-in-the-Loop Web Platform for Structural Characterization in Hard Drive Design. `references/ref38_2604.00359.pdf`
- R46. Scanning Electron Microscope Measurement of Width and Shape of 10 nm Patterned Lines Using a JMONSEL-Modeled Library. `references/ref46_nist_jmonsel.pdf`
- R47. The Probe Profile and Lateral Resolution of STEM of Thick Specimens. `references/ref47_probe_profile_pmc.pdf`
- R49. Cross-Section Preparation of Polymer Composite Membranes for TEM Characterization. `references/ref49_mdpi_membranes_15_10_288.pdf`
- R55. Temperature-Dependent Texture Transfer to Hf0.5Zr0.5O2 Films from TiN Electrode and Its Impact on Ferroelectricity. `references/ref55_tin_hzo_texture_pmc.pdf`
- R56. Agentic Material Science. `references/ref56_oae_agentic_material_science.html`
