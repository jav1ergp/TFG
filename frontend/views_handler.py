from frontend.views.login import login
from frontend.views.register import register
from frontend.views.frontv2 import parking_page
from frontend.views.parking import parking
from frontend.views.data import data
from frontend.views.logs import logs
from frontend.views.info import info_page
from frontend.views.graphics import graphics_page

def get_page(page):
    route = page.route
    
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
        
        case _:
            return None
