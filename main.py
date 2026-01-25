from nicegui import ui, app
from ui.pages import cycle
from ui.pages import customer

# Development only import
from database.db_operations import db_reset

app.include_router(cycle.router)
app.include_router(customer.router)


def reset():
    try:
        db_reset()
        ui.notify("Database has been reset.", color="green")
    except Exception as e:
        ui.notify(f"Error resetting database: {e}", color="red")


@ui.page("/")
def home():
    ui.label("Home Page").classes("text-2xl")
    ui.link("Start a new cycle", "/cycle")
    ui.link("View customers", "/customer")

    # development only button
    ui.button("Reset Database", on_click=reset).props("color=red")


ui.run()
