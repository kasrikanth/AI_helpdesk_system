# classifier.py

from app.apis.pydantic_models import TierLevel, SeverityLevel

# LOW_IMPACT = ["what", "who", "when", "where", "help desk"]
# MEDIUM_IMPACT = ["reset", "password", "login", "troubleshoot", "how to"]
# HIGH_IMPACT = ["system down", "outage", "failure", "crash"]
# CRITICAL_IMPACT = ["delete production", "data loss", "security breach"]

TIER_4_KEYWORDS = ["data loss", "production down", "security breach"]
TIER_3_KEYWORDS = ["system down", "outage", "failure", "crash"]
TIER_2_KEYWORDS = ["reset", "password", "login", "troubleshoot", "how to"]
TIER_0_KEYWORDS = ["what", "who", "when", "where", "help desk"]

CRITICAL_KEYWORDS = ["data loss", "production down", "security breach"]
HIGH_KEYWORDS = ["system down", "container crashed", "service unavailable"]
MEDIUM_KEYWORDS = ["slow", "timeout", "login issue"]

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
