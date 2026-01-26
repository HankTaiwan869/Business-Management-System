from nicegui import ui, APIRouter
from database.db_operations import (
    add_customer,
    add_product,
    add_supplier,
    get_customers,
    get_products,
    get_suppliers,
)

router = APIRouter(prefix="/overview")


def submit_customer(name, discount):
    try:
        add_customer(name.value, discount.value)
        ui.notify(f"Customer '{name.value}' added successfully.", color="green")
        name.value = ""
        discount.value = 0.0
    except Exception as e:
        ui.notify(f"Error adding customer: {e}", color="red")


def submit_product(product_name_input):
    try:
        add_product(product_name_input.value)
        ui.notify(
            f"Product '{product_name_input.value}' added successfully.", color="green"
        )
        product_name_input.value = ""
    except Exception as e:
        ui.notify(f"Error adding product: {e}", color="red")


def submit_supplier(supplier_name_input):
    try:
        add_supplier(supplier_name_input.value)
        ui.notify(
            f"Supplier '{supplier_name_input.value}' added successfully.", color="green"
        )
        supplier_name_input.value = ""
    except Exception as e:
        ui.notify(f"Error adding supplier: {e}", color="red")


@router.page("/")
def overview_page():
    ui.query("body").classes("bg-gray-100")

    ui.label("Overview").classes("text-h3 font-bold q-mb-lg")
    with ui.column().classes("w-full max-w-4xl mx-auto p-8"):
        with ui.tabs().classes("justify-left") as tabs:
            ui.tab("add_customer", "Customer", icon="person")
            ui.tab("add_product", "Product", icon="inventory_2")
            ui.tab("add_supplier", "Supplier", icon="local_shipping")

        ui.button("Back to Home", on_click=lambda: ui.navigate.to("/")).props(
            "color=secondary"
        ).classes("self-end q-mb-md")

        with ui.tab_panels(tabs, value="add_customer").classes("w-full"):
            with ui.tab_panel("add_customer").classes("q-pa-md"):
                with ui.column().classes("gap-4 w-full"):
                    name_input = ui.input(
                        "Customer Name",
                    ).classes("w-full")
                    discount_input = ui.number("Discount", value=0.0, min=0.0).classes(
                        "w-full"
                    )
                    ui.button(
                        "Add New Customer",
                        on_click=lambda: submit_customer(name_input, discount_input),
                    ).props("size=lg")
                    ui.table.from_pandas(get_customers()).classes(
                        "w-full mx-auto text-xl"
                    ).props("dense=false")
            with ui.tab_panel("add_product").classes("q-pa-md"):
                with ui.column().classes("gap-4 w-full"):
                    product_name_input = ui.input("Product Name").classes("w-full")
                    ui.button(
                        "Add New Product",
                        on_click=lambda: submit_product(product_name_input),
                    ).props("color=primary size=lg")
                    ui.table.from_pandas(get_products()).classes(
                        "w-full mx-auto text-xl"
                    ).props("dense=false")

            with ui.tab_panel("add_supplier").classes("q-pa-md"):
                with ui.column().classes("gap-4 w-full"):
                    supplier_name_input = ui.input("Supplier Name").classes("w-full")
                    ui.button(
                        "Add New Supplier",
                        on_click=lambda: submit_supplier(supplier_name_input),
                    ).props("color=primary size=lg")
                    ui.table.from_pandas(get_suppliers()).classes(
                        "w-full mx-auto text-xl"
                    ).props("dense=false")
