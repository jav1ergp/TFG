import flet as ft

def home(page: ft.Page):
    return ft.View(
        "/home",
        [
            ft.Text("Bienvenido al Parking", size=20),
            ft.ElevatedButton("Ver Estado del Parking", on_click=lambda _: page.go("/parking")),
            ft.ElevatedButton("Ver Estructura del Parking", on_click=lambda _: page.go("/parking2")),
            ft.ElevatedButton("Ver DataBase", on_click=lambda _: page.go("/data")),
            ft.ElevatedButton("Ver Video", on_click=lambda _: page.go("/video")),
            ft.ElevatedButton("Ver Logs", on_click=lambda _: page.go("/logs")),
            ft.ElevatedButton("Cerrar Sesión", on_click=lambda _: page.go("/login")),
        ]
    )
