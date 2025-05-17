import flet as ft

def InicialPage(page: ft.Page):
    page.title = "Help Desk - Dashboard"
    page.bgcolor = "#F4F6F7"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    if not hasattr(page, "sidebar_expanded"):
        page.sidebar_expanded = False

    def toggle_sidebar(e):
        page.sidebar_expanded = not page.sidebar_expanded
        render_page()

    def sair(e):
        page.session.clear()
        page.go("/")

    def pesquisa(e):
        page.go("/pesquisa")

    def dashboard(e):
        page.go("/dashboard")

    def tickets(e):
        page.go("/tickets")

    def estatistica(e):
        page.go("/estatistica")

    def admin(e):
        page.go("/admin")

    def configuracoes(e):
        page.go("/configuracoes")

    def novo_ticket(e):
        page.go("/novo_ticket")

    def faq(e):
        page.go("/faq")
        
    def notificacoes(e):
        page.go("/notificacoes")
    
    def biblioteca(e):
        page.go("/biblioteca")

    def render_page():
    
        header = ft.Container(
            ft.Row(
                [
                    ft.IconButton(
                        ft.Icons.MENU,
                        icon_color="#2C3E50",
                        tooltip="Expandir/recolher menu",
                        on_click=toggle_sidebar
                    ),
                    ft.Text("Help Desk", size=24, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Container(expand=True),
                    ft.IconButton(ft.Icons.NOTIFICATIONS, icon_color="#2C3E50", tooltip="Notificações", on_click=notificacoes),
                    ft.IconButton(ft.Icons.SEARCH, icon_color="#2C3E50", tooltip="Pesquisar", on_click=pesquisa),
                    ft.IconButton(ft.Icons.EXIT_TO_APP, icon_color="#2C3E50", tooltip="Sair", on_click=sair),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor="#ECF0F1",
            border_radius=ft.border_radius.all(0)
        )

        if page.sidebar_expanded:
            sidebar = ft.Container(
                ft.Column(
                    [
                        ft.Container(
                            ft.Row([ft.Icon(ft.Icons.DASHBOARD, color="white"), ft.Text("Dashboard", color="white", size=16)]),
                            on_click=dashboard,
                            padding=5
                        ),
                        ft.Container(
                            ft.Row([ft.Icon(ft.Icons.SUPPORT, color="white"), ft.Text("Tickets", color="white", size=16)]),
                            on_click=tickets,
                            padding=5
                        ),
                        ft.Container(
                            ft.Row([ft.Icon(ft.Icons.PIE_CHART, color="white"), ft.Text("Estatísticas", color="white", size=16)]),
                            on_click=estatistica,
                            padding=5
                        ),
                        ft.Container(
                            ft.Row([ft.Icon(ft.Icons.ADMIN_PANEL_SETTINGS, color="white"), ft.Text("Admin", color="white", size=16)]),
                            on_click=admin,
                            padding=5
                        ),
                        ft.Divider(color="#34495E"),
                        ft.Container(
                            ft.Row([ft.Icon(ft.Icons.SETTINGS, color="white"), ft.Text("Configurações", color="white", size=16)]),
                            on_click=configuracoes,
                            padding=5
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                width=180,
                bgcolor="#2C3E50",
                padding=10,
                border_radius=ft.border_radius.only(top_left=0, bottom_left=0, top_right=10, bottom_right=10),
            )
        else:
            sidebar = ft.Container(
                ft.Column(
                    [
                        ft.IconButton(icon=ft.Icons.DASHBOARD, tooltip="Dashboard", on_click=dashboard, icon_color="white"),
                        ft.IconButton(icon=ft.Icons.SUPPORT, tooltip="Tickets", on_click=tickets, icon_color="white"),
                        ft.IconButton(icon=ft.Icons.PIE_CHART, tooltip="Estatísticas", on_click=estatistica, icon_color="white"),
                        ft.IconButton(icon=ft.Icons.ADMIN_PANEL_SETTINGS, tooltip="Admin", on_click=admin, icon_color="white"),
                        ft.Divider(color="#34495E"),
                        ft.IconButton(icon=ft.Icons.SETTINGS, tooltip="Configurações", on_click=configuracoes, icon_color="white"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                width=60,
                bgcolor="#2C3E50",
                padding=10,
                border_radius=ft.border_radius.only(top_left=0, bottom_left=0, top_right=10, bottom_right=10),
            )

        dashboard_blocks = ft.Row(
            [
                ft.Container(
                    ft.Column([
                        ft.Text("Tickets Atribuídos", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                        ft.Text("5", size=32, weight=ft.FontWeight.BOLD, color="#2980B9"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    width=200, height=120, bgcolor="#D6EAF8", border_radius=10, padding=20
                ),
                ft.Container(
                    ft.Column([
                        ft.Text("Tickets Novos", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                        ft.Text("2", size=32, weight=ft.FontWeight.BOLD, color="#27AE60"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    width=200, height=120, bgcolor="#D5F5E3", border_radius=10, padding=20
                ),
                ft.Container(
                    ft.Column([
                        ft.Text("Tickets em Espera", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                        ft.Text("1", size=32, weight=ft.FontWeight.BOLD, color="#F39C12"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    width=200, height=120, bgcolor="#FCF3CF", border_radius=10, padding=20
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        quick_actions = ft.Row(
            [
                ft.ElevatedButton(text="Novo Ticket", icon=ft.Icons.ADD, bgcolor="#2980B9", color="white", on_click=novo_ticket),
                ft.ElevatedButton(text="FAQ", icon=ft.Icons.HELP, bgcolor="#F39C12", color="white", on_click=faq),
                ft.ElevatedButton(text="Biblioteca", icon=ft.Icons.LIBRARY_ADD, bgcolor="#2980B9", on_click=biblioteca),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        content = ft.Column(
            [
                ft.Text("Visão Geral", size=20, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                dashboard_blocks,
                ft.Divider(height=30, color="#ECF0F1"),
                quick_actions,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=30,
            expand=True,
        )

        main_layout = ft.Row(
            [
                sidebar,
                ft.Container(content, expand=True, padding=30)
            ],
            expand=True
        )

        footer = ft.Container(
            ft.Text("Powered by Help Desk", size=12, color="#7F8C8D"),
            alignment=ft.alignment.center,
            padding=10,
            bgcolor="#ECF0F1"
        )

        page.controls.clear()
        page.add(header, main_layout, footer)
        page.update()

    render_page()
