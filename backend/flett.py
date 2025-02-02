import flet as ft
from views.admin import admin
from services.db_users import is_admin
from views.login import login
from views.register import register
from views.home import home  # Importa la vista de home
#from views.admin_page import admin  # Importa la vista de la página de admin

# Suponiendo que el email del usuario está almacenado en una variable global
current_user_email = None

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()

        # Si el usuario no está autenticado, redirigir a login
    

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
            page.views.append(admin(page))  # Página solo accesible para admin

        page.update()

    page.on_route_change = route_change
    page.go("/login")  # Establece la ruta inicial

ft.app(target=main)
