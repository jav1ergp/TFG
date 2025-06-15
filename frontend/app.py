import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import flet as ft
from frontend.views_handler import get_page
from frontend.components import *

def main(page: ft.Page):
    """Funcion principal que inicializa la aplicacion Flet"""
    
    def route_change(route):
        """Evento que se ejecuta al cambiar de ruta en la aplicacion"""
        page.views.clear()
        
        view = get_page(page)
        
        if view:
            page.views.append(view)
        else:
            page.session.clear()
            page.go("/login")  # ruta desconocida
        page.update()
    
    page.theme_mode="light"
    page.on_route_change = route_change
    page.go("/login")  # Ruta inicial
    
#,view=ft.WEB_BROWSER
ft.app(target=main)