import flet as ft

def main(page: ft.Page):
    page.title = "Iconos de Flet"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Sección de Vista de Cards
    vista_cards = [
        ft.Icon(ft.icons.VIEW_LIST),
        ft.Icon(ft.icons.LOCAL_PARKING),
        ft.Icon(ft.icons.LOCATION_ON),
        ft.Icon(ft.icons.ART_TRACK),
        ft.Icon(ft.icons.BUSINESS),
        ft.Icon(ft.icons.CARD_TRAVEL_SHARP)
    ]

    # Sección de Vista Visual
    vista_visual = [
        ft.Icon(ft.icons.MAP),
        ft.Icon(ft.icons.VISIBILITY),
        ft.Icon(ft.icons.SURROUND_SOUND),
        ft.Icon(ft.icons.VIDEO_LIBRARY),
        ft.Icon(ft.icons.TOYS),
        ft.Icon(ft.icons.PANORAMA),
        ft.Icon(ft.icons.SATELLITE)
    ]

    # Sección de Navegación entre vistas
    navegacion = [
        ft.Icon(ft.icons.ARROW_FORWARD),
        ft.Icon(ft.icons.ARROW_BACK),
        ft.Icon(ft.icons.TOGGLE_ON),
        ft.Icon(ft.icons.SWITCH_CAMERA),
        ft.Icon(ft.icons.SWIPE)
    ]

    # Mostrar los iconos en la página
    page.add(
        ft.Column(
            [
                ft.Text("Vista de Cards", size=20),
                ft.Row(vista_cards),
                ft.Text("Vista Visual", size=20),
                ft.Row(vista_visual),
                ft.Text("Navegación entre vistas", size=20),
                ft.Row(navegacion)
            ],
            spacing=10
        )
    )

ft.app(target=main)
