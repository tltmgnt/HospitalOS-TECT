"""Offline curriculum answer key. Synthetic checks, never operational approval."""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
for base in (ROOT, ROOT / "src", ROOT / "layer-b"):
    sys.path.insert(0, str(base))
CASES = []

def check(name, actual, expected):
    passed = actual == expected
    CASES.append({"case": name, "actual": actual, "expected": expected, "passed": passed})
    if not passed:
        raise AssertionError(f"{name}: expected {expected!r}, got {actual!r}")

def rejects(name, call, error=ValueError):
    try:
        call()
    except error:
        check(name, error.__name__, error.__name__)
    else:
        raise AssertionError(f"{name}: expected {error.__name__}")




def run():
    from hospitalos_tect.assurance import Claim, Evidence, Rule, assess
    c = Claim("c","Synthetic operations claim",("e",))
    e = [Evidence("e","fictional-source",True,True)]
    rules = [Rule("r","Synthetic rule",True)]
    r = assess(c,e,rules)
    check("complete declarations still need review", r.status, "review_required")
    check("missing evidence blocks", list(assess(c,[],rules).reasons), ["missing_evidence:e"])
    check("unverified evidence blocks", assess(c,[Evidence("e","fictional",True,False)],rules).status, "blocked")
    check("contradiction blocks", list(assess(c,[Evidence("e","fictional",False,True)],rules).reasons), ["contradictory_evidence:e"])
    check("failed rule blocks", list(assess(c,e,[Rule("r","Synthetic",False)]).reasons), ["failed_rule:r"])
    check("digest excludes changing assessment timestamp", assess(c,e,rules).digest, r.digest)
    rejects("duplicate evidence ID", lambda: assess(c,e+e,rules))

if __name__ == "__main__":
    if sys.argv[1:] not in ([], ["--verify"]):
        raise SystemExit("Usage: python curriculum/lab.py [--verify]")
    run()
    report = {"schema_version": 1, "status": "PASS", "case_count": len(CASES),
              "cases": CASES, "scope": "Synthetic curriculum checks only"}
    if sys.argv[1:] == ["--verify"]:
        expected = json.loads((Path(__file__).parent / "expected.json").read_text())
        if report != expected:
            raise AssertionError("Observed answers differ from curriculum/expected.json")
    print(json.dumps(report, sort_keys=True, indent=2, allow_nan=False))
