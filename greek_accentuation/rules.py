# This module defines the Rule class which lists the accentuation rules for which exceptions must be made.
from greek_accentuation.accentuation import Accentuation

class Rule:
    def __init__(self, description:str, accentuation:Accentuation):
        self.description = description
        self.accentuation = accentuation

    def __repr__(self):
        return f"Rule(description={self.description})"