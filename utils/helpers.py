from nicegui import app


def get_current_cycle_id() -> int:
    return app.storage.general["cycle_id"]
