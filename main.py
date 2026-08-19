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
        title=ft.Text("Manual", color=COLOR_MINT),
        content=ft.Text("Pega el enlace, elige formato y dale a EJECUTAR.", color=COLOR_TEXT),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: cerrar_ayuda())],
    )

    def cerrar_ayuda():
        dlg_ayuda.open = False
        page.update()

    def abrir_ayuda(e):
        page.dialog = dlg_ayuda
        dlg_ayuda.open = True
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Text("?", weight=ft.FontWeight.BOLD, color=COLOR_MINT),
        bgcolor=COLOR_CONSOLE,
        on_click=abrir_ayuda,
        shape=ft.CircleBorder()
    )

    # --- UI ---
    txt_url = ft.TextField(hint_text="Pega el enlace aquí", bgcolor=COLOR_CONSOLE, border_color="transparent", color=COLOR_TEXT, border_radius=12)
    dd_calidad = ft.Dropdown(options=[ft.dropdown.Option("🎬 Video HD"), ft.dropdown.Option("📱 Video Ligero"), ft.dropdown.Option("🎵 Solo Audio")], value="🎬 Video HD", bgcolor=COLOR_CONSOLE, color=COLOR_TEXT)
    btn_fetch = ft.ElevatedButton(content=ft.Text("EJECUTAR FETCH", weight=ft.FontWeight.BOLD, color=COLOR_CONSOLE), bgcolor=COLOR_MINT, width=300)
    consola_texto = ft.Text("MintFetch listo...", font_family="monospace", color=COLOR_MINT, size=11)
    consola = ft.Container(content=ft.ListView([consola_texto], auto_scroll=True), bgcolor=COLOR_CONSOLE, padding=15, border_radius=12, height=150)

    def actualizar_consola(t):
        consola_texto.value += f"\n> {t}"
        page.update()

    def ejecutar_fetch(e):
        url = txt_url.value.strip()
        if not url: return
        btn_fetch.disabled = True
        actualizar_consola("Iniciando...")
        
        def trabajo():
            try:
                
                opts = {
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                    'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).50s.%(ext)s'),
                }
                if "Ligero" in dd_calidad.value: opts['format'] = '18'
                elif "Audio" in dd_calidad.value: opts['format'] = 'm4a/bestaudio'
                else: opts['format'] = 'best'

                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
                actualizar_consola("✅ ¡Éxito! Revisa /Download")
            except Exception as e:
                actualizar_consola(f"❌ Fallo: {str(e)[:30]}")
            btn_fetch.disabled = False
            page.update()
        
        threading.Thread(target=trabajo, daemon=True).start()

    btn_fetch.on_click = ejecutar_fetch
    page.add(ft.Text("MintFetch", size=32, weight=ft.FontWeight.BOLD, color=COLOR_MINT), txt_url, dd_calidad, btn_fetch, consola)

ft.app(main)
