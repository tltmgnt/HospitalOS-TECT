"""Run with PYTHONPATH=src python examples/adversarial_campaign.py."""
from dataclasses import asdict
import json
from hospitalos_tect import Claim, Evidence, Rule
from hospitalos_tect.adversarial import run_campaign

result = run_campaign(
    Claim("synthetic-capacity", "Synthetic capacity report", ("synthetic-evidence",)),
    [Evidence("synthetic-evidence", "generated-demo", True, True)],
    [Rule("manual-review", "Review gate", True)],
)
print(json.dumps(asdict(result), indent=2))
