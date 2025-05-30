import flet as ft
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
from database import tickets_por_dia_e_status, contar_tickets_status

def DashboardPage(page: ft.Page):
    page.title = "Dashboard - Help Desk"
    page.bgcolor = "#F4F6F7"

    def voltar(e):
        page.go("/inicial")

    def novo_ticket(e):
        page.go("/novo_ticket")

    def buscar_ticket(e):
        page.go("/pesquisa")

    def faq(e):
        page.go("/faq")

    # --- DADOS DO BANCO ---
    dias, chamados_abertos, chamados_fechados = tickets_por_dia_e_status()
    resumo = contar_tickets_status()

    # --- GRÁFICO ---
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(dias, chamados_abertos, label="Abertos", marker="o", color="#FF6347")
    ax.plot(dias, chamados_fechados, label="Fechados", marker="o", color="#2ECC71")
    ax.set_title("Chamados na Última Semana")
    ax.set_xlabel("Dia")
    ax.set_ylabel("Quantidade")
    ax.set_ylim(0, max(chamados_abertos + chamados_fechados + [1]) + 2)
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    chart = MatplotlibChart(fig, expand=False)

    resumo_blocos = ft.Row(
        [
            ft.Container(
                ft.Column([
                    ft.Text("Atribuídos", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(str(resumo["atribuidos"]), size=32, weight=ft.FontWeight.BOLD, color="#2980B9"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                width=170, height=100, bgcolor="#D6EAF8", border_radius=10, padding=20
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Novos", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(str(resumo["novos"]), size=32, weight=ft.FontWeight.BOLD, color="#27AE60"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                width=170, height=100, bgcolor="#D5F5E3", border_radius=10, padding=20
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Em Espera", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(str(resumo["em_espera"]), size=32, weight=ft.FontWeight.BOLD, color="#F39C12"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                width=170, height=100, bgcolor="#FCF3CF", border_radius=10, padding=20
            ),
            ft.Container(
                ft.Column([
                    ft.Text("Fechados", size=16, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                    ft.Text(str(resumo["fechados"]), size=32, weight=ft.FontWeight.BOLD, color="#AAB7B8"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                width=170, height=100, bgcolor="#EBEDEF", border_radius=10, padding=20
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
    )

    quick_actions = ft.Row(
        [
            ft.ElevatedButton(text="Novo Ticket", icon=ft.Icons.ADD, bgcolor="#2980B9", color="white", on_click=novo_ticket),
            ft.ElevatedButton(text="Buscar Ticket", icon=ft.Icons.SEARCH, bgcolor="#27AE60", color="white", on_click=buscar_ticket),
            ft.ElevatedButton(text="FAQ", icon=ft.Icons.HELP, bgcolor="#F39C12", color="white", on_click=faq),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20,
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
                    "Dashboard",
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

    conteudo_scroll = ft.Container(
        content=ft.ListView(
            controls=[
                ft.Text("Visão Geral", size=22, weight=ft.FontWeight.BOLD, color="#2C3E50"),
                resumo_blocos,
                ft.Divider(height=30, color="#ECF0F1"),
                chart,
                ft.Divider(height=30, color="#ECF0F1"),
                quick_actions,
            ],
            spacing=30,
            padding=ft.padding.all(20),
            expand=True
        ),
        bgcolor="white",
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=12, color="#bbb", offset=ft.Offset(0, 2)),
        margin=ft.margin.all(20),
        expand=True,
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
