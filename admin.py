import flet as ft

def AdminPage(page: ft.Page):
    page.title = "Administração - Help Desk"
    page.bgcolor = "#F4F6F7"

    usuarios = [
        {"nome": "Ana Souza", "email": "ana@empresa.com", "tipo": "Administrador"},
        {"nome": "Carlos Lima", "email": "carlos@empresa.com", "tipo": "Usuário"},
        {"nome": "Maria Silva", "email": "maria@empresa.com", "tipo": "Usuário"},
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

    def atualizar_lista_usuarios():
        lista.controls.clear()
        for u in usuarios:
            lista.controls.append(
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
        page.update()

    lista = ft.Column(spacing=0, expand=True)
    atualizar_lista_usuarios()

    usuarios_tab = ft.Column(
        [
            ft.Text("Usuários Cadastrados", size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
            lista
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
        expand=True
    )

    nome = ft.TextField(label="Nome", width=400)
    email = ft.TextField(label="E-mail", width=400)
    tipo = ft.Dropdown(
        label="Tipo de Usuário",
        width=200,
        options=[
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Usuário"),
        ],
        value="Usuário"
    )
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=200)

    def criar_usuario(e):
        if not nome.value or not email.value or not senha.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Preencha todos os campos!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return
        usuarios.append({
            "nome": nome.value,
            "email": email.value,
            "tipo": tipo.value,
        })
        nome.value = ""
        email.value = ""
        senha.value = ""
        page.snack_bar = ft.SnackBar(
            ft.Text("Usuário criado com sucesso!"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        atualizar_lista_usuarios()
        page.update()

    novo_usuario_tab = ft.Column(
        [
            ft.Text("Novo Usuário", size=18, weight=ft.FontWeight.BOLD, color="#2C3E50"),
            nome,
            email,
            ft.Row([tipo, senha], spacing=20),
            ft.ElevatedButton("Criar Usuário", icon=ft.Icons.PERSON_ADD, bgcolor="#2980B9", color="white", on_click=criar_usuario),
        ],
        alignment=ft.MainAxisAlignment.START,
        spacing=20,
        expand=True
    )

    tabs = ft.Tabs(
        ref=tabs_ref,  # ref p manipular depois 
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
