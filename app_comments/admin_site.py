from django.contrib.admin import AdminSite as DjangoAdminSite


class AdminSite(DjangoAdminSite):

    site_title = 'Comment'
    site_header = 'Comment'
    index_title = 'Comment'
    site_url = '/administration/'
    enable_nav_sidebar = False

comment_admin = AdminSite(name='comment_admin')
