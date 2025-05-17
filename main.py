import flet as ft
from inicial import InicialPage
from novo_ticket import NovoTicketPage
from faq import FAQPage
from dashboard import DashboardPage
from tickets import TicketsPage
from estatistica import EstatisticaPage
from admin import AdminPage
from notificacoes import NotificacoesPage
from pesquisa import PesquisaPage
from configuracoes import ConfiguracoesPage
from biblioteca import BibliotecaPage

def LoginPage(page, on_login_success):
    page.title = "Help Desk - Login"
    page.bgcolor = "#2C3E50"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def entrar_click(e):
        usuario = campo_usuario.value
        senha = campo_senha.value

        if usuario and senha:
            if usuario == "admin" and senha == "1234":
                on_login_success({"usuario": usuario})
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

    lembrar_usuario = ft.Checkbox(label="Lembrar usuário", fill_color="white", label_style=ft.TextStyle(color="white"))

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
                lembrar_usuario,
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
        page.go("/inicial")

    def route_change(route):
        nonlocal usuario_logado

        if page.route == "/":
            LoginPage(page, on_login_success)
        elif page.route == "/inicial":
            if usuario_logado:
                InicialPage(page)
            else:
                page.go("/")
        elif page.route == "/novo_ticket":
            NovoTicketPage(page)
        elif page.route == "/faq":
            FAQPage(page)
        elif page.route == "/dashboard":
            DashboardPage(page)
        elif page.route == "/tickets":
            TicketsPage(page)
        elif page.route == "/estatistica":
            EstatisticaPage(page)
        elif page.route == "/admin":
            AdminPage(page)
        elif page.route == "/notificacoes":
            NotificacoesPage(page)
        elif page.route == "/pesquisa":
            PesquisaPage(page)
        elif page.route == "/configuracoes":
            ConfiguracoesPage(page)
        elif page.route == "/biblioteca":
            BibliotecaPage(page)
        else:
            LoginPage(page, on_login_success)

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
