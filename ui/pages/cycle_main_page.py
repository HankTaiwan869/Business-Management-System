from nicegui import ui
from database.db_operations import finish_cycle
from utils.helpers import get_current_cycle_id


def show_finish_cycle_dialog():
    with ui.dialog() as dialog, ui.card():
        ui.label("Finish Cycle").classes("text-h6 font-medium mb-2")
        ui.label("Are you sure you want to finish the current cycle?").classes("mb-4")

        def ui_finish_cycle():
            if finish_cycle():
                ui.notify("Success. Redirecting to the main page.", type="positive")
                dialog.close()
                ui.navigate.to("/")
            else:
                ui.notify("Failed. Something went wrong.", type="negative")
                dialog.close()

        with ui.row().classes("w-full gap-2 justify-center"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Finish", on_click=lambda: ui_finish_cycle()).props("color=red")

    dialog.open()


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header section
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                with ui.column().classes("gap-1"):
                    ui.label("Cycle Management").classes(
                        "text-h4 font-bold text-primary"
                    )
                    ui.label(f"Cycle ID: {get_current_cycle_id()}").classes(
                        "text-subtitle1 text-gray-600"
                    )

                ui.button(
                    "Back to Home", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("flat color=secondary")

        # Navigation cards
        ui.label("Actions").classes("text-h6 font-medium text-gray-700 q-mt-md")

        with ui.row().classes("w-full gap-4"):
            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/product"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("inventory_2", size="48px").classes("text-primary")
                    ui.label("Product").classes("text-h6 font-medium")
                    ui.label("Manage products").classes("text-caption text-gray-600")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/customer"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("person", size="48px").classes("text-green")
                    ui.label("Customer").classes("text-h6 font-medium")
                    ui.label("Manage customers").classes("text-caption text-gray-600")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/supply"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("local_shipping", size="48px").classes("text-orange")
                    ui.label("Supply").classes("text-h6 font-medium")
                    ui.label("Manage supplies").classes("text-caption text-gray-600")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/cycle/report"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("assessment", size="48px").classes("text-blue")
                    ui.label("Report").classes("text-h6 font-medium")
                    ui.label("View reports").classes("text-caption text-gray-600")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: show_finish_cycle_dialog())
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("check_circle", size="48px").classes("text-red")
                    ui.label("Finish Cycle").classes("text-h6 font-medium")
                    ui.label("Complete current cycle").classes(
                        "text-caption text-gray-600"
                    )
