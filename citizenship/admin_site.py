from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Citizenship'
    site_header = 'Citizenship'
    index_title = 'Citizenship'
    site_url = '/administration/'
    enable_nav_sidebar = False

citizenship_admin = AdminSite(name='citizenship_admin')
