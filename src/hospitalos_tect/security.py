"""Prototype request authentication and access policy. NOT production security."""
from dataclasses import dataclass
from hashlib import sha256
from hmac import compare_digest
import os


@dataclass(frozen=True)
class Principal:
    tenant_id: str
    subject: str
    roles: frozenset[str]


def authenticate(authorization: str | None) -> Principal | None:
    """Single configured token, synthetic tenant only; fail closed by default."""
    expected = os.environ.get("HOSPITALOS_DEV_TOKEN", "")
    if not expected or len(expected) < 32 or not authorization:
        return None
    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token:
        return None
    if not compare_digest(sha256(token.encode()).digest(), sha256(expected.encode()).digest()):
        return None
    return Principal("synthetic-demo", "local-developer", frozenset({"assurance:assess"}))


def permitted(principal: Principal | None, tenant_id: str, permission: str) -> bool:
    return (
        principal is not None
        and bool(tenant_id)
        and principal.tenant_id == tenant_id
        and permission in principal.roles
    )
