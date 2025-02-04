import flet as ft
from views.admin import admin
from services.db_users import is_admin
from views.login import login
from views.register import register
from views.home import home
from views.parking import parking  # Nueva importación

current_user_email = None

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()

        # Verificar si el usuario es administrador antes de permitir el acceso a la página de administrador
        if route == "/admin" and not is_admin(current_user_email):
            page.go("/home")  # Redirigir a home si no es admin

        # Enrutamiento normal
        if page.route == "/login":
            page.views.append(login(page))
        elif page.route == "/register":
            page.views.append(register(page))
        elif page.route == "/home":
            page.views.append(home(page))
        elif page.route == "/admin":
            page.views.append(admin(page))
        elif page.route == "/parking":  # Nueva ruta para la vista del parking
            page.views.append(parking(page))

        page.update()

    page.on_route_change = route_change
    page.go("/login")  # Ruta inicial

ft.app(target=main)
