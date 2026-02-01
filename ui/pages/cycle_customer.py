from nicegui import ui, app
from database.models import Customer, Product, Order
from database.db_operations import (
    get_customers,
    get_products,
    get_orders_by_customer_and_product,
    update_order,
)
from typing import Sequence

cycle_id = app.storage.general.get("cycle_id")


def calculate_total_price(
    customer: Customer,
    products: Sequence[Product],
    orders: dict[tuple[int, int], Order],
) -> float:
    total = 0
    for product in products:
        if (customer.id, product.id) in orders:
            total += orders[(customer.id, product.id)].price
    return total


def ui_update_order(cycle_id: int, customer_id: int, product_id: int, quantity: float):
    try:
        if quantity <= 0:
            ui.notify("Quantity has to be positive", type="negative")
            return
        update_order(cycle_id, customer_id, product_id, quantity)
        ui.notify("Successful!", type="positive")
    except Exception as e:
        ui.notify(f"Failed because of {e}", type="negative")


# dynamically create a card for each customer
def create_customer_card():
    customers = get_customers()
    products = get_products()
    orders = get_orders_by_customer_and_product(
        cycle_id
    )  # Dictionary for Order dataclass

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
                                value=orders[(customer.id, product.id)].quantity
                                if (customer.id, product.id) in orders
                                else 0,
                            )
                            ui.button(
                                "Save",
                                on_click=lambda cust=customer,
                                prod=product,
                                qty=quantity: ui_update_order(
                                    cycle_id,
                                    cust.id,
                                    prod.id,
                                    qty.value,
                                ),
                            )
                    ui.label(
                        f"Total: {calculate_total_price(customer, products, orders)}"
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
                icon="eco",
                on_click=lambda: ui.navigate.to("/cycle/product"),
            ).props("round color=primary").tooltip("Product")

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
                        ui.label("Customer Management").classes(
                            "text-h4 font-bold text-green"
                        )
                        ui.label(f"Cycle ID: {cycle_id}").classes(
                            "text-subtitle1 text-gray-600"
                        )

                    ui.button(
                        "Back to Cycle",
                        icon="arrow_back",
                        on_click=lambda: ui.navigate.to("/cycle"),
                    ).props("flat color=secondary")

            # Customer table section
            ui.label("Customers").classes("text-h6 font-medium text-gray-700 q-mt-md")

            create_customer_card()
