import flet as ft
import requests

API_URL = "http://127.0.0.1:5000/api/logs"

def data(page: ft.Page):
    # Lista para almacenar los registros
    registros = []

    # Diccionario para almacenar el estado de ordenamiento de cada columna
    sort_states = {
        "zona": "asc",
        "date_in": "asc",
        "date_out": "asc"
    }

    # Función para actualizar las filas de la tabla
    def update_rows(registros):
        table.rows.clear()
        for log in registros:
            table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(log.get("plate"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(str(log.get("confidence")), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("zona"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("date_in"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(log.get("date_out", "Pendiente"), color=ft.colors.WHITE)),
                ]
            ))
        page.update()
        
    # Función para actualizar los datos de la tabla
    def update_data():
        nonlocal registros # Variable de data() que se modifica en esta función
        table.rows.clear()

        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                registros = response.json()
                update_rows(registros)
        except requests.RequestException as e:
            print(f"Error al conectar con la API: {e}")

    # Función de ordenamiento
    def sort_data(criterio):
        nonlocal registros, sort_states
        # Alterna el estado de ordenamiento
        if sort_states[criterio] == "asc":
            sort_states[criterio] = "desc"
        else:
            sort_states[criterio] = "asc"

        # Ordena los registros según el criterio y el estado de ordenamiento
        tipo_orden = sort_states[criterio] == "asc"
        registros = sorted(registros, key=lambda log: log.get(criterio), reverse=tipo_orden)

        # Actualiza la tabla con los datos ordenados
        update_rows(registros)

    # Función de búsqueda por matrícula
    def search_by_plate(event):
        nonlocal registros
        search_term = search_field.value.strip().lower()
        
        filtered_registros = []
        
        if search_term:
            for log in registros:
                plate = log.get("plate", "").lower()
                if search_term in plate:
                    filtered_registros.append(log) 
        else:
            filtered_registros = registros

        update_rows(filtered_registros)

    # Crear la tabla
    table = ft.DataTable(
        bgcolor=ft.colors.BLUE_GREY_700,
        border=ft.border.all(2, ft.colors.BLUE_GREY_200),
        columns=[
            ft.DataColumn(ft.Text("Matrícula", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Confianza", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Zona", color=ft.colors.WHITE), on_sort=lambda e: sort_data("zona")),
            ft.DataColumn(ft.Text("Fecha Entrada", color=ft.colors.WHITE), on_sort=lambda e: sort_data("date_in")),
            ft.DataColumn(ft.Text("Fecha Salida", color=ft.colors.WHITE), on_sort=lambda e: sort_data("date_out")),
        ],
        rows=[]
    )

    # Campo de búsqueda por matrícula
    search_field = ft.TextField(
        label="Buscar por matrícula",
        color=ft.colors.BLACK,
        width=300,
        on_submit=search_by_plate
    )

    # Botón de búsqueda
    btn_search = ft.ElevatedButton(
        "Buscar",
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        on_click=search_by_plate
    )

    # Botón para actualizar los datos
    btn_refresh = ft.ElevatedButton("Actualizar", color=ft.colors.WHITE, width=120, bgcolor=ft.colors.GREEN, on_click=lambda _: update_data())

    # Botón para volver
    btn_back = ft.ElevatedButton("Volver", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.LIGHT_BLUE, on_click=lambda _: page.go("/home"))

    # Layout principal
    logs_layout = ft.Column(
        [
            ft.Text("Logs", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
            ft.Row([search_field, btn_search], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            table,
            ft.Row([btn_refresh, btn_back], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Ejecuta la función para llenar la tabla la primera vez
    update_data()

    return ft.View(
        "/data",
        [logs_layout],
        bgcolor=ft.colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )