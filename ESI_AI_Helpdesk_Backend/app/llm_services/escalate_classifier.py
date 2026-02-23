# classifier.py

from app.apis.pydantic_models import TierLevel, SeverityLevel

TIER_4_KEYWORDS = [
    "catastrophic issue", "major incident", "business critical","service collapse", "environment unavailable", 
    "customer impact severe", "revenue blocked", "compliance violation", "regulatory breach"
]

TIER_3_KEYWORDS = [
    "partial disruption", "service instability", "intermittent failure", "unexpected behavior", 
    "dependency issue", "integration broken",  "deployment issue", "rollback required", 
    "resource exhaustion"
]

TIER_2_KEYWORDS = [
    "account assistance", "access request",  "configuration help", "usage guidance", "setup clarification",
    "feature explanation", "permission request", "environment setup", "connectivity issue"
]

TIER_0_KEYWORDS = [
    "general inquiry", "basic question", "clarification needed", "product info", 
    "service details", "availability info", "pricing info", "support contact", "how does it work"
]


CRITICAL_KEYWORDS = ["data loss", "production down", "security breach", "database down", "site down", "full outage", "complete outage", "data leak", "ransomware", "system hacked"]
HIGH_KEYWORDS = ["system down", "container crashed", "service unavailable", "api down", "internal server error", "500 error", "503 error", "authentication failure", "disk full", "high memory usage"]
MEDIUM_KEYWORDS = ["slow","timeout","login issue","latency", "performance issue","job failed","minor bug","page not loading",]


def classify_tier(message: str, severity, kb_coverage, repeated_failure=False):
    msg = message.lower()

    # RULE 1: Critical or repeated failure
    if severity == SeverityLevel.CRITICAL or repeated_failure:
        return TierLevel.TIER_3

    # RULE 2: No KB Coverage
    if not kb_coverage:
        if severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
            return TierLevel.TIER_3
        else:
            return TierLevel.TIER_2

    # RULE 3: Keyword tier mapping
    if any(k in msg for k in TIER_4_KEYWORDS):
        return TierLevel.TIER_4
    if any(k in msg for k in TIER_3_KEYWORDS):
        return TierLevel.TIER_3
    if any(k in msg for k in TIER_2_KEYWORDS):
        return TierLevel.TIER_2
    if any(k in msg for k in TIER_0_KEYWORDS):
        return TierLevel.TIER_0

    return TierLevel.TIER_1

def classify_severity(message: str) -> SeverityLevel:
    msg = message.lower()

    if any(k in msg for k in CRITICAL_KEYWORDS):
        return SeverityLevel.CRITICAL
    elif any(k in msg for k in HIGH_KEYWORDS):
        return SeverityLevel.HIGH
    elif any(k in msg for k in MEDIUM_KEYWORDS):
        return SeverityLevel.MEDIUM
    else:
        return SeverityLevel.LOW
    
def should_escalate(tier, severity, kb_coverage, repeated_failure=False):

    if tier in [TierLevel.TIER_3, TierLevel.TIER_4]:
        return True

    if severity == SeverityLevel.CRITICAL:
        return True

    if repeated_failure:
        return True

    if not kb_coverage and severity in [
        SeverityLevel.HIGH,
        SeverityLevel.MEDIUM
    ]:
        return True

    return False

