from nicegui import ui
from ui.components.cycle_components import (
    create_cycle_navigation_buttons,
    create_header,
)
from logic.logic import calculate_total_cost, calculate_total_revenue
from utils.helpers import get_current_cycle_id
from utils.plotting_helpers import profit_by_product_plot, revenue_by_customer_plot


def content():
    ui.query("body").classes("bg-gray-100")

    cycle_id = get_current_cycle_id()
    new_revenue = calculate_total_revenue(cycle_id)
    new_cost = calculate_total_cost(cycle_id)
    new_profit = new_revenue - new_cost
    old_revenue = calculate_total_revenue(cycle_id - 1)
    old_cost = calculate_total_cost(cycle_id - 1)
    old_profit = old_revenue - old_cost
    if old_profit != 0:  # skip this for the first cycle
        growth = (new_profit - old_profit) / old_profit * 100

    with ui.row().classes("w-full gap-8 p-8"):
        create_cycle_navigation_buttons()

        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("Cycle Report")

            with ui.row().classes("w-full gap-4 justify-center"):
                with ui.column().classes("w-64 gap-4"):
                    # Revenue Card
                    with ui.card().classes("p-4 w-full"):
                        ui.label("Revenue").classes("text-base text-black-600 mb-1")
                        ui.label(f"${round(new_revenue):,}").classes(
                            "text-2xl font-bold text-red-600"
                        )

                    # Cost Card
                    with ui.card().classes("p-4 w-full"):
                        ui.label("Cost").classes("text-base text-black-600 mb-1")
                        ui.label(f"${round(new_cost):,}").classes(
                            "text-2xl font-bold text-green-600"
                        )

                # Net Profit Card with Growth Rate
                with ui.card().classes("p-4 w-64"):
                    ui.label("Net Profit").classes("text-base text-black-600 mb-1")
                    if old_profit == 0 or growth > 0:
                        ui.label(f"${round(new_profit):,}").classes(
                            "text-2xl font-bold text-red-600"
                        )
                    else:
                        ui.label(f"${round(new_profit):,}").classes(
                            "text-2xl font-bold text-green-600"
                        )
                    ui.label("Compared with last cycle").classes(
                        "text-base text-black-600 mb-1"
                    )
                    if old_profit != 0:
                        if growth > 0:
                            ui.label(f"↑ {growth:.2f}%").classes(
                                "text-2xl font-bold text-red-600"
                            )
                        else:
                            ui.label(f"↓ {growth:.2f}%").classes(
                                "text-2xl font-bold text-green-600"
                            )
            with ui.matplotlib(figsize=(8, 5)).figure as fig:
                profit_by_product_plot(fig, cycle_id)
            with ui.matplotlib(figsize=(8, 5)).figure as fig:
                revenue_by_customer_plot(fig, cycle_id)
