import flet as ft
from images import *

class NavBar(ft.AppBar):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.bgcolor = ft.colors.LIGHT_BLUE
        self.leading = self.build_logo()
        self.title = self.build_title()
        self.actions = self._build_dynamic_actions()
        self.dlg = self.confirm_dialog()
        self.page.overlay.append(self.dlg)
        self.page.on_resized = self.on_resized
        self.adaptive = True

    
    def build_logo(self):
        return ft.Container(
            on_click=lambda _: self.page.go("/parking"),
            margin=ft.margin.only(left=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="../images/logougr4.png",
                        ),
                        padding=5
                    )
                ]
            )
        )
    
    def build_title(self):
        if self.page.window.width < 600:
            text=ft.Text(
                "UGR",
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=20
            )
        else:
            text=ft.Text(
                "Parking Etsiit UGR",
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=20
            )
        
        return ft.TextButton(
            on_click=lambda _: self.page.go("/home"),
            content = text    
        )
    
    def _build_dynamic_actions(self):
        actions = []
        
        user = self.page.session.get("user") or {}
        admin_check = user.get("is_admin", False)
        
        if self.page.window.width < 600:
            actions.append(self.mobile_menu(admin_check))
        else:
            actions.extend(self.desktop_menu(admin_check))
            
        actions.append(self.user_status())
        return actions
    
    
    def desktop_menu(self, admin_check):
        actions = []
        settings_items = [
           ft.PopupMenuItem(
                on_click=lambda _: self.toggle_theme(),
                content=ft.Row([
                    ft.Icon(ft.icons.BRIGHTNESS_6, color=ft.colors.GREY),
                    ft.Text("Cambiar tema", color=ft.colors.GREY)
                ])                
            )
        ]
        
        if admin_check:
            settings_items.append(
                ft.PopupMenuItem(
                    on_click=lambda _: self.page.go("/info"),
                    content=ft.Row([
                        ft.Icon(ft.icons.INFO, color=ft.colors.GREY),
                        ft.Text("Parking Fijo", color=ft.colors.GREY)
                    ])
                )
            )
            actions.extend([
                self.nav_button("Panel", ft.icons.HOME, "/home"),
                self.nav_button("Registros", ft.icons.STORAGE, "/data"),
                self.nav_button("Actividad", ft.icons.HISTORY, "/logs"),
            ])
        
        actions.extend([
            ft.PopupMenuButton(
                icon=ft.icons.SETTINGS,
                icon_size=26,
                icon_color=ft.colors.WHITE,
                tooltip="Configuración",
                items=settings_items
            ),
            ft.IconButton(
                on_click=lambda _: self.show_dialog(),
                icon=ft.icons.LOGOUT,
                icon_size=26,
                icon_color=ft.colors.WHITE,
                tooltip="Cerrar sesión"
            )
        ])
        
        return actions
    
    def mobile_menu(self, admin_check):
        base_items = []
        
        if admin_check:
            base_items.extend([
                self.menu_item("Panel", ft.icons.DASHBOARD, "/home"),
                self.menu_item("Datos", ft.icons.CONTENT_PASTE, "/data"),
                self.menu_item("Logs", ft.icons.ASSIGNMENT, "/logs"),
                self.menu_item("Parking Fijo", ft.icons.LOCAL_PARKING, "/info")
            ])
        
        base_items.extend([
            ft.PopupMenuItem(
                on_click=lambda _: self.toggle_theme(),
                content=ft.Row([
                    ft.Icon(ft.icons.BRIGHTNESS_6, color=ft.colors.GREY),
                    ft.Text("Cambiar tema", color=ft.colors.GREY)
                ])                
            ),
            ft.PopupMenuItem(
                on_click=lambda _: self.show_dialog(),
                content=ft.Row([
                    ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.RED_700),
                    ft.Text("Salir", color=ft.colors.RED_700)
                ])
            )
        ])
        
        return ft.PopupMenuButton(
            icon=ft.Icon(ft.icons.MENU, color="white"),
            items=base_items
        )
    
    def toggle_theme(self):
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        self.page.update()


    def on_resized(self, e):
        self.actions = self._build_dynamic_actions()
        self.title = self.build_title()
        self.page.update()
    
    def user_status(self):
        user = self.page.session.get("user")
        name = user.get('email').split('@')[0].upper()
        
        return ft.Container(
            padding=10,
            margin=ft.margin.only(right=20),
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.PERSON, color=ft.colors.WHITE, size=20),
                    ft.Container(
                        content=ft.Text(
                            name,
                            color=ft.colors.WHITE,
                            size=14,
                        )
                    )
                ]
            )
        )
    
    def menu_item(self, text, icon, route):
        return ft.PopupMenuItem(
            on_click=lambda _: self.page.go(route),
            height=40,
            content=ft.Row([
                ft.Icon(icon, color=ft.colors.GREY),
                ft.Text(text, color=ft.colors.GREY)
            ])
        )
    
    def nav_button(self, tooltip, icon, route):
        return ft.IconButton(
            on_click=lambda _: self.page.go(route),
            icon=icon,
            icon_size=24,
            icon_color=ft.colors.WHITE,
            tooltip=tooltip,
        )
    
    def confirm_dialog(self):
        return ft.AlertDialog(
            modal=True,
            title=ft.Row([ft.Icon(ft.icons.WARNING_AMBER), ft.Text("Confirmar")]),
            content=ft.Text("¿Desea cerrar la sesión actual?", size=14),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog, 
                         style=ft.ButtonStyle(color=ft.colors.GREY_800)),
                ft.TextButton("Confirmar", on_click=self.logout,
                         style=ft.ButtonStyle(color=ft.colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
    def show_dialog(self):
        self.dlg.open = True
        self.page.update()
    
    def logout(self, e):
        self.page.session.clear()
        self.page.client_storage.clear()
        self.dlg.open = False
        self.page.update()
        self.page.go("/login")
    
    def close_dialog(self, e):
        self.dlg.open = False
        self.page.update()