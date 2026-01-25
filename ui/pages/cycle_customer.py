from nicegui import ui
from database.db_operations import add_customer
from database.models import Customer


def add_customer_ui(name: str, discount: float = 0.0):
    """Add a new customer to the database."""
    try:
        add_customer(name, discount)
        ui.notify(f"Customer '{name}' added successfully!", type="positive")
    except Exception as e:
        ui.notify(f"Error: {e}", type="negative")


def content():
    ui.label("This is cycle customer page.")
    ui.link("Go back to cycle", "/cycle")
    ui.separator()
    name = ui.input("Customer Name")
    discount = ui.number("Discount", value=0)
    ui.button("Add Customer").on_click(
        lambda: add_customer_ui(name.value, discount.value)
    )
