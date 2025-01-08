from enum import Enum

class MembershipType(Enum):
    monthly = "Monthly"
    quarterly = "quarterly"
    yearly = "Yearly"

class PaymentMethod(Enum):
    credit_card = "Credit Card"
    cash = "Cash"

class RoleType(Enum):
    TRAINER = "trainer"
    MANAGER = "manager"
    SECRETARY = "secretary"
