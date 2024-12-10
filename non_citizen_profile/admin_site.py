from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Non Citizen Profile'
    site_header = 'Non Citizen Profile'
    index_title = 'Non Citizen Profile'
    site_url = '/administration/'
    enable_nav_sidebar = False


non_citizen_profile_admin = AdminSite(name='non_citizen_profile_admin')