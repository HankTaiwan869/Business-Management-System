from nicegui import ui
from ui.components.cycle_components import (
    create_cycle_navigation_buttons,
    create_header,
)
from logic.logic import calculate_cycle_financial_metrics
from utils.helpers import get_current_cycle_id
from utils.plotting_helpers import profit_by_product_plot, revenue_by_customer_plot


def content():
    ui.query("body").classes("bg-gray-100")

    metrics = calculate_cycle_financial_metrics(get_current_cycle_id())

    with ui.row().classes("w-full gap-8 p-8"):
        create_cycle_navigation_buttons()

        with ui.column().classes("flex-1 max-w-4xl gap-6"):
            create_header("本期報告")

            with ui.row().classes("w-full gap-4 justify-center"):
                with ui.column().classes("w-64 gap-4"):
                    # Revenue Card
                    with ui.card().classes("p-4 w-full"):
                        ui.label("營收").classes("text-base text-black-600 mb-1")
                        ui.label(f"${round(metrics['revenue']):,}").classes(
                            "text-2xl font-bold text-red-600"
                        )

                    # Cost Card
                    with ui.card().classes("p-4 w-full"):
                        ui.label("成本").classes("text-base text-black-600 mb-1")
                        ui.label(f"${round(metrics['cost']):,}").classes(
                            "text-2xl font-bold text-green-600"
                        )

                # Net Profit Card with Growth Rate
                with ui.card().classes("p-4 w-64"):
                    ui.label("利潤 (毛利率)").classes("text-base text-black-600 mb-1")
                    if metrics["previous_profit"] == 0 or metrics["growth"] > 0:
                        ui.label(
                            f"${round(metrics['profit']):,} ({metrics['profit_margin']:.2f}%)"
                        ).classes("text-2xl font-bold text-red-600")
                    else:
                        ui.label(
                            f"${round(metrics['profit']):,} ({metrics['profit_margin']:.2f}%)"
                        ).classes("text-2xl font-bold text-green-600")
                    ui.label("與上期比較").classes("text-base text-black-600 mb-1")
                    if metrics["previous_profit"] != 0:
                        if metrics["growth"] > 0:
                            ui.label(f"↑ {metrics['growth']:.2f}%").classes(
                                "text-2xl font-bold text-red-600"
                            )
                        else:
                            ui.label(f"↓ {metrics['growth']:.2f}%").classes(
                                "text-2xl font-bold text-green-600"
                            )
            with ui.matplotlib(figsize=(8, 5)).figure as fig:
                profit_by_product_plot(fig, get_current_cycle_id())
            with ui.matplotlib(figsize=(8, 5)).figure as fig:
                revenue_by_customer_plot(fig, get_current_cycle_id())
