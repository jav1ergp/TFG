import flet as ft
import requests

API_URL = "http://127.0.0.1:5000/api/logs"

def logs(page: ft.Page):
    registros = []
    current_page = 1  # Página actual
    items_per_page = 10  # Cantidad de registros por página

    # Función para actualizar las filas de la tabla
    def update_rows(registros):
        table.rows.clear()
        for log in registros:
            table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(log.get("action"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("description"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("plate"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("zone"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("timestamp"), color=ft.colors.WHITE)),  
                ]
            ))
        page.update()

    # Función para obtener datos desde la API con paginación
    def update_data(page_num=1):
        nonlocal registros, current_page
        current_page = page_num

        try:
            response = requests.get(f"{API_URL}?page={current_page}&limit={items_per_page}")
            if response.status_code == 200:
                registros = response.json()
                update_rows(registros)
        except requests.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    # Funciones para la paginación
    def next_page(_):
        update_data(current_page + 1)

    def prev_page(_):
        if current_page > 1:
            update_data(current_page - 1)

    # Crear la tabla
    table = ft.DataTable(
        bgcolor=ft.colors.BLUE_GREY_700,
        border=ft.border.all(2, ft.colors.BLUE_GREY_200),
        columns=[
            ft.DataColumn(ft.Text("Acción", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Descripción", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Matrícula", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Zona", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Hora", color=ft.colors.WHITE)),
        ],
        rows=[]
    )

    # Botón para actualizar los datos
    btn_refresh = ft.ElevatedButton("Actualizar", color=ft.colors.WHITE, width=120, bgcolor=ft.colors.GREEN, on_click=lambda _: update_data())

    # Botones de paginación
    btn_prev = ft.ElevatedButton("Anterior", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.BLUE, on_click=prev_page)
    btn_next = ft.ElevatedButton("Siguiente", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.BLUE, on_click=next_page)

    # Botón para volver
    btn_back = ft.ElevatedButton("Volver", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.LIGHT_BLUE, on_click=lambda _: page.go("/home"))

    # Layout principal
    logs_layout = ft.Column(
        [
            ft.Text("Logs", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            table,
            ft.Row([btn_prev, btn_refresh, btn_next], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            btn_back
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Cargar datos al iniciar la vista
    update_data()

    return ft.View(
        "/logs",
        [logs_layout],
        bgcolor=ft.colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
