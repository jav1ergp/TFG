import flet as ft
from aiohttp import ClientSession
import asyncio

API_URL = "http://127.0.0.1:5000/api/spots"

class ParkingView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.plazas_zona_entrada = ft.Text("Cargando...", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_salida = ft.Text("Cargando...", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.task = None  # Tarea de actualización

    def build(self):
        # Entrada
        zona_entrada = ft.Container(
            content=ft.Column([
                ft.Text("Entrada", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                self.plazas_zona_entrada
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=100,
            height=250,
            bgcolor=ft.colors.BLUE,
            alignment=ft.alignment.center,
            border_radius=ft.border_radius.only(bottom_right=10, bottom_left=10)
        )

        # Salida
        zona_salida = ft.Container(
            content=ft.Column([
                ft.Text("Salida", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                self.plazas_zona_salida
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=250,
            height=100,
            bgcolor=ft.colors.GREEN,
            alignment=ft.alignment.center,
            border_radius=ft.border_radius.only(bottom_right=10, top_right=10)
        )

        # Curva
        curva = ft.Container(
            width=100,
            height=100,
            bgcolor=ft.colors.BLUE,
            border_radius=ft.border_radius.only(top_left=100)
        )

        # Back
        btn_back = ft.ElevatedButton(
            "Volver",
            color=ft.colors.WHITE,
            width=100,
            bgcolor=ft.colors.LIGHT_BLUE,
            on_click=lambda _: self.page.go("/home")
        )

        # Layout principal
        return ft.Column(
            [
                ft.Text("Parking Status", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.Stack(
                    [
                        ft.Container(content=zona_entrada, margin=ft.margin.only(top=100)),
                        ft.Container(content=curva, margin=ft.margin.only(left=0, top=0)),
                        ft.Container(content=zona_salida, margin=ft.margin.only(left=100, top=0))
                    ],
                    width=350,
                    height=350
                ),
                btn_back
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    async def update_parking_status(self):
        while True:
            try:
                async with ClientSession() as session:
                    async with session.get(API_URL) as response:
                        if response.status == 200:
                            data = await response.json()
                            self.plazas_zona_entrada.value = data.get("entrada", "Error")
                            self.plazas_zona_salida.value = data.get("salida", "Error")
                            self.plazas_zona_entrada.update()
                            self.plazas_zona_salida.update()
            except Exception as e:
                print("Error al obtener datos de la API:", e)
            await asyncio.sleep(5)

    def did_mount(self):
        self.task = self.page.run_task(self.update_parking_status)

    def will_unmount(self):
        self.task.cancel()
        self.task = None

def parking(page: ft.Page):
    parking_view = ParkingView()
    page.add(parking_view)
    
    return ft.View(
        "/parking",
        controls=[parking_view],
        bgcolor=ft.colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )