import flet as ft
from aiohttp import ClientSession
import asyncio
from models.navbar import NavBar
from config import TOTAL_ENTRY_SPOTS_CAR, TOTAL_EXIT_SPOTS_CAR, TOTAL_ENTRY_SPOTS_MOTO, TOTAL_EXIT_SPOTS_MOTO, API_URL_SPOTS


class ParkingZone(ft.UserControl):
    def __init__(self, name, total_slots_car, total_slots_moto):
        super().__init__()
        self.name = name
        self.total_slots_car = total_slots_car
        self.available_slots_car = total_slots_car
        self.total_slots_moto = total_slots_moto
        self.avaible_slots_moto = total_slots_moto
        self.status_car = ft.Text(f"{self.available_slots_car}/{self.total_slots_car}", size=24, weight=ft.FontWeight.BOLD) # 13/13
        self.progress_car = ft.ProgressBar(expand = True, color="green", bgcolor="white") # Barra de progreso
        self.status_moto = ft.Text(f"{self.avaible_slots_moto}/{self.total_slots_moto}", size=24, weight=ft.FontWeight.BOLD) # 13/13
        self.progress_moto = ft.ProgressBar(expand = True, color="green", bgcolor="white") 
        
    def build(self):
        self.title = ft.Text(self.name, size=20, weight=ft.FontWeight.BOLD)
        P_icon = ft.Icon(ft.icons.LOCAL_PARKING, size=30)
        Car_icon = ft.Icon(ft.icons.DIRECTIONS_CAR, size=30)
        Moto_icon = ft.Icon(ft.icons.TWO_WHEELER, size=30)
        
        return ft.Card(
            expand=True,
            content=ft.Container(
                content=ft.Column([
                    ft.Row([P_icon, self.title]),
                    ft.Row([Car_icon, self.status_car]),
                    self.progress_car,
                    ft.Row([Moto_icon, self.status_moto]),
                    self.progress_moto
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                margin=10,
            )
        )

    def update_status(self, available_car, available_moto): # Actualiza el estado de la zona
        self.available_slots_car = available_car 
        self.status_car.value = f"{self.available_slots_car}/{self.total_slots_car}" 
        self.progress_car.value = self.available_slots_car / self.total_slots_car 
        
        self.avaible_slots_moto = available_moto
        self.status_moto.value = f"{self.avaible_slots_moto}/{self.total_slots_moto}"
        self.progress_moto.value = self.avaible_slots_moto / self.total_slots_moto
        
        self.update()

class ParkingView(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.zone_a = ParkingZone("Zona Entrada", TOTAL_ENTRY_SPOTS_CAR, TOTAL_ENTRY_SPOTS_MOTO)
        self.zone_b = ParkingZone("Zona Salida", TOTAL_EXIT_SPOTS_CAR, TOTAL_EXIT_SPOTS_MOTO)
        self.task = None  # Tarea de actualización
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Container(
                    ft.Text("Parking Status", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ),
                
                ft.Container(
                    margin=60,
                    content=ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                self.zone_a,
                                col={"xs": 10, "sm": 5},
                                padding=10
                            ),
                            ft.Container(
                                self.zone_b,
                                col={"xs": 10, "sm": 5},
                                padding=10
                            )
                        ]
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


    async def update_parking_status(self):
        while True:
            try:
                async with ClientSession() as session:
                    async with session.get(API_URL_SPOTS) as response:
                        if response.status == 200:
                            data = await response.json()
                            self.zone_a.update_status(data.get("entrada_coche"), data.get("entrada_moto"))
                            self.zone_b.update_status(data.get("salida_coche"), data.get("salida_moto"))
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
    page.appbar = NavBar(page)
    
    return ft.View(
        "/home",
        controls=[parking_view],
        appbar=page.appbar,
        bgcolor=ft.Colors.WHITE,
        scroll=ft.ScrollMode.AUTO
    )
