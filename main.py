import os
import threading
import flet as ft
import yt_dlp

# --- LA PALETA MINTFETCH (EL REGRESO DEL REY) ---
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
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- VENTANA DE AYUDA (MODAL ESTILO LMDE) ---
    dlg = ft.AlertDialog(
        modal=True,
        bgcolor=COLOR_CONSOLE,
        title=ft.Text("Guía de Usuario", color=COLOR_MINT),
        content=ft.Text("1. Pega el link.\n2. Elige formato.\n3. Presiona EJECUTAR.\n\nSoporta: YouTube, TikTok, Facebook, Instagram, Reddit, Twitch.", color=COLOR_TEXT),
        actions=[ft.TextButton("Entendido", on_click=lambda e: cerrar_dlg(), style=ft.ButtonStyle(color=COLOR_MINT))],
    )

    def cerrar_dlg():
        dlg.open = False
        page.update()

    def abrir_dlg(e):
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Botón flotante estilo Android Nativo
    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Text("?", weight=ft.FontWeight.BOLD, color=COLOR_MINT),
        bgcolor=COLOR_CONSOLE,
        on_click=abrir_dlg,
        shape=ft.CircleBorder()
    )

    # --- ELEMENTOS PREMIUM ---
    titulo = ft.Text("MintFetch", size=32, weight=ft.FontWeight.BOLD, color=COLOR_MINT)
    subtitulo = ft.Text("Descargador Estructurado", size=13, color=COLOR_MUTED)

    txt_url = ft.TextField(hint_text="Pega el enlace aquí", hint_style=ft.TextStyle(color=COLOR_MUTED), bgcolor=COLOR_CONSOLE, border_color="transparent", color=COLOR_TEXT, border_radius=12)
    dd = ft.Dropdown(options=[ft.dropdown.Option("🎬 HD (Video)"), ft.dropdown.Option("📱 Ligero (360p)"), ft.dropdown.Option("🎵 Audio (M4A)")], value="🎬 HD (Video)", bgcolor=COLOR_CONSOLE, color=COLOR_TEXT, border_radius=12, border_color="transparent")
    btn = ft.ElevatedButton(content=ft.Text("EJECUTAR FETCH", weight=ft.FontWeight.BOLD, color=COLOR_CONSOLE), bgcolor=COLOR_MINT, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=18), width=300)
    
    consola_texto = ft.Text("MintFetch v1.6 iniciado...", font_family="monospace", color=COLOR_MINT, size=11)
    consola = ft.Container(content=ft.ListView([consola_texto], auto_scroll=True), bgcolor=COLOR_CONSOLE, padding=15, border_radius=12, height=150, width=float('inf'))
    
    firma = ft.Text("Desarrollado por semg_mc © 2026", size=10, color=COLOR_MUTED)

    def log(t):
        consola_texto.value += f"\n> {t}"
        page.update()

    def accion_descarga(e):
        url = txt_url.value.strip()
        if not url: return
        btn.disabled = True
        btn.bgcolor = COLOR_MUTED
        log("Iniciando conexión...")
        
        def run():
            try:
                ydl_opts = {
                    'quiet': True,
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                    'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).50s.%(ext)s'),
                }
                if "Ligero" in dd.value: ydl_opts['format'] = '18'
                elif "Audio" in dd.value: ydl_opts['format'] = 'm4a/bestaudio'
                else: ydl_opts['format'] = 'best'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                log("✅ ¡Éxito! Archivo guardado en /Download")
            except Exception as ex:
                log(f"❌ Fallo crítico: {str(ex)[:30]}")
            btn.disabled = False
            btn.bgcolor = COLOR_MINT
            page.update()
        
        threading.Thread(target=run, daemon=True).start()

    btn.on_click = accion_descarga
    
    # Ensamblaje con espaciado elegante
    page.add(titulo, subtitulo, ft.Container(height=10), txt_url, dd, ft.Container(height=10), btn, ft.Container(height=10), consola, firma)

ft.app(main)
