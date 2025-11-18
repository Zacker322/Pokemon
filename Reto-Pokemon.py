import pygame
import sys
import os
from PIL import Image, ImageSequence

# Inicializar Pygame
pygame.init()

# Constantes de la pantalla
ANCHO = 1200
ALTO = 800
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 215, 0)
VERDE = (0, 200, 0)
CREMA = (255, 253, 208)
AZUL_CLARO = (173, 216, 230)
GRIS = (128, 128, 128)
GRIS_CLARO = (200, 200, 200)

# Estados del juego
MENU = 0
SELECCION = 1
GALERIA = 2
COMBATE = 3

# Variables globales
estado_juego = MENU
pokemon_seleccionado_1 = None
pokemon_seleccionado_2 = None
pokemon_jugador = None
pokemon_enemigo = None
indice_galeria = 0
modo_galeria = "grid"  # "grid" o "detalle"
pokemon_detalle = None  # Pokemon seleccionado para ver detalles
hover_pokemon_index = None  # Índice del pokemon sobre el que está el mouse

# Configurar pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pokémon Game - Pokédex")
reloj = pygame.time.Clock()

# Fuentes
fuente_titulo = pygame.font.Font(None, 72)
fuente_grande = pygame.font.Font(None, 48)
fuente_normal = pygame.font.Font(None, 36)
fuente_pequena = pygame.font.Font(None, 24)
fuente_muy_pequena = pygame.font.Font(None, 18)

# Clase para manejar GIFs animados
class AnimatedSprite:
    def __init__(self, gif_path, ancho=None, alto=None):
        self.frames = []
        self.frame_actual = 0
        self.tiempo_ultimo_frame = pygame.time.get_ticks()
        self.frame_delay = 100  # milisegundos entre frames
        
        if os.path.exists(gif_path):
            try:
                gif = Image.open(gif_path)
                for frame in ImageSequence.Iterator(gif):
                    frame_rgba = frame.convert("RGBA")
                    if ancho and alto:
                        frame_rgba = frame_rgba.resize((ancho, alto), Image.Resampling.LANCZOS)
                    
                    mode = frame_rgba.mode
                    size = frame_rgba.size
                    data = frame_rgba.tobytes()
                    
                    pygame_surface = pygame.image.fromstring(data, size, mode)
                    self.frames.append(pygame_surface)
            except Exception as e:
                print(f"Error cargando GIF {gif_path}: {e}")
                # Crear un sprite de respaldo
                surface = pygame.Surface((ancho or 100, alto or 100))
                surface.fill(GRIS)
                self.frames.append(surface)
        else:
            # Crear un sprite de respaldo si no existe el archivo
            surface = pygame.Surface((ancho or 100, alto or 100))
            surface.fill(GRIS)
            self.frames.append(surface)
    
    def get_surface(self):
        if not self.frames:
            surface = pygame.Surface((100, 100))
            surface.fill(GRIS)
            return surface
            
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultimo_frame > self.frame_delay:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.tiempo_ultimo_frame = tiempo_actual
        
        return self.frames[self.frame_actual]

# Clase Pokemon
class Pokemon:
    def __init__(self, nombre, tipo, ataque, defensa, salud, movimientos, id_pokedex, sprite_pequeno, sprite_grande):
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.salud = salud
        self.salud_maxima = salud
        self.movimientos = movimientos
        self.id_pokedex = id_pokedex
        self.sprite_pequeno = sprite_pequeno
        self.sprite_grande = sprite_grande
        self.sprite_pequeno_animado = None
        self.sprite_grande_animado = None
    
    def cargar_sprites(self):
        """Carga los sprites animados del Pokemon"""
        self.sprite_pequeno_animado = AnimatedSprite(self.sprite_pequeno, 80, 80)
        self.sprite_grande_animado = AnimatedSprite(self.sprite_grande, int(ANCHO * 0.25), int(ANCHO * 0.25))
    
    def recibir_dano(self, dano):
        dano_real = max(1, dano - self.defensa // 2)
        self.salud = max(0, self.salud - dano_real)
        return dano_real
    
    def esta_vivo(self):
        return self.salud > 0
    
    def curar(self):
        self.salud = self.salud_maxima

# Datos de movimientos
movimientos_disponibles = {
    "Impactrueno": {"tipo": "Eléctrico", "poder": 40, "precision": 100},
    "Rayo": {"tipo": "Eléctrico", "poder": 90, "precision": 100},
    "Trueno": {"tipo": "Eléctrico", "poder": 110, "precision": 70},
    "Ataque Rápido": {"tipo": "Normal", "poder": 40, "precision": 100},
    "Ascuas": {"tipo": "Fuego", "poder": 40, "precision": 100},
    "Lanzallamas": {"tipo": "Fuego", "poder": 90, "precision": 100},
    "Giro Fuego": {"tipo": "Fuego", "poder": 35, "precision": 85},
    "Llamarada": {"tipo": "Fuego", "poder": 110, "precision": 85},
    "Pistola Agua": {"tipo": "Agua", "poder": 40, "precision": 100},
    "Hidrobomba": {"tipo": "Agua", "poder": 110, "precision": 80},
    "Surf": {"tipo": "Agua", "poder": 90, "precision": 100},
    "Rayo Burbuja": {"tipo": "Agua", "poder": 65, "precision": 100},
    "Látigo Cepa": {"tipo": "Planta", "poder": 45, "precision": 100},
    "Hoja Afilada": {"tipo": "Planta", "poder": 55, "precision": 95},
    "Rayo Solar": {"tipo": "Planta", "poder": 120, "precision": 100},
    "Bomba Germen": {"tipo": "Planta", "poder": 80, "precision": 100},
    "Placaje": {"tipo": "Normal", "poder": 40, "precision": 100},
    "Hiperrayo": {"tipo": "Normal", "poder": 150, "precision": 90},
}

# Crear lista de Pokemon
lista_pokemon = [
    Pokemon("Pikachu", "Eléctrico", 55, 40, 35, ["Impactrueno", "Ataque Rápido", "Rayo", "Trueno"], 25, "sprites/pikachu_small.gif", "sprites/pikachu_large.gif"),
    Pokemon("Charmander", "Fuego", 52, 43, 39, ["Ascuas", "Giro Fuego", "Lanzallamas", "Placaje"], 4, "sprites/charmander_small.gif", "sprites/charmander_large.gif"),
    Pokemon("Squirtle", "Agua", 48, 65, 44, ["Pistola Agua", "Rayo Burbuja", "Surf", "Placaje"], 7, "sprites/squirtle_small.gif", "sprites/squirtle_large.gif"),
    Pokemon("Bulbasaur", "Planta", 49, 49, 45, ["Látigo Cepa", "Hoja Afilada", "Rayo Solar", "Placaje"], 1, "sprites/bulbasaur_small.gif", "sprites/bulbasaur_large.gif"),
    Pokemon("Charizard", "Fuego", 84, 78, 78, ["Lanzallamas", "Llamarada", "Giro Fuego", "Hiperrayo"], 6, "sprites/charizard_small.gif", "sprites/charizard_large.gif"),
    Pokemon("Blastoise", "Agua", 83, 100, 79, ["Hidrobomba", "Surf", "Pistola Agua", "Placaje"], 9, "sprites/blastoise_small.gif", "sprites/blastoise_large.gif"),
    Pokemon("Venusaur", "Planta", 82, 83, 80, ["Rayo Solar", "Bomba Germen", "Látigo Cepa", "Placaje"], 3, "sprites/venusaur_small.gif", "sprites/venusaur_large.gif"),
    Pokemon("Raichu", "Eléctrico", 90, 55, 60, ["Trueno", "Rayo", "Impactrueno", "Ataque Rápido"], 26, "sprites/raichu_small.gif", "sprites/raichu_large.gif"),
    Pokemon("Jigglypuff", "Normal", 45, 20, 115, ["Placaje", "Ataque Rápido", "Hiperrayo", "Placaje"], 39, "sprites/jigglypuff_small.gif", "sprites/jigglypuff_large.gif"),
    Pokemon("Meowth", "Normal", 45, 35, 40, ["Placaje", "Ataque Rápido", "Hiperrayo", "Placaje"], 52, "sprites/meowth_small.gif", "sprites/meowth_large.gif"),
    Pokemon("Psyduck", "Agua", 52, 48, 50, ["Pistola Agua", "Rayo Burbuja", "Surf", "Placaje"], 54, "sprites/psyduck_small.gif", "sprites/psyduck_large.gif"),
    Pokemon("Growlithe", "Fuego", 70, 45, 55, ["Ascuas", "Lanzallamas", "Giro Fuego", "Placaje"], 58, "sprites/growlithe_small.gif", "sprites/growlithe_large.gif"),
    Pokemon("Poliwag", "Agua", 50, 40, 40, ["Pistola Agua", "Rayo Burbuja", "Surf", "Placaje"], 60, "sprites/poliwag_small.gif", "sprites/poliwag_large.gif"),
    Pokemon("Machop", "Lucha", 80, 50, 70, ["Placaje", "Ataque Rápido", "Hiperrayo", "Placaje"], 66, "sprites/machop_small.gif", "sprites/machop_large.gif"),
    Pokemon("Geodude", "Roca", 80, 100, 40, ["Placaje", "Ataque Rápido", "Hiperrayo", "Placaje"], 74, "sprites/geodude_small.gif", "sprites/geodude_large.gif"),
    Pokemon("Magikarp", "Agua", 10, 55, 20, ["Placaje", "Ataque Rápido", "Pistola Agua", "Rayo Burbuja"], 129, "sprites/magikarp_small.gif", "sprites/magikarp_large.gif"),
]

# Cargar sprites para todos los Pokemon
for pokemon in lista_pokemon:
    pokemon.cargar_sprites()

# Funciones para cargar sonidos (con manejo de errores)
def cargar_sonido(ruta):
    if os.path.exists(ruta):
        try:
            return pygame.mixer.Sound(ruta)
        except:
            return None
    return None

# Sonidos
sonido_scroll = cargar_sonido("sounds/scroll.mp3")
sonido_select = cargar_sonido("sounds/select.mp3")
sonido_ataque = cargar_sonido("sounds/attack.mp3")

def reproducir_sonido(sonido):
    if sonido:
        try:
            sonido.play()
        except:
            pass

# Función para dibujar texto con sombra
def dibujar_texto_sombra(texto, fuente, color, x, y, centrado=False):
    # Sombra
    texto_surface_sombra = fuente.render(texto, True, NEGRO)
    if centrado:
        rect_sombra = texto_surface_sombra.get_rect(center=(x+2, y+2))
    else:
        rect_sombra = texto_surface_sombra.get_rect(topleft=(x+2, y+2))
    pantalla.blit(texto_surface_sombra, rect_sombra)
    
    # Texto principal
    texto_surface = fuente.render(texto, True, color)
    if centrado:
        rect = texto_surface.get_rect(center=(x, y))
    else:
        rect = texto_surface.get_rect(topleft=(x, y))
    pantalla.blit(texto_surface, rect)

# Función para dibujar botón con efecto 3D
def dibujar_boton_3d(texto, x, y, ancho, alto, color_base, color_sombra, color_texto=BLANCO):
    # Sombra (más oscura)
    pygame.draw.rect(pantalla, color_sombra, (x+5, y+5, ancho, alto), border_radius=10)
    # Botón principal
    pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto), border_radius=10)
    # Borde
    pygame.draw.rect(pantalla, NEGRO, (x, y, ancho, alto), 3, border_radius=10)
    # Texto
    dibujar_texto_sombra(texto, fuente_normal, color_texto, x + ancho // 2, y + alto // 2, centrado=True)

# Función para dibujar panel con efecto 3D
def dibujar_panel_3d(x, y, ancho, alto, color_base):
    # Sombra
    pygame.draw.rect(pantalla, (max(0, color_base[0]-50), max(0, color_base[1]-50), max(0, color_base[2]-50)), 
                    (x+5, y+5, ancho, alto), border_radius=15)
    # Panel principal
    pygame.draw.rect(pantalla, color_base, (x, y, ancho, alto), border_radius=15)
    # Borde
    pygame.draw.rect(pantalla, NEGRO, (x, y, ancho, alto), 3, border_radius=15)

# Función para dibujar el menú principal
def dibujar_menu():
    # Fondo degradado
    for i in range(ALTO):
        color_r = int(CREMA[0] + (AZUL_CLARO[0] - CREMA[0]) * i / ALTO)
        color_g = int(CREMA[1] + (AZUL_CLARO[1] - CREMA[1]) * i / ALTO)
        color_b = int(CREMA[2] + (AZUL_CLARO[2] - CREMA[2]) * i / ALTO)
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, i), (ANCHO, i))
    
    # Título
    dibujar_texto_sombra("POKEMON GAME", fuente_titulo, ROJO, ANCHO // 2, 150, centrado=True)
    
    # Botones
    dibujar_boton_3d("SELECCIONAR POKEMON", ANCHO // 2 - 200, 300, 400, 60, VERDE, (0, 150, 0))
    dibujar_boton_3d("VER POKEDEX", ANCHO // 2 - 200, 400, 400, 60, AZUL, (0, 50, 180))
    dibujar_boton_3d("SALIR", ANCHO // 2 - 200, 500, 400, 60, ROJO, (180, 0, 0))
    
    # Instrucciones
    dibujar_texto_sombra("Haz clic en una opción para comenzar", fuente_pequena, NEGRO, ANCHO // 2, 650, centrado=True)

# Función para dibujar la pantalla de selección
def dibujar_seleccion():
    global pokemon_seleccionado_1, pokemon_seleccionado_2
    
    # Fondo degradado
    for i in range(ALTO):
        color_r = int(CREMA[0] + (AZUL_CLARO[0] - CREMA[0]) * i / ALTO)
        color_g = int(CREMA[1] + (AZUL_CLARO[1] - CREMA[1]) * i / ALTO)
        color_b = int(CREMA[2] + (AZUL_CLARO[2] - CREMA[2]) * i / ALTO)
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, i), (ANCHO, i))
    
    # Título
    dibujar_texto_sombra("SELECCIONA TU POKEMON", fuente_grande, ROJO, ANCHO // 2, 50, centrado=True)
    
    # Mostrar 6 Pokemon para seleccionar
    pokemon_muestra = lista_pokemon[:6]
    for i, pokemon in enumerate(pokemon_muestra):
        col = i % 3
        fila = i // 3
        x = 150 + col * 350
        y = 150 + fila * 300
        
        # Panel del Pokemon
        color_panel = AMARILLO if pokemon == pokemon_seleccionado_1 else BLANCO
        dibujar_panel_3d(x - 80, y - 80, 160, 240, color_panel)
        
        # Sprite
        sprite_surface = pokemon.sprite_pequeno_animado.get_surface()
        sprite_rect = sprite_surface.get_rect(center=(x, y))
        pantalla.blit(sprite_surface, sprite_rect)
        
        # Nombre
        dibujar_texto_sombra(pokemon.nombre, fuente_normal, NEGRO, x, y + 80, centrado=True)
    
    # Botón de iniciar combate
    if pokemon_seleccionado_1:
        dibujar_boton_3d("INICIAR COMBATE", ANCHO // 2 - 150, 650, 300, 60, VERDE, (0, 150, 0))
    
    # Botón de volver
    dibujar_boton_3d("← VOLVER", 50, 50, 150, 50, GRIS, (80, 80, 80))

# Función para dibujar la galería (nueva versión con grid/detalle)
def dibujar_galeria():
    global modo_galeria
    
    if modo_galeria == "grid":
        dibujar_galeria_grid()
    else:
        dibujar_galeria_detalle()

# Función para dibujar la galería en modo grid
def dibujar_galeria_grid():
    global hover_pokemon_index
    
    # Fondo degradado
    for i in range(ALTO):
        color_r = int(CREMA[0] + (AZUL_CLARO[0] - CREMA[0]) * i / ALTO)
        color_g = int(CREMA[1] + (AZUL_CLARO[1] - CREMA[1]) * i / ALTO)
        color_b = int(CREMA[2] + (AZUL_CLARO[2] - CREMA[2]) * i / ALTO)
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, i), (ANCHO, i))
    
    # Panel superior con título
    dibujar_panel_3d(50, 20, ANCHO - 100, 80, ROJO)
    dibujar_texto_sombra("POKEDEX", fuente_titulo, BLANCO, ANCHO // 2, 60, centrado=True)
    
    # Calcular dimensiones de la cuadrícula
    margen_horizontal = int(ANCHO * 0.05)
    margen_superior = int(ALTO * 0.15)
    columnas = 4
    filas = 4
    espaciado = 20
    
    ancho_disponible = ANCHO - 2 * margen_horizontal - (columnas - 1) * espaciado
    alto_disponible = ALTO - margen_superior - 150 - (filas - 1) * espaciado
    
    ancho_celda = ancho_disponible // columnas
    alto_celda = alto_disponible // filas
    
    # Obtener posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hover_pokemon_index = None
    
    # Dibujar cuadrícula de Pokemon (16 primeros)
    for i in range(min(16, len(lista_pokemon))):
        pokemon = lista_pokemon[i]
        col = i % columnas
        fila = i // columnas
        
        x = margen_horizontal + col * (ancho_celda + espaciado)
        y = margen_superior + fila * (alto_celda + espaciado)
        
        # Verificar si el mouse está sobre este Pokemon
        mouse_sobre_pokemon = (x <= mouse_x <= x + ancho_celda and 
                              y <= mouse_y <= y + alto_celda)
        
        if mouse_sobre_pokemon:
            hover_pokemon_index = i
        
        # Calcular escala y colores según hover
        if mouse_sobre_pokemon:
            escala = 1.1
            color_fondo = AMARILLO
            color_borde = ROJO
            borde_grosor = 5
        else:
            escala = 1.0
            color_fondo = BLANCO
            color_borde = NEGRO
            borde_grosor = 3
        
        # Calcular posición y tamaño con escala
        centro_x = x + ancho_celda // 2
        centro_y = y + alto_celda // 2
        ancho_escalado = int(ancho_celda * escala)
        alto_escalado = int(alto_celda * escala)
        x_escalado = centro_x - ancho_escalado // 2
        y_escalado = centro_y - alto_escalado // 2
        
        # Dibujar celda
        pygame.draw.rect(pantalla, (max(0, color_fondo[0]-30), max(0, color_fondo[1]-30), max(0, color_fondo[2]-30)),
                        (x_escalado+5, y_escalado+5, ancho_escalado, alto_escalado), border_radius=10)
        pygame.draw.rect(pantalla, color_fondo, (x_escalado, y_escalado, ancho_escalado, alto_escalado), border_radius=10)
        pygame.draw.rect(pantalla, color_borde, (x_escalado, y_escalado, ancho_escalado, alto_escalado), borde_grosor, border_radius=10)
        
        # Número de Pokédex en esquina superior izquierda
        numero_texto = f"#{pokemon.id_pokedex:03d}"
        dibujar_texto_sombra(numero_texto, fuente_muy_pequena, NEGRO, x_escalado + 10, y_escalado + 10)
        
        # Sprite
        sprite_surface = pokemon.sprite_pequeno_animado.get_surface()
        sprite_escalado = pygame.transform.scale(sprite_surface, 
                                                 (int(sprite_surface.get_width() * escala), 
                                                  int(sprite_surface.get_height() * escala)))
        sprite_rect = sprite_escalado.get_rect(center=(centro_x, centro_y - 10))
        pantalla.blit(sprite_escalado, sprite_rect)
        
        # Nombre centrado en la parte inferior
        dibujar_texto_sombra(pokemon.nombre, fuente_muy_pequena, NEGRO, centro_x, y_escalado + alto_escalado - 20, centrado=True)
    
    # Panel inferior con instrucciones
    dibujar_panel_3d(50, ALTO - 80, ANCHO - 100, 60, AZUL)
    dibujar_texto_sombra("Haz clic en un Pokémon para ver detalles | ESC: Volver al menú", 
                        fuente_pequena, BLANCO, ANCHO // 2, ALTO - 50, centrado=True)

# Función para dibujar la galería en modo detalle
def dibujar_galeria_detalle():
    global pokemon_detalle
    
    if not pokemon_detalle:
        return
    
    # Fondo degradado
    for i in range(ALTO):
        color_r = int(CREMA[0] + (AZUL_CLARO[0] - CREMA[0]) * i / ALTO)
        color_g = int(CREMA[1] + (AZUL_CLARO[1] - CREMA[1]) * i / ALTO)
        color_b = int(CREMA[2] + (AZUL_CLARO[2] - CREMA[2]) * i / ALTO)
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, i), (ANCHO, i))
    
    # Botón volver
    dibujar_boton_3d("← Volver", 50, 50, 120, 50, GRIS, (80, 80, 80), BLANCO)
    
    # Sprite grande del Pokemon (lado izquierdo)
    sprite_x = 250
    sprite_y = ALTO // 2 - 50
    sprite_surface = pokemon_detalle.sprite_grande_animado.get_surface()
    sprite_rect = sprite_surface.get_rect(center=(sprite_x, sprite_y))
    
    # Panel detrás del sprite
    panel_margen = 30
    dibujar_panel_3d(sprite_rect.left - panel_margen, sprite_rect.top - panel_margen,
                     sprite_rect.width + 2*panel_margen, sprite_rect.height + 2*panel_margen, BLANCO)
    pantalla.blit(sprite_surface, sprite_rect)
    
    # Placa con nombre debajo del sprite
    nombre_y = sprite_rect.bottom + 50
    dibujar_panel_3d(sprite_rect.left - 20, nombre_y - 30, sprite_rect.width + 40, 60, AMARILLO)
    dibujar_texto_sombra(pokemon_detalle.nombre, fuente_grande, NEGRO, sprite_x, nombre_y, centrado=True)
    dibujar_texto_sombra(f"#{pokemon_detalle.id_pokedex:03d}", fuente_pequena, GRIS, sprite_x, nombre_y + 30, centrado=True)
    
    # Panel de estadísticas (lado derecho)
    stats_x = 550
    stats_y = 150
    stats_ancho = 600
    stats_alto = 550
    
    dibujar_panel_3d(stats_x, stats_y, stats_ancho, stats_alto, BLANCO)
    
    # Título de estadísticas
    dibujar_texto_sombra("ESTADISTICAS", fuente_grande, ROJO, stats_x + stats_ancho // 2, stats_y + 40, centrado=True)
    
    # Estadísticas
    y_actual = stats_y + 100
    espaciado_stats = 50
    
    stats_info = [
        ("Tipo:", pokemon_detalle.tipo, AZUL),
        ("Ataque:", str(pokemon_detalle.ataque), ROJO),
        ("Defensa:", str(pokemon_detalle.defensa), AZUL),
        ("Salud:", str(pokemon_detalle.salud_maxima), VERDE),
    ]
    
    for etiqueta, valor, color in stats_info:
        dibujar_texto_sombra(etiqueta, fuente_normal, NEGRO, stats_x + 50, y_actual)
        dibujar_texto_sombra(valor, fuente_normal, color, stats_x + 250, y_actual)
        y_actual += espaciado_stats
    
    # Título de movimientos
    y_actual += 30
    dibujar_texto_sombra("MOVIMIENTOS", fuente_grande, ROJO, stats_x + stats_ancho // 2, y_actual, centrado=True)
    y_actual += 60
    
    # Lista de movimientos
    for i, mov_nombre in enumerate(pokemon_detalle.movimientos):
        if mov_nombre in movimientos_disponibles:
            mov_info = movimientos_disponibles[mov_nombre]
            # Nombre del movimiento
            dibujar_texto_sombra(f"{i+1}. {mov_nombre}", fuente_normal, NEGRO, stats_x + 50, y_actual)
            # Tipo y poder
            texto_info = f"{mov_info['tipo']} | Poder: {mov_info['poder']}"
            dibujar_texto_sombra(texto_info, fuente_pequena, GRIS, stats_x + 70, y_actual + 30)
            y_actual += 70

# Función para dibujar el combate
def dibujar_combate():
    global pokemon_jugador, pokemon_enemigo
    
    # Fondo degradado
    for i in range(ALTO):
        color_r = int(CREMA[0] + (AZUL_CLARO[0] - CREMA[0]) * i / ALTO)
        color_g = int(CREMA[1] + (AZUL_CLARO[1] - CREMA[1]) * i / ALTO)
        color_b = int(CREMA[2] + (AZUL_CLARO[2] - CREMA[2]) * i / ALTO)
        pygame.draw.line(pantalla, (color_r, color_g, color_b), (0, i), (ANCHO, i))
    
    # Pokemon enemigo (arriba derecha)
    enemigo_x = ANCHO - 300
    enemigo_y = 150
    dibujar_panel_3d(enemigo_x - 100, enemigo_y - 100, 200, 280, BLANCO)
    sprite_enemigo = pokemon_enemigo.sprite_pequeno_animado.get_surface()
    pantalla.blit(sprite_enemigo, sprite_enemigo.get_rect(center=(enemigo_x, enemigo_y)))
    dibujar_texto_sombra(pokemon_enemigo.nombre, fuente_normal, NEGRO, enemigo_x, enemigo_y + 80, centrado=True)
    
    # Barra de vida enemigo
    barra_ancho = 180
    barra_alto = 20
    porcentaje_vida = pokemon_enemigo.salud / pokemon_enemigo.salud_maxima
    pygame.draw.rect(pantalla, ROJO, (enemigo_x - barra_ancho//2, enemigo_y + 110, barra_ancho, barra_alto))
    pygame.draw.rect(pantalla, VERDE, (enemigo_x - barra_ancho//2, enemigo_y + 110, int(barra_ancho * porcentaje_vida), barra_alto))
    pygame.draw.rect(pantalla, NEGRO, (enemigo_x - barra_ancho//2, enemigo_y + 110, barra_ancho, barra_alto), 2)
    dibujar_texto_sombra(f"{pokemon_enemigo.salud}/{pokemon_enemigo.salud_maxima}", fuente_pequena, NEGRO, 
                        enemigo_x, enemigo_y + 145, centrado=True)
    
    # Pokemon jugador (abajo izquierda)
    jugador_x = 300
    jugador_y = ALTO - 250
    dibujar_panel_3d(jugador_x - 100, jugador_y - 100, 200, 280, BLANCO)
    sprite_jugador = pokemon_jugador.sprite_pequeno_animado.get_surface()
    pantalla.blit(sprite_jugador, sprite_jugador.get_rect(center=(jugador_x, jugador_y)))
    dibujar_texto_sombra(pokemon_jugador.nombre, fuente_normal, NEGRO, jugador_x, jugador_y + 80, centrado=True)
    
    # Barra de vida jugador
    porcentaje_vida_j = pokemon_jugador.salud / pokemon_jugador.salud_maxima
    pygame.draw.rect(pantalla, ROJO, (jugador_x - barra_ancho//2, jugador_y + 110, barra_ancho, barra_alto))
    pygame.draw.rect(pantalla, VERDE, (jugador_x - barra_ancho//2, jugador_y + 110, int(barra_ancho * porcentaje_vida_j), barra_alto))
    pygame.draw.rect(pantalla, NEGRO, (jugador_x - barra_ancho//2, jugador_y + 110, barra_ancho, barra_alto), 2)
    dibujar_texto_sombra(f"{pokemon_jugador.salud}/{pokemon_jugador.salud_maxima}", fuente_pequena, NEGRO, 
                        jugador_x, jugador_y + 145, centrado=True)
    
    # Panel de movimientos
    panel_mov_x = ANCHO - 450
    panel_mov_y = ALTO - 200
    dibujar_panel_3d(panel_mov_x, panel_mov_y, 400, 180, BLANCO)
    dibujar_texto_sombra("Elige un movimiento:", fuente_normal, NEGRO, panel_mov_x + 20, panel_mov_y + 20)
    
    for i, mov in enumerate(pokemon_jugador.movimientos[:4]):
        col = i % 2
        fila = i // 2
        x = panel_mov_x + 20 + col * 190
        y = panel_mov_y + 70 + fila * 50
        dibujar_boton_3d(mov, x, y, 180, 40, AZUL, (0, 50, 180), BLANCO)
    
    # Botón volver
    dibujar_boton_3d("← VOLVER", 50, 50, 150, 50, GRIS, (80, 80, 80))

# Función principal del juego
def main():
    global estado_juego, pokemon_seleccionado_1, pokemon_jugador, pokemon_enemigo
    global indice_galeria, modo_galeria, pokemon_detalle, hover_pokemon_index
    
    ejecutando = True
    
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos
                
                # MENU
                if estado_juego == MENU:
                    # Botón Seleccionar Pokemon
                    if 400 <= mouse_x <= 800 and 300 <= mouse_y <= 360:
                        reproducir_sonido(sonido_select)
                        estado_juego = SELECCION
                    # Botón Ver Pokedex
                    elif 400 <= mouse_x <= 800 and 400 <= mouse_y <= 460:
                        reproducir_sonido(sonido_select)
                        estado_juego = GALERIA
                        modo_galeria = "grid"
                    # Botón Salir
                    elif 400 <= mouse_x <= 800 and 500 <= mouse_y <= 560:
                        ejecutando = False
                
                # SELECCION
                elif estado_juego == SELECCION:
                    # Botón volver
                    if 50 <= mouse_x <= 200 and 50 <= mouse_y <= 100:
                        reproducir_sonido(sonido_select)
                        estado_juego = MENU
                        pokemon_seleccionado_1 = None
                    # Seleccionar Pokemon
                    else:
                        pokemon_muestra = lista_pokemon[:6]
                        for i, pokemon in enumerate(pokemon_muestra):
                            col = i % 3
                            fila = i // 3
                            x = 150 + col * 350
                            y = 150 + fila * 300
                            if x - 80 <= mouse_x <= x + 80 and y - 80 <= mouse_y <= y + 160:
                                reproducir_sonido(sonido_select)
                                pokemon_seleccionado_1 = pokemon
                    # Botón iniciar combate
                    if pokemon_seleccionado_1 and ANCHO // 2 - 150 <= mouse_x <= ANCHO // 2 + 150 and 650 <= mouse_y <= 710:
                        reproducir_sonido(sonido_select)
                        import random
                        pokemon_jugador = pokemon_seleccionado_1
                        pokemon_jugador.curar()
                        pokemon_enemigo = random.choice([p for p in lista_pokemon if p != pokemon_jugador])
                        pokemon_enemigo.curar()
                        estado_juego = COMBATE
                
                # GALERIA
                elif estado_juego == GALERIA:
                    if modo_galeria == "grid":
                        # Detectar click en Pokemon
                        if hover_pokemon_index is not None and 0 <= hover_pokemon_index < len(lista_pokemon):
                            reproducir_sonido(sonido_scroll)
                            pokemon_detalle = lista_pokemon[hover_pokemon_index]
                            modo_galeria = "detalle"
                    elif modo_galeria == "detalle":
                        # Botón volver
                        if 50 <= mouse_x <= 170 and 50 <= mouse_y <= 100:
                            reproducir_sonido(sonido_scroll)
                            modo_galeria = "grid"
                            pokemon_detalle = None
                
                # COMBATE
                elif estado_juego == COMBATE:
                    # Botón volver
                    if 50 <= mouse_x <= 200 and 50 <= mouse_y <= 100:
                        reproducir_sonido(sonido_select)
                        estado_juego = SELECCION
                    # Botones de movimientos
                    else:
                        panel_mov_x = ANCHO - 450
                        panel_mov_y = ALTO - 200
                        for i, mov in enumerate(pokemon_jugador.movimientos[:4]):
                            col = i % 2
                            fila = i // 2
                            x = panel_mov_x + 20 + col * 190
                            y = panel_mov_y + 70 + fila * 50
                            if x <= mouse_x <= x + 180 and y <= mouse_y <= y + 40:
                                reproducir_sonido(sonido_ataque)
                                # Realizar ataque
                                import random
                                if mov in movimientos_disponibles:
                                    mov_info = movimientos_disponibles[mov]
                                    if random.randint(1, 100) <= mov_info['precision']:
                                        dano = pokemon_enemigo.recibir_dano(mov_info['poder'])
                                        print(f"{pokemon_jugador.nombre} usó {mov}! Causó {dano} de daño")
                                
                                # Turno del enemigo
                                if pokemon_enemigo.esta_vivo():
                                    mov_enemigo = random.choice(pokemon_enemigo.movimientos)
                                    if mov_enemigo in movimientos_disponibles:
                                        mov_info_e = movimientos_disponibles[mov_enemigo]
                                        if random.randint(1, 100) <= mov_info_e['precision']:
                                            dano_e = pokemon_jugador.recibir_dano(mov_info_e['poder'])
                                            print(f"{pokemon_enemigo.nombre} usó {mov_enemigo}! Causó {dano_e} de daño")
                                
                                # Verificar ganador
                                if not pokemon_enemigo.esta_vivo():
                                    print(f"¡{pokemon_jugador.nombre} ganó!")
                                    estado_juego = SELECCION
                                elif not pokemon_jugador.esta_vivo():
                                    print(f"¡{pokemon_enemigo.nombre} ganó!")
                                    estado_juego = SELECCION
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if estado_juego == GALERIA:
                        if modo_galeria == "detalle":
                            reproducir_sonido(sonido_scroll)
                            modo_galeria = "grid"
                            pokemon_detalle = None
                        else:
                            reproducir_sonido(sonido_select)
                            estado_juego = MENU
                    elif estado_juego == SELECCION or estado_juego == COMBATE:
                        reproducir_sonido(sonido_select)
                        estado_juego = MENU
        
        # Dibujar según el estado
        if estado_juego == MENU:
            dibujar_menu()
        elif estado_juego == SELECCION:
            dibujar_seleccion()
        elif estado_juego == GALERIA:
            dibujar_galeria()
        elif estado_juego == COMBATE:
            dibujar_combate()
        
        pygame.display.flip()
        reloj.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
