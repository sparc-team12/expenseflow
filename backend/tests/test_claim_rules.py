from app.domain.claim_rules import validate_claim, next_status


def test_valid_claim_has_no_errors():
    assert validate_claim(500, "Food", "Team lunch") == []


def test_zero_amount_is_rejected():
    assert "Amount must be greater than 0" in validate_claim(0, "Food", "x")


def test_unknown_category_is_rejected():
    assert any("Category must be one of" in e for e in validate_claim(10, "Travel", "x"))


def test_submitted_claim_can_be_approved():
    assert next_status("submitted", "approve") == "approved"