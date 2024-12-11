from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Work Flow'
    site_header = 'Work Flow'
    index_title = 'Work Flow'
    site_url = '/administration/'
    enable_nav_sidebar = False


workflow_admin = AdminSite(name='workflow_admin')