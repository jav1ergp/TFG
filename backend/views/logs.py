import flet as ft

def logs(page: ft.Page):
    def logs_view():
        # home
        btn_back = ft.ElevatedButton("Volver", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.LIGHT_BLUE, on_click=lambda _: page.go("/home"))
        
        # layout
        logs_layout = ft.Column(
            [
                ft.Text("Logs", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                btn_back
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        return logs_layout

    return ft.View(
        "/logs",
        bgcolor=ft.Colors.WHITE,
        controls=[
            logs_view()
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )