from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "Authentication"
    site_header = "Authentication"
    index_title = "Authentication"
    site_url = "/administration/"
    enable_nav_sidebar = False


authentication_admin = AdminSite(name="authentication_admin")
