import logging
import ast


class AssessmentEvaluator(object):
    """ Takes source object , and dict like valuesets to compares, return True or False
    """
    def __init__(self, source, rules, exclude_fields=[]):
        self.exclude_fields = exclude_fields or ["maximum_points", "pass_mark", "totals"]
        self.source = source
        self.rules = rules
        self.results = []
        self.points_list = {}
        self.flatten_criteria()
        self.assessment_results = {}
        self.logger = logging.getLogger("app_assessment")

    def flatten_criteria(self):
        for prop, value in self.rules.items():
            if prop not in self.exclude_fields:
                if isinstance(value, dict):
                    self.points_list.update(value)

    def update_data(self, source, prop, value):
        if hasattr(source, prop):
            if isinstance(getattr(source, prop), dict):
                self.predicate(getattr(source, prop), value)
            else:
                if getattr(source, prop):
                    obtained_value = self.points_list.get(prop)
                    if obtained_value:
                        self.assessment_results.update({prop: obtained_value})
                        self.results.append(obtained_value)

    def predicate(self, source, conditions):
        try:
            rules = ast.literal_eval(str(conditions))
            for prop, value in rules.items():
                if isinstance(value, dict):
                    for prop, value in value.items():
                        self.update_data(source, prop, value)
                else:
                    self.update_data(source, prop, value)
        except ValueError as e:
            self.logger.debug("Failed to create rules from json string, got ", e)

    def evaluate(self):
        return self.predicate(self.source, self.rules)

    def calculate_score(self):
        return sum(self.results)
