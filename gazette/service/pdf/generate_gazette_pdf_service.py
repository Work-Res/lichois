import docx
from docx2pdf import convert


class GenerateGazettePDFService:
    def __init__(self, data, word_file_path, pdf_file_path):
        self.data = data
        self.word_file_path = word_file_path
        self.pdf_file_path = pdf_file_path

    def create_word_document(self):
        doc = docx.Document()

        # Add a title
        doc.add_heading('Gazette List', 0)

        # Create a table
        table = doc.add_table(rows=1, cols=len(self.data[0]))
        table.style = 'Table Grid'

        # Add header row
        hdr_cells = table.rows[0].cells
        for i, heading in enumerate(self.data[0]):
            hdr_cells[i].text = heading

        # Add data rows
        for row in self.data[1:]:
            row_cells = table.add_row().cells
            for i, cell in enumerate(row):
                row_cells[i].text = str(cell)

        # Save the document
        doc.save(self.word_file_path)

    def convert_to_pdf(self):
        # Convert the Word document to PDF
        convert(self.word_file_path, self.pdf_file_path)

    def generate_pdf(self):
        self.create_word_document()
        self.convert_to_pdf()
