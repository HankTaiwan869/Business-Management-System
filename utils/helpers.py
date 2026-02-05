from nicegui import app
from datetime import datetime


def get_current_cycle_id() -> int:
    return app.storage.general["cycle_id"]


def is_valid_name(input: str) -> bool:
    return input.strip() != ""


def is_valid_number(input: float | int) -> bool:
    return input >= 0


def is_valid_year(input: float | int) -> bool:
    if input.is_integer():
        # the max year accepted should not exceed this year
        if input > 1950 and input <= datetime.now().year:
            return True
    return False


def is_valid_month(input: float | int) -> bool:
    if input.is_integer():
        if input >= 1 and input <= 12:
            return True
    return False
