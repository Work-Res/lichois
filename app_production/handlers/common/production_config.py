class ProductionConfig:
    def __init__(
        self, template_path: str, document_output_path: str, is_required=False, document_output_path_pdf=None
    ):
        self.template_path = template_path
        self.document_output_path = document_output_path
        self.document_output_path_pdf = document_output_path_pdf
        self.is_required = is_required
