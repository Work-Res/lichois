from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Work and Residence Permit'
    site_header = 'Work and Residence Permit'
    index_title = 'Work and Residence Permit'
    site_url = '/administration/'
    enable_nav_sidebar = False


workresidencepermit_admin = AdminSite(name='workresidencepermit_admin')