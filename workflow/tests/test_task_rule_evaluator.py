from django.test import TestCase

from ..classes import TaskRuleEvaluator


class TestDataRuleOR(object):

    def __init__(self):
        self.previous_status = 'NEW'
        self.field1 = '1'
        self.field2 = '3'
        self.minister_decision = "accepted"

class TestDataRule(object):

    def __init__(self):
        self.previous_status = 'NEW'
        self.current_status = 'VERIFICATION'


class TestDataRule1:

    def __init__(self, data):
        self.data = data
        self.previous_status_1 = 'NEW'
        self.current_status_1 = 'VERIFICATION'

class SourceModel:

    def __init__(self, previous_status=None, current_status=None, next_activity_name=None, verification_decision=None,
                 board_decision=None, security_decision=None):
        self.previous_status = previous_status
        self.current_status = current_status
        self.verification_decision = verification_decision
        self.board_decision = board_decision
        self.security_decision = security_decision
        self.next_activity_name = next_activity_name


class TestTaskRuleEvaluator(TestCase):

    def test_predicate_when_values_exists(self):
        source = TestDataRule()
        rules = "{'previous_status': 'NEW', 'current_status': 'VERIFICATION'}"
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertTrue(rule.evaluate())

    def test_predicate_when_values_not_exists(self):
        source = TestDataRule()
        rules = "{ 'previous_status_1': 'NEW', 'current_status_1': 'VERIFICATION'}"
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertFalse(rule.evaluate())

    def test_predicate_nested_object_when_values_exists(self):
        data = TestDataRule()
        source = TestDataRule1(data=data)
        rules = "{'previous_status_1': 'NEW','current_status_1': 'VERIFICATION'}"
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertTrue(rule.evaluate())

    def test_evaluator_with_source(self):
        source = SourceModel(
            previous_status="NEW",
            current_status="VERIFICATION",
            next_activity_name="SECOND_VERIFICATION"
        )

        rules = '{"previous_status": "NEW", "current_status": "VERIFICATION", "next_activity_name": "SECOND_VERIFICATION"}'

        evaluator = TaskRuleEvaluator(source, rules)
        result = evaluator.evaluate()
        self.assertTrue(result)

        print("Evaluation Result:", result)

    def test_predicate_when_rules_exists_or_condition(self):
        source = TestDataRuleOR()
        rules = '{"previous_status": "NEW", "or": {"field1": 1, "field2": 2}}'
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertTrue(rule.evaluate())

    def test_predicate_when_rules_exists_or_condition_1(self):
        source = TestDataRuleOR()
        source.previous_status = "NEW"
        source.field1 = 1
        source.field2 = 3
        rules = '{"previous_status": "NEW", "or": {"field1": 1, "field2": 2}}'
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertTrue(rule.evaluate())

    def test_predicate_when_rules_exists_or_condition_2(self):
        source = TestDataRuleOR()
        source.previous_status = "NEW"
        source.field1 = 5
        source.field2 = 6
        rules = '{"previous_status": "NEW", "or": {"field1": 1, "field2": 2}}'
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertFalse(rule.evaluate())

    def test_predicate_when_rules_exists_or_condition_3(self):
        source = TestDataRuleOR()
        source.previous_status = "NEW"
        source.minister_decision = "rejected"

        rules = '{"previous_status": "NEW", "or": {"minister_decision": "accepted|rejected"}}'
        rule = TaskRuleEvaluator(source=source, rules=rules)
        self.assertTrue(rule.evaluate())
