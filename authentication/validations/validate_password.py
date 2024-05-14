from django.core.exceptions import ValidationError


def validate_password(data):
	password = data['password'].strip()
	if not password:
		raise ValidationError('a password is needed')
	return True
