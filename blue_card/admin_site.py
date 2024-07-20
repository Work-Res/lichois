from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = "Blue Card Administration"
    site_header = "Blue Card Administration"
    index_title = "Welcome to Blue Card Administration"
    site_url = "/administration/"
    enable_nav_sidebar = False


blue_card_admin = AdminSite(name="blue_card_admin")
