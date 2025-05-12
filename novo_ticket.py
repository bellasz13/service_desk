import flet as ft

def NovoTicketPage(page: ft.Page):
    page.title = "Novo Ticket - Help Desk"
    page.bgcolor = "#F4F6F7"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    titulo = ft.TextField(label="Título do Chamado", width=400)
    descricao = ft.TextField(label="Descrição detalhada", multiline=True, min_lines=4, max_lines=8, width=400)
    prioridade = ft.Dropdown(
        label="Prioridade",
        width=200,
        options=[
            ft.dropdown.Option("Baixa"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Alta"),
            ft.dropdown.Option("Crítica"),
        ],
        value="Média"
    )
    categoria = ft.Dropdown(
        label="Categoria",
        width=200,
        options=[
            ft.dropdown.Option("Suporte Técnico"),
            ft.dropdown.Option("Financeiro"),
            ft.dropdown.Option("Infraestrutura"),
            ft.dropdown.Option("Outro"),
        ],
        value="Suporte Técnico"
    )
    anexo = ft.FilePicker()
    anexo_button = ft.ElevatedButton(
        "Anexar Arquivo",
        icon=ft.Icons.ATTACH_FILE,
        on_click=lambda e: anexo.pick_files(allow_multiple=False)
    )

    def voltar(e):
        page.go("/inicial")

    def enviar_ticket(e):
        if not titulo.value or not descricao.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Preencha o título e a descrição do chamado!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        #  salvar o ticket no banco de dados ou API
        page.snack_bar = ft.SnackBar(
            ft.Text("Ticket criado com sucesso!"),
            bgcolor="green"
        )
        page.snack_bar.open = True
        page.update()

    form = ft.Column(
        [
            ft.Text("Novo Ticket de Chamado", size=24, weight=ft.FontWeight.BOLD, color="#2C3E50"),
            titulo,
            descricao,
            ft.Row([prioridade, categoria], spacing=20),
            ft.Row([anexo_button, anexo], spacing=10),
            ft.Row([
                ft.ElevatedButton("Enviar", icon=ft.Icons.SEND, bgcolor="#2980B9", color="white", on_click=enviar_ticket),
                ft.OutlinedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=voltar)
            ], spacing=20),
        ],
        width=500,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20
    )

    page.controls.clear()
    page.add(
        ft.Container(
            form,
            alignment=ft.alignment.center,
            padding=40,
            bgcolor="white",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=12, color="#bbb", offset=ft.Offset(0, 2))
        )
    )
    page.update()
