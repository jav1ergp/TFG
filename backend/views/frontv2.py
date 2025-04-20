import flet as ft
from aiohttp import ClientSession
import asyncio
from models.navbar import NavBar
from config import TOTAL_ENTRY_SPOTS_CAR, TOTAL_EXIT_SPOTS_CAR, TOTAL_ENTRY_SPOTS_MOTO, TOTAL_EXIT_SPOTS_MOTO, API_URL_SPOTS


class ParkingZone:
    def __init__(self, name, total_car, total_moto):
        self.name = name
        self.total_slots_car = total_car
        self.total_slots_moto = total_moto

        # Crear controles directamente
        self.status_car = ft.Text(f"{total_car}/{total_car}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self.progress_car = ft.ProgressBar(expand=True, color="green", bgcolor="white")
        self.status_moto = ft.Text(f"{total_moto}/{total_moto}", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        self.progress_moto = ft.ProgressBar(expand=True, color="green", bgcolor="white")
        
        self.control = self._build_card()

    def _build_card(self):
        title = ft.Text(self.name, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        P_icon = ft.Icon(ft.icons.LOCAL_PARKING, size=30)
        Car_icon = ft.Icon(ft.icons.DIRECTIONS_CAR, size=30)
        Moto_icon = ft.Icon(ft.icons.TWO_WHEELER, size=30)
        
        return ft.Card(
            expand=True,
            color="#1E1E1E",
            content=ft.Container(
                content=ft.Column([
                    ft.Row([P_icon, title]),
                    ft.Row([Car_icon, self.status_car]),
                    self.progress_car,
                    ft.Row([Moto_icon, self.status_moto]),
                    self.progress_moto
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                margin=10,
            )
        )

    def update_status(self, available_car, available_moto):
        self.status_car.value = f"{available_car}/{self.total_slots_car}"
        self.progress_car.value = available_car / self.total_slots_car
        self.status_moto.value = f"{available_moto}/{self.total_slots_moto}"
        self.progress_moto.value = available_moto / self.total_slots_moto
        self.control.update()

class ParkingView:
    def __init__(self):
        self.zone_a = ParkingZone("Zona Entrada", TOTAL_ENTRY_SPOTS_CAR, TOTAL_ENTRY_SPOTS_MOTO)
        self.zone_b = ParkingZone("Zona Salida", TOTAL_EXIT_SPOTS_CAR, TOTAL_EXIT_SPOTS_MOTO)
        self.task = None
        self.control = self._build_view()

    def _build_view(self):
        return ft.Column(
            controls=[
                ft.Container(
                    ft.Text("PLAZAS LIBRES", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                ),
                ft.Container(
                    margin=60,
                    content=ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                self.zone_a.control,
                                col={"xs": 12, "sm": 5}
                            ),
                            ft.Container(
                                self.zone_b.control,
                                col={"xs": 12, "sm": 5}
                            )
                        ]
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def update_parking_status(self, page):
        while True:
            if page.route != "/home":
                break
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



def parking_page(page: ft.Page):
    parking_view = ParkingView()
    page.add(parking_view)
    page.appbar = NavBar(page)
    
    switch_button = ft.IconButton(
        icon=ft.icons.VISIBILITY,
        tooltip="Vista visual",
        on_click=lambda e: page.go("/info")
    )
    
    # Iniciar la actualización periódica
    page.run_task(parking_view.update_parking_status, page)
    
    return ft.View(
        "/home",
        controls=[
            parking_view.control,
            switch_button
        ],
        appbar=page.appbar,
        bgcolor=ft.colors.WHITE,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )