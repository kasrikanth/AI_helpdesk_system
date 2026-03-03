# escalate_classifier.py

from app.apis.pydantic_models import TierLevel, SeverityLevel

TIER_4_KEYWORDS = [
    "catastrophic issue", "major incident", "business critical", "service collapse",
    "environment unavailable", "customer impact severe", "revenue blocked",
    "compliance violation", "regulatory breach"
]

TIER_3_KEYWORDS = [
    "partial disruption", "service instability", "intermittent failure",
    "unexpected behavior", "dependency issue", "integration broken",
    "deployment issue", "rollback required", "resource exhaustion"
]

TIER_2_KEYWORDS = [
    "account assistance", "access request", "configuration help", "usage guidance",
    "setup clarification", "feature explanation", "permission request",
    "environment setup", "connectivity issue"
]

TIER_1_KEYWORDS = [
    "general inquiry", "basic question", "clarification needed", "product info",
    "service details", "availability info", "pricing info", "support contact",
    "how does it work"
]


CRITICAL_KEYWORDS = [
    "data loss", "production down", "security breach", "database down",
    "site down", "full outage", "complete outage", "data leak",
    "ransomware", "system hacked"
]

HIGH_KEYWORDS = [
    "system down", "container crashed", "service unavailable", "api down",
    "internal server error", "500 error", "503 error", "authentication failure",
    "disk full", "high memory usage"
]

MEDIUM_KEYWORDS = [
    "slow", "timeout", "login issue", "latency", "performance issue",
    "job failed", "minor bug", "page not loading"
]

FORCE_TIER2_PATTERNS = [
    # Auth issues requiring human Support Engineer
    "vm clock", "clock is behind", "time drift", "ntp", "time synchronization",
    "session expires immediately", "logged out after",

    # Lab infrastructure issues requiring engineer
    "kernel panic", "stack trace", "kernel crash",
    "container init failed", "missing /opt/startup.sh",
    "vm frozen", "vm unresponsive", "lab unresponsive",
    "environment mismatch", "wrong environment", "wrong toolset",
    "mapping mismatch", "wrong range",

    # MFA resets always need a ticket
    "reset mfa", "mfa reset", "lost mfa", "new mfa device",
    "authenticator app lost", "mfa not working",
]

FORCE_TIER3_PATTERNS = [
    # Requests that violate security policy — flag immediately
    "disable logging", "disable log", "hide activity", "bypass logging",
    "run quietly", "no logs", "without logs", "avoid logging", "clear audit",
    "overwrite log","manually mount", "mount the file","mount startup",

    # Hypervisor / host OS access — always denied + escalated
    "hypervisor", "host os", "host shell", "ssh to host",
    "access host", "connect to host", "host-level",

    # Kernel/OS modification — out of scope for helpdesk
    "kernel module", "boot parameter", "modify kernel", "load driver",
    "edit /etc/hosts", "modify hosts file", "hosts entry",
    "docker command", "container image", "mount file",
]

FORCE_TIER3_HIGH_SEVERITY = [
    # These always need a senior engineer
    "kernel panic", "stack trace",
    "missing /opt/startup.sh",
    "multiple users", "all users affected", "cohort blocked",
]


def classify_tier(message: str, severity: SeverityLevel, kb_coverage: bool, repeated_failure: bool = False) -> TierLevel:
    msg = message.lower()

    # Critical severity or repeated failure always → Tier 3
    if severity == SeverityLevel.CRITICAL or repeated_failure:
        return TierLevel.TIER_3

    # Security policy violations / restricted requests → Tier 3
    if any(p in msg for p in FORCE_TIER3_PATTERNS):
        return TierLevel.TIER_3

    # High-severity platform issues → Tier 3
    if any(p in msg for p in FORCE_TIER3_HIGH_SEVERITY):
        return TierLevel.TIER_3

    #Issues requiring a Support Engineer → Tier 2
    if any(p in msg for p in FORCE_TIER2_PATTERNS):
        return TierLevel.TIER_2

    # No KB coverage
    if not kb_coverage:
        if severity in [SeverityLevel.CRITICAL, SeverityLevel.HIGH]:
            return TierLevel.TIER_3
        else:
            return TierLevel.TIER_2

    #Keyword fallback (least reliable — only reached if no rule above matched)
    if any(k in msg for k in TIER_4_KEYWORDS):
        return TierLevel.TIER_4
    if any(k in msg for k in TIER_3_KEYWORDS):
        return TierLevel.TIER_3
    if any(k in msg for k in TIER_2_KEYWORDS):
        return TierLevel.TIER_2
    if any(k in msg for k in TIER_1_KEYWORDS):
        return TierLevel.TIER_1

    return TierLevel.TIER_0

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


def should_escalate(tier: TierLevel, severity: SeverityLevel, kb_coverage: bool, repeated_failure: bool = False) -> bool:
    
    if tier in [TierLevel.TIER_2, TierLevel.TIER_3, TierLevel.TIER_4]:
        return True

    if severity == SeverityLevel.CRITICAL:
        return True

    if repeated_failure:
        return True

    if not kb_coverage and severity in [SeverityLevel.HIGH, SeverityLevel.MEDIUM]:
        return True

    return False