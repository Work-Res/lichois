import os
from django.conf import settings


class GroupFileScanner:
    def __init__(self):
        self.installed_apps = settings.INSTALLED_APPS

    def scan(self):
        """
        Scans all installed apps and looks for `groups.txt` files.
        Returns a list of file paths to the `groups.txt` files.
        """
        group_files = []
        for app in self.installed_apps:
            if app.startswith('django.') or 'rest_framework' in app:
                continue

            app_path = self.get_app_path(app)
            group_file_path = os.path.join(app_path, "data", "groups", 'groups.txt')

            if os.path.exists(group_file_path):
                group_files.append(group_file_path)

        return group_files

    def get_app_path(self, app_name):
        """
        Utility function to get the file system path of an app.
        """
        module = __import__(app_name)
        return os.path.dirname(module.__file__)
