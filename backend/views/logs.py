import flet as ft
import requests
import threading

API_URL = "http://127.0.0.1:5000/api/logs"

def data(page: ft.Page):
    def update_data():
        table.rows.clear()

        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                registros = response.json()
                for log in registros:
                    table.rows.append(ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(log.get("plate", "N/A"), color=ft.colors.WHITE)),
                            ft.DataCell(ft.Text(str(log.get("confidence", "Desconocido")), color=ft.colors.WHITE)),
                            ft.DataCell(ft.Text(log.get("zona", "N/A"), color=ft.colors.WHITE)),
                            ft.DataCell(ft.Text(log.get("date_in", "N/A"), color=ft.colors.WHITE)),
                            ft.DataCell(ft.Text(log.get("date_out", "Pendiente"), color=ft.colors.WHITE)),
                        ]
                    ))
                page.update()
        except requests.RequestException as e:
            print(f"Error al conectar con la API: {e}")


    table = ft.DataTable(
        bgcolor=ft.colors.BLUE_GREY_700,
        border=ft.border.all(2, ft.colors.BLUE_GREY_200),
        columns=[
            ft.DataColumn(ft.Text("Matrícula", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Confianza", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Zona", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Fecha Entrada", color=ft.colors.WHITE)),
            ft.DataColumn(ft.Text("Fecha Salida", color=ft.colors.WHITE)),
        ],
        rows=[]  
    )

    # actualizar datos de la tabla
    btn_refresh = ft.ElevatedButton("Actualizar", color=ft.Colors.WHITE, width=120, bgcolor=ft.Colors.GREEN, on_click=lambda _: threading.Thread(target=update_data).start())
    #page.run_task(update_logs))

    # Botón para volver
    btn_back = ft.ElevatedButton("Volver", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.LIGHT_BLUE, on_click=lambda _: page.go("/home"))

    # Layout
    logs_layout = ft.Column(
        [
            ft.Text("Logs", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
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
        bgcolor=ft.Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
