import flet as ft
from services.db_users import register_user

# Vista de Registro
def register(page):
    def on_register_submit(e):
        email = register_email_field.value
        password = register_pass_field.value
        confirm_password = confirm_register_pass_field.value

        # Comprobar si las contraseñas coinciden
        if password != confirm_password:
            lbl_error.value = "Las contraseñas no coinciden"
        elif email and password:
            result = register_user(email, password)
            
            if result == "success":
                user_data = {
                    "email": email,
                    "is_admin": False,
                }
                page.session.set("user", user_data)
                page.client_storage.set("user", user_data)
                
                page.go("/home")
            elif result == "email_exists":
                lbl_error.value = "El correo electrónico ya está registrado"
            elif result == "invalid_email":
                lbl_error.value = "El formato del correo electrónico es inválido"
        else:
            lbl_error.value = "Por favor, ingrese los datos correctamente"

        lbl_error.update()
        page.update()

    def on_login_click(e):
        page.go("/login") 

    logo = ft.Image(
        src="https://webmailest.ugr.es/skins/elastic/images/logougr.png?s=1718096294",
    )

    logo_container = ft.Container(
        content=logo,
        margin=ft.margin.only(top=40)
    )

    register_email_field = ft.TextField(
        label="Correo electrónico",
        width=300,
        color=ft.Colors.BLACK,
        prefix_icon=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLACK)
    )

    register_pass_field = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        color=ft.Colors.BLACK,
        prefix_icon=ft.Icon(ft.Icons.LOCK, color=ft.Colors.BLACK)
    )
    
    confirm_register_pass_field = ft.TextField(
        label="Confirmar Contraseña",
        password=True,
        can_reveal_password=True,
        width=300,
        color=ft.Colors.BLACK,
        prefix_icon=ft.Icon(ft.Icons.LOCK, color=ft.Colors.BLACK),
        on_submit=on_register_submit
    )

    register_button = ft.ElevatedButton(
        "REGISTRARSE",
        on_click=on_register_submit,
        width=300,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.LIGHT_BLUE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )

    lbl_error = ft.Text(color="red")
    lbl_login = ft.Text("¿Tienes una cuenta?", color=ft.Colors.BLACK)
    
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
        "/register",
        bgcolor=ft.Colors.WHITE,
        controls=[
            ft.Column(
                [
                    logo_container,
                    register_email_field,
                    register_pass_field,
                    confirm_register_pass_field,
                    register_button,
                    lbl_login,
                    login_button,
                    footer_text,
                    lbl_error,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO
    )