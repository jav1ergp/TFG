import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import flet as ft
from frontend.views_handler import get_page
from frontend.components import *

def main(page: ft.Page):       
    def route_change(route):
        page.views.clear()
        user = page.session.get("user")
        route = page.route
        
        if not user and route not in ("/login", "/register"):
            page.go("/login")
            page.update()
            return
        
        if user and route in ("/login", "/register"):
            page.session.clear()
            page.update()
        
        view = get_page(page)
        
        if view:
            page.views.append(view)
        else:
            page.session.clear()
            page.go("/login")  # Redirección en caso de ruta desconocida
        page.update()

    page.theme_mode="light"
    page.bgcolor = ft.Colors.BLACK if page.theme_mode == ft.ThemeMode.DARK else ft.Colors.WHITE
    page.on_route_change = route_change
    page.go("/login")  # Ruta inicial
    
#,view=ft.WEB_BROWSER
ft.app(target=main,view=ft.WEB_BROWSER)