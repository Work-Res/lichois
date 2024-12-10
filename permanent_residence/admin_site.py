from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Permanent Residence'
    site_header = 'Permanent Residence'
    index_title = 'Permanent Residence'
    site_url = '/administration/'
    enable_nav_sidebar = False


permanent_residence_admin = AdminSite(name='permanent_residence_admin')