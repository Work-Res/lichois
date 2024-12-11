from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Address'
    site_header = 'Address'
    index_title = 'Address'
    site_url = '/administration/'
    enable_nav_sidebar = False

address_admin = AdminSite(name='address_admin')
