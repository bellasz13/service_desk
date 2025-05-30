import flet as ft
from database import pesquisar_tickets, pesquisar_usuarios, pesquisar_categorias, buscar_respostas_ticket, inserir_resposta

def PesquisaPage(page: ft.Page, usuario_logado=None):  
    page.title = "Pesquisa - Help Desk"
    page.bgcolor = "#F4F6F7"

    tipos_pesquisa = ["Tickets", "Usuários", "Categorias"]
    tipo_selecionado = ft.Dropdown(
        label="Pesquisar por",
        width=180,
        options=[ft.dropdown.Option(tp) for tp in tipos_pesquisa],
        value="Tickets"
    )

    campo_busca = ft.TextField(
        label="Digite o termo de pesquisa",
        prefix_icon=ft.Icons.SEARCH,
        width=320,
        on_submit=lambda e: atualizar_lista()
    )

    def voltar(e):
        page.go("/inicial")

    resultado = ft.Column(spacing=0, expand=True)

    def abrir_ticket(ticket):
        def voltar_lista(e):
            render_pesquisa()

        resposta_field = ft.TextField(
            label="Adicionar resposta",
            multiline=True,
            min_lines=2,
            max_lines=5,
            width=500,
            label_style=ft.TextStyle(color="#2C3E50")
        )

        respostas = buscar_respostas_ticket(ticket["id"])

        def adicionar_resposta(e):
            texto = resposta_field.value.strip()
            if texto and usuario_logado:
                from datetime import datetime
                data_resposta = datetime.now().strftime("%Y-%m-%d")
                hora_resposta = datetime.now().strftime("%H:%M:%S")
                inserir_resposta(
                    ticket["id"],
                    usuario_logado["id_usuario"],
                    texto,
                    data_resposta,
                    hora_resposta
                )
                resposta_field.value = ""
                page.snack_bar = ft.SnackBar(
                    ft.Text("Resposta adicionada!", color="#2C3E50"),
                    bgcolor="#2980B9"
                )
                page.snack_bar.open = True
                abrir_ticket(ticket)

        respostas_list = ft.Column([
            ft.Container(
                ft.Column([
                    ft.Text(f"{r['id_usuario']} ({r['data_resposta']} {r['hora_resposta']}):", size=14, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(r["mensagem"], color="#2C3E50")
                ], spacing=2),
                bgcolor="#F8F9F9",
                border_radius=8,
                padding=10,
                margin=ft.margin.only(bottom=8)
            )
            for r in respostas
        ], spacing=8)

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
                            bgcolor="#27AE60" if ticket["status"] == "Aberto" else "#AAB7B8",
                            padding=ft.padding.symmetric(horizontal=10, vertical=2),
                            border_radius=6,
                        ),
                        ft.Container(
                            ft.Text(ticket["categoria"], color="#2C3E50", size=12),
                            padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        ),
                    ], alignment=ft.MainAxisAlignment.START, spacing=10),
                    ft.Divider(),
                    ft.Text("Respostas:", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    respostas_list if respostas else ft.Text("Nenhuma resposta ainda.", color="#2C3E50"),
                    ft.Divider(),
                    resposta_field if usuario_logado else ft.Text("Faça login para responder.", color="#AAB7B8"),
                    ft.Row([
                        ft.ElevatedButton(
                            "Adicionar Resposta",
                            icon=ft.Icons.SEND,
                            bgcolor="#2980B9",
                            color="white",
                            on_click=adicionar_resposta,
                            disabled=not usuario_logado
                        ),
                    ], spacing=20)
                ], spacing=18, expand=True, scroll=ft.ScrollMode.ALWAYS),
                padding=30,
                bgcolor="white",
                border_radius=12,
                margin=ft.margin.all(30),
                width=700,
                alignment=ft.alignment.top_center,
                expand=True
            )
        )
        page.update()

    def atualizar_lista():
        termo = campo_busca.value.strip()
        tipo = tipo_selecionado.value
        resultado.controls.clear()

        if tipo == "Tickets":
            encontrados = pesquisar_tickets(termo)
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum ticket encontrado.", color="#7F8C8D"))
            for t in encontrados:
                resultado.controls.append(
                    ft.GestureDetector(
                        on_tap=lambda e, ticket=t: abrir_ticket(ticket),
                        content=ft.Card(
                            ft.Container(
                                ft.Row([
                                    ft.Text(f"#{t['id']}", size=14, color="#7F8C8D"),
                                    ft.Text(t["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                    ft.Container(
                                        ft.Text(t["status"], color="white", size=12),
                                        bgcolor="#27AE60" if t["status"]=="Aberto" else "#AAB7B8",
                                        padding=ft.padding.symmetric(horizontal=10, vertical=2),
                                        border_radius=6,
                                        margin=ft.margin.only(left=10)
                                    ),
                                    ft.Text(t["categoria"], size=12, color="#2C3E50"),
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                padding=16,
                                bgcolor="white",
                                border_radius=8,
                            ),
                            margin=ft.margin.symmetric(vertical=8, horizontal=0),
                            elevation=2
                        )
                    )
                )
        elif tipo == "Usuários":
            encontrados = pesquisar_usuarios(termo)
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum usuário encontrado.", color="#7F8C8D"))
            for u in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Row([
                                ft.Text(u["nome"], size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(u["email"], size=14, color="#7F8C8D"),
                                ft.Container(
                                    ft.Text(u["tipo"], color="white", size=12),
                                    bgcolor="#2980B9" if u["tipo"]=="administrador" else "#27AE60",
                                    padding=ft.padding.symmetric(horizontal=10, vertical=2),
                                    border_radius=6,
                                    margin=ft.margin.only(left=10)
                                ),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        elif tipo == "Categorias":
            encontrados = pesquisar_categorias(termo)
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhuma categoria encontrada.", color="#7F8C8D"))
            for c in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Text(c["nome"], size=16, color="#2C3E50"),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        page.update()

    def render_pesquisa():
        page.controls.clear()
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
                        "Pesquisa",
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

        barra_busca = ft.Row(
            [
                tipo_selecionado,
                campo_busca,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
        )

        conteudo_scroll = ft.ListView(
            controls=[
                barra_busca,
                ft.Divider(height=10, color="#F4F6F7"),
                resultado,
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

        page.add(layout_completo)
        page.update()

    tipo_selecionado.on_change = lambda e: atualizar_lista()
    campo_busca.on_change = lambda e: atualizar_lista()

    atualizar_lista()
    render_pesquisa()
