from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from ..models import User
from ..admin_site import authentication_admin


@admin.register(User, site=authentication_admin)
class UserAdmin(DjangoUserAdmin):
	list_filter = ()
	list_display = (
		'username',
		'last_name',
		'first_name',
		'email',
		'is_active',
	)
	
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
		('Permissions', {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
		}),
		('Important dates', {'fields': ('last_login', 'date_joined')}),
	)
	
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2'),
		}),
		('Personal info', {
			'classes': ('wide',),
			'fields': ('first_name', 'last_name', 'email'),
		}),
	)
