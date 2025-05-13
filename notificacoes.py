import flet as ft

def NotificacoesPage(page: ft.Page):
    page.title = "Notificações - Help Desk"
    page.bgcolor = "#F4F6F7"

    notificacoes = [
        {
            "id": 1,
            "tipo": "Novo Ticket",
            "mensagem": "Novo chamado criado: Erro ao acessar sistema.",
            "data": "2024-05-13 09:15",
            "lida": False
        },
        {
            "id": 2,
            "tipo": "Status Alterado",
            "mensagem": "Chamado #101 foi fechado.",
            "data": "2024-05-12 17:32",
            "lida": True
        },
        {
            "id": 3,
            "tipo": "Comentário",
            "mensagem": "Novo comentário no chamado #102.",
            "data": "2024-05-12 15:10",
            "lida": False
        },
        {
            "id": 4,
            "tipo": "Atribuição",
            "mensagem": "Você foi atribuído ao chamado #103.",
            "data": "2024-05-11 11:45",
            "lida": True
        },
    ]

    tipo_icone = {
        "Novo Ticket": (ft.Icons.NOTIFICATIONS_ACTIVE, "#2980B9"),
        "Status Alterado": (ft.Icons.CHECK_CIRCLE, "#27AE60"),
        "Comentário": (ft.Icons.COMMENT, "#F39C12"),
        "Atribuição": (ft.Icons.PERSON_ADD, "#A569BD"),
    }

    def voltar(e):
        page.go("/inicial")

    lista_notificacoes = ft.Column(
        [
            ft.Card(
                ft.Container(
                    ft.Row([
                        ft.Icon(
                            tipo_icone.get(n["tipo"], (ft.Icons.NOTIFICATIONS, "#7F8C8D"))[0],
                            color=tipo_icone.get(n["tipo"], (ft.Icons.NOTIFICATIONS, "#7F8C8D"))[1],
                            size=32
                        ),
                        ft.Column([
                            ft.Text(n["mensagem"], size=16, color="#2C3E50", weight=ft.FontWeight.BOLD if not n["lida"] else ft.FontWeight.NORMAL),
                            ft.Text(n["data"], size=12, color="#7F8C8D"),
                        ], spacing=4),
                    ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=16,
                    bgcolor="#F9E79F" if not n["lida"] else "white",
                    border_radius=8,
                ),
                margin=ft.margin.symmetric(vertical=8, horizontal=0),
                elevation=2
            )
            for n in notificacoes
        ],
        spacing=0,
        expand=True
    )

    cabecalho = ft.Container(
        content=ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    icon_size=24,
                    icon_color="#7F8C8D",
                    on_click=voltar,
                ),
                ft.Text(
                    "Notificações",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#2C3E50",
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#F4F6F7",
        height=60,
    )

    conteudo_scroll = ft.ListView(
        controls=[
            lista_notificacoes,
        ],
        spacing=10,
        padding=ft.padding.all(20),
        expand=True
    )

    layout_completo = ft.Column(
        [
            cabecalho,
            conteudo_scroll,
        ],
        spacing=0,
        expand=True,
    )

    page.controls.clear()
    page.add(layout_completo)
    page.update()
