from nicegui import ui, app
from ui.pages import cycle
from ui.pages import overview

# Development only import
from database.db_operations import db_reset, start_cycle, get_settings

app.include_router(cycle.router)
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

    # Store cycle information
    current_settings = get_settings()
    app.storage.general["cycle_id"] = current_settings.cycle_id

    ui.label("Home Page").classes("text-2xl")
    ui.label(f"Current Cycle ID: {current_settings.cycle_id}").classes("text-lg")
    start_cycle_button = ui.link("Start a new cycle", "/cycle").bind_visibility_from(
        current_settings, "is_in_cycle", lambda v: not v
    )
    start_cycle_button.on("click", lambda: ui_start_cycle(current_settings))
    ui.link("Continue the current cycle", "/cycle").bind_visibility_from(
        current_settings, "is_in_cycle"
    )
    ui.link("Overview/Add to Database", "/overview")

    # development only button
    ui.button("Reset Database", on_click=reset).props("color=red")


ui.run()
