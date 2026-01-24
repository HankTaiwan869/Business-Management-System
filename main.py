from nicegui import ui
import model as db
from model import Book

# Initialize database for the first time
db.db_init()


# Define Welcome page
@ui.page("/")
def welcome_page():
    ui.image(
        "https://images.theconversation.com/files/45159/original/rptgtpxd-1396254731.jpg?ixlib=rb-4.1.0&q=45&auto=format&w=754&h=502&fit=crop&dpr=1"
    )
    with ui.column().classes("w-full items-center justify-center"):
        ui.label("WELCOME!").classes("text-6xl font-bold")
        ui.link("Press to continune...", "/home").classes("text-2xl")


# Define Home page
@ui.page("/home")
def home_page():
    splitter = ui.splitter(horizontal=True).classes("w-full")
    with splitter.before:
        with ui.tabs().classes("w-full") as tabs:
            view = ui.tab("View", icon="table_rows")
            submit = ui.tab("Submit", icon="send")
            search = ui.tab("Search", icon="search")
            delete = ui.tab("Delete", icon="delete")
            update = ui.tab("Update", icon="edit")
    with splitter.after:
        with ui.tab_panels(tabs, value=view).classes("w-full"):
            with ui.tab_panel(view).classes("w-full"):
                df = db.view()
                ui.table.from_pandas(
                    df,
                    row_key="id",
                    pagination=10,
                    column_defaults={
                        "align": "center",
                        "headerClasses": "uppercase text-primary",
                    },
                ).classes("w-full max-h-[500px] test-base")
            with ui.tab_panel(submit):
                book = Book(title="", rating=0)
                ui.input("Enter book title").bind_value(book, "title").classes(
                    "w-full text-lg"
                )
                ui.number("Enter your rating (1-5)").bind_value(book, "rating").classes(
                    "w-full text-lg"
                )
                ui.button("Submit", on_click=lambda e: submit_book(book)).classes(
                    "w-full text-lg"
                )
            with ui.tab_panel(search):
                pass
            with ui.tab_panel(delete):
                pass
            with ui.tab_panel(update):
                pass


def submit_book(book):
    try:
        db.submit(book)
        ui.notify("Saved Sucessfully", type="positive")
    except Exception as e:
        ui.notify(f"Saving failed due to {e}", type="negative")


ui.run()
