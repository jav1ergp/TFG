import flet as ft
import requests
from collections import defaultdict, Counter
from datetime import datetime
from config.front_config import API_URL_DATA
from frontend.components.navbar import NavBar
from frontend.components.graphics import *

def obtener_datos():
    try:
        response = requests.get(API_URL_DATA, params={"limit": 1000})
        response.raise_for_status()
        registros = response.json().get("data", [])
    except Exception as e:
        return [], f"Error al obtener datos: {e}"

    # Preparar estructuras de datos
    entradas_dia = defaultdict(int)
    ocupacion_zonas = Counter()
    tipos_vehiculos = Counter()

    # Procesar cada registro
    for r in registros:
        try:
            fecha_in = datetime.fromisoformat(r["date_in"])
            dia = fecha_in.strftime("%m/%d")
            entradas_dia[dia] += 1
            
            # Calcular ocupación por zona
            zona = r.get("zona")
            if zona and zona != "fuera":
                ocupacion_zonas[zona] += 1

            # Calcular tipos de vehículos
            tipo = r.get("vehicle")
            tipos_vehiculos[tipo] += 1
        except Exception:
            continue

    return entradas_dia, ocupacion_zonas, tipos_vehiculos

def graphics_page(page: ft.Page):
    page.appbar = NavBar(page)
    
    entradas_dia, ocupacion_zonas, tipos_vehiculos = obtener_datos()
    
    layout = ft.Column([
        ft.Row([Graf1(tipos_vehiculos), Graf2(ocupacion_zonas)], expand=True),
        ft.Row([Graf3(entradas_dia)], expand=True)
    ], spacing=20, expand=True)

    return ft.View(
        route="/graphics",
        controls=[
            ft.Column(
                [ft.Text("Estadísticas del Parking", size=30, weight=ft.FontWeight.BOLD), layout], 
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        ],
        appbar=page.appbar
    )