from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "Travel Certificate"
    site_header = "Travel Certificate"
    index_title = "Travel Certificate"
    site_url = "/administration/"
    enable_nav_sidebar = False


travel_certificate_admin = AdminSite(name="travel_certificate_admin")
