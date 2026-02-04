from nicegui import app


def get_current_cycle_id() -> int:
    return app.storage.general["cycle_id"]


def is_valid_name(input: str) -> bool:
    return input.strip() != ""


def is_valid_number(input: float | int) -> bool:
    return input >= 0
