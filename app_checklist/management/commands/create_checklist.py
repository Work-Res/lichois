import os

from django.core.management.base import BaseCommand


class CreateChecklist(BaseCommand):
    help = 'This is management command to create checklist data'

    def add_arguments(self, parser):
        parser.add_argument('create', type=str, help='Create system classifier for document types')

    def handle(self, *args, **kwargs):
        parameter = kwargs['create']
        file_name = "attachment_documents.json"
        output_file = os.path.join(os.getcwd(), "app_checklist", "data", file_name)
        create = CreateChecklist()
        create.create(file_location=output_file)
        self.stdout.write(self.style.SUCCESS(f'Create or Update document types: {parameter}'))
