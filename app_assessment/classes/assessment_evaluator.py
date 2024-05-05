import logging
import ast


class AssessmentEvaluator(object):
    """ Takes source object , and dict like valuesets to compares, return True or False
    """
    def __init__(self, source, rules):
        self.source = source
        self.rules = rules
        self.results = []
        self.points_list = {}
        self.flatten_criteria()
        self.assessment_results = {}

    def flatten_criteria(self):
        for prop, value in self.rules.items():
            if isinstance(value, dict):
                self.points_list.update(value)

    def predicate(self, source, conditions):
        self.logger = logging.getLogger("app_assessment")
        try:
            rules = ast.literal_eval(str(conditions))
            for prop, value in rules.items():
                if hasattr(source, prop):
                    if isinstance(getattr(source, prop), dict):
                        self.predicate(getattr(source, prop), value)
                    else:
                        obtained_value = self.points_list.get(getattr(source, prop))
                        if obtained_value:
                            self.results.append(self.points_list.get(getattr(source, prop)))
        except ValueError as e:
            self.logger.debug("Failed to create rules from json string, got ", e)

    def evaluate(self):
        return self.predicate(self.source, self.rules)

    def calculate_score(self):
        return sum(self.results)
