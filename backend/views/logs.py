import flet as ft
import requests
from models.navbar import NavBar
from config import API_URL_LOGS

def logs(page: ft.Page):
    current_page = 1
    total_pages = 1
    
    if page.window.width < 600:
        limit = 7
    else:
        limit = 10
    
    # Función para actualizar las filas de la tabla
    def update_rows(registros):
        table.rows.clear()
        for log in registros:
            table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(log.get("action"), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("description"), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("plate"), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("zone"), color=ft.Colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("timestamp"), color=ft.Colors.WHITE)),  
                ]
            ))
        page.update()

    # Función para obtener datos desde la API con paginación
    def update_data(page_num=1):
        nonlocal current_page, total_pages
        params = {
            "page": current_page,
            "limit": limit,
        }

        try:
            response = requests.get(API_URL_LOGS, params=params)
            if response.status_code == 200:
                data = response.json()
                registros = data["data"]
                total = data["total"]
                total_pages = (total // limit) + (1 if total % limit > 0 else 0)
                update_rows(registros)
                page_counter.value = f"Página {current_page} de {total_pages}"
                page.update()
        except requests.RequestException as e:
            print(f"Error: {e}")

    # Funciones para la paginación
    def next_page(e):
        nonlocal current_page
        if current_page < total_pages:
            current_page += 1
            update_data()

    def prev_page(e):
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_data()

    # Crear la tabla
    table = ft.DataTable(
        bgcolor=ft.Colors.BLUE_GREY_700,
        border=ft.border.all(2, ft.Colors.BLUE_GREY_200),
        columns=[
            ft.DataColumn(ft.Text("Acción", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Descripción", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Matrícula", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Zona", color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Hora", color=ft.Colors.WHITE)),
        ],
        rows=[]
    )

    # Botón para actualizar los datos
    btn_refresh = ft.ElevatedButton("Actualizar", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.GREEN, on_click=lambda _: update_data())

    # Botones de paginación
    btn_prev = ft.ElevatedButton("Anterior", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.BLUE, on_click=prev_page)
    btn_next = ft.ElevatedButton("Siguiente", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.BLUE, on_click=next_page)

    page_counter = ft.Text(f"Página {current_page} de {total_pages}", color=ft.Colors.BLACK)
    
    # Layout principal
    logs_layout = ft.Column(
        [
            ft.Text("Logs", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
            ft.Row(
                [table],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            ft.Row([btn_prev, btn_refresh, btn_next], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            page_counter
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.appbar = NavBar(page)
    # Cargar datos al iniciar la vista
    update_data()

    return ft.View(
        "/logs",
        [logs_layout],
        appbar=page.appbar,
        bgcolor=ft.Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )
