import flet as ft
from database import buscar_usuarios, inserir_usuario, atualizar_usuario, excluir_usuario

def AdminPage(page: ft.Page):
    page.title = "Administração - Help Desk"
    page.bgcolor = "#F4F6F7"

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
        nome_field = ft.TextField(label="Nome", value=usuario["nome_completo"], width=400, label_style=ft.TextStyle(color="#2C3E50"))
        usuario_field = ft.TextField(label="Nome de Usuário", value=usuario["nome_usuario"], width=300, label_style=ft.TextStyle(color="#2C3E50"))
        email_field = ft.TextField(label="E-mail", value=usuario["email"], width=400, label_style=ft.TextStyle(color="#2C3E50"))
        tipo_field = ft.Dropdown(
            label="Tipo de Usuário",
            width=200,
            options=[
                ft.dropdown.Option("administrador"),
                ft.dropdown.Option("comum"),
            ],
            value=usuario["tipo_usuario"],
            label_style=ft.TextStyle(color="#2C3E50")
        )
        senha_field = ft.TextField(label="Nova Senha", password=True, can_reveal_password=True, width=300, label_style=ft.TextStyle(color="#2C3E50"))

        def voltar_lista(e):
            render_lista_usuarios()

        def salvar_alteracoes(e):
            atualizar_usuario(
                usuario["id_usuario"],
                nome_field.value,
                usuario_field.value,
                email_field.value,
                tipo_field.value,
                senha_field.value if senha_field.value else None
            )
            senha_field.value = ""
            page.snack_bar = ft.SnackBar(
                ft.Text("Dados alterados com sucesso!", color="#2C3E50"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            render_usuario_detalhe({
                "id_usuario": usuario["id_usuario"],
                "nome_completo": nome_field.value,
                "nome_usuario": usuario_field.value,
                "email": email_field.value,
                "tipo_usuario": tipo_field.value
            })

        def excluir_usuario_click(e):
            excluir_usuario(usuario["id_usuario"])
            page.snack_bar = ft.SnackBar(
                ft.Text("Usuário excluído!", color="#2C3E50"),
                bgcolor="#E74C3C"
            )
            page.snack_bar.open = True
            render_lista_usuarios()

        page.controls.clear()
        page.add(
            ft.Container(
                ft.Column([
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar_lista),
                        ft.Text(f"Usuário: {usuario['nome_completo']}", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    nome_field,
                    usuario_field,
                    email_field,
                    tipo_field,
                    senha_field,
                    ft.Row([
                        ft.ElevatedButton("Salvar Alterações", icon=ft.Icons.SAVE, bgcolor="#2980B9", color="white", on_click=salvar_alteracoes),
                        ft.ElevatedButton(
                            "Excluir usuário",
                            icon=ft.Icons.DELETE,
                            bgcolor="#E74C3C",
                            color="white",
                            on_click=excluir_usuario_click
                        ),
                    ], spacing=20),
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

    def render_lista_usuarios():
        usuarios = buscar_usuarios()
        lista = ft.Column(spacing=0, expand=True)
        for u in usuarios:
            lista.controls.append(
                ft.GestureDetector(
                    on_tap=lambda e, usuario=u: render_usuario_detalhe(usuario),
                    content=ft.Card(
                        ft.Container(
                            ft.Row([
                                ft.Text(u["nome_completo"], size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                                ft.Text(u["nome_usuario"], size=14, color="#27AE60"),
                                ft.Text(u["email"], size=14, color="#7F8C8D"),
                                ft.Container(
                                    ft.Text(u["tipo_usuario"], color="white", size=12),
                                    bgcolor="#2980B9" if u["tipo_usuario"] == "administrador" else "#27AE60",
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

        nome = ft.TextField(label="Nome", width=400, label_style=ft.TextStyle(color="#2C3E50"))
        usuario_nome = ft.TextField(label="Nome de Usuário", width=300, label_style=ft.TextStyle(color="#2C3E50"))
        email = ft.TextField(label="E-mail", width=400, label_style=ft.TextStyle(color="#2C3E50"))
        tipo = ft.Dropdown(
            label="Tipo de Usuário",
            width=200,
            options=[
                ft.dropdown.Option("administrador"),
                ft.dropdown.Option("comum"),
            ],
            value="comum",
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
            inserir_usuario(nome.value, usuario_nome.value, email.value, tipo.value, senha.value)
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
