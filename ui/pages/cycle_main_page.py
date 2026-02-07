from nicegui import ui
from database.db_operations_general import finish_cycle
from utils.helpers import get_current_cycle_id
from logic.logic import calculate_total_revenue, calculate_total_cost


def show_finish_cycle_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label("結束本期").classes("text-h6 font-medium mb-2")
        ui.label("確認是否結束本期？").classes("mb-4")

        def ui_finish_cycle():
            if finish_cycle(
                calculate_total_revenue(get_current_cycle_id()),
                calculate_total_cost(get_current_cycle_id()),
            ):
                ui.notify("成功結束，回到首頁", type="positive")
                dialog.close()
                ui.navigate.to("/")
            else:
                ui.notify("失敗，請聯繫開發者", type="negative")
                dialog.close()

        with ui.row().classes("w-full gap-2 justify-center"):
            ui.button("取消", on_click=dialog.close).props("flat")
            ui.button("確認結束", on_click=lambda: ui_finish_cycle()).props("color=red")

    dialog.open()


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header section
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                with ui.column().classes("gap-1"):
                    ui.label("週期管理").classes("text-h4 font-bold text-black")
                    ui.label(f"第{get_current_cycle_id()}期").classes(
                        "text-subtitle1 text-gray-600"
                    )

                ui.button(
                    "回首頁", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("flat color=secondary")

        # Navigation cards
        ui.label("主選單").classes("text-h6 font-medium text-gray-700 q-mt-md")

        with ui.row().classes("w-full gap-4"):
            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/product"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("eco", size="48px").classes("text-primary")
                    ui.label("產品價格").classes("text-h6 font-medium")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/customer"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("person", size="48px").classes("text-green")
                    ui.label("顧客訂單").classes("text-h6 font-medium")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/supply"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("local_shipping", size="48px").classes("text-orange")
                    ui.label("上游叫貨").classes("text-h6 font-medium")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/report"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("assessment", size="48px").classes("text-blue")
                    ui.label("本期報告").classes("text-h6 font-medium")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: show_finish_cycle_dialog())
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("check_circle", size="48px").classes("text-red")
                    ui.label("結束本期").classes("text-h6 font-medium")
