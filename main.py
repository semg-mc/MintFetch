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

# --- NUEVA RUTA: CARPETA INTELIGENTE ---
RUTA_BASE = "/storage/emulated/0/Download"
RUTA_DESCARGAS = os.path.join(RUTA_BASE, "MintFetch")

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
            "• X (Twitter), Facebook, Instagram\n"
            "• Reddit, Twitch y muchas más.",
            color=COLOR_TEXT,
            size=14
        ),
        actions=[
            # CORRECCIÓN: Usamos page.close() para cerrar
            ft.TextButton("Entendido", on_click=lambda e: page.close(dlg_ayuda), style=ft.ButtonStyle(color=COLOR_MINT))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=12)
    )

    # CORRECCIÓN: Usamos page.open() para abrir
    def abrir_ayuda(e):
        page.open(dlg_ayuda)

    # Botón Flotante
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
        "[root@android]~ $ MintFetch v1.1 listo.\n[root@android]~ $ Esperando órdenes...",
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

    def reiniciar_interfaz():
        txt_url.disabled = False
        dd_calidad.disabled = False
        btn_fetch.disabled = False
        btn_fetch.bgcolor = COLOR_MINT
        page.update()

    def ejecutar_fetch(e):
        url = txt_url.value.strip()
        if not url:
            return

        seleccion = dd_calidad.value
        
        txt_url.disabled = True
        dd_calidad.disabled = True
        btn_fetch.disabled = True
        btn_fetch.bgcolor = COLOR_MUTED
        consola_texto.value = "[root@android]~ $ Iniciando protocolo de extracción..."
        page.update()

        def trabajo_descarga():
            # Crear la carpeta inteligente si no existe
            os.makedirs(RUTA_DESCARGAS, exist_ok=True)
            
            max_intentos = 4
            intento_actual = 1
            descarga_exitosa = False

            while intento_actual <= max_intentos and not descarga_exitosa:
                try:
                    estado_ui = {"ultimo_p": -10}

                    def hook_progreso(d):
                        if d['status'] == 'downloading':
                            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                            p_str = ansi_escape.sub('', d.get('_percent_str', '0.0%')).replace('%', '').strip()
                            try:
                                p = float(p_str)
                                if p - estado_ui["ultimo_p"] >= 10:
                                    actualizar_consola(f"Extrayendo datos: {p_str}%")
                                    estado_ui["ultimo_p"] = p
                            except ValueError:
                                pass
                        elif d['status'] == 'finished':
                            actualizar_consola("Descarga completa. Finalizando archivo...")
                            page.update()

                    class InterceptorLogger:
                        def debug(self, msg): pass
                        def info(self, msg): pass
                        def warning(self, msg): pass
                        def error(self, msg): pass

                    opts = {
                        'quiet': True,
                        'progress_hooks': [hook_progreso],
                        'logger': InterceptorLogger(),
                        'nocheckcertificate': True,
                        'geo_bypass': True,
                        'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).100s.%(ext)s'),
                    }

                    # --- EL NUEVO CEREBRO DE FORMATOS ---
                    if "Ligero" in seleccion:
                        opts['format'] = '18/b[height<=480]/b' # Formato pre-ensamblado seguro
                    elif "Audio" in seleccion:
                        opts['format'] = 'm4a/bestaudio/best' # M4A nativo para evitar ffmpeg
                    else:
                        opts['format'] = 'best' # MP4 HD pre-ensamblado

                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([url])

                    descarga_exitosa = True
                    actualizar_consola("✅ Operación Exitosa. Archivo en /MintFetch")
                    time.sleep(2)
                    txt_url.value = ""
                    actualizar_consola("✅ Esperando nuevo enlace...")

                except Exception as ex:
                    if intento_actual < max_intentos:
                        actualizar_consola(f"⚠️ Servidor hostil. Reintentando ({intento_actual}/{max_intentos})")
                        time.sleep(2)
                        intento_actual += 1
                    else:
                        actualizar_consola("❌ Error crítico. Enlace roto o formato no disponible.")
                        break
            
            reiniciar_interfaz()

        threading.Thread(target=trabajo_descarga, daemon=True).start()

    btn_fetch.on_click = ejecutar_fetch

    # ENSAMBLAJE FINAL
    page.add(
        titulo, 
        subtitulo,
        ft.Container(height=15),
        txt_url,
        dd_calidad,
        ft.Container(height=5),
        btn_fetch,
        ft.Container(height=15),
        consola,
        firma
    )

if __name__ == "__main__":
    ft.app(main)
    
