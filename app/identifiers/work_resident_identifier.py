from identifier.identifier import Identifier


class WorkResidentPermitIdentifier(Identifier):
	template = '{identifier_type}{address_code}{dob}{sequence}'
	label = 'workresidentpermit'  # e.g. work_permit_identifier, visa_identifier, etc
	identifier_type = 'WR'


class SpecialPermitIdentifier(Identifier):
	template = '{identifier_type}{address_code}{dob}{sequence}'
	label = 'workresidentpermit'  # e.g. work_permit_identifier, visa_identifier, etc
	identifier_type = 'SP'


class WorkPermitIdentifier(Identifier):
	template = '{identifier_type}{address_code}{dob}{sequence}'
	label = 'workpermit'  # e.g. work_permit_identifier, visa_identifier, etc
	identifier_type = 'W'


class ResidentPermitIdentifier(Identifier):
	template = '{identifier_type}{address_code}{dob}{sequence}'
	label = 'residentpermit'  # e.g. work_permit_identifier, visa_identifier, etc
	identifier_type = 'R'
