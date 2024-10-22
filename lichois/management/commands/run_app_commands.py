import os
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Runs all management commands inside the specified app"

    def add_arguments(self, parser):
        parser.add_argument(
            "app_name", type=str, help="The name of the app to run commands for"
        )

    def handle(self, *args, **kwargs):
        app_name = kwargs["app_name"]
        commands_dir = os.path.join(app_name, "management", "commands")
        self.stdout.write(f"Running commands for : {commands_dir}")
        commands = self.find_commands(commands_dir)
        self.stdout.write(f"Found commands: {commands}")

        for command in commands:
            if command != "run_app_commands":  # Avoid running itself
                self.stdout.write(f"Running command: {command}")
                try:
                    call_command(command)
                except Exception as e:
                    self.stderr.write(f"Error running command {command}: {e}")

    def find_commands(self, commands_dir):
        """
        Find all Python files in the specified directory that are not __init__.py.
        """
        commands = []
        for filename in os.listdir(commands_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                command_name = filename[:-3]  # Remove the .py extension
                commands.append(command_name)
        return commands
