import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import flet as ft
from frontend.views_handler import get_page

current_user_email = None
# Definición del método principal con el enrutamiento de la aplicación
def main(page: ft.Page):
    def route_change(route):
        page.views.clear()

        view = get_page(page, current_user_email)

        if view:
            page.views.append(view)
        else:
            page.go("/login")  # Redirección en caso de ruta desconocida
        page.update()

    page.theme_mode="light"
    page.bgcolor = ft.Colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE,
    page.on_route_change = route_change
    page.go("/login")  # Ruta inicial

ft.app(target=main)