import logging

from datetime import date

from app_checklist.models import Classifier, ClassifierItem
from workflow.models import BusinessProcess, Activity


class WorkflowEvent(object):

    def __init__(self, application):
        self.application = application
        self.bussiness_process = None
        self.logger = logging.getLogger("workflow")
        self.logger.setLevel(logging.DEBUG)

    def create_workflow_process(self):
        """
        Searches for business process in the classifier records then create workflow models based on that.
        """
        self.logger.info(
            "self.application.process_name: ", self.application.process_name
        )
        try:
            classifier = Classifier.objects.get(code=self.application.process_name)
        except Classifier.DoesNotExist:
            self.logger.debug(f"No workflow exits for {self.application.process_name}.")
            pass
        else:
            self.logger.debug(f"Found workflow {self.application.process_name}.")
            classifier_items = ClassifierItem.objects.filter(classifier=classifier)
            self.bussiness_process = BusinessProcess.objects.create(
                name=classifier.code,
                description=classifier.description,
                document_number=self.application.application_document.document_number,
            )
            self.logger.debug(
                f"Created business process: {self.bussiness_process.name}."
            )
            for item in classifier_items:
                Activity.objects.create(
                    name=item.code,
                    process=self.bussiness_process,
                    sequence=item.sequence,
                    description=item.description,
                    create_task_rules=item.create_task_rules,
                    next_activity_name=item.next_activity_name,
                    valid_from=date.today(),
                )
                self.logger.debug(
                    f"Created task activity {self.application.application_document.document_number}"
                    f"-  {item.name}."
                )
