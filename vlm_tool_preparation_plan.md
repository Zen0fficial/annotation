# Plan

Prepare the non-LLM toolchain as one pipeline: first stabilize image/calibration/metrology outputs, then feed that state into anomaly reasoning tools. The LLM/VLM is treated as ready and will call or audit these tools through structured schemas.

## Scope

- In: Tool contracts, calibration, boundary/thickness tools, layer-map assembly, anomaly candidate tools, validators, review logging.
- Out: VLM training, UI polish, telemetry/retrieval, physics extensions like JMONSEL until the core pipeline works.

## Action Items

- [ ] Define shared JSON/YAML schemas for inputs, tool calls, `layer_map`, `thickness_result`, `anomaly_candidate`, and review flags.
- [ ] Prepare a small fixture set of SEM/TEM images with ROIs, layer-stack tables, scale bars or metadata, and expert notes.
- [ ] Implement image loader, ROI cropper, coordinate transform, and preprocessing tools.
- [ ] Implement calibration tools: metadata parser, scale-bar detector, OCR reader, and calibration validator.
- [ ] Implement metrology tools: intensity profile extraction, gradient boundary detection, thickness calculation, and roughness tracking.
- [ ] Build the layer-map assembler that merges VLM hypotheses, measured boundaries, inferred boundaries, calibration, and confidence flags.
- [ ] Implement Module B support tools: rule-based anomaly checker, anomaly candidate generator, and anomaly-to-layer mapper.
- [ ] Add schema validation and guardrails to reject unsupported claims, missing calibration, and measured coordinates for invisible boundaries.
- [ ] Add review logging so expert edits become structured correction data.
- [ ] Validate end to end on 20-50 ROIs, tracking calibration success, boundary accuracy, thickness error, anomaly affected-layer accuracy, and review-required cases.

## Open Questions

- What image formats should the first version support: PNG/JPEG only, or microscope formats such as DM/EMD/TIFF?
- Do we have expert boundary labels already, or should the first milestone include annotation?
- Should anomaly detection start rule-based only, or include a self-supervised candidate generator from the first prototype?
