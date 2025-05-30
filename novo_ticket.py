import flet as ft
from datetime import datetime
import os
from database import inserir_ticket, inserir_anexo

def NovoTicketPage(page: ft.Page, usuario_logado):
    page.title = "Novo Ticket - Help Desk"
    page.bgcolor = "#F4F6F7"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START

    label_style = ft.TextStyle(color="black")
    hint_style = ft.TextStyle(color="black")

    categoria_sla = {
        "Novo cadastro": "12 horas",
        "Alterar cadastro": "16 horas",
        "Liberar acesso": "8 horas",
        "Cancelar cadastro/acesso": "4 horas",
        "Alterar senha": "6 horas",
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
        "Falha em computador/periférico": "8 horas",
        "Outro": "24h"
    }
    
    anexo_info = ft.Text("", size=14, color="#2C3E50", visible=False)
    anexo_remover_btn = ft.IconButton(
        icon=ft.Icons.CLOSE, icon_color="#7F8C8D", visible=False
    )

    anexo_arquivo = {"file": None}

    def on_file_picker_result(e: ft.FilePickerResultEvent):
        if e.files:
            f = e.files[0]
            uploads_dir = "uploads"
            if not os.path.exists(uploads_dir):
                os.makedirs(uploads_dir)
            caminho_arquivo = os.path.join(uploads_dir, f.name)
            with open(f.path, "rb") as source:
                with open(caminho_arquivo, "wb") as dest:
                    dest.write(source.read()) 
                
            anexo_arquivo["file"] = f
            anexo_arquivo["file_path"] = caminho_arquivo
            anexo_info.value = f"{f.name} ({round(f.size/1024)}K)"
            anexo_info.visible = True
            anexo_remover_btn.visible = True
            anexo_info.update()
            anexo_remover_btn.update()
        else:
            remover_anexo(None)

    anexo = ft.FilePicker(on_result=on_file_picker_result)
    if anexo not in page.overlay:
        page.overlay.append(anexo)

    def remover_anexo(e):
        anexo_arquivo["file"] = None
        anexo_info.value = ""
        anexo_info.visible = False
        anexo_remover_btn.visible = False
        anexo_info.update()
        anexo_remover_btn.update()

    anexo_remover_btn.on_click = remover_anexo

    anexo_button = ft.ElevatedButton(
        "Anexar Arquivo",
        icon=ft.Icons.ATTACH_FILE,
        on_click=lambda e: anexo.pick_files(allow_multiple=False)
    )

    def get_sla_by_categoria(cat):
        return categoria_sla.get(cat, "24 horas")  

    titulo = ft.TextField(
        label="Título do Chamado",
        width=400,
        color="black",
        label_style=label_style,
        hint_style=hint_style
    )
    descricao = ft.TextField(
        label="Descrição detalhada",
        multiline=True,
        min_lines=4,
        max_lines=8,
        width=400,
        color="black",
        label_style=label_style,
        hint_style=hint_style
    )
    prioridade = ft.Dropdown(
        label="Prioridade",
        width=200,
        options=[
            ft.dropdown.Option("Baixa"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Alta"),
            ft.dropdown.Option("Crítica"),
        ],
        value="Média",
        color="black",
        label_style=label_style
    )

    categoria = ft.Dropdown(
        label="Categoria",
        width=200,
        options=[ft.dropdown.Option(cat) for cat in categoria_sla.keys()],
        value="Novo cadastro",
        color="black",
        label_style=label_style
    )

    urgencia = ft.Dropdown(
        label="Urgência",
        width=200,
        options=[
            ft.dropdown.Option("Baixa"),
            ft.dropdown.Option("Normal"),
            ft.dropdown.Option("Alta"),
            ft.dropdown.Option("Imediata"),
        ],
        value="Normal",
        color="black",
        label_style=label_style
    )

    sla = ft.TextField(
        label="SLA",
        width=200,
        color="black",
        label_style=label_style,
        value=get_sla_by_categoria(categoria.value),
        read_only=True
    )

    def categoria_change(e):
        sla.value = get_sla_by_categoria(categoria.value)
        page.update()

    categoria.on_change = categoria_change

    def voltar(e):
        if usuario_logado and usuario_logado.get("tipo") == "administrador":
            page.go("/inicial")
        else:
            page.go("/user")

    def enviar_ticket(e):
        if not titulo.value or not descricao.value:
            page.snack_bar = ft.SnackBar(
                ft.Text("Preencha o título e a descrição do chamado!"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()
            return

        data_atual = datetime.now()
        data_criacao = data_atual.strftime("%Y-%m-%d")
        hora_criacao = data_atual.strftime("%H:%M:%S")
        status = "Aberto"
        sla_valor = sla.value

        try:
            id_ticket = inserir_ticket(
                titulo.value,
                descricao.value,
                data_criacao,
                hora_criacao,
                status,
                prioridade.value,
                urgencia.value,
                categoria.value,
                sla_valor,
                usuario_logado["id_usuario"]
            )

            if anexo_arquivo.get("file"):
                file_obj = anexo_arquivo["file"]
                nome_arquivo = file_obj.name
                caminho_arquivo = f"uploads/{nome_arquivo}"
                data_upload = data_atual.strftime("%Y-%m-%d %H:%M:%S")
                inserir_anexo(
                    id_ticket,
                    nome_arquivo,
                    caminho_arquivo,
                    data_upload
                )

            page.snack_bar = ft.SnackBar(
                ft.Text("Ticket criado com sucesso!"),
                bgcolor="green"
            )
            page.snack_bar.open = True
            
            titulo.value = ""
            descricao.value = ""
            prioridade.value = "Média"
            categoria.value = "Novo cadastro"
            urgencia.value = "Normal"
            sla.value = get_sla_by_categoria("Novo cadastro")
            remover_anexo(None)
            page.update()
        except Exception as err:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro ao criar ticket: {err}"),
                bgcolor="red"
            )
            page.snack_bar.open = True
            page.update()

    form = ft.Column(
        [
            ft.Text("Novo Ticket de Chamado", size=24, weight=ft.FontWeight.BOLD, color="#2C3E50"),
            titulo,
            descricao,
            ft.Row([prioridade, categoria], spacing=20),
            ft.Row([urgencia, sla], spacing=20),  
            ft.Row([anexo_button], spacing=10),
            ft.Row([anexo_info, anexo_remover_btn], spacing=5), 
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
