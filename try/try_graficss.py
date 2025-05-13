import flet as ft
from collections import Counter
from datetime import datetime

style_frame: dict = {
    "expand": True,
    "bgcolor": ft.Colors.WHITE,
    "border_radius": 10,
}

class GraphOne(ft.Container):
    def __init__(self, tipos_vehiculos):
        super().__init__(**style_frame)
        self.normal_radius = 110
        self.normal_badge_size = 50
        total_vehiculos = sum(tipos_vehiculos.values())
        title = ft.Text("Tipos de Vehículos", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        
        chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    count,
                    title=f"{(count / total_vehiculos) * 100:.1f}%",
                    title_style=ft.TextStyle(size=25, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD,),
                    color="blue" if tipo == "coche" else "green",
                    radius=self.normal_radius,
                    badge=ft.Icon(
                        ft.Icons.CAR_CRASH if tipo == "coche" else ft.Icons.MOTORCYCLE,
                        size=self.normal_badge_size
                    ),
                    badge_position=1
                )
                for tipo, count in tipos_vehiculos.items()
            ],
            sections_space=0,
            center_space_radius=0,
        )

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[title, chart],
            expand=True
        )
    
class GraphTwo(ft.Container):
    def __init__(self, ocupacion_zonas):
        super().__init__(**style_frame)
        self.normal_bar_width = 40
        self.border_radius = 20
        title = ft.Text("Vehiculos por Zona", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)
        # Que no cuente fuera
        zonas_filtradas = []
        for zona, count in ocupacion_zonas.items():
            if zona != "fuera":
                zonas_filtradas.append((zona, count))

        # Crear grupos de barras
        bar_groups = []
        for i, (zona, count) in enumerate(zonas_filtradas):
            bar_group = ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=count,
                        width=self.normal_bar_width,
                        border_radius=self.border_radius,
                        gradient=ft.LinearGradient([ft.Colors.CYAN, ft.Colors.CYAN_100], rotation=90)
                    )
                ]
            )
            bar_groups.append(bar_group)

        # Etiquetas eje x
        x_labels = []
        for i, (zona, _) in enumerate(zonas_filtradas):
            label = ft.ChartAxisLabel(
                value=i,
                label=ft.Container(ft.Text(zona, color=ft.Colors.BLACK), padding=10)
            )
            x_labels.append(label)

        # Etiquetas eje y
        max_count = 0
        for _, count in zonas_filtradas:
            if count > max_count:
                max_count = count
                
        y_max = max_count + 5
        y_labels = []
        for y in range(0, y_max + 1, 5):
            y_labels.append(
                ft.ChartAxisLabel(
                    value=y,
                    label=ft.Text(y, color=ft.Colors.BLACK)
                )
            )
            
        title = ft.Text("Vehiculos por Zona", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER)
        
        chart = ft.BarChart(
            bar_groups=bar_groups,
            border=ft.border.all(1, ft.Colors.BLACK),
            bottom_axis=ft.ChartAxis(labels=x_labels, labels_size=40),
            left_axis=ft.ChartAxis(
                title=ft.Container(ft.Text("Número de Vehículos", color=ft.Colors.BLACK)),
                title_size=40,
                labels=y_labels,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), width=1, dash_pattern=[3, 3]
            ),
            groups_space=20,
            max_y=y_max,
        )

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[title, 
                    ft.Container(
                        chart, margin=ft.margin.only(right=20), expand=True)
                    ],
        )
        
class GraphThree(ft.Container):
    def __init__(self, fechas_entrada):
        super().__init__(**style_frame)
        title = ft.Text("Entradas por Día", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK)

        # Contar entradas por día
        fechas_formateadas = [datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S").strftime("%m/%d") for fecha in fechas_entrada]
        conteo_por_dia = Counter(fechas_formateadas)
        dias_ordenados = sorted(conteo_por_dia.keys())
        
        # Generar puntos del gráfico
        data_points = []
        x_labels = []

        y_max = max(conteo_por_dia.values()) + 2 if conteo_por_dia else 2
        y_labels = []
        for y in range(0, y_max + 1, 2):
            y_labels.append(ft.ChartAxisLabel(value=y, label=ft.Text(str(y), color=ft.Colors.BLACK)))

        for i, dia in enumerate(dias_ordenados):
            data_points.append(ft.LineChartDataPoint(i, conteo_por_dia[dia]))

            x_labels.append(
                ft.ChartAxisLabel(
                    value=i,
                    label=ft.Container(
                        ft.Text(
                            dia,
                            color=ft.Colors.BLACK
                        ),
                    ),
                ),
            )
            
        line_chart = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=data_points,
                    stroke_width=5,
                    color=ft.Colors.CYAN,
                    curved=True,
                    gradient=ft.LinearGradient([ft.Colors.CYAN, ft.Colors.WHITE])
                )
            ],
            left_axis=ft.ChartAxis(
                labels=y_labels,
                labels_interval=2,
                title=ft.Text("Nº de Entradas", color=ft.Colors.BLACK),
                title_size=40
            ),
            bottom_axis=ft.ChartAxis(
                labels=x_labels,
                labels_interval=1,
                title=ft.Container(
                    ft.Text("Fecha", color=ft.Colors.BLACK)
                ),
                title_size=20
            ),
            border=ft.border.all(1, ft.Colors.BLACK),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), width=1, dash_pattern=[3, 3],
            ),
            vertical_grid_lines=ft.ChartGridLines(
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK), dash_pattern=[3, 3], width=1
            ),
            max_y=y_max,
            min_y=0,
            expand=True,
        )

        self.content = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                title,
                ft.Container(
                    line_chart,
                    margin=ft.margin.only(right=20),
                    expand=True)
                ]
        )
        
def main(page: ft.Page):
    # Datos de ejemplo
    tipos_vehiculos = {
        "coche": 70,
        "moto": 30
    }
    
    ocupacion_zonas = {
        "Zona 1": 50,
        "Zona 2": 30,
        "fuera": 20
    }
    
    fechas_entrada = [
        "2025-04-18 08:00:00",
        "2025-04-18 09:30:00",
        "2025-04-19 10:15:00",
        "2025-04-12 11:45:00",
        "2025-04-25 12:00:00",
        "2025-04-18 13:00:00",
    ]
    

    graph_one = GraphOne(tipos_vehiculos)
    graph_two = GraphTwo(ocupacion_zonas)
    graph_three = GraphThree(fechas_entrada)
    
    # Añadir el gráfico a la página
    layout = ft.Column(
        [
            ft.Row(
                [graph_one, graph_two],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
                expand=True
            ),
            graph_three
        ],
        spacing=30,
        expand=True
    )

    page.add(layout)

# Configurar la aplicación Flet
ft.app(target=main)
