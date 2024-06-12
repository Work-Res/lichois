import logging

from datetime import date

from app_checklist.models import Classifier, ClassifierItem
from workflow.models import BusinessProcess, Activity


class WorkflowEvent(object):

    def __init__(self, application):
        self.application = application
        self.bussiness_process = None
        self.logger = logging.getLogger('workflow')

    def create_workflow_process(self):
        """
        Searches for business process in the classifier records then create workflow models based on that.
        """
        print("self.application.process_name: ", self.application.process_name)
        classifer = None
        try:
            classifer = Classifier.objects.get(
                code=self.application.process_name
            )
        except Classifier.DoesNotExist:
            self.logger.debug(f"No workflow exits for {self.application.process_name}.")
            pass
        if classifer:
            self.logger.debug(f"Found workflow {self.application.process_name}.")
            classifier_items = ClassifierItem.objects.filter(classifier=classifer)
            self.bussiness_process = BusinessProcess.objects.create(
                name=classifer.code,
                description=classifer.description,
                document_number=self.application.application_document.document_number
            )
            self.logger.debug(f"Created business process: {self.bussiness_process.name}.")
            for item in classifier_items:
                Activity.objects.create(
                    name=item.code,
                    process=self.bussiness_process,
                    sequence=item.sequence,
                    description=item.description,
                    create_task_rules=item.create_task_rules,
                    valid_from=date.today()
                )
                self.logger.debug(
                    f"Created task activity {self.application.application_document.document_number}"
                    f"-  {item.name}.")
