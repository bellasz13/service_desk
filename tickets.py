import flet as ft

def TicketsPage(page: ft.Page):
    page.title = "Tickets - Help Desk"
    page.bgcolor = "#F4F6F7"

    tickets = [
        {
            "id": 101,
            "titulo": "Erro ao acessar sistema",
            "status": "Aberto",
            "prioridade": "Alta",
            "categoria": "Suporte Técnico",
            "data": "2024-05-10",
            "respostas": [
                {"autor": "Agente", "mensagem": "Estamos analisando o problema.", "data": "2024-05-10 10:00"}
            ]
        },
        {
            "id": 102,
            "titulo": "Solicitação de reembolso",
            "status": "Fechado",
            "prioridade": "Média",
            "categoria": "Financeiro",
            "data": "2024-05-08",
            "respostas": [
                {"autor": "Financeiro", "mensagem": "Reembolso realizado.", "data": "2024-05-09 09:00"}
            ]
        },
        {
            "id": 103,
            "titulo": "Problema na impressora",
            "status": "Em Espera",
            "prioridade": "Baixa",
            "categoria": "Infraestrutura",
            "data": "2024-05-07",
            "respostas": []
        },
        {
            "id": 104,
            "titulo": "Dúvida sobre nota fiscal",
            "status": "Aberto",
            "prioridade": "Média",
            "categoria": "Financeiro",
            "data": "2024-05-06",
            "respostas": []
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
        value="Todos",
        label_style=ft.TextStyle(color="#2C3E50")
    )

    busca = ft.TextField(
        label="Buscar por título ou ID",
        prefix_icon=ft.Icons.SEARCH,
        width=320,
        on_submit=lambda e: render_lista_tickets(),
        label_style=ft.TextStyle(color="#2C3E50")
    )

    def voltar(e):
        page.go("/inicial")

    def novo_ticket(e):
        page.go("/novo_ticket")

    def abrir_ticket(ticket):
        render_detalhe_ticket(ticket)

    def render_detalhe_ticket(ticket):
        def voltar_lista(e):
            render_lista_tickets()

        def fechar_ticket(e):
            ticket["status"] = "Fechado"
            page.snack_bar = ft.SnackBar(
                ft.Text("Ticket fechado com sucesso!", color="#2C3E50"),
                bgcolor="#27AE60"
            )
            page.snack_bar.open = True
            render_detalhe_ticket(ticket)

        def em_espera_ticket(e):
            ticket["status"] = "Em Espera"
            page.snack_bar = ft.SnackBar(
                ft.Text("Ticket colocado em espera!", color="#2C3E50"),
                bgcolor="#F39C12"
            )
            page.snack_bar.open = True
            render_detalhe_ticket(ticket)

        resposta_field = ft.TextField(
            label="Adicionar resposta",
            multiline=True,
            min_lines=2,
            max_lines=5,
            width=500,
            label_style=ft.TextStyle(color="#2C3E50")
        )

        def adicionar_resposta(e):
            texto = resposta_field.value.strip()
            if texto:
                ticket["respostas"].append({
                    "autor": "Você",
                    "mensagem": texto,
                    "data": "Agora"
                })
                resposta_field.value = ""
                page.snack_bar = ft.SnackBar(
                    ft.Text("Resposta adicionada!", color="#2C3E50"),
                    bgcolor="#2980B9"
                )
                page.snack_bar.open = True
                render_detalhe_ticket(ticket)

        cor_status = {"Aberto": "#27AE60", "Fechado": "#AAB7B8", "Em Espera": "#F39C12"}.get(ticket["status"], "#7F8C8D")
        cor_prioridade = "#2980B9" if ticket["prioridade"] == "Alta" else "#27AE60" if ticket["prioridade"] == "Média" else "#F39C12"

        respostas_list = ft.Column([
            ft.Container(
                ft.Column([
                    ft.Text(f"{r['autor']} ({r['data']}):", size=14, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(r["mensagem"], color="#2C3E50")
                ], spacing=2),
                bgcolor="#F8F9F9",
                border_radius=8,
                padding=10,
                margin=ft.margin.only(bottom=8)
            )
            for r in ticket["respostas"]
        ], spacing=8)

        # Botões de ação
        botoes = [
            ft.ElevatedButton(
                "Adicionar Resposta",
                icon=ft.Icons.SEND,
                bgcolor="#2980B9",
                color="white",
                on_click=adicionar_resposta,
                disabled=ticket["status"] == "Fechado"
            ),
            ft.ElevatedButton(
                "Fechar Ticket",
                icon=ft.Icons.LOCK,
                bgcolor="#AAB7B8",
                color="white",
                on_click=fechar_ticket,
                disabled=ticket["status"] == "Fechado"
            )
        ]
        # Adiciona o botão "Deixar em espera" se não está fechado nem já em espera
        if ticket["status"] != "Fechado" and ticket["status"] != "Em Espera":
            botoes.append(
                ft.ElevatedButton(
                    "Deixar em Espera",
                    icon=ft.Icons.PAUSE_CIRCLE,
                    bgcolor="#F39C12",
                    color="white",
                    on_click=em_espera_ticket
                )
            )

        page.controls.clear()
        page.add(
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar_lista),
                        ft.Text(f"Ticket #{ticket['id']}", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Text(ticket["titulo"], size=20, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Row([
                        ft.Container(
                            ft.Text(ticket["status"], color="white", size=12),
                            bgcolor=cor_status,
                            padding=ft.padding.symmetric(horizontal=10, vertical=2),
                            border_radius=6,
                        ),
                        ft.Container(
                            ft.Text(ticket["prioridade"], color="white", size=12),
                            bgcolor=cor_prioridade,
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                            border_radius=6,
                        ),
                        ft.Container(
                            ft.Text(ticket["categoria"], color="#2C3E50", size=12),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        ),
                        ft.Text(ticket["data"], size=12, color="#7F8C8D"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=10),
                    ft.Divider(),
                    ft.Text("Respostas:", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    respostas_list if ticket["respostas"] else ft.Text("Nenhuma resposta ainda.", color="#2C3E50"),
                    ft.Divider(),
                    resposta_field if ticket["status"] != "Fechado" else ft.Text("Ticket fechado. Não é possível responder.", color="#AAB7B8"),
                    ft.Row(botoes, spacing=20)
                ], spacing=18),
                padding=30,
                bgcolor="white",
                border_radius=12,
                margin=ft.margin.all(30),
                width=700,
                alignment=ft.alignment.top_center
            )
        )
        page.update()

    def render_lista_tickets():
        lista_tickets = ft.Column(spacing=0, expand=True)
        status = filtro_status.value
        termo = busca.value.lower()
        filtrados = [
            t for t in tickets
            if (status == "Todos" or t["status"] == status)
            and (termo in t["titulo"].lower() or termo in str(t["id"]))
        ]
        for t in filtrados:
            cor_status = {"Aberto": "#27AE60", "Fechado": "#AAB7B8", "Em Espera": "#F39C12"}.get(t["status"], "#7F8C8D")
            lista_tickets.controls.append(
                ft.GestureDetector(
                    on_tap=lambda e, ticket=t: abrir_ticket(ticket),
                    content=ft.Card(
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

    filtro_status.on_change = lambda e: render_lista_tickets()
    busca.on_change = lambda e: render_lista_tickets()

    render_lista_tickets()
