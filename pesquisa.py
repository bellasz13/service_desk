import flet as ft

def PesquisaPage(page: ft.Page):
    page.title = "Pesquisa - Help Desk"
    page.bgcolor = "#F4F6F7"

    tickets = [
        {"id": 101, "titulo": "Erro ao acessar sistema", "status": "Aberto", "categoria": "Suporte Técnico"},
        {"id": 102, "titulo": "Solicitação de reembolso", "status": "Fechado", "categoria": "Financeiro"},
    ]
    usuarios = [
        {"nome": "Ana Souza", "email": "ana@empresa.com", "tipo": "Administrador"},
        {"nome": "Carlos Lima", "email": "carlos@empresa.com", "tipo": "Usuário"},
    ]
    categorias = [
        {"nome": "Suporte Técnico"},
        {"nome": "Financeiro"},
        {"nome": "Infraestrutura"},
        {"nome": "Outro"},
    ]

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

    def atualizar_lista():
        termo = campo_busca.value.lower()
        tipo = tipo_selecionado.value
        resultado.controls.clear()

        if tipo == "Tickets":
            encontrados = [
                t for t in tickets
                if termo in t["titulo"].lower() or termo in str(t["id"]) or termo in t["categoria"].lower()
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum ticket encontrado.", color="#7F8C8D"))
            for t in encontrados:
                resultado.controls.append(
                    ft.Card(
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
        elif tipo == "Usuários":
            encontrados = [
                u for u in usuarios
                if termo in u["nome"].lower() or termo in u["email"].lower() or termo in u["tipo"].lower()
            ]
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
                                    bgcolor="#2980B9" if u["tipo"]=="Administrador" else "#27AE60",
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
            encontrados = [
                c for c in categorias
                if termo in c["nome"].lower()
            ]
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

    tipo_selecionado.on_change = lambda e: atualizar_lista()
    campo_busca.on_change = lambda e: atualizar_lista()

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

    page.controls.clear()
    page.add(layout_completo)
    page.update()
