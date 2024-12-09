from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Personal Details'
    site_header = 'Personal Details'
    index_title = 'Personal Details'
    site_url = '/administration/'
    enable_nav_sidebar = False


personal_details_admin = AdminSite(name='personal_details_admin')