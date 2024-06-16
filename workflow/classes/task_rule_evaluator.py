import logging
import ast

from django.conf import settings


class TaskRuleEvaluator(object):
    """ Takes source object , and dict like valuesets to compares, return True or False
    """
    def predicate(self, source, conditions):
        if settings.DEBUG:
            print("TaskRuleEvaluator.predicate")
        self.logger = logging.getLogger(__name__)
        all_rules = []
        try:
            rules = ast.literal_eval(conditions)
            print(rules)
            for prop, value in rules.items():
                if hasattr(source, prop):
                    if isinstance(getattr(source, prop), dict):
                        self.predicate(getattr(source, prop), value)
                    else:
                        all_rules.append(True) if getattr(source, prop) == value else all_rules.append(False)
                else:
                    all_rules.append(False)
            if settings.DEBUG:
                print("TaskRuleEvaluator.result: ", all(all_rules))
            return all(all_rules)
        except ValueError as e:
            print(f"{e}")
            self.logger.debug("Failed to create rules from json string, got ", e)

    def __init__(self, source, rules):
        self.source = source
        self.rules = rules

    def evaluate(self):
        return self.predicate(self.source, self.rules)
