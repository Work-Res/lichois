from docx import Document


class WordDocumentTemplateService:

    def __init__(self, template_path):
        self.template_path = template_path

    def replace_placeholders(self, context):
        # Load the template document
        doc = Document(self.template_path)

        # Replace placeholders in paragraphs
        for paragraph in doc.paragraphs:
            for key, value in context.items():
                if f'{{{{ {key} }}}}' in paragraph.text:
                    paragraph.text = paragraph.text.replace(f'{{{{ {key} }}}}', value)

        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for key, value in context.items():
                        if f'{{{{ {key} }}}}' in cell.text:
                            cell.text = cell.text.replace(f'{{{{ {key} }}}}', value)

        return doc

    def save_document(self, doc, output_path):
        doc.save(output_path)
