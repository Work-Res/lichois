from viewflow import jsonstore
from viewflow.workflow.models import Process


class ApplicationProcess(Process):
    document_number = jsonstore.CharField(max_length=100)
    application_id = jsonstore.CharField(max_length=100)
    text = jsonstore.CharField(max_length=150)
    decision = jsonstore.BooleanField(default=False)

    class Meta:
        proxy = True
