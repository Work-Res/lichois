import logging

from app_pdf_utilities.classes import ConvertHtmlToPdf
from .work_resident_permit_data import WorkResidentPermitData
from .report_details import ReportDetails

from django.conf import settings


class WorkPermitApplicationPDFGenerator:
    EXT = ".pdf"

    def __init__(self, work_resident_permit):
        self.work_resident_permit = work_resident_permit
        self.logger = logging.getLogger("workresidentpermit")

    def prepare_application(self):
        process_name = self.work_resident_permit.application_version.application.process_name \
            if self.work_resident_permit else ""
        data = {}
        data.update({
            'application_type': process_name,
            'application_status': self.work_resident_permit.application_version.application_status.name
        })
        return data

    def generate(self):
        self.logger.info("Preparing to generate summary PDF data.")

        file_name = f"work_resident_permit_summary_{self.work_resident_permit.document_number}{self.EXT}"

        work_permit_data = WorkResidentPermitData(document_number=self.work_resident_permit.document_number)
        application_summary_data = work_permit_data.prepare()
        report = ReportDetails(name="Application Summary", department=settings.DEPARTMENT)
        application_summary_data.report_details = report

        data = application_summary_data.__dict__
        data.update(self.prepare_application(self))

        pdf_generator = ConvertHtmlToPdf()
        pdf = pdf_generator.convert_html_to_pdf(
            context=application_summary_data,
            template_path=settings.PDF_TEMPLATE_WORKRESIDENTPERMIT,
            file_name=file_name
        )
        self.logger.info(f"Completed generation of PDF document for {self.work_resident_permit.document_number}")
        if pdf:
            return file_name
