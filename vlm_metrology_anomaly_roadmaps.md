# Unified VLM Pipeline: Metrology Orchestration and Anomaly Reasoning

## Scope

This document defines a unified MLLM/VLM-centered pipeline for electron micrograph metrology and anomaly reasoning:

- Module A: VLM-Orchestrated Metrology Agent.
- Module B: VLM Defect and Anomaly Reasoning After Layer Context.

Module A produces the calibrated, evidence-typed layer/metrology state. Module B consumes that state and uses VLM reasoning to describe anomalies, connect them to affected layers or interfaces, and generate cautious failure-analysis hypotheses.

The guiding claim should remain modest and reference-faithful:

> The VLM is the reasoning, orchestration, and explanation layer. It does not directly replace calibrated metrology, expert validation, or physics-aware modeling.

## Unified Pipeline Overview

```text
Image + ROI + Layer Stack + Metadata
          |
          v
Module A: VLM-Orchestrated Metrology
  - parse stack table
  - identify visual anchors
  - choose calibration path
  - classify boundary evidence
  - call metrology tools
  - audit thickness outputs
          |
          v
Pipeline State
  - layer_map
  - thickness_result
  - boundary_evidence
  - calibration_record
  - review_flags
          |
          v
Module B: VLM Layer-Aware Anomaly Reasoning
  - consume layer/metrology state
  - attach anomaly candidates to layers/interfaces
  - explain visual and measurement evidence
  - grade severity and missing evidence
  - generate cautious hypotheses
          |
          v
Expert Review + Correction Logs
          |
          v
Benchmark updates / VLM fine-tuning data / report export
```

## Required Tools

The LLM/VLM is assumed to be ready. The remaining work is to provide reliable tools that the VLM can call, audit, or consume as structured evidence.

### Minimal Tool Set

| Tool | Used By | Purpose | Input | Output |
| --- | --- | --- | --- | --- |
| Image loader | Module A, Module B | Load SEM/TEM/STEM images into a standard array format. | Image path, modality hint. | Image array, dimensions, basic metadata. |
| ROI cropper | Module A, Module B | Extract the user-specified region and preserve coordinate mapping to the full image. | Image, ROI box. | ROI image, coordinate transform. |
| Metadata parser | Module A | Extract pixel size, magnification, detector, voltage, file metadata where available. | Original image or microscope file. | `calibration_record`, metadata fields, confidence. |
| Scale-bar detector | Module A | Locate the scale bar when metadata is missing or unreliable. | Full image or footer crop. | Scale-bar bounding box, pixel length, confidence. |
| OCR for scale text | Module A | Read scale value and unit. | Scale-bar/text crop. | Numeric value, unit, OCR confidence. |
| Calibration validator | Module A | Check unit plausibility and convert pixels to nm. | Metadata or scale-bar/OCR result. | `nm_per_pixel`, source, confidence, review flag. |
| Image preprocessor | Module A, Module B | Normalize contrast and reduce noise for profiles and anomaly tools. | ROI image. | Processed ROI, preprocessing parameters. |
| Intensity profile extractor | Module A | Generate vertical or normal-direction line profiles across candidate layers. | ROI image, candidate direction/region. | Intensity profiles, profile statistics. |
| Boundary detector | Module A | Find visible interfaces from gradients/peaks. | Profiles or processed ROI. | Boundary positions, confidence, evidence type. |
| Thickness calculator | Module A | Convert boundary spacing into thickness statistics. | Boundaries, calibration. | Mean/std/min/max thickness per layer. |
| Roughness tracker | Module A, Module B | Quantify interface roughness where boundaries are visible. | Boundary traces, calibration. | Roughness metrics and confidence. |
| Layer-map assembler | Module A | Combine VLM hypotheses, measured boundaries, inferred boundaries, and calibration. | VLM plan, tool outputs, layer table. | `layer_map`, `thickness_result`, `review_flags`. |
| Rule-based anomaly checker | Module B | Detect missing/extra layers, thickness excursions, roughness excursions, and continuity issues. | `layer_map`, `thickness_result`, ROI image. | `anomaly_candidate` records. |
| Anomaly candidate generator | Module B | Surface local visual anomalies, including unknown or novel candidates. | ROI image, optional masks/layer map. | Candidate boxes/masks, anomaly scores. |
| Anomaly-to-layer mapper | Module B | Attach anomaly candidates to affected layers or interfaces. | Candidates, `layer_map`, coordinate transform. | Candidates with affected layer/interface. |
| Report/schema validator | Module A, Module B | Enforce structured outputs and block unsupported claims. | VLM JSON/YAML output. | Validated output, errors, review flags. |
| Review logger | Module A, Module B | Store expert corrections for benchmarks and future tuning. | Expert edits, original predictions. | Correction log, updated labels. |

### Optional Extension Tools

| Tool | When Needed | Purpose |
| --- | --- | --- |
| Visible-region segmentation | When a layer or defect has clear contrast. | Produce masks for visible metal lines, voids, delamination, or other observable regions. |
| JMONSEL-style SEM model fitting | For sub-20 nm SEM edge-profile or critical-dimension cases. | Model beam-sample interaction and improve nanoscale edge/shape estimates. |
| STEM probe-broadening estimator | For thick STEM/TEM specimens or uncertain resolution. | Estimate reduced confidence due to probe broadening and sample thickness. |
| EDS/EELS/HAADF fusion reader | When auxiliary modality data is available. | Convert inferred boundaries into better-supported compositional or Z-contrast evidence. |
| Historical-case retriever | For failure-analysis reporting. | Retrieve similar expert-approved cases for cautious hypothesis generation. |
| Telemetry/process-log connector | When fab/process context is available. | Ground root-cause hypotheses in equipment or process evidence. |

### First Implementation Priority

Build these first:

1. Image loader and ROI cropper.
2. Metadata parser plus scale-bar/OCR calibration fallback.
3. Intensity profile extractor and boundary detector.
4. Thickness calculator and layer-map assembler.
5. Rule-based anomaly checker.
6. Report/schema validator.
7. Review logger.

Add the anomaly candidate generator after the layer-map handoff is stable. Add physics extensions and retrieval/telemetry only after the core pipeline can separate observed, weak, inferred, and review-required boundaries.

## Shared System Contract

Both modules should use the same structured inputs and outputs. They can be developed incrementally, but the final design is one pipeline with a required handoff from Module A to Module B.

### Inputs

```yaml
sample_id: string
image_path: string
modality: SEM | TEM | STEM | HAADF_STEM | other
roi:
  x: int
  y: int
  width: int
  height: int
layer_stack:
  - name: string
    material: string
    nominal_thickness_nm: float | null
    expected_contrast: bright | dark | variable | unknown
    sequence_index: int
calibration:
  source: metadata | scale_bar | manual | unknown
  nm_per_pixel: float | null
  confidence: float
metadata:
  instrument: string | null
  detector: string | null
  voltage_kv: float | null
  pixel_size_nm: float | null
```

### Boundary Evidence Types

```yaml
boundary_evidence_type:
  observed_boundary: "Visible boundary supported by image evidence."
  weak_visual_boundary: "Possible boundary with weak/noisy contrast."
  design_inferred_boundary: "Not visibly separable; inferred from layer order, nominal thickness, or process prior."
  metadata_inferred_boundary: "Inferred from instrument metadata or external measurement."
  requires_review: "Ambiguous or high-risk; expert review required."
```

### Shared Output Objects

```yaml
pipeline_state:
  sample_id: string
  source_image: string
  module_a_status: complete | partial | failed | requires_review
  module_b_status: not_started | complete | partial | failed | requires_review
  blocking_review_flags: [string]

layer_map:
  - layer_name: string
    material: string
    y_range_px: [int, int] | null
    y_range_nm: [float, float] | null
    evidence_type: observed_boundary | weak_visual_boundary | design_inferred_boundary | metadata_inferred_boundary | requires_review
    confidence: float
    notes: string

thickness_result:
  - layer_name: string
    mean_nm: float | null
    std_nm: float | null
    min_nm: float | null
    max_nm: float | null
    boundary_source: visible_profile | weak_visual | design_inferred | metadata_inferred | manual
    calibration_source: metadata | scale_bar | manual | unknown
    confidence: float
    requires_review: bool

anomaly_candidate:
  - anomaly_id: string
    location_px: [int, int, int, int]
    affected_layer: string | null
    anomaly_type: missing_layer | extra_layer | thickness_out_of_tolerance | void | delamination | discontinuity | roughness_excursion | abnormal_contrast | unknown
    evidence: visual | measurement_rule | anomaly_model | expert | mixed
    confidence: float
```

## Module A: VLM-Orchestrated Metrology Agent

### Research Question

Can a VLM reliably orchestrate a metrology workflow by interpreting an image, ROI, layer-stack table, and calibration evidence, then selecting appropriate tools and producing auditable layer/thickness outputs?

This module centers the VLM as the planner and evidence arbiter, not as the numeric measuring instrument.

### Core VLM Responsibilities

1. Parse the layer-stack table into ordered constraints.
2. Identify high-contrast visual anchors, especially metal layers.
3. Decide which boundaries are visible, weakly visible, inferred, or review-required.
4. Select a calibration pathway: metadata first, scale-bar OCR second, manual fallback.
5. Select measurement tools for visible interfaces.
6. Reject direct measurement for invisible interfaces.
7. Audit measurement outputs for unit errors, impossible thicknesses, or layer-order violations.
8. Generate a structured report that separates observed measurements from inferred priors.

### Non-VLM Tool Responsibilities

The VLM should call or consume outputs from specialized tools:

- Metadata parser for pixel size and microscope information.
- Scale-bar detector and OCR module.
- ROI cropper and image preprocessor.
- Intensity-profile extractor.
- Gradient/peak boundary detector.
- Roughness tracker.
- Optional segmentation module for visible regions only.
- Optional JMONSEL-style model fitting for SEM edge-profile cases.
- Optional probe-broadening uncertainty module for STEM/TEM.

### Agent Flow

```text
Image + ROI + Layer Stack
          |
          v
VLM parses table and identifies visual anchors
          |
          v
Calibration request:
  metadata -> scale bar OCR -> manual fallback
          |
          v
VLM classifies boundary evidence:
  visible / weak visual / inferred / review-required
          |
          v
Tool calls:
  visible boundaries -> profile + gradient + roughness
  weak boundaries -> profile + uncertainty + review
  invisible boundaries -> constrained inference only
          |
          v
VLM audits outputs:
  layer order, units, thickness plausibility, confidence
          |
          v
Structured layer map + thickness report + review queue
```

### Required Handoff to Module B

Module A must emit a pipeline state that Module B can consume without reinterpreting raw metrology from scratch.

```yaml
module_a_handoff:
  sample_id: LTPS_ROI_001
  calibration_record:
    source: scale_bar
    nm_per_pixel: 5.0
    confidence: 0.87
    review_required: false
  layer_map_ref: outputs/LTPS_ROI_001_layer_map.json
  thickness_result_ref: outputs/LTPS_ROI_001_thickness.json
  boundary_evidence_summary:
    observed_count: 8
    weak_visual_count: 2
    design_inferred_count: 5
    requires_review_count: 1
  review_flags:
    - "PLN2/PLN3 boundary is design-inferred, not visually measured."
  safe_for_module_b: true
```

### Tool-Call Schema

```yaml
tool_call:
  task_id: string
  tool_name: metadata_calibration | scale_bar_ocr | intensity_profile | gradient_boundary_detection | roughness_tracking | segmentation_visible_region | jmonsel_fit | probe_broadening_uncertainty | manual_review
  input:
    image_path: string
    roi: {x: int, y: int, width: int, height: int}
    layer_names: [string]
    expected_boundary_type: observed_boundary | weak_visual_boundary | design_inferred_boundary | requires_review
  expected_output:
    type: calibration | boundary_positions | thickness_stats | roughness_stats | uncertainty | review_flag
  vlm_rationale: string
```

### Example VLM Plan

```yaml
vlm_metrology_plan:
  sample_id: LTPS_ROI_001
  visual_anchors:
    - layer_name: GE1
      rationale: "Bright high-Z band consistent with Mo gate electrode in expected stack order."
      confidence: 0.86
    - layer_name: SD2
      rationale: "Large bright metal routing feature; expected Ti/Al/Ti source-drain stack."
      confidence: 0.89
  calibration:
    selected_path: scale_bar_ocr
    reason: "No embedded metadata provided; visible scale bar present."
  tool_calls:
    - tool_name: scale_bar_ocr
      target: full_image_footer
    - tool_name: intensity_profile
      target: roi
      layers: [GE1, GE2, SD1, SD2]
    - tool_name: gradient_boundary_detection
      target: visible_metal_dielectric_interfaces
  inferred_boundaries:
    - between: [PLN2, PLN3]
      reason: "Adjacent organic layers have similar contrast and no visible discontinuity."
      policy: "Do not measure directly; infer from nominal thickness only and require review if critical."
```

### Development Phases

#### Phase A0: Schema and Reference Cleanup

Deliverables:

- Unified input/output schema.
- Evidence-type definitions.
- Clean reference table.
- Annotation guide for visible, weak, inferred, and review-required boundaries.

Success criteria:

- Every output can distinguish measured evidence from design inference.
- Every citation used for a core claim maps to a vetted reference.

#### Phase A1: VLM Planning-Only Prototype

Deliverables:

- Prompt template for VLM metrology planning.
- Structured output parser.
- Tool-call schema validation.
- Expert review of VLM plans on a small ROI set.

Success metrics:

- Valid structured output rate.
- Tool-selection accuracy against expert expectation.
- Boundary evidence classification accuracy.
- Unsupported measurement instruction rate.

#### Phase A2: Calibration and Visible-Boundary Tool Integration

Deliverables:

- Metadata calibration path.
- Scale-bar OCR path.
- Intensity profile and gradient boundary modules.
- VLM audit of calibration and measurement outputs.

Success metrics:

- Calibration success rate.
- Unit error detection rate.
- Visible-boundary thickness MAE/RMSE.
- Percentage of low-confidence cases routed to review.

#### Phase A3: Uncertainty and Review Queue

Deliverables:

- Confidence propagation from calibration and boundary detection.
- Review queue sorted by risk.
- Report format with evidence labels.

Success metrics:

- Confidence calibration vs empirical error.
- Expert correction time.
- False precision rate for invisible boundaries.

#### Phase A4: Physics Extensions

Deliverables:

- JMONSEL-inspired experiment for selected SEM edge-profile cases.
- STEM/TEM probe-broadening uncertainty module where applicable.
- Cross-modality review protocol.

Success metrics:

- Improvement on sub-20 nm or beam-broadened cases.
- Clear failure-mode reporting.
- Expert approval of physics-extension thresholds.

### Evaluation Design

Use ablations that test the VLM's actual contribution:

| Ablation | Purpose |
| --- | --- |
| Tools only, no VLM | Measures deterministic baseline. |
| VLM planning, no layer table | Tests image-only reasoning. |
| VLM planning with layer table | Tests table-grounded reasoning. |
| VLM planning with calibration output | Tests whether scale/unit evidence improves decisions. |
| VLM planning with expert examples | Tests few-shot improvement. |
| VLM without audit step | Tests value of VLM self/checker pass. |

### Key Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| VLM overclaims invisible boundaries | Force evidence-type labels and reject coordinates for invisible boundaries unless marked inferred. |
| VLM chooses wrong tool | Compare tool plans against expert tool-selection labels. |
| Scale OCR error causes systematic thickness error | Prefer metadata, use OCR confidence, add unit plausibility checks. |
| Segmentation is used on low-contrast boundaries | Restrict segmentation to visible regions and evaluate against profile methods. |
| The pipeline seems too tool-heavy | Frame VLM contribution as orchestration, evidence arbitration, and grounded reporting. |

### Primary References for Module A

- R05. `references/ref05_2510.11260.pdf`  
  Supports automated SEM scale-bar detection, OCR, and LLM-assisted verification.

- R33. `references/ref33_simplipytem_plos.pdf`  
  Supports metadata extraction, scale-bar handling, contrast enhancement, and TEM workflow automation.

- R38. `references/ref38_2604.00359.pdf`  
  Supports human-in-the-loop multilayer TEM/STEM thickness and roughness analysis with gradient-based methods and interactive correction.

- R46. `references/ref46_nist_jmonsel.pdf`  
  Supports physics-based SEM model fitting for nanoscale line width and shape measurement.

- R47. `references/ref47_probe_profile_pmc.pdf`  
  Supports uncertainty from probe broadening and resolution limits in thick STEM specimens.

## Module B: VLM Defect and Anomaly Reasoning After Layer Context

### Research Question

Can a VLM use a calibrated, evidence-typed layer map to explain defects and anomalies more usefully than image-only defect classification?

This module consumes Module A's pipeline state. The VLM's task is to reason over that calibrated layer/metrology context and produce structured, cautious anomaly explanations.

### Core VLM Responsibilities

1. Interpret anomaly candidates in relation to the layer map.
2. Identify the affected layer or interface.
3. Describe the visual and measurement evidence.
4. Distinguish known defect categories from unknown anomalies.
5. Generate severity and review priority.
6. Produce root-cause hypotheses only when evidence supports them.
7. Mark root-cause statements as weak, moderate, or strong depending on available process/telemetry context.

### Non-VLM Tool Responsibilities

- Rule-based checks from Module A outputs:
  - thickness out of tolerance
  - missing or extra layer
  - roughness excursion
  - discontinuity in a metal line
- Self-supervised or image-intrinsic anomaly detection:
  - novel defect candidates
  - abnormal local contrast
  - unknown morphology
- Optional segmentation/detection:
  - visible voids
  - delamination regions
  - metal discontinuities
- Optional retrieval:
  - prior cases
  - process recipes
  - equipment telemetry

### Agent Flow

```text
Image + ROI
   |
   v
Layer map + thickness report from Module A
   |
   v
Rule checks:
  missing/extra layer, thickness tolerance, roughness, discontinuity
   |
   v
Anomaly model:
  known and novel defect candidates
   |
   v
VLM anomaly reasoner:
  affected layer, visual evidence, severity, explanation
   |
   v
Optional retrieval/telemetry:
  strengthen or weaken root-cause hypotheses
   |
   v
Structured anomaly report + review priority
```

### Required Input From Module A

Module B should not run as a free-floating image-only defect explainer unless the experiment is explicitly an ablation. Its standard input is Module A's handoff.

```yaml
module_b_required_context:
  module_a_handoff: required
  layer_map: required
  thickness_result: required_if_available
  calibration_record: required
  boundary_evidence_summary: required
  review_flags: required
```

If `safe_for_module_b` is false, Module B should still be allowed to draft a review note, but it should not produce confident affected-layer or root-cause claims.

### Anomaly Report Schema

```yaml
anomaly_report:
  sample_id: string
  anomaly_id: string
  affected_layer: string | null
  affected_interface: [string, string] | null
  anomaly_type: missing_layer | extra_layer | thickness_out_of_tolerance | void | delamination | discontinuity | roughness_excursion | abnormal_contrast | unknown
  localization:
    bbox_px: [int, int, int, int]
    mask_path: string | null
  evidence:
    visual_description: string
    measurement_evidence:
      metric: string
      observed_value: float | null
      expected_range: [float, float] | null
      unit: string | null
    evidence_sources:
      - image
      - layer_map
      - thickness_result
      - anomaly_detector
      - historical_case
      - telemetry
  severity:
    level: low | medium | high | critical | unknown
    rationale: string
  root_cause_hypotheses:
    - hypothesis: string
      support_level: weak | moderate | strong
      supporting_evidence: [string]
      missing_evidence: [string]
  confidence: float
  requires_review: bool
```

### Example VLM Output

```yaml
anomaly_report:
  sample_id: LTPS_ROI_014
  anomaly_id: A003
  affected_layer: SD2
  affected_interface: null
  anomaly_type: discontinuity
  localization:
    bbox_px: [428, 190, 512, 244]
    mask_path: outputs/LTPS_ROI_014_A003_mask.png
  evidence:
    visual_description: "The bright SD2 metal band is locally interrupted inside the ROI."
    measurement_evidence:
      metric: continuity
      observed_value: null
      expected_range: null
      unit: null
    evidence_sources:
      - image
      - layer_map
      - anomaly_detector
  severity:
    level: medium
    rationale: "The anomaly affects a conductive routing layer, but electrical impact cannot be confirmed from the image alone."
  root_cause_hypotheses:
    - hypothesis: "Possible local patterning, etch, or sample-preparation artifact."
      support_level: weak
      supporting_evidence:
        - "Image shows localized interruption in bright metal contrast."
      missing_evidence:
        - "No process telemetry or cross-modality confirmation."
  confidence: 0.74
  requires_review: true
```

### Development Phases

#### Phase B0: Anomaly Taxonomy and Data Schema

Deliverables:

- Defect/anomaly taxonomy tied to layer context.
- Schema for anomaly candidates and VLM reports.
- Expert annotation guide for affected layer/interface and evidence type.

Success criteria:

- Defects can be represented as layer-aware events, not only generic image classes.
- Unknown anomalies can be labeled without forcing a known class.

#### Phase B1: Rule-Based Layer-Context Checks

Deliverables:

- Missing/extra layer checks.
- Thickness tolerance checks.
- Interface roughness checks.
- Metal continuity checks for visible conductive layers.

Success metrics:

- Rule precision against expert labels.
- False-positive rate per ROI.
- Correct affected-layer assignment.

#### Phase B2: Novel Anomaly Candidate Generation

Deliverables:

- Self-supervised or image-intrinsic anomaly detector.
- Candidate masks or bounding boxes.
- Confidence score and unknown-class flag.

Success metrics:

- Novel-defect recall.
- Candidate localization IoU.
- False-positive rate suitable for expert review.

#### Phase B3: VLM Layer-Aware Anomaly Explanation

Deliverables:

- Prompt/schema for VLM anomaly reports.
- VLM explanation tied to layer map and anomaly candidates.
- Severity and review priority output.

Success metrics:

- Defect description accuracy.
- Affected-layer identification accuracy.
- Expert usefulness rating.
- Unsupported root-cause claim rate.

#### Phase B4: Optional Retrieval and Telemetry

Deliverables:

- Retrieval over historical cases.
- Optional process/telemetry connector.
- Root-cause confidence grading.

Success metrics:

- Root-cause hypothesis precision when telemetry is available.
- Reduction in unsupported process claims.
- Report acceptance rate.

### Evaluation Design

Use ablations that show why layer context matters:

| Ablation | Purpose |
| --- | --- |
| VLM image-only anomaly explanation | Baseline for visual reasoning. |
| VLM with layer map | Tests value of layer context. |
| VLM with layer map + thickness report | Tests value of measurement evidence. |
| VLM with anomaly mask only | Tests whether localization without layer context is enough. |
| VLM with retrieval/telemetry | Tests root-cause grounding. |
| VLM with root-cause disabled | Measures defect-description quality separately from hypothesis generation. |

### Key Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| VLM invents root cause from image only | Require support-level labels and missing-evidence fields. |
| Generic defect labels ignore layer context | Force affected layer/interface fields in the schema. |
| Novel anomalies get forced into known categories | Include `unknown` anomaly type and novelty score. |
| Anomaly detector creates too many false positives | Tune for expert-review workload and report false positives per ROI. |
| Layer-map errors propagate into anomaly report | Include layer-map confidence and route low-confidence cases to review. |

### Primary References for Module B

- R07. `references/ref07_2407.10810.pdf`  
  Supports VLM-based wafer defect detection, localization, and defect knowledge querying.

- R10. `references/ref10_2511.03120.pdf`  
  Supports image-intrinsic priors and novel class discovery for IC SEM defects.

- R01. `references/ref01_semifa_arxiv.pdf`  
  Supports agentic semiconductor failure-analysis report generation with multimodal fusion and telemetry. Use as architecture inspiration, not as proof of layer metrology accuracy.

- R38. `references/ref38_2604.00359.pdf`  
  Supports using measured layer thickness and roughness outputs as structured evidence for downstream review.

## Unified Pipeline Stages

The modules should be staged as one research program.

### Stage 1: VLM Metrology Planning

Goal:

- Show that a VLM can produce valid metrology plans from image + ROI + layer table.

Key output:

- Tool-call plan and boundary evidence labels.

### Stage 2: Calibrated Layer Map

Goal:

- Produce a layer map with observed/inferred boundaries, thickness statistics, confidence, and review flags.

Key output:

- `module_a_handoff`, `layer_map`, `thickness_result`, `calibration_record`, and `review_flags`.

### Stage 3: Layer-Aware Anomaly Detection

Goal:

- Detect candidate anomalies using rules and anomaly models, then attach each candidate to a layer or interface using Module A's layer map.

Key output:

- `anomaly_candidate`.

### Stage 4: VLM Anomaly Explanation

Goal:

- Generate structured, cautious reports that explain anomaly type, evidence, affected layer, severity, and missing evidence using the Module A pipeline state.

Key output:

- `anomaly_report`.

### Stage 5: Expert Review and Feedback

Goal:

- Let experts correct layer maps, anomaly labels, severity, and hypotheses. Store corrections for model improvement.

Key output:

- Correction logs and benchmark updates.

## Minimal Experiment Plan

### Dataset

Start with 20 to 50 ROIs:

- Each ROI has a layer-stack table.
- Each ROI has calibration metadata or scale bar.
- Experts label visible boundaries and inferred boundaries separately.
- Experts mark anomalies where present.

### Experiment 1: VLM Metrology Planning

Ask the VLM to produce:

- Visual anchors.
- Boundary evidence labels.
- Tool-call plan.
- Review-required cases.

Evaluate:

- Structured output validity.
- Tool-selection accuracy.
- Boundary evidence classification.
- Unsupported measurement claims.

### Experiment 2: VLM-Orchestrated Thickness Reporting

Run calibration/profile tools according to the VLM plan.

Ask the VLM to audit:

- Units.
- Layer order.
- Thickness plausibility.
- Observed vs inferred separation.

Evaluate:

- Visible-boundary thickness error.
- Calibration error detection.
- Expert correction time.
- False precision on invisible boundaries.

### Experiment 3: Layer-Aware Anomaly Explanation

Provide the VLM with:

- Image and ROI.
- Module A handoff.
- Layer map.
- Thickness report.
- Anomaly candidates.

Ask it to produce:

- Affected layer/interface.
- Anomaly type.
- Evidence summary.
- Severity.
- Root-cause hypotheses with support level.

Evaluate:

- Affected-layer accuracy.
- Defect description accuracy.
- Novel-defect handling.
- Unsupported root-cause claim rate.
- Expert usefulness rating.

## Reference Discipline

Use the references as follows:

| Claim Type | Best References |
| --- | --- |
| VLM/MLLM semiconductor or defect reasoning | R06, R07, R08 |
| VLM agentic FA reporting | R01 |
| Scale-bar/OCR calibration with LLM verification | R05 |
| TEM metadata and workflow automation | R33 |
| Human-in-the-loop layer thickness/roughness analysis | R38 |
| Physics-based SEM metrology | R46 |
| STEM probe broadening and resolution limits | R47 |
| Novel IC defect discovery | R10 |

Avoid relying on blocked, incomplete, or off-topic sources from `references/reference_audit.md` for core claims. Vendor blogs and tutorial pages can be used only for implementation background.

## Writing Positioning

A faithful positioning paragraph for a proposal:

> We propose a unified VLM-centered pipeline for electron micrograph layer analysis and anomaly reasoning. In Module A, the VLM interprets the image, ROI, layer-stack table, calibration outputs, and tool results to produce structured metrology plans, boundary evidence labels, calibrated layer maps, and thickness reports. In Module B, the VLM consumes this layer/metrology state to generate layer-aware anomaly reports, severity assessments, and cautious failure-analysis hypotheses. Quantitative thickness measurements are performed by calibrated image-processing or physics-aware metrology tools, while the VLM serves as the orchestration, evidence-arbitration, and explanation layer. This design avoids treating invisible interfaces as directly segmented image evidence and preserves expert review for ambiguous or high-risk cases.

This positioning keeps the contribution centered on MLLM/VLM reasoning while staying faithful to the strongest references.
