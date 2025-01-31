# main.py
import flet as ft
from views.login import login
from views.register import register
#from views.home_view import home_view  # Importa otras vistas si las tienes

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()
        if page.route == "/login":
            page.views.append(login(page))
        elif page.route == "/register":
            page.views.append(register(page))
        # Agrega más rutas según sea necesario
        page.update()

    page.on_route_change = route_change
    page.go("/login")  # Establece la ruta inicial

ft.app(target=main)