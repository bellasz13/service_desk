import flet as ft

def BibliotecaPage(page: ft.Page, usuario_logado=None):
    page.title = "Base de Conhecimento"
    page.bgcolor = "#F4F6F7"

    faqs = [
        {"pergunta": "Como redefinir minha senha?", "resposta": "Acesse a tela de login, clique em 'Esqueci minha senha' e siga as instruções."},
        {"pergunta": "Como abrir um chamado?", "resposta": "Clique em 'Novo Ticket' no menu lateral e preencha o formulário."},
    ]
    tutoriais = [
        {"titulo": "Configurar e-mail corporativo", "passos": [
            "Abra o aplicativo de e-mail.",
            "Insira seu endereço e senha.",
            "Clique em 'Avançar' e siga as instruções na tela."
        ]},
        {"titulo": "Acessar o sistema remoto", "passos": [
            "Baixe o aplicativo VPN.",
            "Insira suas credenciais.",
            "Conecte-se e acesse o sistema normalmente."
        ]}
    ]
    dicas = [
        {"titulo": "Impressora não imprime", "dica": "Verifique se está ligada, conectada ao computador e com papel."},
        {"titulo": "Erro de login", "dica": "Confira se o CAPS LOCK está ativado e tente novamente."}
    ]
    manuais = [
        {"titulo": "Política de uso de TI", "conteudo": "Todos os colaboradores devem seguir as normas de segurança para uso dos recursos de TI."},
        {"titulo": "Manual do sistema de chamados", "conteudo": "Guia completo para uso do sistema de tickets."}
    ]
    tecnicos = [
        {"titulo": "Script para reset de senha", "conteudo": "Execute o comando: reset_user_password --user <usuário>"},
        {"titulo": "Melhores práticas de atendimento", "conteudo": "Registre todos os detalhes, mantenha comunicação clara e siga os SLAs."}
    ]
    midias = [
        {"titulo": "Vídeo: Como abrir um chamado", "url": "https://www.youtube.com/watch?v=exemplo"},
        {"titulo": "Tutorial em PDF: Configuração de e-mail", "url": "https://www.seusite.com/tutorial-email.pdf"}
    ]
    feedbacks = []

    categorias = [
        "FAQs", "Tutoriais", "Dicas", "Manuais", "Artigos Técnicos", "Materiais Multimídia"
    ]
    categoria_selecionada = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option(cat) for cat in categorias],
        value="FAQs",
        width=250,
        label_style=ft.TextStyle(color="#2C3E50")
    )
    busca = ft.TextField(
        label="Buscar artigo ou palavra-chave",
        prefix_icon=ft.Icons.SEARCH,
        width=350,
        label_style=ft.TextStyle(color="#2C3E50")
    )

    resultado = ft.Column(expand=True)

    def atualizar_lista(e=None):
        termo = busca.value.lower()
        cat = categoria_selecionada.value
        resultado.controls.clear()

        if cat == "FAQs":
            encontrados = [
                f for f in faqs
                if termo in f["pergunta"].lower() or termo in f["resposta"].lower()
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhuma FAQ encontrada.", color="#2C3E50"))
            for f in encontrados:
                resultado.controls.append(
                    ft.ExpansionTile(
                        title=ft.Text(f["pergunta"], color="#2C3E50", weight=ft.FontWeight.BOLD),
                        controls=[ft.Text(f["resposta"], color="#2C3E50")]
                    )
                )
        elif cat == "Tutoriais":
            encontrados = [
                t for t in tutoriais
                if termo in t["titulo"].lower() or any(termo in p.lower() for p in t["passos"])
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum tutorial encontrado.", color="#2C3E50"))
            for t in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Text(t["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text("Passos:", color="#2C3E50"),
                                ft.Column([ft.Text(f"{idx+1}. {p}", color="#2C3E50") for idx, p in enumerate(t["passos"])], spacing=2)
                            ], spacing=8),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        elif cat == "Dicas":
            encontrados = [
                d for d in dicas
                if termo in d["titulo"].lower() or termo in d["dica"].lower()
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhuma dica encontrada.", color="#2C3E50"))
            for d in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Text(d["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(d["dica"], color="#2C3E50"),
                            ], spacing=8),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        elif cat == "Manuais":
            encontrados = [
                m for m in manuais
                if termo in m["titulo"].lower() or termo in m["conteudo"].lower()
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum manual ou política encontrada.", color="#2C3E50"))
            for m in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Text(m["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(m["conteudo"], color="#2C3E50"),
                            ], spacing=8),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        elif cat == "Artigos Técnicos":
            encontrados = [
                a for a in tecnicos
                if termo in a["titulo"].lower() or termo in a["conteudo"].lower()
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum artigo técnico encontrado.", color="#2C3E50"))
            for a in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Text(a["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(a["conteudo"], color="#2C3E50"),
                            ], spacing=8),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        elif cat == "Materiais Multimídia":
            encontrados = [
                m for m in midias
                if termo in m["titulo"].lower() or termo in m["url"].lower()
            ]
            if not encontrados:
                resultado.controls.append(ft.Text("Nenhum material multimídia encontrado.", color="#2C3E50"))
            for m in encontrados:
                resultado.controls.append(
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Text(m["titulo"], size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(m["url"], color="#2C3E50"),
                            ], spacing=8),
                            padding=16,
                            bgcolor="white",
                            border_radius=8,
                        ),
                        margin=ft.margin.symmetric(vertical=8, horizontal=0),
                        elevation=2
                    )
                )
        resultado.controls.append(
            ft.Container(
                ft.Row([
                    ft.Text("Não encontrou o que procurava?", color="#2C3E50"),
                    ft.ElevatedButton(
                        "Abrir Ticket",
                        icon=ft.Icons.CONTACT_SUPPORT,
                        bgcolor="#2980B9",
                        color="white",
                        on_click=lambda e: page.go("/novo_ticket")
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(top=20)
            )
        )
        page.update()

    categoria_selecionada.on_change = atualizar_lista
    busca.on_change = atualizar_lista

    atualizar_lista()

    def voltar(e):
        if usuario_logado and usuario_logado.get("tipo") == "admin":
            page.go("/inicial")
        else:
            page.go("/user")

    cabecalho = ft.Container(
        ft.Row([
            ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar),
            ft.Text("Base de Conhecimento", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
        ], alignment=ft.MainAxisAlignment.START),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#F4F6F7",
        height=60,
    )

    filtros = ft.Row([categoria_selecionada, busca], spacing=20)

    conteudo = ft.ListView(
        controls=[filtros, resultado],
        spacing=10,
        padding=ft.padding.all(20),
        expand=True
    )

    layout = ft.Column([cabecalho, conteudo], expand=True, spacing=0)

    page.controls.clear()
    page.add(layout)
    page.update()
