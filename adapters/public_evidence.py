"""Standalone public-evidence packet builder. Does not import AutoDNA agents or lab code."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

def build_packet(document):
    if set(document) != {"classification", "question", "sources"}:
        raise ValueError("Only public evidence fields are accepted")
    if document["classification"] != "public":
        raise ValueError("Public literature only")
    if not isinstance(document["question"], str) or not 1 <= len(document["question"]) <= 500:
        raise ValueError("Bounded question required")
    sources = document["sources"]
    if not isinstance(sources, list) or not 1 <= len(sources) <= 40:
        raise ValueError("Expected 1–40 public sources")
    for source in sources:
        if set(source) != {"doi", "title", "url", "access_level", "claim_status"}:
            raise ValueError("Unexpected source fields")
        if not all(isinstance(value, str) for value in source.values()):
            raise ValueError("Source values must be text")
        if not source["doi"].startswith("10.") or urlsplit(source["url"]).scheme != "https":
            raise ValueError("DOI and HTTPS source required")
        if source["claim_status"] != "review_required":
            raise ValueError("This adapter cannot approve scientific claims")
        if source["access_level"] not in {"metadata", "abstract", "full_text"}:
            raise ValueError("Source access must be explicit")
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":")).encode()
    return {"input_sha256": hashlib.sha256(encoded).hexdigest(),
            "classification": "public", "question": document["question"], "sources": sources,
            "status": "human_review_required", "laboratory_execution": False,
            "model_execution": False, "biological_validation": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input"); parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = build_packet(json.loads(Path(args.input).read_text()))
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"sources": len(result["sources"]), "status": result["status"]}))
if __name__ == "__main__": main()
