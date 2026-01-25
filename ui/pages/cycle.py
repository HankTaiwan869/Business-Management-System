from nicegui import ui, APIRouter
from . import cycle_customer, cycle_product, cycle_supply

router = APIRouter(prefix="/cycle")


@router.page("/")
def cycle_page():
    ui.label("This is cycle page")
    ui.link("Go back to Home", "/")
    ui.link("Product", "/cycle/product")
    ui.link("Customer", "/cycle/customer")
    ui.link("suuply", "/cycle/supply")


@router.page("/product")
def cycle_product_page():
    cycle_product.content()


@router.page("/customer")
def cycle_customer_page():
    cycle_customer.content()


@router.page("/supply")
def cycle_supply_page():
    cycle_supply.content()
