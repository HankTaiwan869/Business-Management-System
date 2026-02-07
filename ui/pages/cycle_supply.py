from nicegui import ui
from database.db_operations_general import (
    get_products,
    get_suppliers,
)
from database.db_operations_cycle import (
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
    cycle_id: int,
    supplier_id: int,
    product_id: int,
    quantity: float,
    price: float,
    dialog=None,
) -> None:
    try:
        if not is_valid_number(quantity) or not is_valid_number(price):
            ui.notify("數量/價格須為正數", type="negative")
            return
        if product_id is None:
            ui.notify("未選擇商品", type="negative")
            return
        update_supplier_order(cycle_id, supplier_id, product_id, quantity, price)
        ui.notify("儲存成功", type="positive")
        if dialog is not None:
            dialog.close()
    except Exception:
        ui.notify(f"失敗({Exception})", type="negative")


def add_supply_order_dialog(
    cycle_id: int, supplier_id: int, supplier_name: str
) -> None:
    products = get_products()
    products_dict = {product.name: product.id for product in products}
    with ui.dialog() as dialog, ui.card():
        ui.label(f"新增訂單：{supplier_name}")
        update_prod = ui.select(
            options=list(products_dict.keys()), label="選擇一項商品"
        ).classes("w-full")
        update_quan = ui.number(label="輸入訂單數量", value=0, min=0, step=1)
        update_price = ui.number(label="輸入訂單價格", value=0, min=0)
        ui.button(
            "確認新增",
            on_click=lambda: ui_update_supply_order(
                cycle_id,
                supplier_id,
                products_dict.get(update_prod.value),
                update_quan.value,
                update_price.value,
                dialog,
            ),
        )
    dialog.open()


# dynamically create supplier order cards
def create_supplier_cards():
    suppliers = get_suppliers()
    products = get_products()
    # dictionary mapping from tuple (supplier id, product id) to namedtuple (quantity, buy price)
    orders = get_orders_by_supplier_and_product(get_current_cycle_id())

    with ui.grid(columns=3):
        for supplier in suppliers:
            with ui.card():
                with ui.row().classes("w-full"):
                    ui.label(supplier.name).classes("text-h6 font-medium flex-1")
                    ui.button(
                        "新增訂單",
                        on_click=lambda sup=supplier: add_supply_order_dialog(
                            get_current_cycle_id(), sup.id, sup.name
                        ),
                    ).props("outline color=green").classes("self-end")
                with ui.column().classes("gap-2"):
                    for product in products:
                        if (supplier.id, product.id) not in orders:
                            continue
                        with ui.column().classes("gap-1"):
                            ui.label(product.name).classes("text-subtitle2 font-medium")
                            with ui.row().classes("gap-2"):
                                quantity = ui.number(
                                    "叫貨數量",
                                    min=0.0,
                                    value=orders[(supplier.id, product.id)].quantity
                                    if (supplier.id, product.id) in orders
                                    else 0,
                                ).classes("flex-1")
                                price = ui.number(
                                    "價錢",
                                    min=0.0,
                                    value=orders[(supplier.id, product.id)].price
                                    if (supplier.id, product.id) in orders
                                    else 0,
                                ).classes("flex-1")
                            ui.button(
                                "儲存",
                                on_click=lambda _, sup=supplier, prod=product, qty=quantity, pri=price: (
                                    ui_update_supply_order(
                                        get_current_cycle_id(),
                                        sup.id,
                                        prod.id,
                                        qty.value,
                                        pri.value,
                                    )
                                ),
                            ).props("outline color=primary").classes("self-end")
                ui.separator()
                ui.label(
                    f"叫貨訂單總額：${calculate_total_price(supplier.id):.2f}"
                ).classes("text-subtitle1 font-bold")


def create_product_demand_cards():
    products = get_products()

    with ui.column().classes("gap-3"):
        ui.label("產品需求列表").classes("text-h6 font-medium text-gray-700")
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
                    ui.label(f"目前尚須{remaining}").classes(
                        "text-body2 text-orange-600"
                    )
                elif remaining == 0:
                    ui.label("數量剛好！").classes("text-body2 text-green-600")
                else:
                    ui.label(f"目前多訂{abs(remaining)}").classes(
                        "text-body2 text-blue-600"
                    )


def content():
    ui.query("body").classes("bg-gray-100")

    with ui.row().classes("w-full gap-8 p-8"):
        create_cycle_navigation_buttons()

        # Main content area
        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("上游叫貨管理")

            # Supply table section
            ui.label("上游總覽").classes("text-h6 font-medium text-gray-700 q-mt-md")

            create_supplier_cards()

            # Product demand section
            with ui.card().classes("w-full q-mt-md"):
                create_product_demand_cards()
