import flet as ft
import requests
from collections import defaultdict, Counter
from datetime import datetime
from backend.app.config import API_URL_DATA
from models.navbar import NavBar


def ChartsView(page: ft.Page):
    # Obtener datos de la API
    try:
        response = requests.get(API_URL_DATA, params={"limit": 1000})
        response.raise_for_status()
        registros = response.json().get("data", [])
    except Exception as e:
        return ft.View("/charts", [ft.Text(f"Error al obtener datos: {e}")])

    # Preparar estructuras de datos
    entradas_por_dia = defaultdict(int)
    duraciones_por_dia = defaultdict(list)
    ocupacion_zonas = Counter()
    tipos_vehiculos = Counter()

    for r in registros:
        try:
            fecha_in = datetime.fromisoformat(r["date_in"])
            dia = fecha_in.strftime("%Y-%m-%d")
            entradas_por_dia[dia] += 1

            if r.get("date_out"):
                fecha_out = datetime.fromisoformat(r["date_out"])
                duracion = (fecha_out - fecha_in).total_seconds() / 3600
                duraciones_por_dia[dia].append(duracion)

            zona = r.get("zona")
            if zona:
                ocupacion_zonas[zona] += 1

            tipo = r.get("vehicle", "Desconocido")
            tipos_vehiculos[tipo] += 1
        except Exception:
            continue

    # Duración media por día
    duracion_media_por_dia = {
        dia: (sum(vals) / len(vals) if vals else 0)
        for dia, vals in duraciones_por_dia.items()
    }

    # Función para crear un recuadro con gráfico de barras (Flet v0.27 API)
    def crear_bar_chart(datos, titulo, color):
        labels = list(datos.keys())
        values = list(datos.values())

        # Grupos de barras
        bar_groups = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=v,
                        width=20,
                        color=color,
                        tooltip=str(v)
                    )
                ]
            )
            for i, v in enumerate(values)
        ]

        # Etiquetas del eje X
        axis_labels = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Text(lbl, size=10, overflow=ft.TextOverflow.ELLIPSIS)
            )
            for i, lbl in enumerate(labels)
        ]

        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.GREY_400),
            bottom_axis=ft.ChartAxis(labels=axis_labels, labels_size=12),
            left_axis=ft.ChartAxis(title=ft.Text("Cantidad", size=12)),
            groups_space=20,
            max_y=50,
            interactive=True,
            expand=True,
            height=400,
            width=500
        )

        return ft.Container(
            content=ft.Column([
                ft.Text(titulo, size=16, weight=ft.FontWeight.BOLD),
                chart
            ], spacing=8),
            padding=10,
            margin=10,
            bgcolor=ft.Colors.WHITE,
            border_radius=10
        )

    # Crear cada gráfico
    chart1 = crear_bar_chart(entradas_por_dia, "Entradas por Día", ft.Colors.BLUE)
    chart2 = crear_bar_chart(ocupacion_zonas, "Ocupación por Zona", ft.Colors.GREEN)
    chart3 = crear_bar_chart(duracion_media_por_dia, "Duración Media (h)", ft.Colors.AMBER)
    chart4 = crear_bar_chart(tipos_vehiculos, "Tipos de Vehículos", ft.Colors.PURPLE)

    # Layout en cuadrícula 2x2
    grid = ft.Column([
        ft.Row([chart1, chart2], alignment=ft.MainAxisAlignment.CENTER, expand=True),
        ft.Row([chart3, chart4], alignment=ft.MainAxisAlignment.CENTER, expand=True)
    ], scroll=ft.ScrollMode.AUTO, spacing=20, expand=True)

    page.appbar = NavBar(page)
    
    return ft.View(
        route="/charts",
        controls=[
            ft.Column([
                ft.Text("Estadísticas del Parking", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                grid
            ], alignment=ft.MainAxisAlignment.CENTER,
               horizontal_alignment=ft.CrossAxisAlignment.CENTER,)
        ],
        appbar=page.appbar,
        bgcolor=ft.Colors.BLUE_GREY_50,
    )