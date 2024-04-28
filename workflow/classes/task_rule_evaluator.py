import json
import logging
import ast


class TaskRuleEvaluator(object):
    """ Takes source object , and dict like valuesets to compares, return True or False
    """
    def predicate(self, source, conditions):
        self.logger = logging.getLogger(__name__)
        all_rules = []
        try:
            rules = ast.literal_eval(conditions)
            for prop, value in rules.items():
                if hasattr(source, prop):
                    if isinstance(getattr(source, prop), dict):
                        self.predicate(getattr(source, prop), value)
                    else:
                        all_rules.append(True) if getattr(source, prop) == value else all_rules.append(False)
            return all(all_rules)
        except ValueError as e:
            self.logger.debug("Failed to create rules from json string, got ", e)

    def __init__(self, source, rules):
        self.source = source
        self.rules = rules

    def evaluate(self):
        return self.predicate(self.source, self.rules)
