# guardrail.py

from app.apis.api_schema import GuardrailStatus

RISKY_TERMS = [
    # Database / Destructive Operations
    "delete production", "drop table", "drop database", "truncate table",
    "delete from", "delete all", "wipe database", "destroy data",
    "rollback production", "disable backup",

    # Privilege Escalation & Access Control
    "grant admin", "grant root", "grant superuser", "revoke access",
    "bypass authentication", "bypass login", "disable auth",
    "disable mfa", "remove permissions", "escalate privileges",

    # Hacking & Exploitation
    "hack", "exploit", "zero-day", "0day", "buffer overflow",
    "sql injection", "xss attack", "cross-site scripting",
    "remote code execution", "rce payload", "reverse shell",
    "privilege escalation", "path traversal", "directory traversal",

    # Malware & Malicious Code
    "ransomware", "keylogger", "rootkit", "trojan", "backdoor",
    "botnet", "malware", "spyware", "worm payload", "virus payload",
    "inject malicious", "obfuscated code",

    # Network Attacks
    "ddos", "dos attack", "syn flood", "ping flood", "packet flood",
    "port scan", "network sniff", "man in the middle", "mitm",
    "arp spoofing", "dns spoofing", "ip spoofing",

    # Social Engineering & Phishing
    "phish", "spear phish", "credential harvest", "fake login",
    "impersonate user", "social engineer", "pretexting",

    # Credential & Secret Theft
    "steal credentials", "dump passwords", "password spray",
    "brute force", "credential stuffing", "api key leak",
    "expose secret", "exfiltrate data", "data exfiltration",

    # Infrastructure Sabotage
    "security breach", "disable firewall", "disable logging",
    "disable monitoring", "kill process", "shutdown server",
    "corrupt database", "overwrite logs", "clear audit trail",
    "bypass firewall", "disable ssl", "disable tls",

    # Legal / Compliance Risk
    "illegal", "violate gdpr", "violate hipaa", "bypass compliance",
    "launder", "fraud", "counterfeit",

    # Physical Threats
    "bomb", "threat", "weapon",
]


def check_guardrail(message: str) -> GuardrailStatus:
    msg = message.lower()

    for term in RISKY_TERMS:
        if term in msg:
            return GuardrailStatus(
                blocked=True,
                reason=f"Detected restricted request: '{term}'",
                severity="HIGH"
            )

    return GuardrailStatus(blocked=False, reason=None, severity="LOW")

