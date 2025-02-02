import flet as ft

def home(page: ft.Page):
    print("Página de inicio")
    return ft.View(
        ft.Container(
            ft.Text("Bienvenido a la página de inicio"),
        )
    )