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

        
    def build_logo(self):
        """Logo"""
        return ft.Container(
            on_click=lambda _: self.page.go("/home"),
            margin=ft.margin.only(left=10),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="../images/logougr4.png",
                        ),
                        padding=5,
                    )
                ]
            )
        )
    
    def build_title(self):
        """Title"""
        return ft.TextButton(
            content=ft.Text(
                "Parking UGR",
                color=ft.colors.WHITE,
                weight=ft.FontWeight.BOLD,
                size=20             
            ),
            on_click=lambda _: self.page.go("/home")
        )
    
    def _build_dynamic_actions(self):
        """Menu desktop o movil"""
        actions = []
        
        user = self.page.session.get("user") or {}
        admin_check = user.get("is_admin", False)
        
        if self.page.window_width < 600:
            actions.append(self.mobile_menu(admin_check))
        else:
            actions.extend(self.desktop_menu(admin_check))
            
        actions.append(self.user_status())
        return actions
    
    
    def desktop_menu(self, admin_check):
        """Menú desktop"""
        actions = [
            self.nav_button("Panel", ft.icons.DASHBOARD, "/home")
        ]
        
        if admin_check:
            actions.extend([
                self.nav_button("Registros", ft.icons.CONTENT_PASTE, "/data"),
                self.nav_button("Actividad", ft.icons.ASSIGNMENT, "/logs")
            ])
        
        actions.append(
            ft.IconButton(
                icon=ft.icons.EXIT_TO_APP,
                icon_size=26,
                icon_color=ft.colors.WHITE,
                tooltip="Cerrar sesión",
                on_click=lambda _: self.show_dialog(),
            )
        )
        
        return actions
    
    def mobile_menu(self, admin_check):
        """Menú móvil"""
        base_items = [
            self.menu_item("Panel", ft.icons.DASHBOARD, "/home"),
        ]
        
        if admin_check:
            base_items.extend([
                self.menu_item("Registros", ft.icons.CONTENT_PASTE, "/data"),
                self.menu_item("Actividad", ft.icons.ASSIGNMENT, "/logs"),

            ])
        
        base_items.append(
            ft.PopupMenuItem(
                content=ft.Row([
                    ft.Icon(ft.icons.EXIT_TO_APP, color=ft.colors.RED_700),
                    ft.Text("Salir", color=ft.colors.RED_700)
                ]),
                on_click=lambda _: self.show_dialog()
            )
        )
        
        return ft.PopupMenuButton(
            icon=ft.Icon(ft.icons.MENU, color="white"),
            items=base_items
        )
    
    def user_status(self):
        """Indicador de usuario"""
        user = self.page.session.get("user")
        name = user.get('email').split('@')[0].upper()
        
        return ft.Container(
            padding=10,
            margin=ft.margin.only(right=20),
            content=ft.Row(
                controls=[
                    ft.Icon(ft.icons.PERSON_PIN, color=ft.colors.WHITE, size=20),
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
        """Elemento de menú"""
        return ft.PopupMenuItem(
            height=40,
            content=ft.Row([
                ft.Icon(icon, color=ft.colors.GREY_800),
                ft.Text(text, color=ft.colors.GREY_800)
            ]),
            on_click=lambda _: self.page.go(route)
        )
    
    def nav_button(self, tooltip, icon, route):
        """Botón de navegación"""
        return ft.IconButton(
            icon=icon,
            icon_size=24,
            icon_color=ft.colors.WHITE,
            tooltip=tooltip,
            on_click=lambda _: self.page.go(route),
        )
    
    def confirm_dialog(self):
        """Diálogo de confirmación"""
        return ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.icons.WARNING_AMBER), ft.Text("Confirmar")]),
            content=ft.Text("¿Desea cerrar la sesión actual?", size=14),
            actions=[
                ft.TextButton("Cancelar", on_click=self.close_dialog, 
                         style=ft.ButtonStyle(color=ft.colors.GREY_800)),
                ft.TextButton("Confirmar", on_click=self.logout,
                         style=ft.ButtonStyle(color=ft.colors.RED)),
            ],
            modal=True,
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
    def show_dialog(self):
        """Muestra el diálogo de confirmación"""
        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()
    
    def logout(self, e):
        """Cierra la sesión"""
        self.page.session.clear()
        self.page.client_storage.clear()
        self.page.dialog.open = False
        self.page.update()
        self.page.go("/login")
    
    def close_dialog(self, e):
        """Cierra el diálogo"""
        self.page.dialog.open = False
        self.page.update()