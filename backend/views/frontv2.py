import flet as ft
from aiohttp import ClientSession
import asyncio

API_URL = "http://127.0.0.1:5000/api/spots"

class ParkingZone(ft.UserControl):
    def __init__(self, name, total_slots):
        super().__init__()
        self.name = name
        self.total_slots = total_slots
        self.available_slots = total_slots
        self.status = ft.Text(f"{self.available_slots}/{self.total_slots}", size=24, weight=ft.FontWeight.BOLD) # 13/13
        self.progress = ft.ProgressBar(width=200, color="green", bgcolor="#eeeeee") # Barra de progreso

    def build(self):
        self.title = ft.Text(self.name, size=20, weight=ft.FontWeight.BOLD)
        P_icon = ft.Icon(ft.icons.LOCAL_PARKING, size=30)
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([P_icon, self.title]),
                    self.status,
                    self.progress
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=250,
                padding=20,
            )
        )

    def update_status(self, available): # Actualiza el estado de la zona
        self.available_slots = available 
        self.status.value = f"{self.available_slots}/{self.total_slots}" 
        self.progress.value = self.available_slots / self.total_slots 
        self.update()

class ParkingView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.zone_a = ParkingZone("Entrada", 13)
        self.zone_b = ParkingZone("Salida", 150)
        self.task = None  # Tarea de actualización
    
    def build(self):
        btn_back = ft.ElevatedButton(
            "Volver",
            color=ft.colors.WHITE,
            width=100,
            bgcolor=ft.colors.LIGHT_BLUE,
            on_click=lambda _: self.page.go("/home")
        )
        
        return ft.Column(
            controls=[
                ft.Text("Parking Status", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ft.Row([self.zone_a, self.zone_b], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
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
                            self.zone_a.update_status(data.get("entrada"))
                            self.zone_b.update_status(data.get("salida"))
            except Exception as e:
                print("Error al obtener datos de la API:", e)
            await asyncio.sleep(5) 

    def did_mount(self): # Se ejecuta al cargar la página
        self.task = self.page.run_task(self.update_parking_status) # Inicia la tarea de actualización

    def will_unmount(self): # Se ejecuta al salir de la página
        self.task.cancel()  # Cancela la tarea al salir
        self.task = None  # Limpia la referencia
        

def parking_page(page: ft.Page):
    parking_view = ParkingView()
    page.add(parking_view)
    
    return ft.View(
        "/parking2",
        controls=[parking_view],
        bgcolor=ft.Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )
