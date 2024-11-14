from app.utils.system_enums import ApplicationProcesses
from lichois.management.base_command import CustomBaseCommand


class Command(CustomBaseCommand):
    help = "Populate data for Res Application model"
    application_type = None
    process_name = ApplicationProcesses.RESIDENT_PERMIT.value
