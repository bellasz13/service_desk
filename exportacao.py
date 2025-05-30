import flet as ft
import xml.etree.ElementTree as ET
from datetime import datetime
from database import buscar_tickets_filtrados

CATEGORIAS_SLA = {
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

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def ExportacaoPage(page: ft.Page):
    page.title = "Exportar Incidentes"
    page.bgcolor = "#F4F6F7"
    
    def voltar(e):
        page.go("/inicial")

    status_field = ft.Dropdown(
        label="Status",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Aberto"),
            ft.dropdown.Option("Fechado"),
            ft.dropdown.Option("Em Espera")
        ],
        value="Todos"
    )
    categoria_field = ft.Dropdown(
        label="Categoria",
        options=[ft.dropdown.Option("Todas")] + [ft.dropdown.Option(cat) for cat in CATEGORIAS_SLA.keys()],
        value="Todas"
    )
    prioridade_field = ft.Dropdown(
        label="Prioridade",
        options=[
            ft.dropdown.Option("Todas"),
            ft.dropdown.Option("Baixa"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Alta"),
            ft.dropdown.Option("Crítica")
        ],
        value="Todas"
    )
    data_inicio_field = ft.TextField(label="Data Inicial (YYYY-MM-DD)", width=160)
    data_fim_field = ft.TextField(label="Data Final (YYYY-MM-DD)", width=160)

    campos = [
        ("id", "ID"),
        ("titulo", "Título"),
        ("descricao", "Descrição"),   
        ("criador", "Criado por"),
        ("status", "Status"),
        ("prioridade", "Prioridade"),
        ("categoria", "Categoria"),
        ("urgencia", "Urgência"),
        ("sla", "SLA"),
        ("data", "Data"),
        ("respostas", "Respostas")
    ]
    campos_checkboxes = [
        ft.Checkbox(label=label, value=True) for key, label in campos
    ]

    def filtrar_tickets():
        return buscar_tickets_filtrados(
            status=status_field.value,
            categoria=categoria_field.value,
            prioridade=prioridade_field.value,
            data_inicio=data_inicio_field.value,
            data_fim=data_fim_field.value
        )

    def gerar_xml(incidentes, campos_selecionados):
        root = ET.Element("incidentes")
        for t in incidentes:
            incidente = ET.SubElement(root, "incidente")
            for idx, (key, _) in enumerate(campos):
                if campos_selecionados[idx].value:
                    if key == "respostas":
                        respostas = ET.SubElement(incidente, "respostas")
                        for resp in t.get("respostas", []):
                            resposta = ET.SubElement(respostas, "resposta")
                            for k, v in resp.items():
                                ET.SubElement(resposta, k).text = str(v)
                    else:
                        ET.SubElement(incidente, key).text = str(t.get(key, ""))
        indent(root) 
        return ET.tostring(root, encoding="utf-8", xml_declaration=True)

    def exportar(e):
        incidentes_filtrados = filtrar_tickets()
        xml_bytes = gerar_xml(incidentes_filtrados, campos_checkboxes)
        nome_arquivo = f"incidentes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xml"

        with open(nome_arquivo, "wb") as f:
            f.write(xml_bytes)
        page.launch_url(f"/download/{nome_arquivo}") 

        page.snack_bar = ft.SnackBar(ft.Text("Exportação concluída!", color="#2C3E50"), bgcolor="#27AE60")
        page.snack_bar.open = True
        page.update()

    page.controls.clear()
    page.controls.clear()
    page.add(
        ft.Container(
            ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color="#7F8C8D",
                        on_click=voltar
                    ),
                    ft.Text("Exportar Incidentes", size=24, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Divider(),
                ft.Text("Filtros:", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([status_field, categoria_field, prioridade_field], spacing=20),
                ft.Row([data_inicio_field, data_fim_field], spacing=20),
                ft.Divider(),
                ft.Text("Campos a Exportar:", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(campos_checkboxes, spacing=10),
                ft.Divider(),
                ft.ElevatedButton("Exportar para XML", icon=ft.Icons.DOWNLOAD, bgcolor="#2980B9", color="white", on_click=exportar)
            ], spacing=18),
            padding=30,
            bgcolor="white",
            border_radius=12,
            margin=ft.margin.all(30),
            width=900,
            alignment=ft.alignment.top_center
        )
    )
    page.update()