import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location("public_evidence",Path(__file__).resolve().parents[1]/"public_evidence.py")
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class PublicPacketTests(unittest.TestCase):
    def fixture(self):
        return {"classification":"public","question":"Can a source remain unapproved?","sources":[{"doi":"10.1038/s41592-026-03213-8","title":"IRIS","url":"https://doi.org/10.1038/s41592-026-03213-8","access_level":"abstract","claim_status":"review_required"}]}
    def test_read_only_packet_has_no_execution(self):
        packet=module.build_packet(self.fixture());self.assertFalse(packet["laboratory_execution"]);self.assertFalse(packet["model_execution"]);self.assertEqual(packet["status"],"human_review_required")
    def test_commands_and_private_inputs_are_rejected(self):
        for change in [{"command":"execute"},{"classification":"private"}]:
            with self.assertRaises(ValueError):module.build_packet({**self.fixture(),**change})
    def test_adapter_cannot_approve_a_claim(self):
        d=self.fixture();d["sources"][0]["claim_status"]="validated"
        with self.assertRaises(ValueError):module.build_packet(d)
