from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
	site_title = 'Board'
	site_header = 'Board'
	index_title = 'Board'
	site_url = '/administration/'
	enable_nav_sidebar = False


board_admin = AdminSite(name='board')
