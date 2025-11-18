# Pokémon Game - Pokédex Edition

Un juego de Pokémon desarrollado con Pygame que incluye un sistema de Pokédex interactivo con vista de cuadrícula.

## Características

### 🎮 Funcionalidades del Juego
- **Menú Principal**: Navega entre diferentes modos de juego
- **Selección de Pokémon**: Elige tu Pokémon favorito de una lista de 6
- **Sistema de Combate**: Batalla contra Pokémon enemigos usando movimientos
- **Pokédex Interactivo**: Explora todos los Pokémon disponibles

### 📱 Pokédex - Vista de Cuadrícula
La galería ha sido rediseñada como un Pokédex con las siguientes características:

#### Vista Grid (4x4)
- Muestra 16 Pokémon simultáneamente en una cuadrícula
- Cada celda incluye:
  - Sprite animado del Pokémon (GIF)
  - Nombre del Pokémon
  - Número de Pokédex (ID)

#### Efectos Interactivos
- **Hover Effect**: Cuando pasas el ratón sobre un Pokémon:
  - Se agranda ligeramente (escala 1.1)
  - Fondo cambia a amarillo
  - Borde se vuelve rojo
  - Indica claramente cuál Pokémon está seleccionado

#### Vista Detallada
Al hacer clic en un Pokémon, se abre una vista detallada que muestra:
- Sprite grande animado del Pokémon
- Nombre y número de Pokédex
- Tipo del Pokémon
- Estadísticas completas:
  - Ataque
  - Defensa
  - Salud
- Lista de 4 movimientos con:
  - Nombre del movimiento
  - Tipo
  - Poder

#### Navegación
- **Click**: Abre detalles de un Pokémon en la vista grid
- **← Volver**: Botón en vista detalle para regresar a la cuadrícula
- **ESC**: 
  - En vista detalle: vuelve a la cuadrícula
  - En vista grid: vuelve al menú principal

## 🎨 Diseño Visual

El juego mantiene un estilo visual inspirado en Pokémon:
- Fondo degradado de crema a azul claro
- Botones con efecto 3D
- Bordes redondeados
- Animaciones GIF fluidas
- Colores vibrantes que recuerdan a los juegos clásicos

## 🎵 Sonidos

- `scroll.mp3`: Se reproduce al cambiar entre vistas del Pokédex
- `select.mp3`: Se reproduce al seleccionar opciones
- `attack.mp3`: Se reproduce durante los combates

## 🕹️ Controles

### Menú Principal
- Click en "SELECCIONAR POKEMON": Ir a selección
- Click en "VER POKEDEX": Abrir Pokédex
- Click en "SALIR": Cerrar el juego

### Pokédex
- **Mouse sobre Pokémon**: Efecto hover
- **Click en Pokémon**: Ver detalles
- **Click en "← Volver"**: Regresar a cuadrícula (desde vista detalle)
- **ESC**: Navegar hacia atrás

### Selección
- Click en un Pokémon para seleccionarlo
- Click en "INICIAR COMBATE": Comenzar batalla

### Combate
- Click en un movimiento para atacar
- Click en "← VOLVER": Regresar a selección

## 📋 Requisitos

```bash
pip install pygame pillow
```

## 🚀 Cómo Ejecutar

```bash
python3 Reto-Pokemon.py
```

## 📁 Estructura del Proyecto

```
Pokemon/
├── Reto-Pokemon.py       # Archivo principal del juego
├── sprites/              # Sprites animados de Pokémon
│   ├── pikachu_small.gif
│   ├── pikachu_large.gif
│   └── ...
├── sounds/               # Efectos de sonido
│   ├── scroll.mp3
│   ├── select.mp3
│   └── attack.mp3
└── README.md            # Este archivo
```

## 🎯 Pokémon Disponibles

El juego incluye 16 Pokémon:
1. Pikachu (#025) - Eléctrico
2. Charmander (#004) - Fuego
3. Squirtle (#007) - Agua
4. Bulbasaur (#001) - Planta
5. Charizard (#006) - Fuego
6. Blastoise (#009) - Agua
7. Venusaur (#003) - Planta
8. Raichu (#026) - Eléctrico
9. Jigglypuff (#039) - Normal
10. Meowth (#052) - Normal
11. Psyduck (#054) - Agua
12. Growlithe (#058) - Fuego
13. Poliwag (#060) - Agua
14. Machop (#066) - Lucha
15. Geodude (#074) - Roca
16. Magikarp (#129) - Agua

## 🔧 Características Técnicas

### Arquitectura
- Sistema de estados (MENU, SELECCION, GALERIA, COMBATE)
- Modo de galería dual ("grid" y "detalle")
- Manejo de sprites animados con PIL
- Sistema de detección de hover en tiempo real

### Clases Principales
- `Pokemon`: Gestiona datos y comportamiento de cada Pokémon
- `AnimatedSprite`: Maneja la animación de sprites GIF

### Variables Globales Clave
- `modo_galeria`: Controla vista actual ("grid" o "detalle")
- `pokemon_detalle`: Pokémon seleccionado para vista detallada
- `hover_pokemon_index`: Índice del Pokémon bajo el cursor

## 📝 Notas de Desarrollo

### Cambios Implementados
- ✅ Transformación de carrusel a vista de cuadrícula 4x4
- ✅ Sistema de hover con efectos visuales
- ✅ Vista detallada con información completa
- ✅ Navegación con botón "Volver" y tecla ESC
- ✅ Integración de sonido "scroll.mp3" al cambiar vistas
- ✅ Diseño visual Pokémon con degradados y efectos 3D
- ✅ Animaciones GIF funcionando correctamente
- ✅ Sin modificaciones a combate, menú, o selección existente

## 📜 Licencia

Este es un proyecto educativo de demostración.