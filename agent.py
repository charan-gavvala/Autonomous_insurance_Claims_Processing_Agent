#!/usr/bin/env python3
"""Autonomous insurance claims triage agent.

This module provides deterministic first-pass claim triage with:
- input validation
- risk scoring
- payout recommendation
- CLI support for local runs
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal["low", "medium", "high"]
Decision = Literal["approve", "manual_review", "reject"]
IncidentType = Literal["collision", "theft", "injury", "fire", "other"]


@dataclass(frozen=True)
class Claim:
    claim_id: str
    amount: float
    policy_limit: float
    police_report: bool
    prior_fraud_flag: bool
    incident_type: IncidentType
    claimant_tenure_years: float


@dataclass(frozen=True)
class ClaimResult:
    claim_id: str
    risk_level: RiskLevel
    decision: Decision
    recommended_payout: float
    reason: str
    risk_score: int


def validate_claim(claim: Claim) -> None:
    if not claim.claim_id.strip():
        raise ValueError("claim_id must be non-empty")
    if claim.amount <= 0:
        raise ValueError("amount must be greater than 0")
    if claim.policy_limit <= 0:
        raise ValueError("policy_limit must be greater than 0")
    if claim.amount > claim.policy_limit * 2:
        raise ValueError("amount is implausibly above policy_limit")
    if claim.claimant_tenure_years < 0:
        raise ValueError("claimant_tenure_years cannot be negative")


def assess_risk(claim: Claim) -> int:
    score = 0

    if claim.amount > 15000:
        score += 3
    elif claim.amount > 5000:
        score += 1

    if claim.amount > claim.policy_limit:
        score += 4

    if not claim.police_report and claim.incident_type in {"collision", "theft", "injury", "fire"}:
        score += 2

    if claim.prior_fraud_flag:
        score += 4

    if claim.claimant_tenure_years < 1:
        score += 1

    if claim.incident_type == "injury":
        score += 1

    return score


def score_to_risk(score: int) -> RiskLevel:
    if score >= 7:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def recommend_payout(claim: Claim, risk_level: RiskLevel) -> float:
    capped = min(claim.amount, claim.policy_limit)
    multiplier = {"low": 1.0, "medium": 0.85, "high": 0.0}[risk_level]
    return round(capped * multiplier, 2)


def decide(claim: Claim) -> ClaimResult:
    validate_claim(claim)
    score = assess_risk(claim)
    risk_level = score_to_risk(score)

    if risk_level == "high":
        decision: Decision = "reject" if claim.prior_fraud_flag else "manual_review"
        reason = "High-risk claim requires fraud/investigation review."
    elif risk_level == "medium":
        decision = "manual_review"
        reason = "Moderate risk profile requires adjuster review."
    else:
        decision = "approve"
        reason = "Low-risk claim approved automatically."

    return ClaimResult(
        claim_id=claim.claim_id,
        risk_level=risk_level,
        decision=decision,
        recommended_payout=recommend_payout(claim, risk_level),
        reason=reason,
        risk_score=score,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Autonomous insurance claims triage agent")
    parser.add_argument("--claim-id", default="CLM-2026-0001")
    parser.add_argument("--amount", type=float, default=4200.0)
    parser.add_argument("--policy-limit", type=float, default=10000.0)
    parser.add_argument("--police-report", action="store_true", default=False)
    parser.add_argument("--prior-fraud-flag", action="store_true", default=False)
    parser.add_argument(
        "--incident-type",
        choices=["collision", "theft", "injury", "fire", "other"],
        default="collision",
    )
    parser.add_argument("--claimant-tenure-years", type=float, default=2.0)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    claim = Claim(
        claim_id=args.claim_id,
        amount=args.amount,
        policy_limit=args.policy_limit,
        police_report=args.police_report,
        prior_fraud_flag=args.prior_fraud_flag,
        incident_type=args.incident_type,
        claimant_tenure_years=args.claimant_tenure_years,
    )

    result = decide(claim)
    print("Autonomous Insurance Claims Processing Agent")
    print("-" * 48)
    print(f"Claim ID            : {result.claim_id}")
    print(f"Risk Score          : {result.risk_score}")
    print(f"Risk Level          : {result.risk_level}")
    print(f"Decision            : {result.decision}")
    print(f"Recommended Payout  : {result.recommended_payout}")
    print(f"Reason              : {result.reason}")


if __name__ == "__main__":
    main()
