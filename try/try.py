import flet as ft
import random
import time
import threading


def main(page: ft.Page):
    page.title = "Gráficas en Tiempo Real"
    # Estado compartido para el eje X
    state = {"x": 0}

    # === Sliders y sus indicadores ===
    def make_slider(initial):
        s = ft.Slider(value=initial, min=0, max=100, inactive_color="black", active_color="white", expand=True)
        lbl = ft.Text(f"{initial}%", color="black")
        return s, lbl

    slider1, indicator1 = make_slider(30)
    slider2, indicator2 = make_slider(50)
    slider3, indicator3 = make_slider(20)
    slider4, indicator4 = make_slider(80)

    # Datos para la segunda gráfica (actualizable con sliders)
    data2 = [
        ft.LineChartData(
            data_points=[
                ft.LineChartDataPoint(0, slider1.value),
                ft.LineChartDataPoint(25, slider2.value),
                ft.LineChartDataPoint(50, slider3.value),
                ft.LineChartDataPoint(100, slider4.value),
            ],
            curved=True,
            stroke_width=2,
            color="black",
            point=True,
            below_line_gradient=ft.LinearGradient(["white", "purple"]),
        )
    ]

    chart2 = ft.LineChart(
        data_series=data2,
        min_x=0,
        max_x=100,
        min_y=0,
        max_y=100,
        point_line_start=0,
        expand=True,
        interactive=False,
        border=ft.Border(
            bottom=ft.BorderSide(2, ft.colors.with_opacity(0.3, "white")),
            left=ft.BorderSide(2, ft.colors.with_opacity(0.3, "white")),
        ),
    )

    # Callback para actualizar indicadores y gráfica 2
    def on_slider_change(slider, indicator, index):
        def handler(e):
            val = int(slider.value)
            indicator.value = f"{val}%"
            data2[0].data_points[index].y = val
            chart2.update()
        return handler

    slider1.on_change = on_slider_change(slider1, indicator1, 0)
    slider2.on_change = on_slider_change(slider2, indicator2, 1)
    slider3.on_change = on_slider_change(slider3, indicator3, 2)
    slider4.on_change = on_slider_change(slider4, indicator4, 3)

    # Datos para la gráfica de tiempo real
    data1 = [ft.LineChartData(data_points=[], curved=True, stroke_width=2, color="black", point=True)]
    chart1 = ft.LineChart(
        data_series=data1,
        min_x=0,
        max_x=50,
        min_y=0,
        max_y=50,
        point_line_start=0,
        expand=True,
        interactive=False,
        left_axis=ft.ChartAxis(visible=True, labels_size=30),
        bottom_axis=ft.ChartAxis(visible=True, labels_size=30),
        border=ft.Border(
            bottom=ft.BorderSide(2, ft.colors.with_opacity(0.3, "white")),
            left=ft.BorderSide(2, ft.colors.with_opacity(0.3, "white")),
        ),
    )

    # Hilo para actualizar datos en tiempo real
    def real_time_data():
        while True:
            state['x'] += 1
            data1[0].data_points.append(ft.LineChartDataPoint(state['x'], random.randint(5, 45)))
            if len(data1[0].data_points) >= 50:
                state['x'] = 0
                data1[0].data_points.clear()
            chart1.update()
            time.sleep(0.3)

    threading.Thread(target=real_time_data, daemon=True).start()

    # Controles agrupados
    controls_group = ft.Column([
        ft.Row([slider1, indicator1], spacing=0, expand=True),
        ft.Row([slider2, indicator2], spacing=0, expand=True),
        ft.Row([slider3, indicator3], spacing=0, expand=True),
        ft.Row([slider4, indicator4], spacing=0, expand=True),
    ], expand=True)

    # Layout principal
    content = ft.Column([
        ft.Container(
            expand=True,
            gradient=ft.LinearGradient(["purple", "white"], rotation=30),
            border_radius=10,
            content=ft.Column([
                ft.Container(
                    height=60,
                    padding=10,
                    alignment=ft.alignment.center,
                    content=ft.Text("Gráfica en tiempo real", font_family="vivaldi", size=30, weight=ft.FontWeight.BOLD)
                ),
                ft.Container(expand=True, padding=20, content=chart1)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ),
        ft.Container(
            expand=True,
            gradient=ft.LinearGradient(["purple", "white"]),
            border_radius=10,
            padding=10,
            content=ft.Row([
                controls_group,
                ft.Column([chart2], expand=True)
            ], spacing=20)
        )
    ], expand=True)

    page.add(content)


if __name__ == "__main__":
    ft.app(target=main)
