import flet as ft
from inicial import InicialPage
from novo_ticket import NovoTicketPage
from dashboard import DashboardPage
from tickets import TicketsPage
from admin import AdminPage
from pesquisa import PesquisaPage
from configuracoes import ConfiguracoesPage
from biblioteca import BibliotecaPage
from user import UserPage
from ticket_user import TicketUserPage
from perfil_user import PerfilUserPage
from exportacao import ExportacaoPage

from database import verificar_usuario

def LoginPage(page, on_login_success):
    page.title = "Help Desk - Login"
    page.bgcolor = "#2C3E50"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def entrar_click(e):
        usuario = campo_usuario.value
        senha = campo_senha.value

        if usuario and senha:
            usuario_db = verificar_usuario(usuario, senha)
            if usuario_db:
                on_login_success({
                    "id_usuario": usuario_db["id_usuario"],
                    "usuario": usuario_db["nome_usuario"],
                    "tipo": usuario_db["tipo_usuario"],
                    "nome_completo": usuario_db["nome_completo"],
                    "email": usuario_db["email"]
                })
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

    global campo_usuario, campo_senha
    campo_usuario = ft.TextField(
        label="Usuário",
        prefix_icon=ft.Icons.PERSON,
        border_color="white",
        color="white",
        label_style=ft.TextStyle(color="white"),
        bgcolor="#34495E",
    )
    
    campo_senha = ft.TextField(
        label="Senha",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        border_color="white",
        color="white",
        label_style=ft.TextStyle(color="white"),
        bgcolor="#34495E",
    )

    botao_entrar = ft.ElevatedButton(
        text="Entrar",
        on_click=entrar_click,
        bgcolor="#F39C12",
        color="white",
    )

    page.controls.clear()
    page.add(
        ft.Column(
            [
                logo,
                campo_usuario,
                campo_senha,
                botao_entrar,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            width=400,  
        )
    )

def main(page: ft.Page):
    page.title = "Help Desk"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#2C3E50"
    
    usuario_logado = None

    def on_login_success(usuario):
        nonlocal usuario_logado
        usuario_logado = usuario
        if usuario["tipo"] == "administrador":
            page.go("/inicial")
        elif usuario["tipo"] == "comum":
            page.go("/user")

    def route_change(route):
        nonlocal usuario_logado

        if page.route == "/":
            LoginPage(page, on_login_success)
        elif page.route == "/inicial":
            if usuario_logado and usuario_logado.get("tipo") == "administrador":
                InicialPage(page)
            else:
                page.go("/")
        elif page.route == "/user":
            if usuario_logado and usuario_logado.get("tipo") == "comum":
                UserPage(page, usuario_logado)
            else:
                page.go("/")
        elif page.route == "/meus_tickets":
            if usuario_logado and usuario_logado.get("tipo") == "comum":
                TicketUserPage(page, usuario_logado)
            else:
                page.go("/")
        elif page.route == "/novo_ticket":
            NovoTicketPage(page, usuario_logado)
        elif page.route == "/perfil":
            PerfilUserPage(page, usuario_logado)
        elif page.route == "/dashboard":
            DashboardPage(page)
        elif page.route == "/tickets":
            TicketsPage(page, usuario_logado)
        elif page.route == "/admin":
            AdminPage(page)
        elif page.route == "/pesquisa":
            PesquisaPage(page)
        elif page.route == "/configuracoes":
            ConfiguracoesPage(page)
        elif page.route == "/biblioteca":
            BibliotecaPage(page, usuario_logado)
        elif page.route == "/exportacao":
            ExportacaoPage(page)
        else:
            LoginPage(page, on_login_success)

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main, upload_dir="uploads")
