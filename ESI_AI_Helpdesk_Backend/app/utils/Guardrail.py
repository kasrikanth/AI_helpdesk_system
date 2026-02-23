# guardrail.py

from app.apis.api_schema import GuardrailStatus

CRITICAL_TERMS = {

    # Total Data Destruction
    "drop database",
    "wipe database",
    "destroy data",
    "corrupt database",

    # Full System Compromise
    "remote code execution",
    "rce payload",
    "reverse shell",
    "backdoor",
    "rootkit",

    # Malware / Extortion
    "ransomware",

    # Critical Infra Shutdown
    "shutdown server",
    "disable firewall",
    "bypass firewall",

    # Data Exfiltration at Scale
    "exfiltrate data",
    "data exfiltration",

    # Critical Legal / Criminal
    "fraud",
    "launder",

    # Severe Physical Threat
    "bomb",
    "weapon"
}

HIGH_TERMS = {

    # Destructive SQL / Data Manipulation
    "drop table",
    "truncate table",
    "delete production",
    "delete all",

    # Privilege Escalation
    "grant root",
    "grant superuser",
    "grant admin",
    "escalate privileges",
    "privilege escalation",

    # Authentication Bypass
    "bypass authentication",
    "bypass login",
    "disable auth",
    "disable mfa",

    # Exploits
    "sql injection",
    "xss attack",
    "cross-site scripting",
    "zero-day",
    "0day",
    "buffer overflow",
    "path traversal",
    "directory traversal",

    # Credential Attacks
    "steal credentials",
    "dump passwords",
    "brute force",
    "password spray",
    "credential stuffing",
    "api key leak",

    # Network Attacks
    "ddos",
    "dos attack",
    "syn flood",
    "man in the middle",
    "mitm",
    "arp spoofing",
    "dns spoofing",
    "ip spoofing",

    # Infra Tampering
    "disable logging",
    "disable monitoring",
    "clear audit trail",
    "overwrite logs",

    # Social Engineering
    "phish",
    "spear phish",
    "credential harvest",
    "impersonate user",
    "social engineer",
}

MEDIUM_TERMS = {

    # SQL Contextual
    "delete from",
    "rollback production",

    # Access Control Changes
    "revoke access",
    "remove permissions",

    # Malware Keywords (context-sensitive)
    "trojan",
    "virus payload",
    "worm payload",
    "malware",
    "spyware",
    "keylogger",

    # Network Recon
    "port scan",
    "network sniff",
    "packet flood",
    "ping flood",

    # Code Risk
    "inject malicious",
    "obfuscated code",

    # Security Configuration
    "disable ssl",
    "disable tls",
    "disable backup",
    "kill process",

    # Compliance / Legal
    "illegal",
    "violate gdpr",
    "violate hipaa",
    "bypass compliance",
    "counterfeit",

    # Social Engineering (soft forms)
    "fake login",
    "pretexting",

    # General Threat
    "threat"
}

def check_guardrail(message: str) -> GuardrailStatus:
    msg = message.lower()
    for term in CRITICAL_TERMS:
        if term in msg:
            return GuardrailStatus(blocked=True, reason=f"Restricted: '{term}'", severity="CRITICAL")
    for term in HIGH_TERMS:
        if term in msg:
            return GuardrailStatus(blocked=True, reason=f"Restricted: '{term}'", severity="HIGH")
    for term in MEDIUM_TERMS:
        if term in msg:
            return GuardrailStatus(blocked=True, reason=f"Restricted: '{term}'", severity="MEDIUM")
        
    return GuardrailStatus(blocked=False, reason=None, severity="LOW")

