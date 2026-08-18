import os
import re
import time
import threading
import flet as ft
import yt_dlp

# --- LA PALETA MINTFETCH ---
COLOR_BG = "#313338"
COLOR_CONSOLE = "#1e1f22"
COLOR_MINT = "#87c095"
COLOR_TEXT = "#dbdee1"
COLOR_MUTED = "#949ba4"

RUTA_DESCARGAS = "/storage/emulated/0/Download"

def main(page: ft.Page):
    page.title = "MintFetch"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 25
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- VENTANA EMERGENTE (MANUAL) ---
    dlg_ayuda = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CONSOLE,
        title=ft.Text("Manual de Operaciones", color=COLOR_MINT, weight=ft.FontWeight.BOLD, size=20),
        content=ft.Text(
            "1. Pega el enlace de tu video o música.\n"
            "2. Selecciona el formato deseado.\n"
            "3. Presiona 'EJECUTAR FETCH'.\n\n"
            "🌐 Plataformas Compatibles:\n"
            "• YouTube (Videos y Música)\n"
            "• TikTok (Videos sin marca de agua)\n"
            "• X (Twitter), Facebook, Instagram",
            color=COLOR_TEXT,
            size=14
        ),
        actions=[
            ft.TextButton("Entendido", on_click=lambda e: cerrar_ayuda(), style=ft.ButtonStyle(color=COLOR_MINT))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=12)
    )

    def cerrar_ayuda():
        dlg_ayuda.open = False
        page.update()

    def abrir_ayuda(e):
        page.dialog = dlg_ayuda # Registramos el diálogo
        dlg_ayuda.open = True
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Text("?", size=24, weight=ft.FontWeight.BOLD, color=COLOR_MINT),
        bgcolor=COLOR_CONSOLE,
        on_click=abrir_ayuda,
        shape=ft.CircleBorder()
    )

    # --- ELEMENTOS VISUALES ---
    titulo = ft.Text("MintFetch", size=32, weight=ft.FontWeight.BOLD, color=COLOR_MINT)
    subtitulo = ft.Text("Descargador Universal Estructurado", size=13, color=COLOR_MUTED)

    txt_url = ft.TextField(
        hint_text="[ Pega el enlace del video aquí ]",
        hint_style=ft.TextStyle(color=COLOR_MUTED),
        bgcolor=COLOR_CONSOLE,
        border_color="transparent",
        focused_border_color=COLOR_MINT,
        color=COLOR_TEXT,
        border_radius=12,
        text_size=14,
    )

    dd_calidad = ft.Dropdown(
        options=[
            ft.dropdown.Option("🎬 Video HD (Mejor Calidad)"),
            ft.dropdown.Option("📱 Video Ligero (Ahorro Datos)"),
            ft.dropdown.Option("🎵 Solo Audio (Música M4A)")
        ],
        value="🎬 Video HD (Mejor Calidad)",
        bgcolor=COLOR_CONSOLE,
        border_color="transparent",
        focused_border_color=COLOR_MINT,
        color=COLOR_TEXT,
        border_radius=12,
        text_size=13,
    )

    btn_fetch = ft.ElevatedButton(
        content=ft.Text("EJECUTAR FETCH", weight=ft.FontWeight.BOLD, color=COLOR_CONSOLE),
        bgcolor=COLOR_MINT,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=18),
        width=300
    )

    consola_texto = ft.Text(
        "[root@android]~ $ MintFetch v1.3 listo.\n[root@android]~ $ Esperando órdenes...",
        font_family="monospace",
        color=COLOR_MINT,
        size=11,
    )

    consola = ft.Container(
        content=ft.ListView([consola_texto], auto_scroll=True),
        bgcolor=COLOR_CONSOLE,
        padding=15,
        border_radius=12,
        width=float('inf'),
        height=150
    )
    
    firma = ft.Text("Desarrollado por semg_mc © 2026", size=10, color=COLOR_MUTED)

    # --- FUNCIONES DEL CEREBRO ---
    def actualizar_consola(texto):
        consola_texto.value += f"\n> {texto}"
        page.update()

    def ejecutar_fetch(e):
        url = txt_url.value.strip()
        if not url: return

        seleccion = dd_calidad.value
        txt_url.disabled = True
        dd_calidad.disabled = True
        btn_fetch.disabled = True
        btn_fetch.bgcolor = COLOR_MUTED
        consola_texto.value = "[root@android]~ $ Iniciando protocolo de extracción..."
        page.update()

        def trabajo_descarga():
            max_intentos = 4
            intento_actual = 1
            descarga_exitosa = False

            while intento_actual <= max_intentos and not descarga_exitosa:
                try:
                    # DISFRAZ DE NAVEGADOR
                    opts = {
                        'quiet': True,
                        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        'nocheckcertificate': True,
                        'geo_bypass': True,
                        'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).100s.%(ext)s'),
                    }

                    if "Ligero" in seleccion:
                        opts['format'] = 'best[height<=480]'
                    elif "Audio" in seleccion:
                        opts['format'] = 'm4a/bestaudio/best'
                    else:
                        opts['format'] = 'best'

                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([url])

                    descarga_exitosa = True
                    actualizar_consola("✅ Operación Exitosa.")
                    txt_url.value = ""
                except Exception as ex:
                    if intento_actual < max_intentos:
                        actualizar_consola(f"⚠️ Reintentando... ({intento_actual})")
                        time.sleep(2)
                        intento_actual += 1
                    else:
                        actualizar_consola(f"❌ Fallo crítico: {str(ex)}")
                        break
            
            txt_url.disabled = False
            dd_calidad.disabled = False
            btn_fetch.disabled = False
            btn_fetch.bgcolor = COLOR_MINT
            page.update()

        threading.Thread(target=trabajo_descarga, daemon=True).start()

    btn_fetch.on_click = ejecutar_fetch

    page.add(titulo, subtitulo, ft.Container(height=15), txt_url, dd_calidad, ft.Container(height=5), btn_fetch, ft.Container(height=15), consola, firma)

if __name__ == "__main__":
    ft.app(main)
