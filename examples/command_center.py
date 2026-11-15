"""Run with PYTHONPATH=src python examples/command_center.py.

Writes a self-contained HTML dashboard with *synthetic* operational metrics.
"""
from dataclasses import asdict
from html import escape
from pathlib import Path
from hospitalos_tect.operations import HospitalSnapshot, evaluate

snapshot = HospitalSnapshot("synthetic-hospital-a", 120, 102, 14, 135.0, 12, 20)
baseline = evaluate(snapshot)
surge = evaluate(snapshot, admission_delta=15)
rows = [
    ("Staffed beds", snapshot.beds_staffed),
    ("Occupied beds", snapshot.beds_occupied),
    ("Occupancy", f"{baseline.occupancy_pct}%"),
    ("Available beds", baseline.available_beds),
    ("ED waiting", baseline.ed_waiting),
    ("ED wait (minutes)", baseline.ed_wait_minutes),
    ("Projected occupancy", f"{baseline.projected_occupancy_pct}%"),
    ("Surge scenario (+15 admissions)", f"{surge.projected_occupancy_pct}%"),
]
cards = "".join(f"<article><span>{escape(str(label))}</span><strong>{escape(str(value))}</strong></article>" for label, value in rows)
flags = ", ".join(baseline.flags) or "None"
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>HospitalOS TECT — Synthetic Command Center</title>
<style>
body{{font:16px system-ui,sans-serif;margin:0;background:#0b1324;color:#edf3ff}}
main{{max-width:1000px;margin:auto;padding:36px 22px}}
header{{border-bottom:1px solid #31405b;margin-bottom:25px}}
small{{color:#9fb4d0}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}}
article{{padding:20px;border:1px solid #304364;border-radius:14px;background:#17243b;display:grid;gap:12px}}
article span{{color:#b5c7df}}article strong{{font-size:30px}}.notice{{margin-top:24px;padding:16px;border:1px solid #a77837;border-radius:12px}}
</style></head><body><main><header><small>HOSPITALOS | TECT · PHASE 6</small>
<h1>Hospital Command Center</h1><p>Demonstration using generated synthetic data only</p></header>
<section class="grid">{cards}</section><div class="notice"><strong>Simulation only — not operational guidance</strong>
<p>Threshold flags: {escape(flags)}</p><p>No live EHR feeds, patient records, predictions, or clinical decision support.</p>
<small>Baseline digest: {escape(baseline.digest)}</small></div></main></body></html>"""
output = Path("synthetic-command-center.html")
output.write_text(page, encoding="utf-8")
print(f"Wrote {output.resolve()}")
