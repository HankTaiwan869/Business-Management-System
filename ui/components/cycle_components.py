from nicegui import ui
from utils.helpers import get_current_cycle_id


def create_cycle_navigation_buttons():
    with ui.column().classes("gap-4"):
        ui.button(
            "Home",
            icon="home",
            on_click=lambda: ui.navigate.to("/"),
        ).props("color=secondary").classes("w-full")

        ui.button(
            "Cycle", icon="loop", on_click=lambda: ui.navigate.to("/cycle")
        ).props("color=cyan").classes("w-full")

        ui.button(
            "Product",
            icon="eco",
            on_click=lambda: ui.navigate.to("/cycle/product"),
        ).props("color=primary").classes("w-full")

        ui.button(
            "Customer",
            icon="person",
            on_click=lambda: ui.navigate.to("/cycle/customer"),
        ).props("color=green").classes("w-full")

        ui.button(
            "Supply",
            icon="local_shipping",
            on_click=lambda: ui.navigate.to("/cycle/supply"),
        ).props("color=orange").classes("w-full")

        ui.button(
            "Report",
            icon="assessment",
            on_click=lambda: ui.navigate.to("/cycle/report"),
        ).props("color=blue").classes("w-full")


def create_header(header: str):
    with ui.card().classes("w-full"):
        with ui.row().classes("items-center justify-between w-full"):
            with ui.column().classes("gap-1"):
                ui.label(f"{header}").classes("text-h4 font-bold text-black")
                ui.label(f"Cycle ID: {get_current_cycle_id()}").classes(
                    "text-subtitle1 text-gray-600"
                )
