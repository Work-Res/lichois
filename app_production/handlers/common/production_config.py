class ProductionConfig:
    def __init__(
        self, template_path: str, document_output_path: str, is_required=False
    ):
        self.template_path = template_path
        self.document_output_path = document_output_path
        self.is_required = is_required
