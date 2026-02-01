from nicegui import ui, app
from database.db_operations import (
    get_product_prices,
    get_products,
    update_product_price,
)
import utils.validators as validators

cycle_id = app.storage.general.get("cycle_id")


def update_price_dialog(product_name):
    with ui.dialog() as dialog, ui.card():
        ui.label("Update price").classes("text-h6")
        price_input = ui.number(label="New Price", value=0, min=0, step=0.01)

        def update_price():
            try:
                new_price = float(price_input.value)
                if not validators.is_valid_number(new_price):
                    ui.notify(
                        "Price has to be positive. Please try again.", type="negative"
                    )
                update_product_price(
                    cycle_id=cycle_id, product_name=product_name, new_price=new_price
                )
                ui.notify(f"Price updated successfully to {new_price}", type="positive")
                product_price_table.refresh()
                dialog.close()
            except Exception as e:
                ui.notify(f"Error updating price: {e}", type="negative")

        with ui.row().classes("gap-2 q-mt-md"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Update", on_click=update_price).props("color=primary")

    dialog.open()


@ui.refreshable
def product_price_table():
    # table definition
    columns = [
        {"name": "product_id", "label": "ID", "field": "product_id"},
        {"name": "product", "label": "Product", "field": "product"},
        {"name": "price", "label": "Price", "field": "price"},
        {"name": "update", "label": "Update", "align": "center"},
    ]

    product_prices = get_product_prices(cycle_id)  # List of ProductPrice Objects
    products = get_products()  # List of Product objects
    rows = []
    for product in products:
        product_name = product.name
        price = 0
        for item in product_prices:
            if item.product_id == product.id:
                price = item.sell_price
                break
        rows.append({"product_id": product.id, "product": product_name, "price": price})

    table = ui.table(columns=columns, rows=rows, row_key="product_id").classes("w-full")
    # table buttons definition
    with table.add_slot("body-cell-update"):
        with table.cell("update"):
            ui.button("update").props("flat color=primary").on(
                "click",
                js_handler="() => emit(props.row.product)",
                handler=lambda e: update_price_dialog(e.args),
            )


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
                icon="person",
                on_click=lambda: ui.navigate.to("/cycle/customer"),
            ).props("round color=green").tooltip("Customer")

            ui.button(
                icon="local_shipping",
                on_click=lambda: ui.navigate.to("/cycle/supply"),
            ).props("round color=orange").tooltip("Supply")

        # Main content area
        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            # Header section
            with ui.card().classes("w-full"):
                with ui.row().classes("items-center justify-between w-full"):
                    with ui.column().classes("gap-1"):
                        ui.label("Product Management").classes(
                            "text-h4 font-bold text-primary"
                        )
                        ui.label(f"Cycle ID: {cycle_id}").classes(
                            "text-subtitle1 text-gray-600"
                        )

                    ui.button(
                        "Back to Cycle",
                        icon="arrow_back",
                        on_click=lambda: ui.navigate.to("/cycle"),
                    ).props("flat color=secondary")

            # Product prices section
            ui.label("Product Prices").classes(
                "text-h6 font-medium text-gray-700 q-mt-md"
            )

            with ui.card().classes("w-full"):
                product_price_table()
