from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Services'
    site_header = 'Services'
    index_title = 'Services'
    site_url = '/administration/'
    enable_nav_sidebar = False


services_admin = AdminSite(name='services_admin')