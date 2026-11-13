# AutoDNA → Open Biomedical Resource Center: software-only integration plan

**Created:** 2026-11-06  
**Status:** Proposed; not installed or executing  
**Fork:** https://github.com/davidwpace/AutoDNA  
**Upstream:** https://github.com/IPADS-X/AutoDNA  
**Resource catalog:** https://github.com/davidwpace/open-biomedical-resource-center/blob/main/data/resources.json

## Objective
Reuse suitable AutoDNA multi-agent patterns to build an auditable, human-supervised, public-data-only research loop for the Open DNA Agent Observatory. **Do not deploy automated wet-lab execution or patient-specific clinical services.**

## What is available
The upstream `autodna` branch contains a Python multi-agent engine (`AutoDNA-python/scientist`), UI, scheduler, and firmware. The README notes that operation without specialized laboratory hardware is limited. Relevant software components for inspection are:

| File | Potential role |
| --- | --- |
| `AutoDNA-python/scientist/agents/Literature.py` | Evidence retrieval from local paper collection |
| `AutoDNA-python/scientist/agents/Hypothesis.py` | Experiment optimization hypotheses |
| `AutoDNA-python/scientist/agents/Protocol.py` | Protocol planning; **not safe to execute unreviewed** |
| `AutoDNA-python/scientist/llm/model.py` | Gemini model configuration and credentials |
| `AutoDNA-python/scientist/server.py` | API interface; **not suitable for public deployment as-is** |

## Immediate safety concerns
Initial static inspection (not a full security audit) found:
1. The FastAPI server uses wildcard CORS.
2. The server logs submitted prompts and writes them to a local file.
3. The server launches the scientist using `--no_filtering`.
4. Code generation, scheduler/hardware controls, remote LLM use, and dependencies require a more complete isolation and permission review.

**Do not deploy the upstream server to the internet. Do not send private clinical records or secrets through it. Do not run generated laboratory commands.**

## Milestones

### 1. Audit and isolate
- [ ] Record pinned upstream commit, component dependency versions and Apache-2.0 attribution.
- [ ] Review model, tool, and shell/code execution pathways; build threat model.
- [ ] Determine which read-only agents function without physical scheduler/firmware.
- [ ] Add a dry-run interface that cannot invoke hardware, shell tools, generated Python, or unrestricted networking.
- [ ] Disable raw prompt logging, require access control and explicit allowed origins for any service, and use secret-safe model configuration.

### 2. Establish a reproducible computational pilot
- [ ] Choose one well-annotated **public** dataset and formulate a falsifiable, non-clinical question.
- [ ] Produce structured evidence records: hypothesis, source citation, dataset version, assumptions, uncertainties, checks, failures, and date.
- [ ] Assemble a literature → hypothesis → computational test design → human review workflow.
- [ ] Use mock models/tools to test deterministic orchestration first; then enable vetted model calls with a budget ceiling.
- [ ] Benchmark against a human-curated answer and measure citation fidelity / unsupported assertions.

### 3. Integrate conditionally
- [ ] Publish an *adapter* rather than directly exposing the wet-lab controller.
- [ ] Link the reviewed workflow from the Biomedical Resource Center catalog and record provenance in the Observatory.
- [ ] Keep patient data in a separate protected system; no patient information in public code, prompts, or logs.
- [ ] Only consider laboratory partner handoff after expert review and explicit approvals.

## Acceptance criteria
A reproducible **software-only**, **read-only**, documented demonstration with sources, independent checks, no laboratory execution, no patient information, and no claims of clinical validation.

## Current state
- The repository fork exists and is linked to upstream.
- AutoDNA is resource #43 in the Open Biomedical Resource Center; the GitHub catalog-validation run passed: https://github.com/davidwpace/open-biomedical-resource-center/actions/runs/42172821542.
- The full software-only integration has **not** been installed, run, or validated.


## Completion pass
A standalone read-only public-evidence packet adapter and tests now qualify the narrow software interface. See SOFTWARE_PILOT_ACCEPTANCE.md. Upstream agent/model/laboratory integration remains gated; the adapter does not silently import or execute upstream controls.
