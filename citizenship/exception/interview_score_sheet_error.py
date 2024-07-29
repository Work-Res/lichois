

class InterviewScoreSheetError(Exception):
    """Base class for exceptions in this module."""
    pass


class WordDocumentCreationError(InterviewScoreSheetError):
    """Exception raised for errors in the creation of the Word document."""
    def __init__(self, message="Error creating Word document"):
        self.message = message
        super().__init__(self.message)


class PDFConversionError(InterviewScoreSheetError):
    """Exception raised for errors in the conversion of the Word document to PDF."""
    def __init__(self, message="Error converting Word document to PDF"):
        self.message = message
        super().__init__(self.message)

