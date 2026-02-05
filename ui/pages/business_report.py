from nicegui import ui, APIRouter
from datetime import datetime
from utils.helpers import is_valid_year, is_valid_month, get_current_cycle_id
from utils.plotting_helpers import (
    profits_by_cycle_plot,
    orders_by_product_and_cycle_plot,
)
from database.db_operations import get_monthly_figures

router = APIRouter(prefix="/report")


def ui_monthly_report(container, year: float, month: float) -> None:
    if not is_valid_year(year) or not is_valid_month(month):
        ui.notify("Please enter valid year/month!", type="negative")
        return
    revenue, cost = get_monthly_figures(int(year), int(month))

    container.clear()
    with container:
        with ui.grid(columns=2).classes("gap-4 w-full"):
            with ui.card().classes("p-6"):
                ui.label("Revenue").classes("text-sm text-gray-500 mb-2")
                ui.label(f"${round(revenue):,}").classes(
                    "text-3xl font-bold text-blue-600"
                )
            with ui.card().classes("p-6"):
                ui.label("Cost").classes("text-sm text-gray-500 mb-2")
                ui.label(f"${round(cost):,}").classes("text-3xl font-bold text-red-600")
            with ui.card().classes("p-6"):
                ui.label("Profit").classes("text-sm text-gray-500 mb-2")
                profit = revenue - cost
                ui.label(f"${round(profit):,}").classes(
                    f"text-3xl font-bold {'text-green-600' if profit >= 0 else 'text-red-600'}"
                )
            with ui.card().classes("p-6"):
                ui.label("Profit Margin").classes("text-sm text-gray-500 mb-2")
                margin = (revenue - cost) / revenue * 100 if revenue != 0 else 0
                ui.label(f"{margin:.2f}%").classes(
                    f"text-3xl font-bold {'text-green-600' if margin >= 0 else 'text-red-600'}"
                )


def ui_trend_plots() -> None:
    current_cycle_id = get_current_cycle_id()
    begin_cycle = max(current_cycle_id - 20, 1)
    end_cycle = current_cycle_id
    with ui.matplotlib(figsize=(8, 5)).figure as fig:
        profits_by_cycle_plot(fig, begin_cycle, end_cycle)
    with ui.matplotlib(figsize=(8, 5)).figure as fig:
        orders_by_product_and_cycle_plot(fig, begin_cycle, end_cycle)


@router.page("/")
def report_page():
    ui.query("body").classes("bg-gray-100")

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header card
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                with ui.column().classes("gap-1"):
                    ui.label("Business Report").classes(
                        "text-h4 font-bold text-primary"
                    )

                ui.button(
                    "Back to Home", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("flat color=secondary")

        # Tabs card
        with ui.card().classes("w-full"):
            with ui.tabs().classes("w-full") as tabs:
                ui.tab("monthly_report", "Monthly Report", icon="local_atm")
                ui.tab("trend", "Trend", icon="trending_up")

            ui.separator()

            with ui.tab_panels(tabs, value="monthly_report").classes("w-full"):
                with ui.tab_panel("monthly_report"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        with ui.row().classes("w-full justify-center items-end gap-4"):
                            year = ui.number(
                                "Year",
                                min=2000,
                                step=1,
                                value=datetime.now().year,
                            ).classes("w-32 text-lg")
                            month = ui.number(
                                "Month",
                                min=1,
                                max=12,
                                step=1,
                                value=datetime.now().month,
                            ).classes("w-32 text-lg")
                            ui.button(
                                "Search",
                                on_click=lambda: ui_monthly_report(
                                    container, year.value, month.value
                                ),
                                icon="search",
                            ).props("color=primary").classes("px-6")
                        container = ui.column().classes("w-full")

                with ui.tab_panel("trend"):
                    with ui.column().classes("gap-4 w-full p-4"):
                        ui_trend_plots()
