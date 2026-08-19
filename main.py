import os
import re
import time
import threading
import flet as ft
import yt_dlp


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
            "• TikTok, X (Twitter), Facebook, Instagram, Reddit, Twitch.",
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
        page.dialog = dlg_ayuda
        dlg_ayuda.open = True
        page.update()

    
    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Text("?", size=24, weight=ft.FontWeight.BOLD, color=COLOR_MINT),
        bgcolor=COLOR_CONSOLE,
        on_click=abrir_ayuda,
        shape=ft.CircleBorder()
    )

    
    titulo = ft.Text("MintFetch", size=32, weight=ft.FontWeight.BOLD, color=COLOR_MINT)
    subtitulo = ft.Text("Descargador Universal Estructurado", size=13, color=COLOR_MUTED)

    txt_url = ft.TextField(
        hint_text="[ Pega el enlace aquí ]",
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
            ft.dropdown.Option("📱 Video Ligero (360p)"),
            ft.dropdown.Option("🎵 Solo Audio (M4A)")
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
        "[root@android]~ $ MintFetch v1.4 listo.\n[root@android]~ $ Esperando órdenes...",
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

    
    def actualizar_consola(texto):
        consola_texto.value += f"\n> {texto}"
        page.update()

    def reiniciar_interfaz():
        txt_url.disabled = False
        dd_calidad.disabled = False
        btn_fetch.disabled = True 
        btn_fetch.bgcolor = COLOR_MINT
        btn_fetch.disabled = False
        page.update()

    def ejecutar_fetch(e):
        url = txt_url.value.strip()
        if not url: return

        seleccion = dd_calidad.value
        txt_url.disabled = True
        dd_calidad.disabled = True
        btn_fetch.disabled = True
        btn_fetch.bgcolor = COLOR_MUTED
        consola_texto.value = "[root@android]~ $ Iniciando conexión segura..."
        page.update()

        def trabajo_descarga():
            
            opts = {
                'quiet': True,
                'nocheckcertificate': True,
                'geo_bypass': True,
                'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).100s.%(ext)s'),
            }

            if "Ligero" in seleccion:
                opts['format'] = '18' 
            elif "Audio" in seleccion:
                opts['format'] = 'm4a'
            else:
                opts['format'] = 'best'

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                actualizar_consola("✅ Operación Exitosa. Archivo en /Download")
            except Exception as ex:
                actualizar_consola(f"❌ Error: {str(ex)[:40]}...")
            
            reiniciar_interfaz()

        threading.Thread(target=trabajo_descarga, daemon=True).start()

    btn_fetch.on_click = ejecutar_fetch

    page.add(titulo, subtitulo, ft.Container(height=15), txt_url, dd_calidad, ft.Container(height=5), btn_fetch, ft.Container(height=15), consola, firma)

if __name__ == "__main__":
    ft.app(main)
