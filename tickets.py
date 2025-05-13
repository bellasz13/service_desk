import flet as ft

def TicketsPage(page: ft.Page):
    page.title = "Tickets - Help Desk"
    page.bgcolor = "#F4F6F7"

   #substituir por banco de dados
    tickets = [
        {
            "id": 101,
            "titulo": "Erro ao acessar sistema",
            "status": "Aberto",
            "prioridade": "Alta",
            "categoria": "Suporte Técnico",
            "data": "2024-05-10"
        },
        {
            "id": 102,
            "titulo": "Solicitação de reembolso",
            "status": "Fechado",
            "prioridade": "Média",
            "categoria": "Financeiro",
            "data": "2024-05-08"
        },
        {
            "id": 103,
            "titulo": "Problema na impressora",
            "status": "Em Espera",
            "prioridade": "Baixa",
            "categoria": "Infraestrutura",
            "data": "2024-05-07"
        },
        {
            "id": 104,
            "titulo": "Dúvida sobre nota fiscal",
            "status": "Aberto",
            "prioridade": "Média",
            "categoria": "Financeiro",
            "data": "2024-05-06"
        },
    ]

    filtro_status = ft.Dropdown(
        label="Filtrar por status",
        width=180,
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Aberto"),
            ft.dropdown.Option("Fechado"),
            ft.dropdown.Option("Em Espera"),
        ],
        value="Todos"
    )

    busca = ft.TextField(
        label="Buscar por título ou ID",
        prefix_icon=ft.Icons.SEARCH,
        width=320,
        on_submit=lambda e: atualizar_lista()
    )

    def voltar(e):
        page.go("/inicial")

    def novo_ticket(e):
        page.go("/novo_ticket")

    def atualizar_lista():
        status = filtro_status.value
        termo = busca.value.lower()
        filtrados = [
            t for t in tickets
            if (status == "Todos" or t["status"] == status)
            and (termo in t["titulo"].lower() or termo in str(t["id"]))
        ]
        lista_tickets.controls.clear()
        for t in filtrados:
            cor_status = {"Aberto": "#27AE60", "Fechado": "#AAB7B8", "Em Espera": "#F39C12"}.get(t["status"], "#7F8C8D")
            lista_tickets.controls.append(
                ft.Card(
                    ft.Container(
                        ft.Column([
                            ft.Row([
                                ft.Text(f"#{t['id']}", size=14, color="#7F8C8D"),
                                ft.Text(t["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Container(
                                    ft.Text(t["status"], color="white", size=12),
                                    bgcolor=cor_status,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=2),
                                    border_radius=6,
                                    margin=ft.margin.only(left=10)
                                ),
                                ft.Container(
                                    ft.Text(t["prioridade"], color="white", size=12),
                                    bgcolor="#2980B9" if t["prioridade"]=="Alta" else "#27AE60" if t["prioridade"]=="Média" else "#F39C12",
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    border_radius=6,
                                    margin=ft.margin.only(left=10)
                                ),
                                ft.Container(
                                    ft.Text(t["categoria"], color="#2C3E50", size=12),
                                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                    margin=ft.margin.only(left=10)
                                ),
                                ft.Text(t["data"], size=12, color="#7F8C8D"),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ], spacing=8),
                        padding=16,
                        bgcolor="white",
                        border_radius=8,
                    ),
                    margin=ft.margin.symmetric(vertical=8, horizontal=0),
                    elevation=2
                )
            )
        page.update()

    filtro_status.on_change = lambda e: atualizar_lista()
    busca.on_change = lambda e: atualizar_lista()

    lista_tickets = ft.Column(spacing=0, expand=True)
    atualizar_lista()

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
                    "Meus Tickets",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#2C3E50",
                ),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    text="Novo Ticket",
                    icon=ft.Icons.ADD,
                    bgcolor="#2980B9",
                    color="white",
                    on_click=novo_ticket,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#F4F6F7",
        height=60,
    )

    barra_busca = ft.Row(
        [
            busca,
            filtro_status,
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
    )

    conteudo_scroll = ft.ListView(
        controls=[
            barra_busca,
            ft.Divider(height=10, color="#F4F6F7"),
            lista_tickets,
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
