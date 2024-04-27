import rules

from workflow.classes import TaskRuleEvaluator


@rules.predicate
def can_create_or_update_task(source, conditions):
    run_rules = TaskRuleEvaluator(source=source, conditions=conditions)
    return run_rules.predicate(source, conditions)


work_resident_permit_rules = rules.RuleSet()
work_resident_permit_rules.add_rule("first_verification_task", can_create_or_update_task)
work_resident_permit_rules.add_rule("second_verification_task", can_create_or_update_task)
work_resident_permit_rules.add_rule("vetting_task", can_create_or_update_task)
work_resident_permit_rules.add_rule("commitee_decision_task", can_create_or_update_task)
work_resident_permit_rules.add_rule("final_decision", can_create_or_update_task)
