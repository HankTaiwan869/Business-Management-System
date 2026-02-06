from nicegui import ui, APIRouter
from database.db_operations import (
    add_customer,
    add_product,
    add_supplier,
    get_customers,
    get_products,
    get_suppliers,
    update_customer_discount,
)
from utils.helpers import is_valid_number, is_valid_name

router = APIRouter(prefix="/overview")


def ui_update_customer_discount(dialog, name: str, discount: float) -> None:
    try:
        if not is_valid_number(discount):
            ui.notify("折扣須為正數", type="negative")
            return
        update_customer_discount(name, discount)
        ui.notify("更新成功！", type="positive")
        customer_table.refresh()
        dialog.close()
    except Exception as e:
        ui.notify(f"錯誤({e})", type="negative")


def update_customer_dialogue():
    with ui.dialog() as dialog, ui.card().style("width: 400px; height: 300px;"):
        customers = get_customers()
        customer_discount_map = {
            customer.name: customer.discount for customer in customers
        }

        def show_discount(name: str) -> None:
            discount = ui.number(
                "輸入新折扣", min=0, value=customer_discount_map[name]
            ).classes("w-full")
            ui.button(
                "儲存",
                on_click=lambda: ui_update_customer_discount(
                    dialog, name, discount.value
                ),
            ).classes("w-full mt-4").props("outline color=primary")

        ui.label("更新折扣").classes("text-h6")
        ui.select(
            label="點擊選擇一位顧客",
            options=list(customer_discount_map.keys()),
            clearable=True,
            on_change=lambda name: show_discount(name.value),
        ).classes("w-full")

    dialog.open()


def submit_customer(name, discount):
    try:
        if not is_valid_name(name.value):
            ui.notify("欄位不可空白，請再試一次", type="negative")
            return
        if not is_valid_number(discount.value):
            ui.notify("折扣不可為負數，請再試一次", type="negative")
        add_customer(name.value.strip(), discount.value)
        ui.notify(f"顧客'{name.value.strip()}'已成功加入", type="positive")
        name.value = ""
        discount.value = 0.0
        customer_table.refresh()
    except Exception as e:
        ui.notify(f"錯誤：{e}", type="negative")


def submit_product(product_name_input):
    try:
        if not is_valid_name(product_name_input.value):
            ui.notify("欄位不可空白，請再試一次", type="negative")
            return
        add_product(product_name_input.value.strip())
        ui.notify(
            f"產品'{product_name_input.value.strip()}'已成功加入",
            type="positive",
        )
        product_name_input.value = ""
        product_table.refresh()
    except Exception as e:
        ui.notify(f"錯誤：{e}", type="negative")


def submit_supplier(supplier_name_input):
    try:
        if not is_valid_name(supplier_name_input.value):
            ui.notify("欄位不可空白，請再試一次", type="negative")
            return
        add_supplier(supplier_name_input.value.strip())
        ui.notify(
            f"供應商'{supplier_name_input.value.strip()}'已成功加入",
            type="positive",
        )
        supplier_name_input.value = ""
        supplier_table.refresh()
    except Exception as e:
        ui.notify(f"錯誤：{e}", type="negative")


@ui.refreshable
def customer_table():
    columns = [
        {"name": "id", "label": "顧客編號", "field": "id"},
        {"name": "name", "label": "名字", "field": "name"},
        {"name": "discount", "label": "折扣(退)", "field": "discount"},
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
        {"name": "id", "label": "產品編號", "field": "id"},
        {"name": "name", "label": "產品名", "field": "name"},
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
        {"name": "id", "label": "供應商編號", "field": "id"},
        {"name": "name", "label": "供應商名", "field": "name"},
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
                    ui.label("後臺管理").classes("text-h4 font-bold text-black")
                    ui.label("新增顧客、產品、上游供應商").classes(
                        "text-subtitle1 text-gray-600"
                    )

                ui.button(
                    "回首頁", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("flat color=secondary")

        # Tabs card
        with ui.card().classes("w-full"):
            with ui.tabs().classes("w-full") as tabs:
                ui.tab("add_customer", "顧客", icon="person")
                ui.tab("add_product", "產品", icon="eco")
                ui.tab("add_supplier", "供應商", icon="local_shipping")

            ui.separator()

            with ui.tab_panels(tabs, value="add_customer").classes("w-full"):
                with ui.tab_panel("add_customer"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui.label("新增顧客").classes("text-h6 font-medium")
                        name_input = ui.input("請輸入顧客名").classes("w-full")
                        discount_input = ui.number(
                            "折扣(退)", value=0.0, min=0.0
                        ).classes("w-full")
                        with ui.row():
                            ui.button(
                                "新增顧客",
                                icon="add",
                                on_click=lambda: submit_customer(
                                    name_input, discount_input
                                ),
                            ).props("outline color=primary")
                            ui.button(
                                "更新顧客折扣",
                                icon="edit",
                                on_click=update_customer_dialogue,
                            ).props("outline color=primary")

                        ui.separator().classes("q-my-md")
                        ui.label("現有顧客總覽").classes(
                            "text-subtitle1 font-medium q-mb-sm"
                        )
                        customer_table()

                with ui.tab_panel("add_product"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui.label("新增產品").classes("text-h6 font-medium")
                        product_name_input = ui.input("請輸入產品名").classes("w-full")
                        ui.button(
                            "新增產品",
                            icon="add",
                            on_click=lambda: submit_product(product_name_input),
                        ).props("outline color=primary")

                        ui.separator().classes("q-my-md")
                        ui.label("現有產品總覽").classes(
                            "text-subtitle1 font-medium q-mb-sm"
                        )
                        product_table()

                with ui.tab_panel("add_supplier"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui.label("新增供應商").classes("text-h6 font-medium")
                        supplier_name_input = ui.input("請輸入供應商名").classes(
                            "w-full"
                        )
                        ui.button(
                            "新增供應商",
                            icon="add",
                            on_click=lambda: submit_supplier(supplier_name_input),
                        ).props("outline color=primary")

                        ui.separator().classes("q-my-md")
                        ui.label("現有供應商總覽").classes(
                            "text-subtitle1 font-medium q-mb-sm"
                        )
                        supplier_table()
