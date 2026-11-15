"""Synthetic hospital operations metrics and what-if simulation.

For demonstrations only. Not a forecasting, triage, staffing, or clinical tool.
"""
from dataclasses import dataclass, asdict
from hashlib import sha256
import json
from math import isfinite


@dataclass(frozen=True)
class HospitalSnapshot:
    hospital_id: str
    beds_staffed: int
    beds_occupied: int
    ed_waiting: int
    ed_wait_minutes: float
    discharges_planned: int
    admissions_expected: int


@dataclass(frozen=True)
class OperationalReport:
    hospital_id: str
    occupancy_pct: float
    available_beds: int
    projected_occupied: int
    projected_occupancy_pct: float
    ed_waiting: int
    ed_wait_minutes: float
    flags: tuple[str, ...]
    scenario: str
    digest: str


def _integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")
    return value


def evaluate(snapshot: HospitalSnapshot, *, admission_delta: int = 0,
             discharge_delta: int = 0) -> OperationalReport:
    """Simple arithmetic what-if; no statistical predictions or clinical inference."""
    if not isinstance(snapshot, HospitalSnapshot):
        raise ValueError("Expected HospitalSnapshot")
    if not snapshot.hospital_id.startswith("synthetic-") or len(snapshot.hospital_id) > 80:
        raise ValueError("Synthetic hospital id required")
    for field in ("beds_staffed", "beds_occupied", "ed_waiting",
                  "discharges_planned", "admissions_expected"):
        _integer(getattr(snapshot, field), field)
    if snapshot.beds_staffed == 0 or snapshot.beds_occupied > snapshot.beds_staffed:
        raise ValueError("Invalid bed capacity")
    if type(snapshot.ed_wait_minutes) not in (int, float) or not isfinite(snapshot.ed_wait_minutes) or snapshot.ed_wait_minutes < 0:
        raise ValueError("Invalid ED wait")
    if type(admission_delta) is not int or type(discharge_delta) is not int:
        raise ValueError("Scenario deltas must be integers")
    admissions = snapshot.admissions_expected + admission_delta
    discharges = snapshot.discharges_planned + discharge_delta
    if admissions < 0 or discharges < 0 or discharges > snapshot.beds_occupied:
        raise ValueError("Scenario outside supported synthetic bounds")
    projected = snapshot.beds_occupied - discharges + admissions
    if projected < 0:
        raise ValueError("Negative projected occupancy")
    occupancy = round(100 * snapshot.beds_occupied / snapshot.beds_staffed, 1)
    projected_pct = round(100 * projected / snapshot.beds_staffed, 1)
    flags = []
    if projected > snapshot.beds_staffed:
        flags.append("projected_capacity_exceeded")
    if snapshot.ed_wait_minutes >= 120:
        flags.append("synthetic_ed_wait_threshold")
    if occupancy >= 90:
        flags.append("synthetic_high_occupancy_threshold")
    scenario = f"admissions_delta={admission_delta};discharges_delta={discharge_delta}"
    payload = {"snapshot": asdict(snapshot), "scenario": scenario, "flags": flags}
    digest = sha256(json.dumps(payload, sort_keys=True, allow_nan=False).encode()).hexdigest()
    return OperationalReport(
        snapshot.hospital_id, occupancy, snapshot.beds_staffed - snapshot.beds_occupied,
        projected, projected_pct, snapshot.ed_waiting,
        float(snapshot.ed_wait_minutes), tuple(flags), scenario, digest,
    )
