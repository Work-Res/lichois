import logging
import ast

from django.conf import settings


class TaskRuleEvaluator(object):
    """Takes source object , and dict like valuesets to compares, return True or False"""

    logger = logging.getLogger(__name__)

    def predicate(self, source, conditions):
        # Check if the application is in debug mode and log the entry into the predicate function
        if settings.DEBUG:
            print("TaskRuleEvaluator.predicate")

        # List to keep track of the evaluation of all rules
        all_rules = []

        try:
            # Parse the conditions from a JSON string to a dictionary
            rules = ast.literal_eval(conditions)
            # print(rules)  # Debug print to show the parsed rules
            print(rules)
            # Iterate over each property and its expected value in the rules
            for prop, value in rules.items():
                if prop == "or":
                    or_result = self.handle_or_predicate(source, str(value))
                    print("The or result", or_result)
                    all_rules.append(or_result)
                else:
                    # Check if the source object has the property
                    if hasattr(source, prop):
                        # If the property is a dictionary, recursively evaluate it
                        if isinstance(getattr(source, prop), dict):
                            self.predicate(getattr(source, prop), value)
                        else:
                            # Evaluate the property against the expected value and append the result to all_rules
                            (
                                all_rules.append(True)
                                if getattr(source, prop) == value
                                else all_rules.append(False)
                            )
                    else:
                        # If the property does not exist in the source, append False to all_rules
                        all_rules.append(False)

            # Debug print to show the final result of all rule evaluations
            if settings.DEBUG:
                print("TaskRuleEvaluator.result: ", all(all_rules))

            # Return True if all rules are True, otherwise False
            return all(all_rules)
        except ValueError as e:
            # Handle and log any exceptions that occur during the parsing of conditions
            print(f"{e}")
            self.logger.debug("Failed to create rules from json string, got ", e)

    def handle_or_predicate(self, source, conditions):

        # List to keep track of the evaluation of all rules
        all_rules = []
        try:
            # Parse the conditions from a JSON string to a dictionary
            rules = ast.literal_eval(conditions)
            # print(rules)  # Debug print to show the parsed rules
            print("OR RULES", rules)
            # Iterate over each property and its expected value in the rules
            for prop, value in rules.items():
                # Check if the source object has the property
                if hasattr(source, prop):
                    # If the property is a dictionary, recursively evaluate it
                    if isinstance(getattr(source, prop), dict):
                        self.handle_or_predicate(getattr(source, prop), value)
                    else:
                        # Evaluate the property against the expected value and append the result to all_rules
                        (
                            all_rules.append(True)
                            if str(getattr(source, prop)) in str(value)
                            else all_rules.append(False)
                        )
                else:
                    # If the property does not exist in the source, append False to all_rules
                    all_rules.append(False)

            # Debug print to show the final result of all rule evaluations
            if settings.DEBUG:
                print("TaskRuleEvaluator.result: ", all(all_rules))

            # Return True if exists in rules are True, otherwise False
            return any(all_rules)
        except ValueError as e:
            # Handle and log any exceptions that occur during the parsing of conditions
            print(f"{e}")
            self.logger.debug("Failed to create rules from json string, got ", e)

    def __init__(self, source, rules):
        self.source = source
        self.rules = rules

    def evaluate(self):
        return self.predicate(self.source, self.rules)
