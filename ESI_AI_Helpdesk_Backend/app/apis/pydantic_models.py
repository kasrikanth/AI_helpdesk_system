# pydantic_models.py
from enum import Enum

# class UserRole(str, Enum):
#     trainee = "trainee"
#     operator = "operator"
#     admin = "admin"
#     instructor = "instructor"
#     support_engineer = "support_engineer"


class TierLevel(str, Enum):
    TIER_0 = "TIER_0"
    TIER_1 = "TIER_1"
    TIER_2 = "TIER_2"
    TIER_3 = "TIER_3"
    TIER_4 = "TIER_4"


class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
