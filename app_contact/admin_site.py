from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Contact'
    site_header = 'Contact Details'
    index_title = 'Contact Details'
    site_url = '/administration/'
    enable_nav_sidebar = False


contact_admin = AdminSite(name='contact_admin')