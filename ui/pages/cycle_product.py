from nicegui import ui, app
from database.db_operations import (
    get_product_prices,
    get_products,
    update_product_price,
)

cycle_id = app.storage.general.get("cycle_id")


def update_price_dialog(product_name):
    with ui.dialog() as dialog, ui.card():
        products = get_products()
        product_id = int(products[products["name"] == product_name].id.values[0])

        ui.label(f"Update price for {product_name}").classes("text-h6")
        price_input = ui.number(label="New Price", value=0, min=0, step=0.01)

        def update_price():
            try:
                new_price = float(price_input.value)
                update_product_price(
                    cycle_id=cycle_id, product_id=product_id, new_price=new_price
                )
                ui.notify(f"Price updated successfully to {new_price}", color="green")
                product_price_table.refresh()
                dialog.close()
            except Exception as e:
                ui.notify(f"Error updating price: {e}", color="red")

        with ui.row().classes("gap-2 q-mt-md"):
            ui.button("Cancel", on_click=dialog.close).props("flat")
            ui.button("Update", on_click=update_price).props("color=primary")

    dialog.open()


@ui.refreshable
def product_price_table():
    # table definition
    columns = [
        {"name": "product", "label": "Product", "field": "product"},
        {"name": "price", "label": "Price", "field": "price"},
        {"name": "update", "label": "Update", "align": "center"},
    ]
    product_prices = get_product_prices(cycle_id)
    products = get_products()  # Pandas dataframe of products
    rows = []
    # print(product_prices[0].product_id)
    # print(type(products[products["name"] == "A"]["id"][0]))

    for product in products.to_dict(orient="records"):
        product_name = product["name"]
        price = 0
        for item in product_prices:
            if item.product_id == product["id"]:
                price = item.sell_price
                break
        rows.append({"product": product_name, "price": price})

    table = ui.table(columns=columns, rows=rows, row_key="product")
    # table buttons definition
    with table.add_slot("body-cell-update"):
        with table.cell("update"):
            ui.button("update").props("flat").on(
                "click",
                js_handler="() => emit(props.row.product)",
                handler=lambda e: update_price_dialog(e.args),
            )


def content():
    product_price_table()
