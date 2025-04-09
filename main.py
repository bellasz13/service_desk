import flet as ft

def main(page: ft.Page):
    page.title = "Help Desk"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#2C3E50"

    def entrar_click(e):
        usuario = campo_usuario.value
        senha = campo_senha.value

        if usuario == "admin" and senha == "1234":
            mensagem.text = "Login bem-sucedido! Bem-vindo ao Help Desk!"
            mensagem.color = "green"
        else:
            mensagem.text = "Usuário ou senha inválidos."
            mensagem.color = "red"
        page.update()

    # Logo do sistema
    logo = ft.Text(
        "Help Desk",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="white",
    )

    # Campos de entrada (usuário e senha)
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

    # Checkbox para "Lembrar me"
    lembrar_me = ft.Checkbox(label="Lembrar me", fill_color="white", label_style=ft.TextStyle(color="white"))

    # Botão de envio
    botao_entrar = ft.ElevatedButton(
        text="Entrar",
        on_click=entrar_click,
        bgcolor="#F39C12",
        color="white",
    )

    # Mensagem de feedback
    mensagem = ft.Text("", size=16)

    # Layout principal
    page.add(
        ft.Column(
            [
                logo,
                campo_usuario,
                campo_senha,
                lembrar_me,
                botao_entrar,
                mensagem,
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
