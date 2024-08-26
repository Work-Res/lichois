from identifier.identifier import Identifier
from identifier.simple_identifier import SimpleIdentifier


class BatchIdentifier(SimpleIdentifier):
    template = "{identifier_type}{sequence}"
    label = "gazette"  # e.g. work_permit_identifier, visa_identifier, etc
    identifier_type = "DB"
