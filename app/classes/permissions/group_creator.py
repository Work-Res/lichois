from .group_file_scanner import GroupFileScanner
from .group_manager import GroupManager


class GroupCreator:
    def __init__(self):
        self.scanner = GroupFileScanner()

    def create_groups_from_files(self):
        """
        Scans for groups.txt files and creates or updates groups and permissions
        based on the file contents.
        """
        group_files = self.scanner.scan()

        # Process each group file
        for group_file_path in group_files:
            group_manager = GroupManager(group_file_path)
            group_manager.create_or_update_groups()
