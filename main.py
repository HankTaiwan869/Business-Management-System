from nicegui import ui, app
from ui.pages import cycle_router, overview, business_report
from datetime import datetime

# Development only import
from database.db_operations import (
    db_reset,
    start_cycle,
    get_current_settings,
    get_cycle_start_date,
    initialize_database,
)

from utils.helpers import get_current_cycle_id

app.include_router(cycle_router.router)
app.include_router(overview.router)
app.include_router(business_report.router)


# ======== developemtn only =========
def reset():
    try:
        db_reset()

        ui.notify("Database has been reset.", color="green")
    except Exception as e:
        ui.notify(f"Error resetting database: {e}", color="red")


# ======== developemtn only =========


def ui_start_cycle(current_settings):
    start_cycle()
    app.storage.general["cycle_id"] = get_current_settings().cycle_id


@ui.page("/")
def home():
    ui.query("body").classes("bg-gray-100")

    initialize_database()

    current_settings = get_current_settings()
    app.storage.general["cycle_id"] = current_settings.cycle_id

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header
        with ui.card().classes("w-full"):
            with ui.column().classes("p-4 gap-2"):
                ui.label("荖葉管理中心🍃").classes("text-h4 font-bold")

        # Current cycle status card
        ui.label("期數資訊").classes("text-h6 font-medium text-gray-700 q-mt-md")

        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full p-2"):
                if current_settings.is_in_cycle:
                    # Status badge
                    with ui.badge(color="green").classes("text-sm px-3 py-1"):
                        ui.label("進行中")
                    ui.label(
                        f"現在：第{current_settings.cycle_id}期 (開始日期：{get_cycle_start_date(get_current_cycle_id())})"
                    ).classes("text-subtitle1")
                else:
                    # Status badge
                    with ui.badge(color="gray").classes("text-sm px-3 py-1"):
                        ui.label("休息中")
                    ui.label(f"今日日期：{datetime.now().date()}").classes(
                        "text-subtitle1"
                    )

        # Action cards
        ui.label("主選單").classes("text-h6 font-medium text-gray-700 q-mt-md")

        with ui.row().classes("w-full gap-4"):
            # Start new cycle card
            start_card = ui.card().classes(
                "flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70"
            )
            start_card.bind_visibility_from(
                current_settings, "is_in_cycle", lambda v: not v
            )
            with start_card:
                start_card.on(
                    "click",
                    lambda: [
                        ui_start_cycle(current_settings),
                        ui.navigate.to("/cycle"),
                    ],
                )
                with ui.column().classes(
                    "items-center justify-center gap-3 p-4 w-full h-full"
                ):
                    ui.icon("play_circle", size="48px").classes("text-green")
                    ui.label("開始新一期").classes("text-h6 font-medium")

            # Continue cycle card
            continue_card = ui.card().classes(
                "flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70"
            )
            continue_card.bind_visibility_from(current_settings, "is_in_cycle")
            with continue_card:
                continue_card.on("click", lambda: ui.navigate.to("/cycle"))
                with ui.column().classes(
                    "items-center justify-center gap-3 p-4 w-full h-full"
                ):
                    ui.icon("restart_alt", size="48px").classes("text-blue")
                    ui.label("繼續本期").classes("text-h6 font-medium")

            # Overview card
            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/overview"))
            ):
                with ui.column().classes(
                    "items-center justify-center gap-3 p-4 w-full h-full"
                ):
                    ui.icon("dashboard", size="48px").classes("text-purple")
                    ui.label("後臺總覽").classes("text-h6 font-medium")
                    ui.label("顧客、商品、供應商資訊").classes(
                        "text-subtitle2 text-gray-600 text-center"
                    )

            # Report card
            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow h-70")
                .on("click", lambda: ui.navigate.to("/report"))
            ):
                with ui.column().classes(
                    "items-center justify-center gap-3 p-4 w-full h-full"
                ):
                    ui.icon("assessment", size="48px").classes("text-blue")
                    ui.label("分析報表").classes("text-h6 font-medium")

        # ======== development only =========
        with (
            ui.expansion("開發者工具 (勿點)", icon="build")
            .classes("w-full q-mt-lg bg-red-50")
            .props("dense")
        ):
            with ui.column().classes("gap-2 p-2"):
                ui.label("⚠️ Warning: Development only").classes(
                    "text-caption text-red-600 font-medium"
                )
                ui.button(
                    "Reset Database", on_click=reset, icon="delete_forever"
                ).props("color=red outline")
        # ======== development only =========


ui.run()
