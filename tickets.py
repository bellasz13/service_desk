import flet as ft
import os
import platform
import subprocess
from datetime import datetime
from database import buscar_todos_tickets, buscar_respostas_ticket, inserir_resposta, atualizar_ticket_status, atualizar_ticket_campos, buscar_anexos_ticket, inserir_anexo, buscar_nome_usuario_por_id

def TicketsPage(page: ft.Page, usuario_logado):
    page.title = "Tickets - Help Desk"
    page.bgcolor = "#F4F6F7"

    categoria_sla = {
        "Novo cadastro": "12 horas",
        "Alterar cadastro": "16 horas",
        "Liberar acesso": "8 horas",
        "Cancelar cadastro/acesso": "4 horas",
        "Alterar senha": "6 horas",
        "Senha bloqueada": "4 horas",
        "Problemas com Office 365": "8 horas",
        "Suporte ao Office 365": "16 horas",
        "Suporte a impressora": "8 horas",
        "Instalar impressora": "16 horas",
        "Falha na impressão": "4 horas",
        "Ativar ponto de rede": "12 horas",
        "Compartilhamento de rede": "12 horas",
        "Bloquear/liberar site": "12 horas",
        "Falha de conexão ou rede": "4 horas",
        "Instalar software": "16 horas",
        "Software não funciona": "8 horas",
        "Instalar/substituir equipamentos": "16 horas",
        "Mudança de local": "16 horas",
        "Manutenção preventiva": "24 horas",
        "Teste de equipamentos": "12 horas",
        "Falha em computador/periférico": "8 horas"
    }

    def get_sla_by_categoria(cat):
        return categoria_sla.get(cat, "24 horas")

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
        label_style=ft.TextStyle(color="#2C3E50")
    )

    def voltar(e):
        page.go("/inicial")

    def novo_ticket(e):
        page.go("/novo_ticket")
    
    def exportar_button(e):
        page.go("/exportacao")

    def abrir_ticket(ticket):
        render_detalhe_ticket(ticket)

    def render_detalhe_ticket(ticket):
        anexo_resposta_info = ft.Text("", size=14, color="#2C3E50", visible=False)
        anexo_resposta_remover_btn = ft.IconButton(
            icon=ft.Icons.CLOSE, icon_color="#7F8C8D", visible=False
        )
        anexo_resposta_arquivo = {"file": None, "file_path": None}

        def on_file_picker_result_resposta(e: ft.FilePickerResultEvent):
            if e.files:
                f = e.files[0]
                uploads_dir = "uploads"
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                caminho_arquivo = os.path.join(uploads_dir, f.name)
                with open(f.path, "rb") as source:
                    with open(caminho_arquivo, "wb") as dest:
                        dest.write(source.read())
                anexo_resposta_arquivo["file"] = f
                anexo_resposta_arquivo["file_path"] = caminho_arquivo
                anexo_resposta_info.value = f"{f.name} ({round(f.size/1024)}K)"
                anexo_resposta_info.visible = True
                anexo_resposta_remover_btn.visible = True
                anexo_resposta_info.update()
                anexo_resposta_remover_btn.update()
            else:
                remover_anexo_resposta(None)

        def remover_anexo_resposta(e):
            anexo_resposta_arquivo["file"] = None
            anexo_resposta_arquivo["file_path"] = None
            anexo_resposta_info.value = ""
            anexo_resposta_info.visible = False
            anexo_resposta_remover_btn.visible = False
            anexo_resposta_info.update()
            anexo_resposta_remover_btn.update()

        anexo_resposta_remover_btn.on_click = remover_anexo_resposta

        anexo_resposta = ft.FilePicker(on_result=on_file_picker_result_resposta)
        if anexo_resposta not in page.overlay:
            page.overlay.append(anexo_resposta)

        anexo_resposta_button = ft.ElevatedButton(
            "Anexar Arquivo à Resposta",
            icon=ft.Icons.ATTACH_FILE,
            on_click=lambda e: anexo_resposta.pick_files(allow_multiple=False)
        )

        def voltar_lista(e):
            render_lista_tickets()

        def fechar_ticket(e):
            atualizar_ticket_status(ticket["id_ticket"], "Fechado")
            page.snack_bar = ft.SnackBar(
                ft.Text("Ticket fechado com sucesso!", color="#2C3E50"),
                bgcolor="#27AE60"
            )
            page.snack_bar.open = True
            render_detalhe_ticket({**ticket, "status": "Fechado"})

        def em_espera_ticket(e):
            atualizar_ticket_status(ticket["id_ticket"], "Em Espera")
            page.snack_bar = ft.SnackBar(
                ft.Text("Ticket colocado em espera!", color="#2C3E50"),
                bgcolor="#F39C12"
            )
            page.snack_bar.open = True
            render_detalhe_ticket({**ticket, "status": "Em Espera"})

        resposta_field = ft.TextField(
            label="Adicionar resposta",
            multiline=True,
            min_lines=2,
            max_lines=5,
            width=500,
            label_style=ft.TextStyle(color="#2C3E50")
        )

        prioridade_field = ft.Dropdown(
            label="Prioridade",
            width=180,
            options=[
                ft.dropdown.Option("Baixa"),
                ft.dropdown.Option("Média"),
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Crítica"),
            ],
            value=ticket["prioridade"],
            color="black",
            label_style=ft.TextStyle(color="#2C3E50")
        )

        categoria_field = ft.Dropdown(
            label="Categoria",
            width=220,
            options=[ft.dropdown.Option(cat) for cat in categoria_sla.keys()],
            value=ticket["categoria"] if ticket["categoria"] in categoria_sla else "Novo cadastro",
            color="black",
            label_style=ft.TextStyle(color="#2C3E50")
        )

        urgencia_field = ft.Dropdown(
            label="Urgência",
            width=180,
            options=[
                ft.dropdown.Option("Baixa"),
                ft.dropdown.Option("Normal"),
                ft.dropdown.Option("Alta"),
                ft.dropdown.Option("Imediata"),
            ],
            value=ticket["urgencia"],
            color="black",
            label_style=ft.TextStyle(color="#2C3E50")
        )

        sla_field = ft.TextField(
            label="SLA",
            width=180,
            color="black",
            label_style=ft.TextStyle(color="#2C3E50"),
            value=get_sla_by_categoria(categoria_field.value),
            read_only=True
        )

        def categoria_change(e):
            sla_field.value = get_sla_by_categoria(categoria_field.value)
            page.update()

        categoria_field.on_change = categoria_change

        def salvar_alteracoes(e):
            atualizar_ticket_campos(
                ticket["id_ticket"],
                prioridade_field.value,
                categoria_field.value,
                urgencia_field.value,
                sla_field.value
            )
            page.snack_bar = ft.SnackBar(
                ft.Text("Alterações salvas!", color="#2C3E50"),
                bgcolor="#27AE60"
            )
            page.snack_bar.open = True
            render_detalhe_ticket({
                **ticket,
                "prioridade": prioridade_field.value,
                "categoria": categoria_field.value,
                "urgencia": urgencia_field.value,
                "sla": sla_field.value
            })

        def adicionar_resposta(e):
            texto = resposta_field.value.strip()
            if texto or anexo_resposta_arquivo["file"]:
                data_resposta = datetime.now().strftime("%Y-%m-%d")
                hora_resposta = datetime.now().strftime("%H:%M:%S")
                inserir_resposta(
                    ticket["id_ticket"],
                    usuario_logado["id_usuario"],
                    texto,
                    data_resposta,
                    hora_resposta
                )
                if anexo_resposta_arquivo["file"]:
                    file_obj = anexo_resposta_arquivo["file"]
                    nome_arquivo = file_obj.name
                    caminho_arquivo = anexo_resposta_arquivo["file_path"]
                    data_upload = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    inserir_anexo(
                        ticket["id_ticket"],
                        nome_arquivo,
                        caminho_arquivo,
                        data_upload
                    )
                resposta_field.value = ""
                remover_anexo_resposta(None)
                page.snack_bar = ft.SnackBar(
                    ft.Text("Resposta adicionada!", color="#2C3E50"),
                    bgcolor="#2980B9"
                )
                page.snack_bar.open = True
                render_detalhe_ticket(ticket)   
                
        def baixar_arquivo(path):
            abs_path = os.path.abspath(path)
            if os.path.isfile(abs_path):
                if platform.system() == "Windows":
                    os.startfile(abs_path)
                elif platform.system() == "Darwin":  #mac
                    subprocess.run(["open", abs_path])
                else:  #linux
                    subprocess.run(["xdg-open", abs_path])
            else:
                print(f"Arquivo não encontrado: {abs_path}")
        
        anexos = buscar_anexos_ticket(ticket["id_ticket"])
        if anexos:
            anexos_controles = []
            for anexo in anexos:
                nome_arquivo = anexo["nome_arquivo"]
                caminho_arquivo = anexo["caminho_arquivo"]
                anexos_controles.append(
                    ft.Row([
                        ft.Text(f"Anexo: {nome_arquivo}", color="#2C3E50"),
                        ft.IconButton(
                            icon=ft.Icons.DOWNLOAD,
                            tooltip="Download",
                            on_click=lambda e, path=caminho_arquivo: baixar_arquivo(path)
                        )
                    ], spacing=10)
                )
            anexos_widget = ft.Column(anexos_controles, spacing=5)
        else:
            anexos_widget = ft.Text("Nenhum anexo.", color="#7F8C8D")
        
        cor_status = {"Aberto": "#27AE60", "Fechado": "#AAB7B8", "Em Espera": "#F39C12"}.get(ticket["status"], "#7F8C8D")
        cor_prioridade = "#2980B9" if ticket["prioridade"] == "Alta" else "#27AE60" if ticket["prioridade"] == "Média" else "#F39C12"

        respostas = buscar_respostas_ticket(ticket["id_ticket"])
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

        botoes = [
            anexo_resposta_button,
            ft.ElevatedButton(
                "Adicionar Resposta",
                icon=ft.Icons.SEND,
                bgcolor="#2980B9",
                color="white",
                on_click=adicionar_resposta,
                disabled=ticket["status"] == "Fechado"
            ),
            ft.ElevatedButton(
                "Salvar Alterações",
                icon=ft.Icons.SAVE,
                bgcolor="#27AE60",
                color="white",
                on_click=salvar_alteracoes
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
        
        nome_criador = buscar_nome_usuario_por_id(ticket["id_usuario_criador"])
        
        page.add(
            ft.Container(
                ft.ListView([
                    ft.Row([
                        ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color="#7F8C8D", on_click=voltar_lista),
                        ft.Text(f"Ticket #{ticket['id_ticket']}", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Divider(),
                    ft.Text(f"Criado por: {nome_criador}", color="#2C3E50", size=14),
                    ft.Divider(),
                    ft.Text(ticket["titulo"], size=20, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(ticket["descricao"], color="#2C3E50"), 
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
                        ft.Text(ticket["data_criacao"], size=12, color="#7F8C8D"),
                    ], alignment=ft.MainAxisAlignment.START, spacing=10),
                    ft.Divider(),
                    ft.Row([
                        prioridade_field,
                        categoria_field,
                        urgencia_field,
                        sla_field
                    ], spacing=10),
                    ft.Divider(),
                    ft.Text("Anexos:", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    anexos_widget,
                    ft.Divider(),
                    ft.Text("Respostas:", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    respostas_list if respostas else ft.Text("Nenhuma resposta ainda.", color="#2C3E50"),
                    ft.Divider(),
                    ft.Row([anexo_resposta_info, anexo_resposta_remover_btn], spacing=5),
                    resposta_field if ticket["status"] != "Fechado" else ft.Text("Ticket fechado. Não é possível responder.", color="#AAB7B8"),
                    ft.Row(botoes, spacing=20)
                ], spacing=18, expand=True),
                padding=30,
                bgcolor="white",
                border_radius=12,
                margin=ft.margin.all(30),
                width=900,
                height=600,
                alignment=ft.alignment.top_center
            )
        )
        page.update()

    def render_lista_tickets():
        tickets = buscar_todos_tickets()
        lista_tickets = ft.Column(spacing=0, expand=True)
        status = filtro_status.value
        termo = busca.value.lower() if busca.value else ""
        filtrados = [
            t for t in tickets
            if (status == "Todos" or t["status"] == status)
            and (termo in t["titulo"].lower() or termo in str(t["id_ticket"]))
        ]
        
        for t in filtrados:
            cor_status = {"Aberto": "#27AE60", "Fechado": "#AAB7B8", "Em Espera": "#F39C12"}.get(t["status"], "#7F8C8D")
            nome_criador = buscar_nome_usuario_por_id(t["id_usuario_criador"])
            lista_tickets.controls.append(
                ft.GestureDetector(
                    on_tap=lambda e, ticket=t: abrir_ticket(ticket),
                    content=ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Row([
                                    ft.Text(f"#{t['id_ticket']}", size=14, color="#7F8C8D"),
                                    ft.Text(f"Criado por: {nome_criador}", color="#2C3E50", size=14),
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
                                    ft.Text(t["data_criacao"], size=12, color="#7F8C8D"),
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
                        "Todos os Tickets",
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
                    ft.ElevatedButton(
                        text="Exportar incidente",
                        icon=ft.Icons.DOWNLOAD,
                        bgcolor="#2980B9",
                        color="white",
                        on_click=exportar_button,
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
