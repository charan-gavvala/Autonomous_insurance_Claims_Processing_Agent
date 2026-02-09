import pytest

from agent import Claim, decide


def test_low_risk_auto_approve():
    claim = Claim(
        claim_id="C1",
        amount=1200.0,
        policy_limit=5000.0,
        police_report=True,
        prior_fraud_flag=False,
        incident_type="other",
        claimant_tenure_years=5,
    )
    result = decide(claim)
    assert result.risk_level == "low"
    assert result.decision == "approve"
    assert result.recommended_payout == 1200.0


def test_medium_risk_manual_review_with_discounted_payout():
    claim = Claim(
        claim_id="C2",
        amount=7000.0,
        policy_limit=9000.0,
        police_report=False,
        prior_fraud_flag=False,
        incident_type="collision",
        claimant_tenure_years=0.5,
    )
    result = decide(claim)
    assert result.risk_level == "medium"
    assert result.decision == "manual_review"
    assert result.recommended_payout == 5950.0


def test_high_risk_with_prior_fraud_rejected():
    claim = Claim(
        claim_id="C3",
        amount=16000.0,
        policy_limit=15000.0,
        police_report=False,
        prior_fraud_flag=True,
        incident_type="injury",
        claimant_tenure_years=0.1,
    )
    result = decide(claim)
    assert result.risk_level == "high"
    assert result.decision == "reject"
    assert result.recommended_payout == 0.0


def test_validation_for_invalid_amount():
    claim = Claim(
        claim_id="C4",
        amount=0.0,
        policy_limit=5000.0,
        police_report=True,
        prior_fraud_flag=False,
        incident_type="other",
        claimant_tenure_years=1,
    )
    with pytest.raises(ValueError, match="amount must be greater than 0"):
        decide(claim)
