# Public-evidence software pilot
This standalone adapter creates a hash-addressed public literature review packet. It does not import upstream agents, invoke models, execute generated code, run shell commands, contact external services or control laboratory hardware.

Run `python -m unittest discover -s adapters/tests -v`.
Run `python adapters/public_evidence.py adapters/example_public_input.json --output /tmp/public_packet.json`.

The example uses original-source metadata only. Output remains human-review-required. This qualifies the narrow packet interface, not AutoDNA scientific reasoning or laboratory integration. Upstream CORS, raw-prompt logging and no-filtering concerns are not repaired by this adapter and the upstream server remains unsuitable for public deployment. A model-enabled integration requires explicit credentials, budget and separate evaluation.
