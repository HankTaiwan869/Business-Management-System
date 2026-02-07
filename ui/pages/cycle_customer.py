from nicegui import ui
from database.db_operations_general import (
    get_customers,
    get_products,
)
from database.db_operations_cycle import (
    get_orders_by_customer_and_product,
    update_customer_order,
)
from utils.helpers import get_current_cycle_id, is_valid_number
from logic.logic import calculate_total_price_by_customer
from ui.components.cycle_components import (
    create_cycle_navigation_buttons,
    create_header,
)


def ui_update_order(
    cycle_id: int,
    customer_id: int,
    product_id: int | None,
    quantity: float,
    dialog=None,
) -> None:
    try:
        if not is_valid_number(quantity):
            ui.notify("數量必須為正數", type="negative")
            return
        if product_id is None:
            ui.notify("未選擇商品", type="negative")
            return
        update_customer_order(cycle_id, customer_id, product_id, quantity)
        ui.notify("儲存成功", type="positive")
        if dialog is not None:
            dialog.close()
    except Exception as e:
        ui.notify(f"失敗({e})，請確認商品價錢已更新再下訂單", type="negative")


def add_order_dialog(cycle_id: int, customer_id: int, customer_name: str):
    products = get_products()
    products_dict = {product.name: product.id for product in products}
    with ui.dialog() as dialog, ui.card():
        ui.label(f"新增訂單：{customer_name}")
        update_prod = ui.select(
            options=list(products_dict.keys()), label="選擇一項商品"
        ).classes("w-full")
        update_quan = ui.number(label="輸入訂單數量", value=0, min=0, step=1)
        ui.button(
            "確認新增",
            on_click=lambda: ui_update_order(
                cycle_id,
                customer_id,
                products_dict.get(update_prod.value),
                update_quan.value,
                dialog,
            ),
        )
    dialog.open()


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
                with ui.row().classes("w-full"):
                    ui.label(customer.name).classes("flex-1")
                    ui.button(
                        "新增訂單",
                        on_click=lambda cust=customer: add_order_dialog(
                            get_current_cycle_id(), cust.id, cust.name
                        ),
                    ).props("outline color=green").classes("self-end")
                with ui.column():
                    for product in products:
                        if (customer.id, product.id) not in order_quantities:
                            continue
                        with ui.row():
                            quantity = ui.number(
                                f"{product.name}",
                                min=0.0,
                                value=order_quantities[(customer.id, product.id)],
                            )
                            ui.button(
                                "更新",
                                on_click=lambda _, cust=customer, prod=product, qty=quantity: (
                                    ui_update_order(
                                        get_current_cycle_id(),
                                        cust.id,
                                        prod.id,
                                        qty.value,
                                    )
                                ),
                            ).props("outline color=primary").classes("self-end")

                    ui.label(
                        f"訂單總額：${calculate_total_price_by_customer(get_current_cycle_id(), customer, order_quantities)}"
                    )


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.row().classes("w-full gap-8 p-8"):
        with ui.column():
            create_cycle_navigation_buttons()
        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("顧客訂單管理")

            # Customer table section
            ui.label("顧客總覽").classes("text-h6 font-medium text-gray-700 q-mt-md")

            create_customer_cards()
