# Reference Audit

Source document: `MLLM Layer Analysis and Thickness Estimation.pdf`

## Valid PDFs Fetched

- Ref 1: `ref01_semifa_arxiv.pdf`
- Ref 4: `ref04_Sekitani_NatureMater_2010.pdf`
- Ref 5: `ref05_2510.11260.pdf`
- Ref 6: `ref06_2408.15305.pdf`
- Ref 7: `ref07_2407.10810.pdf`
- Ref 10: `ref10_2511.03120.pdf`
- Ref 13: `ref13_2603.19327.pdf`
- Ref 14: `ref14_orbi_pseudo_haadf.pdf`
- Ref 15: `ref15_rochester_research_day_2026.pdf`
- Ref 16: `ref16_2602.17478.pdf`
- Ref 17: `ref17_QuPAINT_CVF.pdf`
- Ref 18: `ref18_uark_agentic_2d_material.pdf`
- Ref 33: `ref33_simplipytem_plos.pdf`
- Ref 38: `ref38_2604.00359.pdf`
- Ref 46: `ref46_jmonsel_nist.pdf`

## HTML Or Web Sources Fetched

- Ref 1: `ref01_semifa_arxiv.html` also fetched; PDF is available.
- Ref 2: `ref02_covalent_tem.html`
- Ref 5: `ref05_2510.11260_arxiv.html` and `ref32_2510.11260_arxiv_html.html`; PDF is available.
- Ref 8: `ref08_MicroscopyGPT_PMC.html`
- Ref 11: `ref11_nvidia_defect_vfm.html`
- Ref 12: `ref12_hzo_hfoxny_aip_doi.html` plus blocked PDF attempts.
- Ref 19: `ref19_mdpi_lands_15_4_610.html`, but access-denied content only.
- Ref 20: `ref20_spie_segmentation.html`, but anti-bot/interstitial content only.
- Ref 21: `ref21_spie_volume_11325.html`, but anti-bot/interstitial content only.
- Ref 22: `ref22_mdpi_processes_14_12_1888.html`, but access-denied content only.
- Ref 23: `ref23_ieee_10478488.blocked.html`
- Ref 25: `ref25_oae_microstructural_hfo2.html`
- Ref 26: `ref26_roboflow_defect_algorithms.html`
- Ref 27: `ref27_acs_acsnano_5c15856.html`
- Ref 28: `ref28_acs_acsaelm_3c01502.html`
- Ref 29: `ref29_mdpi_rs_18_12_1891.html`, but access-denied content only.
- Ref 33: `ref33_simplipytem_plos.html`; PDF is available.
- Ref 34: `ref34_simplipytem_pmc.html`
- Ref 35: `ref35_pyimagesearch_opencv_size.html`
- Ref 36: `ref36_github_practical_cv.html`
- Ref 37: `ref37_NP_Size.py`
- Ref 39: `ref39_acsami_4c14281.html`
- Ref 40: `ref40_infinite_layer_pmc.html`
- Ref 44: `ref44_handmap_opencv.html`
- Ref 45: `ref45_digitalsurf_thickness.html`
- Ref 47: `ref47_probe_profile_pmc.html`
- Ref 48: `ref48_oxford_sem_eds.html`
- Ref 49: `ref49_mdpi_membranes_15_10_288.html`, but access-denied content only.
- Ref 51: `ref51_sn_pt_pmc.html`
- Ref 52: `ref52_zenml_samsung_llmops.html`
- Ref 53: `ref53_agentic_lab_pmc.html`
- Ref 54: `ref54_zeiss_nims_sem.html`, but response is only a small blocked/redirect page.
- Ref 55: `ref55_tin_hzo_texture_pmc.html`
- Ref 56: `ref56_oae_agentic_material_science.html`

## Need Manual Handling

- Ref 3: DTIC `ADA222582.pdf` returns `403 Request Blocked`.
- Ref 8: PMC page is available; PDF link exists but returns a download-preparation/interstitial page here.
- Ref 9: Hugging Face citation is a search query, not a specific paper; fetch failed.
- Ref 12: AIP PDF/DOI attempts return blocked/landing HTML, not the PDF.
- Ref 19: MDPI returns `403 Access Denied`; PDF variant also blocked.
- Ref 20: SPIE returns anti-bot/interstitial HTML; PDF variant also blocked.
- Ref 21: SPIE proceedings page returns anti-bot/interstitial HTML.
- Ref 22: MDPI returns `403 Access Denied`; PDF variant also blocked.
- Ref 23: IEEE PDF endpoint returns HTML/blocked page, not the PDF.
- Ref 24: Bibliography entry is incomplete: "Interfacial Oxide Layer Scavenging in Ferroelectric Hf" has no URL.
- Ref 27: ACS DOI page fetched only a small publisher shell, not PDF/full text.
- Ref 28: ACS DOI page fetched only a small publisher shell, not PDF/full text.
- Ref 29: MDPI returns `403 Access Denied`; PDF variant also blocked.
- Ref 30: eScholarship PDF returns CloudFront/WAF challenge and zero-byte body.
- Ref 31: Reddit URL could not be reached from this environment.
- Ref 34: PMC page is available; PDF link exists but returns a reCAPTCHA/download-preparation page here. PLOS PDF for the same article was fetched as Ref 33.
- Ref 39: ACS DOI page fetched only a small publisher shell, not PDF/full text.
- Ref 40: PMC page is available; PDF link exists but returns a download-preparation/interstitial page here.
- Ref 41: Kyoto repository URL returned a small HTML page, not a PDF. It is also off-topic for the plan.
- Ref 42: ResearchGate returned a 16-byte blocked response.
- Ref 43: LMU PDF download was partial/corrupt; saved as `ref43_barbone_neuroimaging.partial-download`. It is also off-topic for the plan.
- Ref 47: PMC page is available; PDF link exists but returns a download-preparation/interstitial page here.
- Ref 48: Oxford page fetched only a small publisher shell, not PDF/full text.
- Ref 49: MDPI returns `403 Access Denied`; PDF variant also blocked.
- Ref 50: ResearchGate returned a 16-byte blocked response.
- Ref 51: PMC page is available; PDF link exists but returns a download-preparation/interstitial page here.
- Ref 53: PMC page is available; PDF link exists but returns a download-preparation/interstitial page here.
- Ref 54: ZEISS page returned only a small blocked/redirect response.
- Ref 55: PMC page is available; PDF link exists but returns a download-preparation/interstitial page here.

## Research Plan Review Notes

- The bibliography contains several weak or mismatched sources: Reddit, generic blogs, product/vendor pages, off-topic pasta/neuroimaging sources, and broad conference/proceedings pages.
- Several citations are future-dated or unusual for the current date context, including arXiv IDs in 2026 and 2025/2026 article entries. They need credibility checks before use.
- Ref 24 is malformed/incomplete and cannot be traced directly.
- The plan overstates what MLLMs and SAM-style models can reliably do for invisible layer boundaries. For boundaries with no image contrast, the workflow is interpolation from design priors, not observed segmentation.
- For a stronger research plan, replace weak web sources with primary papers or official tool/model documentation for MLLM vision, segmentation, SEM/TEM metrology, OCR scale-bar extraction, and JMONSEL/physics-based metrology.
