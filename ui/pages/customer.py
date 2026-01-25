from nicegui import ui, APIRouter
from database.db_operations import get_customers

router = APIRouter(prefix="/customer")


@router.page("/")
def customer_page():
    ui.label("This is the customer page.")
    ui.link("Go back to home", "/")
    ui.separator()
    ui.table.from_pandas(get_customers()).classes("w-auto")
