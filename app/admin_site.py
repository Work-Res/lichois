from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):
    site_title = "Application"
    site_header = "Application"
    index_title = "Application"
    site_url = "/administration/"
    enable_nav_sidebar = False


app_admin = AdminSite(name="app")
