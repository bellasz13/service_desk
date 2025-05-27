import flet as ft

def UserPage(page: ft.Page, usuario_logado):
    page.title = "Help Desk - Usuário"
    page.bgcolor = "#F4F6F7"

    def abrir_chamado(e):
        page.go("/novo_ticket")

    def ver_chamados(e):
        page.go("/meus_tickets")

    def biblioteca(e):
        page.go("/biblioteca")

    def perfil(e):
        page.go("/perfil")

    def sair(e):
        page.session.clear()
        page.appbar = None  
        page.go("/")

    page.appbar = ft.AppBar(
        title=ft.Text("Help Desk", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
        bgcolor="#ECF0F1",
        center_title=False,
        elevation=2,
        toolbar_height=60,
        actions=[
            ft.IconButton(icon=ft.Icons.PERSON, icon_color="#2980B9", tooltip="Perfil", on_click=perfil),
            ft.IconButton(icon=ft.Icons.BOOK, icon_color="#2980B9", tooltip="Biblioteca", on_click=biblioteca),
            ft.IconButton(icon=ft.Icons.EXIT_TO_APP, icon_color="#AAB7B8", tooltip="Sair", on_click=sair)
        ]
    )

    blocos = ft.Row(
        [
            ft.Container(
                ft.Column([
                    ft.Text("Abrir Chamado", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text("Registre um novo chamado para o suporte.", color="#2C3E50"),
                    ft.ElevatedButton("Abrir Chamado", icon=ft.Icons.ADD, bgcolor="#2980B9", color="white", on_click=abrir_chamado)
                ], spacing=10),
                width=250, height=180, bgcolor="#D6EAF8", border_radius=10, padding=20
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Meus Chamados", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text("Consulte o histórico dos seus chamados.", color="#2C3E50"),
                    ft.ElevatedButton("Ver Chamados", icon=ft.Icons.LIST, bgcolor="#27AE60", color="white", on_click=ver_chamados)
                ], spacing=10),
                width=250, height=180, bgcolor="#D5F5E3", border_radius=10, padding=20
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Base de Conhecimento", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text("Encontre respostas rápidas para dúvidas frequentes.", color="#2C3E50"),
                    ft.ElevatedButton("Acessar Biblioteca", icon=ft.Icons.BOOK, bgcolor="#F39C12", color="white", on_click=biblioteca)
                ], spacing=10),
                width=250, height=180, bgcolor="#FCF3CF", border_radius=10, padding=20
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    content = ft.Column(
        [
            ft.Container(expand=True),
            ft.Container(
                blocos,
                alignment=ft.alignment.center,
                bgcolor="white",
                border_radius=12,
                shadow=ft.BoxShadow(blur_radius=12, color="#bbb", offset=ft.Offset(0, 2)),
                padding=40,
                width=900
            ),
            ft.Container(expand=True),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.controls.clear()
    page.add(content)
    page.update()
