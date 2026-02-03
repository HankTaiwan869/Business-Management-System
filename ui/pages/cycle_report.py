from nicegui import ui
from ui.components.cycle_components import (
    create_cycle_navigation_buttons,
    create_header,
)


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.row().classes("w-full gap-8 p-8"):
        create_cycle_navigation_buttons()

        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("Cycle Report")

            # Product prices section
            ui.label("Product Prices").classes(
                "text-h6 font-medium text-gray-700 q-mt-md"
            )

            with ui.card().classes("w-full"):
                ui.label("Plots here")
