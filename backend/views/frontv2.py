import flet as ft
import requests
import asyncio

API_URL = "http://127.0.0.1:5000/api/plazas"

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
            ),
            elevation=50,
        )

    def update_status(self, available: int): # Actualiza el estado de la zona
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
        window_width = self.page.width
        margin_value = int(window_width * 0.08)
        return ft.Container(
            content=ft.Column([
                ft.Row([self.zone_a, self.zone_b], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ]),
            margin=margin_value
        )

    async def update_parking_status(self):
        while True:
            try:
                response = requests.get(API_URL)
                if response.status_code == 200:
                    data = response.json()
                    self.zone_a.update_status(data.get("entrada"))
                    self.zone_b.update_status(data.get("fuera"))
            except Exception as e:
                print("Error al obtener datos de la API:", e)
            await asyncio.sleep(5)  # Actualiza cada 5 segundos

    def did_mount(self):
        self.task = self.page.run_task(self.update_parking_status) # Inicia la tarea de actualización

    def will_unmount(self): # Se ejecuta al salir de la página
        if self.task:
            self.task.cancel()  # Cancela la tarea al salir
            self.task = None  # Limpia la referencia

def parking_page(page: ft.Page):
    parking_view = ParkingView()
    page.add(parking_view)
    
    btn_back = ft.ElevatedButton("Volver", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.LIGHT_BLUE, on_click=lambda _: page.go("/home"))
    
    return ft.View(
        "/parking",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.Column([
                ft.Text("Parking Status", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                parking_view,
                btn_back
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )
