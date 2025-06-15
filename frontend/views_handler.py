import flet as ft
from frontend.views.login import login
from frontend.views.register import register
from frontend.views.frontv2 import parking_page
from frontend.views.parking import parking
from frontend.views.data import data
from frontend.views.logs import logs
from frontend.views.info import info_page
from frontend.views.graphics import graphics_page
from frontend.views.panel import panel

def get_page(page: ft.Page):
    """Devuelve la vista correspondiente segun la ruta y el usuario"""
    route = page.route
    user = page.session.get("user")
    if not user and route not in ("/login", "/register"):
        return None

    if user and route in ("/login", "/register"):
        page.session.clear()

    if user and route in ("/data", "/info", "/logs", "/graphics") and not user.get("is_admin"):
        return parking_page(page)
    
    match route:
        case "/login":
            return login(page)
        case "/register":
            return register(page)
        case "/home":
            return parking_page(page)
        case "/parking":
            return parking(page)
        case "/data":
            return data(page)
        case "/logs":
            return logs(page)
        case "/info":
            return info_page(page)
        case "/graphics":
            return graphics_page(page)
        case "/panel":  
            return panel(page)
        
        case _:
            return None
