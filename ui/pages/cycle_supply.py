from nicegui import ui
from database.db_operations import (
    get_products,
    get_suppliers,
    get_orders_by_supplier_and_product,
    get_orders_by_suppliers,
    update_supplier_order,
)
from utils.helpers import get_current_cycle_id, is_valid_number
from logic.logic import (
    calculate_total_customer_order_quantity_by_product,
    calculate_total_supply_order_quantity_by_product,
)
from ui.components.cycle_components import (
    create_cycle_navigation_buttons,
    create_header,
)


def calculate_total_price(supplier_id: int) -> float:
    orders = get_orders_by_suppliers(
        cycle_id=get_current_cycle_id(), supplier_id=supplier_id
    )
    total = 0
    for order in orders:
        total += order.buy_price * order.quantity
    return total


def ui_update_supply_order(
    cycle_id: int, supplier_id: int, product_id: int, quantity: float, price: float
) -> None:
    try:
        if not is_valid_number(quantity) or not is_valid_number(price):
            ui.notify("Quantity/Price have to be positive.", type="negative")
            return
        update_supplier_order(cycle_id, supplier_id, product_id, quantity, price)
        ui.notify("Successful!", type="positive")
    except Exception:
        ui.notify(f"Failed because of {Exception}", type="negative")


# dynamically create supplier order cards
def create_supplier_cards():
    suppliers = get_suppliers()
    products = get_products()
    # dictionary mapping from tuple (supplier id, product id) to namedtuple (quantity, buy price)
    orders = get_orders_by_supplier_and_product(get_current_cycle_id())

    with ui.grid(columns=3):
        for supplier in suppliers:
            with ui.card():
                ui.label(supplier.name).classes("text-h6 font-medium")
                with ui.column().classes("gap-2"):
                    for product in products:
                        with ui.column().classes("gap-1"):
                            ui.label(product.name).classes("text-subtitle2 font-medium")
                            with ui.row().classes("gap-2"):
                                quantity = ui.number(
                                    "Quantity",
                                    min=0.0,
                                    value=orders[(supplier.id, product.id)].quantity
                                    if (supplier.id, product.id) in orders
                                    else 0,
                                ).classes("flex-1")
                                price = ui.number(
                                    "Price",
                                    min=0.0,
                                    value=orders[(supplier.id, product.id)].price
                                    if (supplier.id, product.id) in orders
                                    else 0,
                                ).classes("flex-1")
                            ui.button(
                                "Save",
                                on_click=lambda _,
                                sup=supplier,
                                prod=product,
                                qty=quantity,
                                pri=price: ui_update_supply_order(
                                    get_current_cycle_id(),
                                    sup.id,
                                    prod.id,
                                    qty.value,
                                    pri.value,
                                ),
                            ).props("flat color=primary")
                ui.separator()
                ui.label(f"Total: ${calculate_total_price(supplier.id):.2f}").classes(
                    "text-subtitle1 font-bold"
                )


def create_product_demand_cards():
    products = get_products()

    with ui.column().classes("gap-3"):
        ui.label("Product Demand Summary").classes("text-h6 font-medium text-gray-700")
        for product in products:
            total_customer_order = calculate_total_customer_order_quantity_by_product(
                get_current_cycle_id(), product.id
            )
            total_supply_order = calculate_total_supply_order_quantity_by_product(
                get_current_cycle_id(), product.id
            )
            remaining = round(total_customer_order - total_supply_order, 2)

            with ui.row().classes("items-center gap-2"):
                ui.label(f"{product.name}:").classes("text-body1 font-medium min-w-32")
                if remaining > 0:
                    ui.label(f"Need {remaining} more").classes(
                        "text-body2 text-orange-600"
                    )
                else:
                    ui.label(f"Surplus of {abs(remaining)}").classes(
                        "text-body2 text-blue-600"
                    )


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.row().classes("w-full gap-8 p-8"):
        create_cycle_navigation_buttons()

        # Main content area
        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("Supplier Management")

            # Supply table section
            ui.label("Suppliers").classes("text-h6 font-medium text-gray-700 q-mt-md")

            create_supplier_cards()

            # Product demand section
            with ui.card().classes("w-full q-mt-md"):
                create_product_demand_cards()
