"""Strict, synthetic-only FHIR R4 subset adapter for development.

Not a full FHIR validator, terminology service, or clinical data processor.
"""
from dataclasses import dataclass
import re

ID_PATTERN = re.compile(r"^[A-Za-z0-9.-]{1,64}$")
SUPPORTED = frozenset({"Patient", "Encounter", "Observation"})
ALLOWED_FIELDS = {
    "Patient": frozenset({"resourceType", "id", "meta", "active"}),
    "Encounter": frozenset({"resourceType", "id", "meta", "status", "subject"}),
    "Observation": frozenset({"resourceType", "id", "meta", "status", "code", "subject"}),
}
STATUS = {
    "Encounter": frozenset({"planned", "arrived", "triaged", "in-progress", "onleave", "finished", "cancelled"}),
    "Observation": frozenset({"registered", "preliminary", "final", "amended", "corrected", "cancelled", "entered-in-error", "unknown"}),
}


class FHIRValidationError(ValueError):
    pass


@dataclass(frozen=True)
class ResourceSummary:
    resource_type: str
    resource_id: str
    synthetic: bool


def _reference(value: object) -> None:
    if not isinstance(value, dict) or set(value) != {"reference"}:
        raise FHIRValidationError("Only simple local references are supported")
    ref = value["reference"]
    if not isinstance(ref, str) or not re.fullmatch(r"Patient/[A-Za-z0-9.-]{1,64}", ref):
        raise FHIRValidationError("Only Patient/{synthetic-id} references are allowed")
    if not ref.startswith("Patient/synthetic-"):
        raise FHIRValidationError("Patient reference must use synthetic- prefix")


def validate_synthetic_resource(resource: object) -> ResourceSummary:
    """Reject all unexpected fields to avoid accidental patient data ingestion."""
    if not isinstance(resource, dict):
        raise FHIRValidationError("Resource must be an object")
    kind = resource.get("resourceType")
    if not isinstance(kind, str) or kind not in SUPPORTED:
        raise FHIRValidationError("Unsupported resource type")
    unexpected = set(resource) - ALLOWED_FIELDS[kind]
    if unexpected:
        raise FHIRValidationError("Unexpected fields: " + ", ".join(sorted(unexpected)))
    rid = resource.get("id")
    if not isinstance(rid, str) or not ID_PATTERN.fullmatch(rid) or not rid.startswith("synthetic-"):
        raise FHIRValidationError("Synthetic resource id required")
    meta = resource.get("meta")
    if not isinstance(meta, dict) or set(meta) != {"tag"}:
        raise FHIRValidationError("Synthetic meta.tag required")
    tags = meta["tag"]
    if not isinstance(tags, list) or len(tags) != 1 or tags[0] != {
        "system": "https://hospitalos-tect.example/tags",
        "code": "synthetic",
    }:
        raise FHIRValidationError("Explicit synthetic tag required")
    if kind == "Patient":
        if type(resource.get("active")) is not bool:
            raise FHIRValidationError("Patient.active must be boolean")
    else:
        if not isinstance(resource.get("status"), str) or resource["status"] not in STATUS[kind]:
            raise FHIRValidationError("Invalid resource status")
        _reference(resource.get("subject"))
        if kind == "Observation":
            code = resource.get("code")
            if code != {"text": "synthetic-operational-signal"}:
                raise FHIRValidationError("Only synthetic operational signal supported")
    return ResourceSummary(kind, rid, True)


def validate_synthetic_bundle(bundle: object) -> tuple[ResourceSummary, ...]:
    if not isinstance(bundle, dict) or set(bundle) != {"resourceType", "type", "entry"}:
        raise FHIRValidationError("Only minimal synthetic bundles supported")
    if bundle["resourceType"] != "Bundle" or bundle["type"] != "collection":
        raise FHIRValidationError("Bundle must be a collection")
    entries = bundle["entry"]
    if not isinstance(entries, list) or not 1 <= len(entries) <= 100:
        raise FHIRValidationError("Bundle must contain 1-100 entries")
    summaries = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"resource"}:
            raise FHIRValidationError("Bundle entry must contain only resource")
        summaries.append(validate_synthetic_resource(entry["resource"]))
    keys = [(s.resource_type, s.resource_id) for s in summaries]
    if len(set(keys)) != len(keys):
        raise FHIRValidationError("Duplicate resources")
    patients = {s.resource_id for s in summaries if s.resource_type == "Patient"}
    for entry in entries:
        resource = entry["resource"]
        if resource["resourceType"] != "Patient":
            patient_id = resource["subject"]["reference"].split("/", 1)[1]
            if patient_id not in patients:
                raise FHIRValidationError("Referenced synthetic patient missing")
    return tuple(summaries)
