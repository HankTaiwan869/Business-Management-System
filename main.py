from nicegui import ui, app
from ui.pages import cycle_router
from ui.pages import overview

# Development only import
from database.db_operations import db_reset, start_cycle, get_settings

app.include_router(cycle_router.router)
app.include_router(overview.router)


# developemtn only
def reset():
    try:
        db_reset()

        ui.notify("Database has been reset.", color="green")
    except Exception as e:
        ui.notify(f"Error resetting database: {e}", color="red")


def ui_start_cycle(current_settings):
    start_cycle()
    app.storage.general["cycle_id"] = get_settings().cycle_id


@ui.page("/")
def home():
    ui.query("body").classes("bg-gray-100")

    # Store cycle information in app.storage.general['cycle_id']
    current_settings = get_settings()
    app.storage.general["cycle_id"] = current_settings.cycle_id

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header
        with ui.card().classes("w-full"):
            with ui.column().classes("p-4 gap-2"):
                ui.label("Welcome to Cycle Manager").classes("text-h4 font-bold")
                ui.label("Manage your cycles and database operations").classes(
                    "text-subtitle1 text-gray-600"
                )

        # Current cycle status card
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                with ui.column().classes("gap-1"):
                    ui.label("Current Status").classes("text-h6 font-medium")
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("info", size="20px").classes("text-primary")
                        ui.label(f"Cycle ID: {current_settings.cycle_id}").classes(
                            "text-subtitle1"
                        )

                # Status badge
                with (
                    ui.badge()
                    .props(
                        f"color={'green' if current_settings.is_in_cycle else 'gray'}"
                    )
                    .classes("text-sm px-3 py-1")
                ):
                    ui.label("Active" if current_settings.is_in_cycle else "Inactive")

        # Action cards
        ui.label("Actions").classes("text-h6 font-medium text-gray-700 q-mt-md")

        with ui.row().classes("w-full gap-4"):
            # Start new cycle card
            start_card = ui.card().classes(
                "flex-1 cursor-pointer hover:shadow-lg transition-shadow"
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
                with ui.column().classes("items-center gap-2 p-4"):
                    ui.icon("play_circle", size="40px").classes("text-green")
                    ui.label("Start New Cycle").classes("text-subtitle1 font-medium")
                    ui.label("Begin a fresh cycle").classes(
                        "text-caption text-gray-600 text-center"
                    )

            # Continue cycle card
            continue_card = ui.card().classes(
                "flex-1 cursor-pointer hover:shadow-lg transition-shadow"
            )
            continue_card.bind_visibility_from(current_settings, "is_in_cycle")
            with continue_card:
                continue_card.on("click", lambda: ui.navigate.to("/cycle"))
                with ui.column().classes("items-center gap-2 p-4"):
                    ui.icon("restart_alt", size="40px").classes("text-blue")
                    ui.label("Continue Cycle").classes("text-subtitle1 font-medium")
                    ui.label("Resume current cycle").classes(
                        "text-caption text-gray-600 text-center"
                    )

            # Overview card
            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow")
                .on("click", lambda: ui.navigate.to("/overview"))
            ):
                with ui.column().classes("items-center gap-2 p-4"):
                    ui.icon("dashboard", size="40px").classes("text-purple")
                    ui.label("Overview").classes("text-subtitle1 font-medium")
                    ui.label("Manage database").classes(
                        "text-caption text-gray-600 text-center"
                    )

        # Developer section
        with (
            ui.expansion("Developer Tools", icon="build")
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


ui.run()
