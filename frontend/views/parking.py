import flet as ft
from aiohttp import ClientSession
import asyncio
from config.config import API_URL_SPOTS
from frontend.components.navbar import NavBar

class ParkingView2:
    def __init__(self, page: ft.Page):
        self.page = page
        self.plazas_zona_entrada_coche = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_salida_coche = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_entrada_moto = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.plazas_zona_salida_moto = ft.Text("", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

        platform = self.page.platform
        if platform == "android":
            self.scale = 1
        elif platform == "ios":
            self.scale = 1
        else:
            self.scale = 1.4
        
        self.zona_entrada = None
        self.zona_salida = None
        self.curva = None
        self.stack = None
        self.control = self.build_content()
  
    def build_content(self):
        Car_icon = ft.Icon(ft.icons.DIRECTIONS_CAR, size=25, color=ft.colors.WHITE)
        Moto_icon = ft.Icon(ft.icons.TWO_WHEELER, size=25, color=ft.colors.WHITE)
        Entrada = ft.Text("Entrada", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        Salida = ft.Text("Salida", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

        # Contenedores principales
        self.zona_entrada = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([Entrada], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([Car_icon, self.plazas_zona_entrada_coche], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([Moto_icon, self.plazas_zona_entrada_moto], alignment=ft.MainAxisAlignment.CENTER),
                ],alignment=ft.MainAxisAlignment.SPACE_AROUND, horizontal_alignment=ft.CrossAxisAlignment.START),
                width=130 * self.scale,
                height=250 * self.scale,
                padding=20,
                bgcolor=ft.colors.BLUE,
                border_radius=ft.border_radius.only(bottom_right=10, bottom_left=10),
            ),
            margin=ft.margin.only(top=130 * self.scale)
        )
        
        self.curva = ft.Container(
            content=ft.Container(
                width=130 * self.scale,
                height=130 * self.scale,
                bgcolor=ft.colors.TEAL_500,
                border_radius=ft.border_radius.only(top_left=100)
            ),
            margin=ft.margin.only(left=0, top=0)
        )
        
        self.zona_salida = ft.Container(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([Salida], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([Car_icon, self.plazas_zona_salida_coche, Moto_icon, self.plazas_zona_salida_moto], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                width=250 * self.scale,
                height=130 * self.scale,
                padding=20,
                bgcolor=ft.colors.GREEN,
                border_radius=ft.border_radius.only(bottom_right=10, top_right=10),),
            margin=ft.margin.only(left=130 * self.scale, top=0)
        )
          
        self.stack = ft.Stack(
            [self.zona_entrada, self.curva, self.zona_salida],
            width=350 * self.scale,
            height=350 * self.scale,
        )

        return ft.Column(
            controls=[
                ft.Container(ft.Text("PLAZAS LIBRES", size=30, weight=ft.FontWeight.BOLD)),
                self.stack
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
      
    def update_scale(self, new_scale):
        """Update the scale of all components"""
        if new_scale == self.scale:
            return False
        
        self.scale = new_scale
          
        self.zona_entrada.width = 130 * self.scale
        self.zona_entrada.height = 220 * self.scale
           
        self.zona_salida.width = 250 * self.scale
        self.zona_salida.height = 130 * self.scale
        
        self.curva.width = 130 * self.scale
        self.curva.height = 130 * self.scale

        self.stack.width = 350 * self.scale
        self.stack.height = 350 * self.scale
          
        # Update container margins
        self.stack.controls[0].margin = ft.margin.only(top=130 * self.scale)
        self.stack.controls[2].margin = ft.margin.only(left=130 * self.scale, top=0)
        
        # Update the control  
        self.control.update()
        return True
    
    async def update_parking_status(self):
        while True:
            if self.page.route != "/parking":
                break
            try:
                async with ClientSession() as session:
                    async with session.get(API_URL_SPOTS) as response:
                        if response.status == 200:
                            data = await response.json()
                            # Actualizar valores
                            self.plazas_zona_entrada_coche.value = data.get("entrada_coche", "Error")
                            self.plazas_zona_salida_coche.value = data.get("salida_coche", "Error")
                            self.plazas_zona_entrada_moto.value = data.get("entrada_moto", "Error")
                            self.plazas_zona_salida_moto.value = data.get("salida_moto", "Error")
                            self.control.update()
            except Exception as e:
                print("Error al obtener datos de la API:", e)
            
            await asyncio.sleep(5)
  
def parking(page: ft.Page):
    parking_view = ParkingView2(page)
    page.appbar = NavBar(page)
  
    switch_button = ft.IconButton(
        icon=ft.icons.LOCAL_PARKING,
        icon_color="#84c3e3",
        tooltip="Vista de tarjetas",
        on_click=lambda e: page.go("/home"))
    
    def on_resize(e):
        if page.window.width < 600:
            new_scale = 1
        else:
            new_scale = 1.4

        # Update navbar
        navbar = page.appbar
        navbar.title = navbar.build_title()
        navbar.actions = navbar.responsive_menu()
          
        # Update parking view scale
        parking_view.update_scale(new_scale)
          
        page.update()
  
    page.on_resized = on_resize
    page.run_task(parking_view.update_parking_status)
    
    return ft.View(
        "/parking",
        controls=[parking_view.control, switch_button],
        appbar=page.appbar,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO)