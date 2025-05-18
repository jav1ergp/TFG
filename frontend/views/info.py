import flet as ft
from aiohttp import ClientSession
import asyncio
from config.front_config import API_URL_SPOTS
from datetime import datetime

class InfoView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.title = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.zona1 = ft.Text("Zona 1  ", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.zona2 = ft.Text("Zona 2  ", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.z1_car = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT)
        self.z1_moto = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT)
        self.z2_car = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT)
        self.z2_moto = ft.Text("", weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_ACCENT)
        self.date_time = ft.Text("", weight=ft.FontWeight.NORMAL, color=ft.colors.WHITE)
        self.control = self.build_view()


    def build_view(self):
    # Si la pantalla es más ancha que alta
        if self.page.height < self.page.width:
            cont = ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.title,
                    ft.Row(
                        controls=[self.zona1, self.z1_car, ft.Container(width=30), self.z1_moto],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[self.zona2, self.z2_car, ft.Container(width=30), self.z2_moto],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    self.date_time
                ]
            )
        else:
            # Si la pantalla es más alta
            cont = ft.Column(
                controls=[
                    self.title,
                    ft.Column(
                        controls=[
                            self.zona1,
                            self.z1_car,
                            self.z1_moto
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        controls=[
                            self.zona2,
                            self.z2_car,
                            self.z2_moto
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    self.date_time
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        return ft.Column(
            controls=[cont],
        )


    def update_font_sizes(self, page: ft.Page):
        scale = min(page.width, page.height)
        base_size = scale // 12

        self.title.value = "PLAZAS LIBRES"
        self.title.size = base_size + 6

        self.zona1.size = base_size
        self.zona2.size = base_size
        self.z1_car.size = base_size
        self.z1_moto.size = base_size
        self.z2_car.size = base_size
        self.z2_moto.size = base_size
        self.date_time.size = base_size - 6

    def update_date_time(self):
        now = datetime.now()
        self.date_time.value = now.strftime("%d %B %Y, %H:%M")
        
    def update_field(self, field, label, value):
        if value == 0:
            field.value = f"{label} COMPLETO"
            field.color = ft.colors.RED
        else:
            field.value = f"{label} {value}"
            field.color = ft.colors.GREEN_ACCENT

    async def update_status(self, page: ft.Page):
        while page.route == "/info":
            try:
                async with ClientSession() as session:
                    async with session.get(API_URL_SPOTS) as response:
                        if response.status == 200:
                            data = await response.json()

                            self.update_field(self.z1_car, "coches:", data.get('entrada_coche', 0))
                            self.update_field(self.z1_moto, "motos:", data.get('entrada_moto', 0))
                            self.update_field(self.z2_car, "coches:", data.get('salida_coche', 0))
                            self.update_field(self.z2_moto, "motos:", data.get('salida_moto', 0))

                            self.update_date_time()
                            self.page.update()
            except Exception as e:
                print("Error al obtener datos de la API:", e)
            await asyncio.sleep(5)

def info_page(page: ft.Page):
    info_view = InfoView(page)
    page.bgcolor = ft.colors.BLACK87
    

    async def on_view_loaded():
        info_view.update_font_sizes(page)
    page.run_task(on_view_loaded)
    
    page.on_resized = lambda e: (info_view.update_font_sizes(page), info_view.control.update())  # actualiza vista
    page.run_task(info_view.update_status, page)

    
    def on_key(e: ft.KeyboardEvent):
        if e.key == "Escape":
            page.go("/home")
    page.on_keyboard_event = on_key
    page.theme_mode="dark"
    return ft.View(
        "/info",
        controls=[info_view.control],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )