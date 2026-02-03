from nicegui import ui
from database.models import Customer, Product
from database.db_operations import (
    get_customers,
    get_products,
    get_orders_by_customer_and_product,
    get_product_price_by_product_id,
    update_customer_order,
)
from typing import Sequence
import utils.validators as validators
from utils.helpers import get_current_cycle_id
from ui.components.cycle_components import (
    create_cycle_navigation_buttons,
    create_header,
)


def calculate_total_price(
    customer: Customer,
    products: Sequence[Product],
    order_quantities: dict[tuple[int, int], float],
) -> float | None:
    total = 0
    for product in products:
        if (customer.id, product.id) in order_quantities:
            price = get_product_price_by_product_id(get_current_cycle_id(), product.id)
            if price is None:
                raise ValueError(
                    f"No price found for product {product.id} in cycle {get_current_cycle_id()}"
                )
            total += (price - customer.discount) * order_quantities[
                (customer.id, product.id)
            ]
    return total


def ui_update_order(
    cycle_id: int, customer_id: int, product_id: int, quantity: float
) -> None:
    try:
        if not validators.is_valid_number(quantity):
            ui.notify("Quantity has to be positive", type="negative")
            return
        update_customer_order(cycle_id, customer_id, product_id, quantity)
        ui.notify("Successful!", type="positive")
    except Exception as e:
        ui.notify(f"Failed because of {e}", type="negative")


# dynamically create a card for each customer
def create_customer_cards():
    customers = get_customers()
    products = get_products()
    order_quantities = get_orders_by_customer_and_product(
        get_current_cycle_id()
    )  # Dictionary for order quantity

    with ui.grid(columns=3):
        for customer in customers:
            with ui.card():
                ui.label(customer.name)
                with ui.column():
                    for product in products:
                        with ui.row():
                            quantity = ui.number(
                                f"{product.name}",
                                min=0.0,
                                # Show order quantity if exists, otherwise 0
                                value=order_quantities[(customer.id, product.id)]
                                if (customer.id, product.id) in order_quantities
                                else 0,
                            )
                            ui.button(
                                "Save",
                                on_click=lambda cust=customer,
                                prod=product,
                                qty=quantity: ui_update_order(
                                    get_current_cycle_id(),
                                    cust.id,
                                    prod.id,
                                    qty.value,
                                ),
                            )
                    ui.label(
                        f"Total: {calculate_total_price(customer, products, order_quantities)}"
                    )


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.row().classes("w-full gap-8 p-8"):
        create_cycle_navigation_buttons()

        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("Customer Management")

            # Customer table section
            ui.label("Customers").classes("text-h6 font-medium text-gray-700 q-mt-md")

            create_customer_cards()
