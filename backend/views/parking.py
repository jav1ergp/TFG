import flet as ft

def parking(page: ft.Page):
    def parking_view():
        plazas_zona_entrada = ft.Text("10", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        plazas_zona_salida = ft.Text("15", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)

        # entrada
        zona_entrada = ft.Container(
            content=ft.Column([
                ft.Text("Entrada", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                plazas_zona_entrada
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=100,
            height=250,
            bgcolor=ft.colors.BLUE,
            alignment=ft.alignment.center,
            border_radius=ft.border_radius.only(bottom_right=10, bottom_left=10)
        )

        # salida
        zona_salida = ft.Container(
            content=ft.Column([
                ft.Text("Salida", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                plazas_zona_salida
            ], alignment=ft.MainAxisAlignment.CENTER),
            width=250,
            height=100,
            bgcolor=ft.colors.GREEN,
            alignment=ft.alignment.center,
            border_radius=ft.border_radius.only(bottom_right=10, top_right=10)
        )

        # curva
        curva = ft.Container(
            width=100,
            height=100,
            bgcolor=ft.colors.BLUE,
            border_radius=ft.border_radius.only(top_left=100)
        )

        # home
        btn_back = ft.ElevatedButton("Volver", color=ft.Colors.WHITE, width=100, bgcolor=ft.Colors.LIGHT_BLUE, on_click=lambda _: page.go("/home"))

        # layout
        parking_layout = ft.Column(
            [
                ft.Text("Estado del Parking", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                ft.Stack(
                    [
                        ft.Container(content=zona_entrada, margin=ft.margin.only(top=100)),
                        ft.Container(content=curva, margin=ft.margin.only(left=0, top=0)),
                        ft.Container(content=zona_salida, margin=ft.margin.only(left=100, top=0))
                        
                    ],
                    width=350,
                    height=350
                ),
                btn_back
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

        return parking_layout

    return ft.View(
        "/parking",
        [parking_view()],
        bgcolor=ft.Colors.WHITE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER
    )
