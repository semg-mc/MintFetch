import os
import threading
import flet as ft
import yt_dlp

# --- PALETA DE COLORES (LMDE / DISCORD / STEAM) ---
COLOR_BG = "#1e1f22"         
COLOR_SURFACE = "#2b2d31"    
COLOR_MINT = "#87c095"       
COLOR_TEXT = "#dbdee1"       
COLOR_MUTED = "#949ba4"      
COLOR_TERMINAL = "#000000"   

RUTA_DESCARGAS = "/storage/emulated/0/Download"

def main(page: ft.Page):
    page.title = "MintFetch"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START 

    # --- 1. CABECERA ---
    cabecera = ft.Column(
        controls=[
            ft.Text("MintFetch", size=36, weight=ft.FontWeight.W_900, color=COLOR_MINT),
            ft.Text("Modo Tanque - Máxima Calidad Automática", size=13, color=COLOR_MUTED, weight=ft.FontWeight.W_500),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0
    )

    # --- 2. EL MENÚ DE AYUDA (Indestructible) ---
    guia_desplegable = ft.ExpansionTile(
        title=ft.Text("📖 Guía y Compatibilidad", color=COLOR_TEXT, weight=ft.FontWeight.BOLD),
        collapsed_text_color=COLOR_MUTED,
        text_color=COLOR_MINT,
        icon_color=COLOR_MINT,
        collapsed_icon_color=COLOR_MUTED,
        controls=[
            ft.Container(
                content=ft.Text(
                    "MODO TANQUE ACTIVADO:\n"
                    "El sistema detectará y descargará automáticamente la mejor calidad disponible (Audio+Video).\n\n"
                    "SOPORTA:\n"
                    "• YouTube, TikTok, IG, FB, X, Reddit, Twitch.",
                    color=COLOR_TEXT, size=13
                ),
                padding=15,
                bgcolor=COLOR_SURFACE,
                border_radius=10
            )
        ]
    )

    # --- 3. CAJA DE ENTRADA (SIMPLIFICADA) ---
    txt_url = ft.TextField(
        hint_text="[ Pega el enlace aquí ]",
        hint_style=ft.TextStyle(color=COLOR_MUTED),
        bgcolor=COLOR_SURFACE,
        border_color="transparent",
        focused_border_color=COLOR_MINT,
        color=COLOR_TEXT,
        border_radius=10,
        text_size=15,
        width=320 
    )

    btn_fetch = ft.ElevatedButton(
        content=ft.Text("EJECUTAR FETCH", weight=ft.FontWeight.W_800, color=COLOR_TERMINAL, size=16),
        bgcolor=COLOR_MINT,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=20,
        ),
        width=320 
    )

    # --- 4. LA CONSOLA (¡SIN BORDES PROBLEMÁTICOS!) ---
    consola_texto = ft.Text(
        "[root@android]~ $ MintFetch v3.1 [Tanque] cargado.\n[root@android]~ $ Esperando enlace...",
        font_family="monospace",
        color=COLOR_MINT,
        size=12,
    )

    consola = ft.Container(
        content=ft.ListView([consola_texto], auto_scroll=True),
        bgcolor=COLOR_TERMINAL, 
        padding=15,
        border_radius=10,
        height=160,
        width=320
        # ¡LÍNEA DE BORDE ELIMINADA PARA EVITAR CRASHEOS!
    )

    firma = ft.Text("Desarrollado por semg_mc © 2026", size=11, color=COLOR_MUTED)

    # --- FUNCIONES DEL CEREBRO ---
    def log(texto):
        consola_texto.value += f"\n[root@android]~ $ {texto}"
        page.update()

    def accion_descarga(e):
        url = txt_url.value.strip()
        if not url: return
        
        btn_fetch.disabled = True
        btn_fetch.bgcolor = COLOR_MUTED
        txt_url.disabled = True
        log("Iniciando extracción de máxima calidad...")
        page.update()
        
        def run():
            try:
                # MOTOR MODO TANQUE
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True, 
                    'nocheckcertificate': True,
                    'geo_bypass': True,
                    'outtmpl': os.path.join(RUTA_DESCARGAS, '%(title).50s.%(ext)s'),
                    'format': 'best', 
                    'extractor_args': {'youtube': {'player_client': ['ios', 'android']}}, 
                }
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                log("✅ Operación Exitosa. Archivo en /Download")
                txt_url.value = "" 
                
            except Exception as ex:
                error_msg = str(ex).split(":")[-1].strip()[:50]
                log(f"❌ Error Real: {error_msg}...")
            
            finally:
                btn_fetch.disabled = False
                btn_fetch.bgcolor = COLOR_MINT
                txt_url.disabled = False
                log("Sistema listo para nuevo enlace.")
                page.update()
        
        threading.Thread(target=run, daemon=True).start()

    btn_fetch.on_click = accion_descarga
    
    # --- ENSAMBLAJE FINAL ---
    page.add(
        ft.Container(height=10),
        cabecera,
        ft.Container(height=10),
        guia_desplegable, 
        ft.Container(height=10),
        txt_url,
        ft.Container(height=5),
        btn_fetch,
        ft.Container(height=10),
        consola,
        ft.Container(height=5),
        firma
    )

if __name__ == "__main__":
    ft.app(main)
    
