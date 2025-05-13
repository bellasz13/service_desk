import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

def EstatisticaPage(page: ft.Page):
    page.title = "Estatísticas - Help Desk"
    page.bgcolor = "#F4F6F7"

    def voltar(e):
        page.go("/inicial")

    status = ["Aberto", "Fechado", "Em Espera", "Atribuído"]
    qtd_status = [8, 15, 3, 5]

    categorias = ["Suporte Técnico", "Financeiro", "Infraestrutura", "Outro"]
    qtd_categorias = [12, 5, 7, 2]

    fig_status, ax1 = plt.subplots(figsize=(4, 3))
    bars = ax1.bar(status, qtd_status, color=["#27AE60", "#AAB7B8", "#F39C12", "#2980B9"])
    ax1.set_title("Tickets por Status")
    ax1.set_ylabel("Quantidade")
    ax1.set_ylim(0, max(qtd_status) + 2)
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3), textcoords="offset points",
                     ha='center', va='bottom', fontsize=10)

    chart_status = MatplotlibChart(fig_status, expand=False)

    fig_cat, ax2 = plt.subplots(figsize=(4, 3))
    wedges, texts, autotexts = ax2.pie(
        qtd_categorias,
        labels=categorias,
        autopct='%1.1f%%',
        startangle=140,
        colors=["#2980B9", "#F39C12", "#27AE60", "#AAB7B8"],
        textprops={'color':"#2C3E50"}
    )
    ax2.set_title("Tickets por Categoria")
    chart_categorias = MatplotlibChart(fig_cat, expand=False)

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
                    "Estatísticas",
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

    conteudo_scroll = ft.ListView(
        controls=[
            ft.Text("Painel de Estatísticas", size=20, weight=ft.FontWeight.BOLD, color="#2C3E50"),
            ft.Divider(height=10, color="#F4F6F7"),
            ft.Container(
                chart_status,
                bgcolor="white",
                border_radius=10,
                padding=20,
                margin=ft.margin.only(bottom=20),
                alignment=ft.alignment.center,
                width=450,
                height=300
            ),
            ft.Container(
                chart_categorias,
                bgcolor="white",
                border_radius=10,
                padding=20,
                margin=ft.margin.only(bottom=20),
                alignment=ft.alignment.center,
                width=450,
                height=300
            ),
        ],
        spacing=20,
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
