from nicegui import APIRouter
from . import cycle_customer, cycle_product, cycle_supply, cycle_main_page, cycle_report

router = APIRouter(prefix="/cycle")


@router.page("/")
def cycle_page():
    cycle_main_page.content()


@router.page("/product")
def cycle_product_page():
    cycle_product.content()


@router.page("/customer")
def cycle_customer_page():
    cycle_customer.content()


@router.page("/supply")
def cycle_supply_page():
    cycle_supply.content()


@router.page("/report")
def cycle_report_page():
    cycle_report.content()
