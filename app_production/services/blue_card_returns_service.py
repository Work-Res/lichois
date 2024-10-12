from app.utils.system_enums import ApplicationProcesses
from .blue_card_production_service import BlueCardProductionService


class BlueCardReturnsProductionService(BlueCardProductionService):
    process_name = ApplicationProcesses.BLUE_CARD_RETURNS.value
