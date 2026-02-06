from nicegui import ui
from utils.helpers import get_current_cycle_id


def create_cycle_navigation_buttons():
    with ui.column().classes("gap-4"):
        ui.button(
            "回首頁",
            icon="home",
            on_click=lambda: ui.navigate.to("/"),
        ).props("color=secondary").classes("w-full")

        ui.button(
            "本期總覽", icon="loop", on_click=lambda: ui.navigate.to("/cycle")
        ).props("color=cyan").classes("w-full")

        ui.button(
            "產品價格",
            icon="eco",
            on_click=lambda: ui.navigate.to("/cycle/product"),
        ).props("color=primary").classes("w-full")

        ui.button(
            "顧客訂單",
            icon="person",
            on_click=lambda: ui.navigate.to("/cycle/customer"),
        ).props("color=green").classes("w-full")

        ui.button(
            "上游叫貨",
            icon="local_shipping",
            on_click=lambda: ui.navigate.to("/cycle/supply"),
        ).props("color=orange").classes("w-full")

        ui.button(
            "本期報告",
            icon="assessment",
            on_click=lambda: ui.navigate.to("/cycle/report"),
        ).props("color=blue").classes("w-full")


def create_header(header: str):
    with ui.card().classes("w-full"):
        with ui.row().classes("items-center justify-between w-full"):
            with ui.column().classes("gap-1"):
                ui.label(f"{header}").classes("text-h4 font-bold text-black")
                ui.label(f"第{get_current_cycle_id()}期").classes(
                    "text-subtitle1 text-gray-600"
                )
