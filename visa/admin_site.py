from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Visa'
    site_header = 'Visa'
    index_title = 'Visa'
    site_url = '/administration/'
    enable_nav_sidebar = False

visa_admin = AdminSite(name='visa_admin')
