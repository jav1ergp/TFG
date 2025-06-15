import flet as ft
import asyncio

class NavBar(ft.AppBar):
    """Barra de navegacion que se adapta al tamaño de la ventana y al tipo de usuario (admin o no). 
    Incluye titulo, menus y control de sesion"""
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.adaptative = False
        self.bgcolor = ft.colors.LIGHT_BLUE
        self.title = self.build_title()
        self.actions = self.responsive_menu()
        self.dlg = self.confirm_dialog()
        self.page.overlay.append(self.dlg)
        self.page.on_resized = self.on_resized
    
    def build_title(self):
        """Genera el titulo segun el ancho de la ventana"""
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
    
    def responsive_menu(self):
        """Crea el menu de navegacion segun si es vista de movil o escritorio,
        y si el usuario es administrador"""
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
        """Menu para pantallas grandes, muestra botones si el usuario es admin"""
        actions = []
        settings_items = []
        
        if admin_check:
            settings_items.append(
                ft.PopupMenuItem(
                    on_click=lambda _: self.page.go("/info"),
                    content=ft.Row([
                        ft.Icon(ft.icons.LOCAL_PARKING, color=ft.colors.GREY),
                        ft.Text("Parking Fijo", color=ft.colors.GREY)
                    ])
                )
            )
            actions.extend([
                self.nav_button("Panel de Control", ft.icons.HOME, "/panel"),
                self.nav_button("Registros", ft.icons.ASSIGNMENT, "/data"),
                self.nav_button("Actividad", ft.icons.HISTORY, "/logs"),
                self.nav_button("Graficas", ft.icons.BAR_CHART, "/graphics"),
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
        
        settings_items.append(
            ft.PopupMenuItem(
                on_click=lambda _: self.toggle_theme(),
                content=ft.Row([
                    ft.Icon(ft.icons.BRIGHTNESS_6, color=ft.colors.GREY),
                    ft.Text("Cambiar tema", color=ft.colors.GREY)
                ])                
            )
        )
        return actions
    
    def mobile_menu(self, admin_check):
        """Menu para moviles en forma de popup, muestra botones si el usuario es admin"""
        base_items = []
        
        if admin_check:
            base_items.extend([
                self.menu_item("Panel", ft.icons.HOME, "/panel"),
                self.menu_item("Datos", ft.icons.ASSIGNMENT, "/data"),
                self.menu_item("Logs", ft.icons.HISTORY, "/logs"),
                self.menu_item("Graficas", ft.icons.BAR_CHART, "/graphics"),
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
        """Cambia entre modo claro y oscuro"""
        self.page.on_resized = self.on_resized
        self.page.theme_mode = (
            ft.ThemeMode.LIGHT if self.page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        self.page.update()
        self.page.go(self.page.route)

    def on_resized(self, e):
        """Reacciona al cambio de tamaño de la ventana, reconstruyendola"""
        self.actions = self.responsive_menu()
        self.title = self.build_title()
        self.page.update()
    
    def user_status(self):
        """Muestra el nombre del usuario logueado."""
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
        """Funcion para crear directamente un popup del menu"""
        return ft.PopupMenuItem(
            on_click=lambda _: self.page.go(route),
            height=40,
            content=ft.Row([
                ft.Icon(icon, color=ft.colors.GREY),
                ft.Text(text, color=ft.colors.GREY)
            ])
        )
    
    def nav_button(self, tooltip, icon, route):
        """Funcion para crear directamente un boton del menu"""
        return ft.IconButton(
            on_click=lambda _: self.page.go(route),
            icon=icon,
            icon_size=24,
            icon_color=ft.colors.WHITE,
            tooltip=tooltip,
        )
    
    def confirm_dialog(self):
        """Dialogo de confirmacion de cerrar sesion"""
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
        """Muestra el dialogo de confirmacion de cerrar sesion"""
        self.dlg.open = True
        self.page.update()
    
    def logout(self, e):
        """Cierra sesion y redirige al login"""
        self.page.session.clear()
        self.dlg.open = False
        self.page.update()
        self.page.go("/login")
    
    def close_dialog(self, e):
        """Cierra el cuadro de dialogo"""
        self.dlg.open = False
        self.page.update()