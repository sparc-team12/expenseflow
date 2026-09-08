"""
Feature: FEAT-CLAIM-SUBMIT, FEAT-APPROVAL
Storage for claims. Uses DynamoDB when CLAIMS_TABLE is set,
otherwise an in-memory dict for local development.
"""
import os
from decimal import Decimal

TABLE_NAME = os.environ.get("CLAIMS_TABLE")

_memory: dict[str, dict] = {}
_table = None

if TABLE_NAME:
    import boto3
    _table = boto3.resource("dynamodb").Table(TABLE_NAME)


def _to_storage(claim: dict) -> dict:
    # DynamoDB rejects floats; it wants Decimal.
    out = dict(claim)
    out["amount"] = Decimal(str(claim["amount"]))
    return out


def _from_storage(item: dict) -> dict:
    out = dict(item)
    out["amount"] = float(item["amount"])
    return out


def save(claim: dict) -> dict:
    if _table:
        _table.put_item(Item=_to_storage(claim))
    else:
        _memory[claim["id"]] = claim
    return claim


def get(claim_id: str) -> dict | None:
    if _table:
        item = _table.get_item(Key={"id": claim_id}).get("Item")
        return _from_storage(item) if item else None
    return _memory.get(claim_id)


def list_all() -> list[dict]:
    if _table:
        return [_from_storage(i) for i in _table.scan().get("Items", [])]
    return list(_memory.values())