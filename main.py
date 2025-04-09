import flet as ft

def main(page: ft.Page):

    page.title = "Help Desk"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#2C3E50"

    def entrar_click(e):
        usuario = campo_usuario.value
        senha = campo_senha.value

        if usuario and senha:
            if usuario == "admin" and senha == "1234":  
                snack_bar = ft.SnackBar(
                    content=ft.Text("Login realizado com sucesso!"),
                    bgcolor="green",
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
            else:
                snack_bar = ft.SnackBar(
                    content=ft.Text("Usuário ou senha incorretos!"),
                    bgcolor="red",
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
        else:
            snack_bar = ft.SnackBar(
                content=ft.Text("Preencha todos os campos!"),
                bgcolor="orange",
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True

        page.update()

    logo = ft.Text(
        "Help Desk",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    campo_usuario = ft.TextField(
        label="Usuário",
        prefix_icon=ft.icons.PERSON,
        border_color="white",
        color="white",
        label_style=ft.TextStyle(color="white"),
        bgcolor="#34495E",
    )
    
    campo_senha = ft.TextField(
        label="Senha",
        prefix_icon=ft.icons.LOCK,
        password=True,
        can_reveal_password=True,
        border_color="white",
        color="white",
        label_style=ft.TextStyle(color="white"),
        bgcolor="#34495E",
    )

    lembrar_usuario = ft.Checkbox(label="Lembrar usuário", fill_color="white", label_style=ft.TextStyle(color="white"))

    # Botão de envio
    botao_entrar = ft.ElevatedButton(
        text="Entrar",
        on_click=entrar_click,
        bgcolor="#F39C12",
        color="white",
    )

    # Layout principal
    page.add(
        ft.Column(
            [
                logo,
                campo_usuario,
                campo_senha,
                lembrar_usuario,
                botao_entrar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            width=400,  # Largura fixa para centralizar os elementos
        )
    )

# Executar o aplicativo Flet
if __name__ == "__main__":
    ft.app(target=main)
