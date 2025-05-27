import flet as ft

def PerfilUserPage(page: ft.Page, usuario_logado):
    page.title = "Meu Perfil"
    page.bgcolor = "#F4F6F7"

    def voltar(e):
        page.go("/user")

    cabecalho = ft.Container(
        ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar),
            ft.Text("Meu Perfil", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
        ], alignment=ft.MainAxisAlignment.START),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#F4F6F7",
        height=60,
    )

    card = ft.Container(
        ft.Column(
            [
                ft.Text("Dados do Usuário", size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                ft.Text(f"Nome: {usuario_logado.get('nome', 'Usuário')}", size=16, color="#2C3E50"),
                ft.Text(f"Nome de Usuário: {usuario_logado.get('usuario', 'user')}", size=16, color="#2C3E50"),
                ft.Text(f"E-mail: {usuario_logado.get('email', 'user@empresa.com')}", size=16, color="#2C3E50"),
                ft.Text(f"Tipo: {usuario_logado.get('tipo', 'Usuário')}", size=16, color="#2C3E50"),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20
        ),
        bgcolor="white",
        border_radius=16,
        shadow=ft.BoxShadow(blur_radius=12, color="#bbb", offset=ft.Offset(0, 2)),
        padding=40,
        width=400,
        alignment=ft.alignment.center
    )

    layout = ft.Column(
        [
            cabecalho,
            ft.Row(
                [
                    ft.Container(expand=True),
                    card,
                    ft.Container(expand=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            ),
        ],
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=0
    )

    page.controls.clear()
    page.add(layout)
    page.update()