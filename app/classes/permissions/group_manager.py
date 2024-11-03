import os
import re

import logging
from django.contrib.auth.models import Group, Permission


logger = logging.getLogger(__name__)


class GroupManager:
    def __init__(self, group_file_path):
        self.group_file_path = group_file_path

    def create_or_update_groups(self):
        # Check if the file exists and log appropriately
        if not os.path.exists(self.group_file_path):
            logger.error(f"No groups.txt file found at {self.group_file_path}.")
            return

        logger.info(f"Starting processing for file: {self.group_file_path}")

        # Open the file and process each line
        with open(self.group_file_path, 'r') as file:
            current_group = None
            for line_number, line in enumerate(file, start=1):
                not_stripped_line = line
                line = line.strip()

                if not line:
                    continue  # Skip empty lines

                # Detect group name (lines ending with a colon)
                if line.endswith(':'):
                    group_name = line[:-1].strip()
                    current_group, created = Group.objects.get_or_create(name=group_name)
                    if created:
                        logger.info(f"Created new group '{group_name}' at line {line_number}.")
                    else:
                        logger.info(f"Found existing group '{group_name}' at line {line_number}.")

                # Process permissions under the current group
                elif current_group and re.match(r'^\s{4}\w+', not_stripped_line):
                    permission_codename = line.strip()
                    print(f"About to add permission to group {permission_codename}")
                    self.add_permission_to_group(current_group, permission_codename, line_number)
                else:
                    print(f"On the else:{not_stripped_line}")

        logger.info("Completed processing for group and permission setup.")

    def add_permission_to_group(self, group, permission_codename, line_number=None):
        # Attempt to retrieve or create the permission
        permission = Permission.objects.get(codename=permission_codename)

        # Add the permission to the group
        group.permissions.add(permission)

        # Log the outcome
        logger.info(f"Created and added new permission '{permission_codename}' to group '{group.name}' at line "
                    f"{line_number}.")
