import flet as ft
from services.db_users import is_admin, verify_login

def login(page):
    def on_login_click(e):
        email = gmail_field.value
        password = pass_field.value
        
        if email and password:
            if verify_login(email, password):
                user_data = {
                    "email": email,
                    "is_admin": is_admin(email),
                }
                
                page.session.set("user", user_data)
                page.client_storage.set("user", user_data)
                
                page.go("/home")
            else:
                lbl_error.value = "Usuario o contraseña incorrectos"
        else:
            lbl_error.value = "Por favor, ingrese usuario y contraseña"
        
        lbl_error.update()
        page.update()
        
    def on_register_click(e):
        page.go("/register") 

    logo = ft.Image(src="https://webmailest.ugr.es/skins/elastic/images/logougr.png?s=1718096294")

    gmail_field = ft.TextField(
        label="Nombre de usuario",
        width=300,
        color=ft.Colors.BLACK,
        prefix_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLACK)
    )

    pass_field = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        color=ft.Colors.BLACK,
        prefix_icon=ft.Icon(ft.Icons.LOCK, color=ft.Colors.BLACK),
        on_submit=on_login_click
    )

    login_button = ft.ElevatedButton(
        "INICIAR SESIÓN",
        on_click=on_login_click,
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.LIGHT_BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    lbl_error = ft.Text(color="red")
    lbl_register = ft.Text("¿No tienes una cuenta?", color=ft.Colors.BLACK)
    
    register_button = ft.ElevatedButton(
        "REGÍSTRATE",
        on_click=on_register_click,
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.LIGHT_BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    footer_text = ft.Column(
        controls=[
            ft.Text(
                "Este servicio de correo es exclusivamente para uso académico.",
                color=ft.Colors.BLACK,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
                width=300,
            ),
            ft.Text(
                "La UGR no es responsable de los contenidos transmitidos ni del uso ilícito del mismo, sino, en todo caso, el titular de la cuenta remitente.\n [+info]\n",
                color=ft.Colors.BLACK,
                text_align=ft.TextAlign.CENTER,
                width=300,
            ),
            ft.TextButton(
                text="https://www.ugr.es/universidad/servicios/correo-electronico",
                url="https://www.ugr.es/universidad/servicios/correo-electronico",
                width=300,
            ),
        ]
    )

    return ft.View(
        "/login",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.Column(
                [
                    logo,
                    gmail_field,
                    pass_field,
                    login_button,
                    lbl_register,
                    register_button,
                    footer_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            lbl_error,            
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )
