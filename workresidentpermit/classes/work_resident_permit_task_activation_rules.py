

class WorkResidentPermitTaskActivationRules(object):
    """

    """
    def predicate(self, source, conditions):
        all_rules = []
        for prop, value in conditions.items():
            if hasattr(source, prop):
                if isinstance(getattr(source, prop), dict):
                    self.predicate(getattr(source, prop), value)
                else:
                    all_rules.append(True) if getattr(source, prop) == value else all_rules.append(False)

        return all(all_rules)

    def __init__(self, source, rules):
        self.source = source
        self.rules = rules

    def execute(self):
        self.predicate(self.source, self.rules)
