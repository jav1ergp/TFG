import flet as ft
from aiohttp import ClientSession
import asyncio
from config import API_URL_SPOTS
from models.navbar import NavBar

class ParkingView2:
    def __init__(self):
        self.plazas_zona_entrada_coche = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_salida_coche = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_entrada_moto = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_salida_moto = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.task = None  # Tarea de actualización
        
        self.control = self.build_content()

    def build_content(self):
        Car_icon = ft.Icon(ft.icons.DIRECTIONS_CAR, size=25, color=ft.colors.WHITE)
        Moto_icon = ft.Icon(ft.icons.TWO_WHEELER, size=25, color=ft.colors.WHITE)
        Entrada = ft.Text("Entrada", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        Salida = ft.Text("Salida", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        # Entrada
        zona_entrada = ft.Container(
            content=ft.Column([
                ft.Row([Entrada], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([Car_icon, self.plazas_zona_entrada_coche], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([Moto_icon, self.plazas_zona_entrada_moto],  alignment=ft.MainAxisAlignment.CENTER),
            ]),
            width=130,
            height=220,
            padding=20,
            bgcolor=ft.colors.BLUE,
            border_radius=ft.border_radius.only(bottom_right=10, bottom_left=10)
        )

        # Salida
        zona_salida = ft.Container(
            content=ft.Column([
                ft.Row([Salida], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([Car_icon, self.plazas_zona_salida_coche, Moto_icon, self.plazas_zona_salida_moto], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            width=250,
            height=130,
            padding=20,
            bgcolor=ft.colors.GREEN,
            border_radius=ft.border_radius.only(bottom_right=10, top_right=10)
        )

        # Curva
        curva = ft.Container(
            width=130,
            height=130,
            bgcolor=ft.colors.TEAL_500,
            border_radius=ft.border_radius.only(top_left=100)
        )

        # Layout principal
        return ft.Column(
            controls=[
                ft.Container(
                    ft.Text("Parking Status", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ),
                ft.Container(                        
                    margin=20,
                    content=ft.Stack(
                        [
                            ft.Container(content=zona_entrada, margin=ft.margin.only(top=130)),
                            ft.Container(content=curva, margin=ft.margin.only(left=0, top=0)),
                            ft.Container(content=zona_salida, margin=ft.margin.only(left=130, top=0))
                        ],
                        width=350,
                        height=350
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER            
        )

    async def update_parking_status(self, page):
        while True:
            if page.route != "/parking":
                break
            try:
                async with ClientSession() as session:
                    async with session.get(API_URL_SPOTS) as response:
                        if response.status == 200:
                            data = await response.json()
                            self.plazas_zona_entrada_coche.value = data.get("entrada_coche", "Error")
                            self.plazas_zona_salida_coche.value = data.get("salida_coche", "Error")
                            self.plazas_zona_entrada_moto.value = data.get("entrada_moto", "Error")
                            self.plazas_zona_salida_moto.value = data.get("salida_moto", "Error")
                            self.control.update()
            except Exception as e:
                print("Error al obtener datos de la API:", e)
            await asyncio.sleep(5)
            

def parking(page: ft.Page):
    parking_view = ParkingView2()
    page.add(parking_view)
    page.appbar = NavBar(page)
    
    # Iniciar la actualización periódica
    page.run_task(parking_view.update_parking_status, page)
    
    return ft.View(
        "/parking",
        controls=[parking_view.control],
        appbar=page.appbar,
        bgcolor=ft.colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )