"""
Feature: FEAT-CLAIM-SUBMIT
Business rules for expense claim submission.
Every rule below maps to an acceptance criterion in Jira.
"""

VALID_CATEGORIES = ["Food", "Lodging", "Supplies"]


def validate_claim(amount: float, category: str, description: str) -> list[str]:
    """Returns a list of error messages. Empty list means the claim is valid."""
    errors = []

    # AC-1: amount must be greater than zero
    if amount <= 0:
        errors.append("Amount must be greater than 0")

    # AC-2: category must be one of the allowed values
    if category not in VALID_CATEGORIES:
        errors.append(f"Category must be one of: {', '.join(VALID_CATEGORIES)}")

    # AC-3: description is mandatory
    if not description or not description.strip():
        errors.append("Description is required")

    return errors


def next_status(current: str, action: str) -> str:
    """
    Feature: FEAT-APPROVAL
    AC-1: a submitted claim can be approved or rejected
    """
    if current != "submitted":
        raise ValueError(f"Cannot {action} a claim in status '{current}'")
    return "approved" if action == "approve" else "rejected"