# supply.py
from nicegui import ui, app

cycle_id = app.storage.general.get("cycle_id")


@ui.refreshable
def supply_table():
    # Table definition - to be implemented
    columns = [
        {"name": "supplier", "label": "Supplier Name", "field": "supplier"},
        {"name": "product", "label": "Product", "field": "product"},
        {"name": "quantity", "label": "Quantity", "field": "quantity"},
        {"name": "actions", "label": "Actions", "align": "center"},
    ]
    rows = []

    table = ui.table(columns=columns, rows=rows, row_key="supplier").classes("w-full")


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.row().classes("w-full gap-32 p-8"):
        # Left sidebar with navigation buttons
        with ui.column().classes("gap-4"):
            ui.button(
                icon="home",
                on_click=lambda: ui.navigate.to("/"),
            ).props("round color=secondary").tooltip("Home")

            ui.button(
                icon="eco",
                on_click=lambda: ui.navigate.to("/cycle/product"),
            ).props("round color=primary").tooltip("Product")

            ui.button(
                icon="person",
                on_click=lambda: ui.navigate.to("/cycle/customer"),
            ).props("round color=green").tooltip("Customer")

        # Main content area
        with ui.column().classes("flex-1 max-w-3xl gap-6"):
            # Header section
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between w-full"):
                    with ui.column().classes("gap-1"):
                        ui.label("Supply Management").classes(
                            "text-h4 font-bold text-orange"
                        )
                        ui.label(f"Cycle ID: {cycle_id}").classes(
                            "text-subtitle1 text-gray-600"
                        )

                    ui.button(
                        "Back to Cycle",
                        icon="arrow_back",
                        on_click=lambda: ui.navigate.to("/cycle"),
                    ).props("flat color=secondary")

            # Supply table section
            ui.label("Supplies").classes("text-h6 font-medium text-gray-700 q-mt-md")

            with ui.card().classes("w-full"):
                supply_table()
