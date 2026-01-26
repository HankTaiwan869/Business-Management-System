from nicegui import ui, APIRouter, app
from . import cycle_customer, cycle_product, cycle_supply

router = APIRouter(prefix="/cycle")


@router.page("/")
def cycle_page():
    cycle_id = app.storage.general.get("cycle_id")
    ui.label(f"This is cycle page for cycle {cycle_id}")
    ui.link("Go back to Home", "/")
    ui.link("Product", "/cycle/product")
    ui.link("Customer", "/cycle/customer")
    ui.link("Supply", "/cycle/supply")


@router.page("/product")
def cycle_product_page():
    cycle_product.content()


@router.page("/customer")
def cycle_customer_page():
    cycle_customer.content()


@router.page("/supply")
def cycle_supply_page():
    cycle_supply.content()
