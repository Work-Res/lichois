from citizenship.service.handlers.postsave import AssessmentCaseDecisionHandler


def assessment_case_decision_post_save_handler(sender, instance, created, **kwargs):
    if created:
        role = instance.role
        handler = AssessmentCaseDecisionHandler(assessment_case_decision=instance, role=role)
        handler.transaction()
