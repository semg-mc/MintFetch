import flet as ft


COLOR_BG = "#313338"        # Gris azulado oscuro (Fondo principal)
COLOR_CONSOLE = "#1e1f22"   # Gris muy profundo (Fondo de terminal y cajas)
COLOR_MINT = "#87c095"      # Verde Mint (Acentos y botones)
COLOR_TEXT = "#dbdee1"      # Blanco ceniza (Lectura cómoda)
COLOR_MUTED = "#949ba4"     # Gris tenue (Subtítulos)

def main(page: ft.Page):
    
    page.title = "MintFetch"
    page.bgcolor = COLOR_BG
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 25
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    
    
    
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

    
    btn_fetch = ft.ElevatedButton(
        text="EJECUTAR FETCH",
        bgcolor=COLOR_MINT,
        color=COLOR_CONSOLE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=12),
            padding=18,
        ),
        width=300
    )

    
    consola = ft.Container(
        content=ft.Text(
            "[root@android]~ $ MintFetch v1.0 iniciado...\n[root@android]~ $ Esperando órdenes_",
            font_family="monospace", 
            color=COLOR_MINT,
            size=12,
        ),
        bgcolor=COLOR_CONSOLE,
        padding=15,
        border_radius=12,
        width=float('inf'), 
        height=180,
        alignment=ft.alignment.top_left
    )

    
    page.add(
        titulo,
        subtitulo,
        ft.Container(height=20),
        txt_url,
        ft.Container(height=10),
        btn_fetch,
        ft.Container(height=20),
        consola
    )

if __name__ == "__main__":
    ft.app(main)
