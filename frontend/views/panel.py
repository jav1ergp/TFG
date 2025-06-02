import flet as ft
import requests
from frontend.components.navbar import NavBar
from backend.models.plate import Plate
from backend.models.log import Log
from datetime import datetime
from config.config import API_URL_DATA, API_URL_REGISTER, API_URL_DELETE

def panel(page: ft.Page):
    page.appbar = NavBar(page)
    
    current_page = 1
    total_pages = 1
    search_term = ""

    if page.window.width < 600:
        limit = 5
    else:
        limit = 7

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.icons.WARNING_AMBER), ft.Text("Confirmar eliminación")]),
        content=ft.Text(),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: close_dialog(e),
                    style=ft.ButtonStyle(color=ft.colors.GREY_800)),
            ft.TextButton("Confirmar", on_click=lambda e: None,
                    style=ft.ButtonStyle(color=ft.colors.RED)),
        ],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )
    
    page.overlay.append(dlg)
    
    plate_input = ft.TextField(
        label="Matrícula",
        hint_text="Formato: 1234ABC",
        width=200,
        border_color=ft.colors.BLUE_GREY_400,
        focused_border_color=ft.colors.BLUE,
        prefix_icon=ft.icons.CREDIT_CARD
    )
    
    zonas = ft.Dropdown(
        label="Zona",
        hint_text="Selecciona una zona",
        options=[ft.dropdown.Option("Zona 1"), ft.dropdown.Option("Zona 2")],
        width=200,
        border_color=ft.colors.BLUE_GREY_400,
        focused_border_color=ft.colors.BLUE,
        prefix_icon=ft.icons.LOCATION_ON
    )
    
    tipos = ft.Dropdown(
        label="Tipo vehículo",
        hint_text="Selecciona tipo",
        options=[ft.dropdown.Option("coche"), ft.dropdown.Option("moto")],
        width=200,
        border_color=ft.colors.BLUE_GREY_400,
        focused_border_color=ft.colors.BLUE,
        prefix_icon=ft.icons.DIRECTIONS_CAR
    )

    result = ft.Text(size=14)

    search_input = ft.TextField(
        label="Buscar matrícula",
        width=250,
        prefix_icon=ft.icons.SEARCH,
        on_submit=lambda e: search_plate(),
    )
            
    btn_search = ft.IconButton(icon=ft.icons.SEARCH, on_click=lambda e: search_plate())
    btn_prev = ft.ElevatedButton("Anterior", icon=ft.icons.ARROW_BACK,  color=ft.colors.WHITE, width=100, bgcolor=ft.colors.BLUE, on_click=lambda e: prev_page(e))
    btn_next = ft.ElevatedButton("Siguiente", icon=ft.icons.ARROW_FORWARD, color=ft.colors.WHITE, width=100, bgcolor=ft.colors.BLUE, on_click=lambda e: next_page(e))
    btn_refresh = ft.ElevatedButton("Actualizar", icon=ft.icons.REFRESH, color=ft.colors.WHITE, width=120, bgcolor=ft.colors.GREEN, on_click=lambda e: update_rows(e))
    page_counter = ft.Text(f"Página {current_page} de {total_pages}")

    table = ft.DataTable(
        bgcolor=ft.colors.BLUE_GREY_700,
        expand=True,
        columns=[
            ft.DataColumn(label=ft.Text("Matrícula", color=ft.colors.WHITE)),
            ft.DataColumn(label=ft.Text("Zona", color=ft.colors.WHITE)),
            ft.DataColumn(label=ft.Text("Tipo", color=ft.colors.WHITE)),
            ft.DataColumn(label=ft.Text("Fecha entrada", color=ft.colors.WHITE)),
            ft.DataColumn(label=ft.Text("Horas sin salir", color=ft.colors.WHITE)),
            ft.DataColumn(label=ft.Text("Borrar", color=ft.colors.WHITE)),
        ],
        rows=[]
    )

    btn_empty = ft.ElevatedButton(
        "Vaciar Parking",
        icon=ft.icons.CLEAR_ALL,
        bgcolor=ft.colors.RED,
        color=ft.colors.WHITE,
        on_click=lambda e: empty_parking(e)
    )

    def search_plate():
        nonlocal current_page, search_term
        search_term = search_input.value.strip().upper()
        current_page = 1
        update_rows()

    def update_rows():
        nonlocal current_page, total_pages, search_term

        table.rows.clear()
        
        try:
            params = {
                "page": current_page,
                "limit": limit,
                "search": search_term,
                "order": 1,
                "date_out": "null",
            }
            
            response = requests.get(API_URL_DATA, params=params)
            if response.status_code == 200:
                data = response.json()
                registros = data["data"]
                total = data["total"]
                total_pages = (total // limit) + (1 if total % limit else 0)
                
                now = datetime.now()
                
                for r in registros:
                    plate = r.get("plate")
                    zona = r.get("zona")
                    tipo = r.get("vehicle")
                    date_in = r.get("date_in")
                    
                    matricula=Plate(plate, r.get("confidence"), tipo, date_in, zona)
                    
                    date_in_str = datetime.fromisoformat(r["date_in"])  
                    diff = now - date_in_str
                            
                    horas = diff.total_seconds() / 3600
                    horas_tabla = f"{horas:.2f} h"
                    
                    color_horas = ft.colors.GREEN
                    if horas > 24:
                        color_horas = ft.colors.RED
                    elif horas > 8:
                        color_horas = ft.colors.ORANGE

                    table.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(plate, color=ft.colors.WHITE)),
                        ft.DataCell(ft.Text(zona, color=ft.colors.WHITE)),
                        ft.DataCell(ft.Text(tipo, color=ft.colors.WHITE)),
                        ft.DataCell(ft.Text(date_in, color=ft.colors.WHITE)),
                        ft.DataCell(ft.Text(horas_tabla, color=color_horas)),
                        ft.DataCell(ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_color=ft.colors.RED_400,
                            on_click=lambda e, p=matricula: delete_one_plate(e, p)
                        ))
                    ]))
            page_counter.value = f"Página {current_page} de {total_pages}"
        except Exception as ex:
            result.value = f"Error al cargar datos: {ex}"
            result.color = ft.colors.RED
        
        page.update()


    def registrar_plate(e):
        if not plate_input.value or not zonas.value or not tipos.value:
            result.value = "Todos los campos son obligatorios"
            result.color = ft.colors.RED
            page.update()
            return
        
        if not Plate.is_valid_plate(plate_input.value.upper()):
            result.value = "Formato inválido"
            result.color = ft.colors.RED
            page.update()
            return
        
        datos = {"plate": plate_input.value.upper(), "zona": zonas.value, "vehicle": tipos.value}
        
        try:
            r = requests.post(API_URL_REGISTER, json=datos)
            if r.status_code == 200:
                result.value = "Registrado correctamente"
                result.color = ft.colors.GREEN
                plate_input.value = ""
                zonas.value = None
                tipos.value = None
                update_rows()
            else:
                result.value = f"Error al registrar: {r.text}"
                result.color = ft.colors.RED
                
        except Exception as ex:
            result.value = f"Fallo de conexión: {ex}"
            result.color = ft.colors.RED
        page.update()
    
    def close_dialog(e):
        dlg.open = False
        page.update()

    def next_page(e):
        nonlocal current_page
        if current_page < total_pages:
            current_page += 1
            update_rows()

    def prev_page(e):
        nonlocal current_page
        if current_page > 1:
            current_page -= 1
            update_rows()
            
    def delete_one_plate(e, matricula):
        dlg.content = ft.Text("¿Está seguro que desea eliminar esta matrícula?", size=14)
        dlg.actions[1].on_click = lambda e: delete_plate(e, matricula)
        dlg.open = True
        page.update()
    
    def delete_plate(e, matricula):
        try:
            r = requests.delete(f"{API_URL_DELETE}/{matricula.license_plate_text}")   
            if r.status_code == 200:
                result.value = f"{matricula.license_plate_text} eliminado"
                result.color = ft.colors.GREEN
                dlg.open = False
                page.update()
                
                log = Log(
                    action="Delete Matricula",
                    description=f"La matrícula {matricula.license_plate_text} se ha eliminado del parking ",
                    plate=matricula.license_plate_text,
                    zona=matricula.zona,
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
                
                update_rows()
            else:    
                result.value = f"Error: {r.text}"
                result.color = ft.colors.RED
                dlg.open = False
                page.update()
        except Exception as ex:
            result.value = f"Fallo: {ex}"
            result.color = ft.colors.RED
            dlg.open = False
            page.update()
        
    def empty_parking(e):
        dlg.content = ft.Text("¿Está seguro que desea vaciar todo el parking?", size=14)
        dlg.actions[1].on_click = lambda e: confirm_empty_parking(e)
        dlg.open = True
        page.update()
    
    def confirm_empty_parking(e):
        try:
            r = requests.delete(f"{API_URL_DELETE}/all")
            if r.status_code == 200:
                result.value = "Parking vaciado correctamente"
                result.color = ft.colors.GREEN
                page.update()
                
                log = Log(
                    action="Delete Matriculas Parking",
                    description=f"Se han eliminado todas las matriculas del parking",
                    plate="Todas",
                    zona="parking",
                    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                Log.save_log(log)
                
                update_rows()
            else:  
                result.value = f"Error al vaciar: {r.status_code}"
                result.color = ft.colors.RED
        except Exception as ex:
            result.value = f"Fallo de conexión: {ex}"
            result.color = ft.colors.RED

        dlg.open = False
        page.update()

    def on_resize(e):
        nonlocal limit
        if page.window.width < 600:
            limit = 5
        else:
            limit = 7
        navbar = page.appbar 
        navbar.title = navbar.build_title()
        navbar.actions = navbar.responsive_menu()
        update_inputs_layout()  
        update_rows()   

    page.on_resized = on_resize

    def create_inputs_layout():  
        if limit == 5:
            return ft.Column(  
                [plate_input, zonas, tipos],  
                spacing=20,  
                alignment=ft.MainAxisAlignment.CENTER,  
                horizontal_alignment=ft.CrossAxisAlignment.CENTER  
            )  
        else:
            return ft.Row(  
                [plate_input, zonas, tipos],  
                spacing=60,  
                alignment=ft.MainAxisAlignment.CENTER  
            )  
    
    inputs_container = ft.Container(content=create_inputs_layout())  
    
    def update_inputs_layout():  
        inputs_container.content = create_inputs_layout()  
        page.update()
        
    # cargar datos iniciales
    update_rows()
    
    # layout
    layout = ft.Column(
        [
            ft.Text("Añadir Matrícula", size=30, weight=ft.FontWeight.BOLD),
            inputs_container,
            ft.Row([ft.ElevatedButton("Registrar", on_click=registrar_plate)], alignment=ft.MainAxisAlignment.CENTER),
            result,
            ft.Divider(),
            ft.Text("Eliminar Matrículas", size=30, weight=ft.FontWeight.BOLD),
            ft.Row([search_input, btn_search], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([table],scroll=ft.ScrollMode.AUTO,vertical_alignment=ft.CrossAxisAlignment.START),
            ft.Row([btn_prev, btn_refresh, btn_next], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Row([page_counter], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([btn_empty], alignment=ft.MainAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    return ft.View(
        route="/panel",
        controls=[layout],
        appbar=page.appbar,
        padding=20,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.START
    )
