import flet as ft

def ConfiguracoesPage(page: ft.Page):
    page.title = "Configurações - Help Desk"
    page.bgcolor = "#F4F6F7"

    def voltar(e):
        page.go("/inicial")

    # canais de suporte
    canal_email = ft.Switch(label="Ativar suporte por E-mail", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    canal_chat = ft.Switch(label="Ativar suporte por Chat", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    canal_form = ft.Switch(label="Ativar suporte por Formulário", value=False, label_style=ft.TextStyle(color="#2C3E50"))
    canal_telefone = ft.Switch(label="Ativar suporte por Telefone", value=False, label_style=ft.TextStyle(color="#2C3E50"))
    email_suporte = ft.TextField(label="E-mail do suporte", value="suporte@empresa.com", width=350, label_style=ft.TextStyle(color="#2C3E50"))

    # usuários e permissões
    permissao_admin = ft.Checkbox(label="Administrador pode criar usuários", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    permissao_agente = ft.Checkbox(label="Agente pode fechar tickets", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    permissao_usuario = ft.Checkbox(label="Usuário pode reabrir ticket fechado", value=False, label_style=ft.TextStyle(color="#2C3E50"))

    # base de conhecimento
    base_publica = ft.Switch(label="Base de conhecimento pública", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    artigo_aprovacao = ft.Checkbox(label="Artigos precisam de aprovação", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    artigo_notificacao = ft.Switch(label="Notificar agentes sobre novos artigos", value=True, label_style=ft.TextStyle(color="#2C3E50"))

    # tickets
    categorias = ft.TextField(label="Categorias (separe por vírgula)", value="Suporte Técnico, Financeiro, Infraestrutura, Outro", width=400, label_style=ft.TextStyle(color="#2C3E50"))
    prioridades = ft.TextField(label="Prioridades (separe por vírgula)", value="Baixa, Média, Alta, Crítica", width=400, label_style=ft.TextStyle(color="#2C3E50"))
    status = ft.TextField(label="Status disponíveis (separe por vírgula)", value="Aberto, Em Espera, Fechado, Atribuído", width=400, label_style=ft.TextStyle(color="#2C3E50"))

    # notificações
    notifica_email = ft.Switch(label="Notificar por e-mail", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    notifica_push = ft.Switch(label="Notificar por push", value=False, label_style=ft.TextStyle(color="#2C3E50"))
    notifica_cliente = ft.Checkbox(label="Enviar notificações também para clientes", value=True, label_style=ft.TextStyle(color="#2C3E50"))
    modelo_email = ft.TextField(label="Assunto padrão do e-mail", value="Atualização do seu chamado", width=350, label_style=ft.TextStyle(color="#2C3E50"))

    def salvar_configuracoes(e):
        page.snack_bar = ft.SnackBar(
            ft.Text("Configurações salvas com sucesso!", color="#2C3E50"),
            bgcolor="#27AE60"
        )
        page.snack_bar.open = True
        page.update()

    cabecalho = ft.Container(
        ft.Row(
            [
                ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar),
                ft.Text("Configurações", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        padding=ft.padding.symmetric(horizontal=20, vertical=10),
        bgcolor="#F4F6F7",
        height=60,
    )

    abas = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Canais de Suporte",
                content=ft.Column([
                    ft.Text("Gerencie e personalize canais de atendimento.", color="#2C3E50"),
                    canal_email,
                    canal_chat,
                    canal_form,
                    canal_telefone,
                    email_suporte,
                ], spacing=10)
            ),
            ft.Tab(
                text="Usuários & Permissões",
                content=ft.Column([
                    ft.Text("Permissões de usuários e agentes.", color="#2C3E50"),
                    permissao_admin,
                    permissao_agente,
                    permissao_usuario,
                ], spacing=10)
            ),
            ft.Tab(
                text="Base de Conhecimento",
                content=ft.Column([
                    ft.Text("Configurações da base de conhecimento.", color="#2C3E50"),
                    base_publica,
                    artigo_aprovacao,
                    artigo_notificacao,
                ], spacing=10)
            ),
            ft.Tab(
                text="Tickets",
                content=ft.Column([
                    ft.Text("Configure categorias, prioridades e status de tickets.", color="#2C3E50"),
                    categorias,
                    prioridades,
                    status,
                ], spacing=10)
            ),
            ft.Tab(
                text="Notificações",
                content=ft.Column([
                    ft.Text("Notificações automáticas para clientes e equipe.", color="#2C3E50"),
                    notifica_email,
                    notifica_push,
                    notifica_cliente,
                    modelo_email,
                ], spacing=10)
            ),
    
        ],
        expand=True
    )

    conteudo = ft.ListView(
        controls=[
            abas,
            ft.ElevatedButton(
                "Salvar Configurações",
                icon=ft.Icons.SAVE,
                bgcolor="#2980B9",
                color="white",
                on_click=salvar_configuracoes,
            ),
        ],
        spacing=20,
        padding=ft.padding.all(20),
        expand=True
    )

    layout = ft.Column(
        [
            cabecalho,
            conteudo,
        ],
        expand=True,
        spacing=0,
    )

    page.controls.clear()
    page.add(layout)
    page.update()
