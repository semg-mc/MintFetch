import os
import threading
import flet as ft
import yt_dlp

# --- PALETA DE COLORES (LMDE / DISCORD / STEAM) ---
COLOR_BG = "#1e1f22"         # Fondo hiper oscuro (Discord)
COLOR_SURFACE = "#2b2d31"    # Cajas y tarjetas (Steam)
COLOR_MINT = "#87c095"       # Verde Linux Mint (Acentos)
COLOR_TEXT = "#dbdee1"       # Texto claro
COLOR_MUTED = "#949ba4"      # Texto secundario
COLOR_TERMINAL = "#000000"   # Fondo de consola negro puro

RUTA_DESCARGAS = "/storage/emulated/0/Download"

def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "MintFetch"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START # Alineado arriba para que fluya natural

    # --- 1. CABECERA ---
    cabecera = ft.Column(
        controls=[
            ft.Text("MintFetch", size=36, weight=ft.FontWeight.W_900, color=COLOR_MINT),
            ft.Text("Descargador Universal Estructurado", size=14, color=COLOR_MUTED, weight=ft.FontWeight.W_500),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0
    )

    # --- 2. EL MENÚ DE AYUDA (¡Tu idea del desplegable!) ---
    # Esto jamás va a crashear porque es parte de la misma pantalla.
    guia_desplegable = ft.ExpansionTile(
        title=ft.Text("📖 Guía y Plataformas Compatibles", color=COLOR_TEXT, weight=ft.FontWeight.BOLD),
        collapsed_text_color=COLOR_MUTED,
        text_color=COLOR_MINT,
        icon_color=COLOR_MINT,
        collapsed_icon_color=COLOR_MUTED,
        controls=[
            ft.Container(
                content=ft.Text(
                    "INSTRUCCIONES:\n"
                    "1. Pega el enlace de tu video o música.\n"
                    "2. Selecciona la calidad deseada.\n"
                    "3. Presiona 'EJECUTAR FETCH'.\n\n"
                    "PLATAFORMAS SOPORTADAS:\n"
                    "• YouTube (Videos y Música)\n"
                    "• TikTok (Baja sin marca de agua)\n"
                    "• Facebook, Instagram (Reels), X (Twitter)\n"
                    "• Reddit, Twitch (Clips).",
                    color=COLOR_TEXT, size=13
                ),
                padding=15,
                bgcolor=COLOR_SURFACE,
                border_radius=10
            )
        ]
    )

    # --- 3. CAJAS DE ENTRADA (Simétricas y Elegantes) ---
    txt_url = ft.TextField(
        hint_text="[ Pega el enlace aquí ]",
        hint_style=ft.TextStyle(color=COLOR_MUTED),
        bgcolor=COLOR_SURFACE,
        border_color="transparent",
        focused_border_color=COLOR_MINT,
        color=COLOR_TEXT,
        border_radius=10,
        text_size=15,
        width=320 # Ancho fijo para simetría
    )

    dd_calidad = ft.Dropdown(
        options=[
            ft.dropdown.Option("🎬 Video HD (Mejor Calidad)"),
            ft.dropdown.Option("📱 Video Ligero (360p - Estable)"),
            ft.dropdown.Option("🎵 Solo Audio (Música M4A)")
        ],
        value="🎬 Video HD (Mejor Calidad)",
        bgcolor=COLOR_SURFACE,
        border_color="transparent",
        focused_border_color=COLOR_MINT,
        color=COLOR_TEXT,
        border_radius=10,
        width=320 # Ancho fijo para simetría
    )

    btn_fetch = ft.ElevatedButton(
        content=ft.Text("EJECUTAR FETCH", weight=ft.FontWeight.W_800, color=COLOR_TERMINAL, size=16),
        bgcolor=COLOR_MINT,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
        ),
        width=320 # Sigue la simetría
    )

    # --- 4. LA CONSOLA (Estilo Linux Recuperado) ---
    consola_texto = ft.Text(
        "[root@android]~ $ MintFetch v2.0 cargado.\n[root@android]~ $ Sistema listo.",
        font_family="monospace",
        color=COLOR_MINT,
        size=12,
    )

    consola = ft.Container(
        content=ft.ListView([consola_texto], auto_scroll=True),
        bgcolor=COLOR_TERMINAL, # Negro puro de terminal
        padding=15,
        border_radius=10,
        height=160,
        width=320,
        border=ft.border.all(1, COLOR_SURFACE) # Borde sutil
    )

    firma = ft.Text("Desarrollado por semg_mc © 2026", size=11, color=COLOR_MUTED)

    # --- FUNCIONES DEL CEREBRO ---
    def log(texto):
        # Le regresamos la personalidad a cada línea que imprime
        consola_texto.value += f"\n[root@android]~ $ {texto}"
        page.update()

    def accion_descarga(e):
        url = txt_url.value.strip()
        if not url: return
        
        # Bloqueamos UI
        btn_fetch.disabled = True
        btn_fetch.bgcolor = COLOR_MUTED
        txt_url.disabled = True
        dd_calidad.disabled = True
        log("Iniciando conexión con los servidores...")
        page.update()
        
        def run():
            try:
                # El nuevo motor disfrazado de App de Android
                ydl_opts = {
                    'quiet': True,
                    'nocheckcertificate': True,
                    'geo_bypass': True,
                    'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).50s.%(ext)s'),
                    # EL TRUCO MAESTRO: Le decimos a YouTube que somos un celular, no un bot
                    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                }
                
                seleccion = dd_calidad.value
                if "Ligero" in seleccion:
                    ydl_opts['format'] = '18' 
                elif "Audio" in seleccion:
                    ydl_opts['format'] = 'm4a/bestaudio'
                else:
                    ydl_opts['format'] = 'best'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                log("✅ Operación Exitosa. Archivo en /Download")
                txt_url.value = "" # Limpiamos la caja al terminar
                
            except Exception as ex:
                # Extraemos solo el error importante
                error_msg = str(ex).split(":")[-1].strip()[:40]
                log(f"❌ Error: {error_msg}...")
            
            finally:
                # ESTA ES LA CURA ZOMBIE: Pase lo que pase (éxito o error), la UI se desbloquea
                btn_fetch.disabled = False
                btn_fetch.bgcolor = COLOR_MINT
                txt_url.disabled = False
                dd_calidad.disabled = False
                log("Esperando nuevas órdenes_")
                page.update()
        
        # Lanzamos el hilo
        threading.Thread(target=run, daemon=True).start()

    btn_fetch.on_click = accion_descarga
    
    # --- ENSAMBLAJE FINAL ---
    page.add(
        ft.Container(height=10),
        cabecera,
        ft.Container(height=10),
        guia_desplegable, # El acordeón de ayuda
        ft.Container(height=10),
        txt_url,
        dd_calidad,
        ft.Container(height=5),
        btn_fetch,
        ft.Container(height=10),
        consola,
        ft.Container(height=5),
        firma
    )

if __name__ == "__main__":
    ft.app(main)
    
