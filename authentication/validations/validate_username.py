from django.core.exceptions import ValidationError


def validate_username(data):
	username = data['username'].strip()
	if not username:
		raise ValidationError('choose another username')
	return True
