from nicegui import ui, app


def content():
    cycle_id = app.storage.general.get("cycle_id")

    ui.query("body").classes("bg-gray-100")

    with ui.column().classes("w-full max-w-4xl mx-auto p-8 gap-6"):
        # Header section
        with ui.card().classes("w-full"):
            with ui.row().classes("items-center justify-between w-full"):
                with ui.column().classes("gap-1"):
                    ui.label("Cycle Management").classes(
                        "text-h4 font-bold text-primary"
                    )
                    ui.label(f"Cycle ID: {cycle_id}").classes(
                        "text-subtitle1 text-gray-600"
                    )

                ui.button(
                    "Back to Home", icon="home", on_click=lambda: ui.navigate.to("/")
                ).props("flat color=secondary")

        # Navigation cards
        ui.label("Quick Actions").classes("text-h6 font-medium text-gray-700 q-mt-md")

        with ui.row().classes("w-full gap-4"):
            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow")
                .on("click", lambda: ui.navigate.to("/cycle/product"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("inventory_2", size="48px").classes("text-primary")
                    ui.label("Product").classes("text-h6 font-medium")
                    ui.label("Manage products").classes("text-caption text-gray-600")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow")
                .on("click", lambda: ui.navigate.to("/cycle/customer"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("person", size="48px").classes("text-green")
                    ui.label("Customer").classes("text-h6 font-smedium")
                    ui.label("Manage customers").classes("text-caption text-gray-600")

            with (
                ui.card()
                .classes("flex-1 cursor-pointer hover:shadow-lg transition-shadow")
                .on("click", lambda: ui.navigate.to("/cycle/supply"))
            ):
                with ui.column().classes("items-center gap-3 p-4"):
                    ui.icon("local_shipping", size="48px").classes("text-orange")
                    ui.label("Supply").classes("text-h6 font-medium")
                    ui.label("Manage supplies").classes("text-caption text-gray-600")
