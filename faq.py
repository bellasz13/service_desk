import flet as ft

def FAQPage(page: ft.Page):
    page.title = "FAQ - Perguntas Frequentes"
    page.bgcolor = "#F4F6F7"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    def voltar(e):
        page.go("/inicial")

    faqs = [
        {
            "pergunta": "Como abro um novo chamado?",
            "resposta": "Clique em 'Novo Ticket' no menu lateral ou na tela inicial, preencha os campos obrigatórios e clique em 'Enviar'."
        },
        {
            "pergunta": "Como acompanho o status do meu chamado?",
            "resposta": "Acesse a área de 'Tickets' no menu lateral para visualizar todos os seus chamados e seus respectivos status."
        },
        {
            "pergunta": "Posso anexar arquivos ao meu chamado?",
            "resposta": "Sim, ao abrir um novo ticket, utilize o botão 'Anexar Arquivo' para enviar documentos ou imagens relacionados ao seu chamado."
        },
        {
            "pergunta": "Como altero meus dados de perfil?",
            "resposta": "Clique em 'Perfil' no menu lateral e depois em 'Editar' para atualizar suas informações pessoais."
        },
        {
            "pergunta": "O que faço se esqueci minha senha?",
            "resposta": "Clique em 'Esqueci minha senha' na tela de login e siga as instruções para redefinir sua senha."
        },
    ]

    faq_controls = [
        ft.ExpansionTile(
            title=ft.Text(faq["pergunta"], weight=ft.FontWeight.BOLD, color="#2C3E50"),
            subtitle=None,
            controls=[ft.Text(faq["resposta"], color="#2C3E50")]
        )
        for faq in faqs
    ]

    page.controls.clear()
    page.add(
        ft.Container(
            ft.Column(
                [
                    ft.Text("Perguntas Frequentes (FAQ)", size=24, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Column(faq_controls, spacing=10),
                    ft.ElevatedButton("Voltar", icon=ft.Icons.ARROW_BACK, on_click=voltar)
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                width=600
            ),
            alignment=ft.alignment.center,
            padding=40,
            bgcolor="white",
            border_radius=12,
            shadow=ft.BoxShadow(blur_radius=12, color="#bbb", offset=ft.Offset(0, 2))
        )
    )
    page.update()
