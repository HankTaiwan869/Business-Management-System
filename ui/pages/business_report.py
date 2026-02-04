from nicegui import ui, APIRouter

router = APIRouter(prefix="/report")


@router.page("/")
def report_page():
    ui.label("Hi")
