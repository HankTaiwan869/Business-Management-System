from nicegui import ui, APIRouter
from database.db_operations import (
    add_customer,
    add_product,
    add_supplier,
    get_customers,
    get_products,
    get_suppliers,
)
from utils.helpers import is_valid_number, is_valid_name

router = APIRouter(prefix="/overview")


def submit_customer(name, discount):
    try:
        if not is_valid_name(name.value):
            ui.notify("Name cannot be empty. Please try again.", type="negative")
            return
        if not is_valid_number(discount.value):
            ui.notify("Discount should be positive. Please try again.", type="negative")
        add_customer(name.value.strip(), discount.value)
        ui.notify(
            f"Customer '{name.value.strip()}' added successfully.", type="positive"
        )
        name.value = ""
        discount.value = 0.0
        customer_table.refresh()
    except Exception as e:
        ui.notify(f"Error adding customer: {e}", type="negative")


def submit_product(product_name_input):
    try:
        if not is_valid_name(product_name_input.value):
            ui.notify("Name cannot be empty. Please try again.", type="negative")
            return
        add_product(product_name_input.value.strip())
        ui.notify(
            f"Product '{product_name_input.value.strip()}' added successfully.",
            type="positive",
        )
        product_name_input.value = ""
        product_table.refresh()
    except Exception as e:
        ui.notify(f"Error adding product: {e}", type="negative")


def submit_supplier(supplier_name_input):
    try:
        if not is_valid_name(supplier_name_input.value):
            ui.notify("Name cannot be empty. Please try again.", type="negative")
            return
        add_supplier(supplier_name_input.value.strip())
        ui.notify(
            f"Supplier '{supplier_name_input.value.strip()}' added successfully.",
            type="positive",
        )
        supplier_name_input.value = ""
        supplier_table.refresh()
    except Exception as e:
        ui.notify(f"Error adding supplier: {e}", type="negative")


@ui.refreshable
def customer_table():
    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
        {"discount": "discount", "label": "Discount", "field": "discount"},
    ]
    rows = []
    for row in get_customers():
        rows.append({"id": row.id, "name": row.name, "discount": row.discount})
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full mx-auto").props(
        "dense=false"
    )


@ui.refreshable
def product_table():
    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
    ]
    rows = []
    for row in get_products():
        rows.append({"id": row.id, "name": row.name})
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full mx-auto").props(
        "dense=false"
    )


@ui.refreshable
def supplier_table():
    columns = [
        {"name": "id", "label": "ID", "field": "id"},
        {"name": "name", "label": "Name", "field": "name"},
    ]
    rows = []
    for row in get_suppliers():
        rows.append({"id": row.id, "name": row.name})
    ui.table(columns=columns, rows=rows, row_key="id").classes("w-full mx-auto").props(
        "dense=false"
    )


@router.page("/")
def overview_page():
    ui.query("body").classes("bg-gray-100")

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header card
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                with ui.column().classes("gap-1"):
                    ui.label("Database Overview").classes(
                        "text-h4 font-bold text-primary"
                    )
                    ui.label("Manage customers, products, and suppliers").classes(
                        "text-subtitle1 text-gray-600"
                    )

                ui.button(
                    "Back to Home", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("flat color=secondary")

        # Tabs card
        with ui.card().classes("w-full"):
            with ui.tabs().classes("w-full") as tabs:
                ui.tab("add_customer", "Customer", icon="person")
                ui.tab("add_product", "Product", icon="inventory_2")
                ui.tab("add_supplier", "Supplier", icon="local_shipping")

            ui.separator()

            with ui.tab_panels(tabs, value="add_customer").classes("w-full"):
                with ui.tab_panel("add_customer"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui.label("Add New Customer").classes("text-h6 font-medium")
                        name_input = ui.input("Customer Name").classes("w-full")
                        discount_input = ui.number(
                            "Discount", value=0.0, min=0.0
                        ).classes("w-full")
                        ui.button(
                            "Add Customer",
                            icon="add",
                            on_click=lambda: submit_customer(
                                name_input, discount_input
                            ),
                        ).props("color=primary")

                        ui.separator().classes("q-my-md")
                        ui.label("Current Customers").classes(
                            "text-subtitle1 font-medium q-mb-sm"
                        )
                        customer_table()

                with ui.tab_panel("add_product"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui.label("Add New Product").classes("text-h6 font-medium")
                        product_name_input = ui.input("Product Name").classes("w-full")
                        ui.button(
                            "Add Product",
                            icon="add",
                            on_click=lambda: submit_product(product_name_input),
                        ).props("color=primary")

                        ui.separator().classes("q-my-md")
                        ui.label("Current Products").classes(
                            "text-subtitle1 font-medium q-mb-sm"
                        )
                        product_table()

                with ui.tab_panel("add_supplier"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui.label("Add New Supplier").classes("text-h6 font-medium")
                        supplier_name_input = ui.input("Supplier Name").classes(
                            "w-full"
                        )
                        ui.button(
                            "Add Supplier",
                            icon="add",
                            on_click=lambda: submit_supplier(supplier_name_input),
                        ).props("color=primary")

                        ui.separator().classes("q-my-md")
                        ui.label("Current Suppliers").classes(
                            "text-subtitle1 font-medium q-mb-sm"
                        )
                        supplier_table()
