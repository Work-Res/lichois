
import rules

from workflow.classes import TaskRuleEvaluator


@rules.predicate
def can_create_or_update_task(source, conditions):
    run_rules = TaskRuleEvaluator(source=source, rules=conditions)
    return run_rules.predicate(source, conditions)


@rules.predicate
def update_task(source, conditions):
    run_rules = TaskRuleEvaluator(source=source, rules=conditions)
    return run_rules.predicate(source, conditions)


workflow = rules.RuleSet()
workflow.add_rule("FIRST_VERIFICATION", can_create_or_update_task)
workflow.add_rule("SECOND_VERIFICATION", can_create_or_update_task)

workflow_close = rules.RuleSet()
workflow_close.add_rule("FIRST_VERIFICATION", update_task)
workflow_close.add_rule("SECOND_VERIFICATION", update_task)
