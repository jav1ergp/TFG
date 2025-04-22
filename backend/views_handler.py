from views.login import login
from views.register import register
from views.frontv2 import parking_page
from views.parking import parking
from views.data import data
from views.logs import logs
from views.info import info_page
from views.graphics import graphics_page

def get_page(page, current_user_email):
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
