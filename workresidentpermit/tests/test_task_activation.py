import pytest

from ..classes import WorkResidentPermitTaskActivationRules


class TestRule:

    def __init__(self):
        self.previous_status = 'NEW'
        self.current_status = 'VERIFICATION'


class TestTaskActivation:

    def test_predicate(self):
        source = TestRule()
        rules = {
           "previous_status": 'NEW',
            "current_status": 'VERIFICATION'
        }
        rule = WorkResidentPermitTaskActivationRules(source=source, rules=rules)
        assert rule.execute() == True