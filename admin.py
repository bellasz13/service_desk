import flet as ft

def AdminPage(page: ft.Page):
    page.title = "Administração - Help Desk"
    page.bgcolor = "#F4F6F7"

    usuarios = [
        {"nome": "Ana Souza", "usuario": "ana.souza", "email": "ana@empresa.com", "tipo": "Administrador", "senha": "123456"},
        {"nome": "Carlos Lima", "usuario": "carlos.lima", "email": "carlos@empresa.com", "tipo": "Usuário", "senha": "abc123"},
        {"nome": "Maria Silva", "usuario": "maria.silva", "email": "maria@empresa.com", "tipo": "Usuário", "senha": "senha321"},
    ]

    tabs_ref = ft.Ref[ft.Tabs]()

    def voltar(e):
        page.go("/inicial")

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
                    "Administração",
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

    def render_usuario_detalhe(usuario):
        nome_field = ft.TextField(label="Nome", value=usuario["nome"], width=400, label_style=ft.TextStyle(color="#2C3E50"))
        usuario_field = ft.TextField(label="Nome de Usuário", value=usuario["usuario"], width=300, label_style=ft.TextStyle(color="#2C3E50"))
        email_field = ft.TextField(label="E-mail", value=usuario["email"], width=400, label_style=ft.TextStyle(color="#2C3E50"))
        tipo_field = ft.Dropdown(
            label="Tipo de Usuário",
            width=200,
            options=[
                ft.dropdown.Option("Administrador"),
                ft.dropdown.Option("Usuário"),
            ],
            value=usuario["tipo"],
            label_style=ft.TextStyle(color="#2C3E50")
        )
        senha_field = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, width=300, label_style=ft.TextStyle(color="#2C3E50"))

        def voltar_lista(e):
            render_lista_usuarios()

        def salvar_alteracoes(e):
            # Atualiza os dados do usuário
            usuario["nome"] = nome_field.value
            usuario["usuario"] = usuario_field.value
            usuario["email"] = email_field.value
            usuario["tipo"] = tipo_field.value
            if senha_field.value:
                usuario["senha"] = senha_field.value
                senha_field.value = ""
            page.snack_bar = ft.SnackBar(
                ft.Text("Dados alterados com sucesso!", color="#2C3E50"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            page.update()

        page.controls.clear()
        page.add(
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar_lista),
                        ft.Text(f"Usuário: {usuario['nome']}", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    nome_field,
                    usuario_field,
                    email_field,
                    tipo_field,
                    senha_field,
                    ft.ElevatedButton("Salvar Alterações", icon=ft.Icons.SAVE, bgcolor="#2980B9", color="white", on_click=salvar_alteracoes),
                ], spacing=18),
                padding=30,
                bgcolor="white",
                border_radius=12,
                margin=ft.margin.all(30),
                width=500,
                alignment=ft.alignment.top_center
            )
        )
        page.update()

    def render_lista_usuarios():
        lista = ft.Column(spacing=0, expand=True)
        for u in usuarios:
            lista.controls.append(
                ft.GestureDetector(
                    on_tap=lambda e, usuario=u: render_usuario_detalhe(usuario),
                    content=ft.Card(
                        ft.Container(
                            ft.Row([
                                ft.Text(u["nome"], size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(u["usuario"], size=14, color="#27AE60"),
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
            )
        usuarios_tab = ft.Column(
            [
                ft.Text("Usuários Cadastrados", size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                lista
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            expand=True
        )

        # Novo usuário tab
        nome = ft.TextField(label="Nome", width=400, label_style=ft.TextStyle(color="#2C3E50"))
        usuario_nome = ft.TextField(label="Nome de Usuário", width=300, label_style=ft.TextStyle(color="#2C3E50"))
        email = ft.TextField(label="E-mail", width=400, label_style=ft.TextStyle(color="#2C3E50"))
        tipo = ft.Dropdown(
            label="Tipo de Usuário",
            width=200,
            options=[
                ft.dropdown.Option("Administrador"),
                ft.dropdown.Option("Usuário"),
            ],
            value="Usuário",
            label_style=ft.TextStyle(color="#2C3E50")
        )
        senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=200, label_style=ft.TextStyle(color="#2C3E50"))

        def criar_usuario(e):
            if not nome.value or not usuario_nome.value or not email.value or not senha.value:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Preencha todos os campos!", color="#2C3E50"),
                    bgcolor="red"
                )
                page.snack_bar.open = True
                page.update()
                return
            usuarios.append({
                "nome": nome.value,
                "usuario": usuario_nome.value,
                "email": email.value,
                "tipo": tipo.value,
                "senha": senha.value
            })
            nome.value = ""
            usuario_nome.value = ""
            email.value = ""
            senha.value = ""
            page.snack_bar = ft.SnackBar(
                ft.Text("Usuário criado com sucesso!", color="#2C3E50"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            render_lista_usuarios()
            page.update()

        novo_usuario_tab = ft.Column(
            [
                ft.Text("Novo Usuário", size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                nome,
                usuario_nome,
                email,
                ft.Row([tipo, senha], spacing=20),
                ft.ElevatedButton("Criar Usuário", icon=ft.Icons.PERSON_ADD, bgcolor="#2980B9", color="white", on_click=criar_usuario),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=20,
            expand=True
        )

        tabs = ft.Tabs(
            ref=tabs_ref,
            selected_index=0,
            on_change=lambda e: page.update(),
            tabs=[
                ft.Tab(text="Usuários", content=usuarios_tab),
                ft.Tab(text="Novo Usuário", content=novo_usuario_tab),
            ],
            expand=True,
        )

        conteudo = ft.ListView(
            controls=[
                tabs,
            ],
            spacing=20,
            padding=ft.padding.all(20),
            expand=True,
        )

        layout_completo = ft.Column(
            [
                cabecalho,
                conteudo,
            ],
            spacing=0,
            expand=True,
        )

        page.controls.clear()
        page.add(layout_completo)
        page.update()

    render_lista_usuarios()
