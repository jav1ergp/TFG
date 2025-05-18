import flet as ft
import requests
from frontend.components.navbar import NavBar
from config.front_config import API_URL_DATA


def data(page: ft.Page):
    current_page = 1
    total_pages = 1
    sort_field = "date_in"
    sort_order = 1
    search_term = ""
    
    if page.window.width < 600:
        limit = 7
    else:
        limit = 10
        
    # Función para actualizar las filas de la tabla
    def update_rows(registros):
        table.rows.clear()
        for data in registros:
            table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(data.get("vehicle"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(data.get("plate"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(str(data.get("confidence")), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(data.get("zona"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(data.get("date_in"), color=ft.colors.WHITE)),
                    ft.DataCell(ft.Text(data.get("date_out", "Pendiente"), color=ft.colors.WHITE)),
                ]
            ))
        page.update()
        
    # Función para actualizar los datos de la tabla
    def update_data():
        nonlocal current_page, total_pages
        params = {
            "page": current_page,
            "limit": limit,
            "sort": sort_field,
            "order": sort_order,
            "search": search_term
        }
        
        try:
            response = requests.get(API_URL_DATA, params=params)
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
            
    # Función de ordenamiento 
    def sort_data(e):
        nonlocal sort_field, sort_order, current_page  
        sort_field = e.control.data["field"]
        sort_order = 1 if sort_order == -1 else -1  # Alternar orden
        current_page = 1
        update_data()
   
    # Función de búsqueda por matrícula
    def search_by_plate(e):
        nonlocal search_term, current_page
        search_term = search_field.value.strip().upper()
        current_page = 1
        update_data()
        

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
        bgcolor=ft.colors.BLUE_GREY_700,
        border=ft.border.all(2, ft.colors.BLUE_GREY_200),
        columns=[
            ft.DataColumn(ft.Text("Vehículo", color=ft.colors.WHITE), on_sort=lambda e: sort_data(e), data={"field": "vehicle"}),
            ft.DataColumn(ft.Text("Matrícula", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Confianza", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Zona", color=ft.colors.WHITE), on_sort=lambda e: sort_data(e), data={"field": "zona"}),
            ft.DataColumn(ft.Text("Fecha Entrada", color=ft.colors.WHITE), on_sort=lambda e: sort_data(e), data={"field": "date_in"}),
            ft.DataColumn(ft.Text("Fecha Salida", color=ft.colors.WHITE), on_sort=lambda e: sort_data(e), data={"field": "date_out"})
        ],
        rows=[]
    )

    # Campo de búsqueda por matrícula
    search_field = ft.TextField(
        label="Buscar por matrícula",
        width=250,
        on_submit=search_by_plate
    )

    # Botón de búsqueda
    btn_search = ft.ElevatedButton(
        "Buscar",
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLUE,
        width=70,
        on_click=search_by_plate
    )

    # Botón para actualizar los datos
    btn_refresh = ft.ElevatedButton("Actualizar", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.GREEN, on_click=lambda _: update_data())

    # Botones de paginación
    btn_prev = ft.ElevatedButton("Anterior", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.BLUE, on_click=prev_page)
    btn_next = ft.ElevatedButton("Siguiente", color=ft.colors.WHITE, width=100, bgcolor=ft.colors.BLUE, on_click=next_page)

    page_counter = ft.Text(f"Página {current_page} de {total_pages}")
    # Layout principal
    logs_layout = ft.Column(
        [
            ft.Text("Datos", size=24, weight=ft.FontWeight.BOLD),
            ft.Row(
                [table],
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            ft.Row([search_field, btn_search], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            ft.Row([btn_prev, btn_refresh, btn_next], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            page_counter,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.appbar = NavBar(page)
    # Datos primera vez
    update_data()

    return ft.View(
        "/data",
        [logs_layout],
        appbar=page.appbar,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )