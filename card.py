import flet as ft

def main(page: ft.Page):
    page.title = "Iconos de Cámara en Flet"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    iconos_camara = [
        ("CAMERA", ft.icons.CAMERA),
        ("CAMERA_ALT", ft.icons.CAMERA_ALT),
        ("CAMERA_REAR", ft.icons.CAMERA_REAR),
        ("CAMERA_FRONT", ft.icons.CAMERA_FRONT),
        ("CAMERA_INDOOR", ft.icons.CAMERA_INDOOR),
        ("CAMERA_OUTDOOR", ft.icons.CAMERA_OUTDOOR),
        ("SWITCH_CAMERA", ft.icons.SWITCH_CAMERA),
        ("VIDEOCAM", ft.icons.VIDEOCAM),
        ("VIDEO_CALL", ft.icons.VIDEO_CALL),
        ("VIDEO_CAMERA_BACK", ft.icons.VIDEO_CAMERA_BACK),
        ("VIDEO_CAMERA_FRONT", ft.icons.VIDEO_CAMERA_FRONT),
        ("VIDEO_COLLECTION", ft.icons.VIDEO_COLLECTION),
        ("VIDEO_SURVEILLANCE", ft.icons.VIDEO_LIBRARY),
    ]

    column = ft.Column(
        controls=[
            ft.Row([
                ft.Text("Nombre del icono", weight=ft.FontWeight.BOLD, width=200),
                ft.Text("Vista previa", weight=ft.FontWeight.BOLD)
            ])
        ]
    )

    for nombre, icono in iconos_camara:
        fila = ft.Row([
            ft.Text(nombre, width=200),
            ft.Icon(icono, size=40, color=ft.colors.BLUE)
        ])
        column.controls.append(fila)

    page.add(column)

ft.app(target=main)
