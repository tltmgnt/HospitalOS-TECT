# Phase 6 — Synthetic Hospital Command Center

This phase adds a deterministic hospital operations calculator and a static HTML dashboard generator. All inputs must use a `synthetic-` hospital identifier. The example includes generated counts only, never patient-level information.

## Run

```sh
PYTHONPATH=src python examples/command_center.py
```

Open the generated `synthetic-command-center.html` locally.

## Metrics and scenario assumptions

Occupancy = occupied beds / staffed beds. Available beds = staffed - occupied. Scenario projected occupied beds = occupied - planned discharges + expected admissions + admission delta - discharge delta.

This is a transparent arithmetic what-if, **not** a calibrated digital twin, patient-flow forecast, validated capacity model, or real-time dashboard. Threshold flags are synthetic demonstration settings, not clinical or operational recommendations.

## Safety

No EHR integration, PHI, identity management, or live data pipeline. No hospital should use this prototype for patient care, staffing, or capacity decisions. Future work requires real-world data governance, validated models, uncertainty quantification, operational review, and secure authorization.
