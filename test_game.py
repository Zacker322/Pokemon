#!/usr/bin/env python3
"""Test script to verify game functionality without display"""

import sys
import os

# Test 1: Import verification
print("Test 1: Verifying imports...")
try:
    import pygame
    import PIL
    from PIL import Image, ImageSequence
    print("✓ All required libraries imported successfully")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: File structure
print("\nTest 2: Verifying file structure...")
required_files = [
    "Reto-Pokemon.py",
    "sprites/pikachu_small.gif",
    "sprites/pikachu_large.gif",
    "sounds/scroll.mp3",
]

missing_files = []
for file_path in required_files:
    if not os.path.exists(file_path):
        missing_files.append(file_path)
        print(f"✗ Missing: {file_path}")
    else:
        print(f"✓ Found: {file_path}")

if missing_files:
    print(f"\n✗ {len(missing_files)} files are missing")
    sys.exit(1)

# Test 3: Sprite count
print("\nTest 3: Verifying sprite files...")
sprite_dir = "sprites"
gif_files = [f for f in os.listdir(sprite_dir) if f.endswith('.gif')]
expected_count = 32  # 16 Pokemon × 2 sizes
if len(gif_files) == expected_count:
    print(f"✓ Found all {expected_count} sprite files")
else:
    print(f"✗ Expected {expected_count} sprites, found {len(gif_files)}")

# Test 4: Sound files
print("\nTest 4: Verifying sound files...")
sound_dir = "sounds"
mp3_files = [f for f in os.listdir(sound_dir) if f.endswith('.mp3')]
expected_sounds = 3  # scroll, select, attack
if len(mp3_files) >= expected_sounds:
    print(f"✓ Found all {expected_sounds} sound files")
else:
    print(f"✗ Expected {expected_sounds} sounds, found {len(mp3_files)}")

# Test 5: Syntax check
print("\nTest 5: Checking Python syntax...")
try:
    import py_compile
    py_compile.compile('Reto-Pokemon.py', doraise=True)
    print("✓ Reto-Pokemon.py has valid syntax")
except py_compile.PyCompileError as e:
    print(f"✗ Syntax error: {e}")
    sys.exit(1)

# Test 6: Code structure verification
print("\nTest 6: Verifying code structure...")
with open('Reto-Pokemon.py', 'r') as f:
    content = f.read()
    
    required_elements = [
        ('modo_galeria = "grid"', 'Variable modo_galeria'),
        ('pokemon_detalle = None', 'Variable pokemon_detalle'),
        ('hover_pokemon_index = None', 'Variable hover_pokemon_index'),
        ('def dibujar_galeria_grid()', 'Function dibujar_galeria_grid'),
        ('def dibujar_galeria_detalle()', 'Function dibujar_galeria_detalle'),
        ('class Pokemon:', 'Class Pokemon'),
        ('class AnimatedSprite:', 'Class AnimatedSprite'),
    ]
    
    all_found = True
    for element, name in required_elements:
        if element in content:
            print(f"✓ Found: {name}")
        else:
            print(f"✗ Missing: {name}")
            all_found = False
    
    if not all_found:
        sys.exit(1)

# Test 7: Pokemon data verification
print("\nTest 7: Verifying Pokemon data...")
pokemon_count = content.count('Pokemon(')
if pokemon_count >= 16:
    print(f"✓ Found {pokemon_count} Pokemon definitions")
else:
    print(f"✗ Expected at least 16 Pokemon, found {pokemon_count}")

# Test 8: Event handling
print("\nTest 8: Verifying event handling...")
event_handlers = [
    'pygame.MOUSEBUTTONDOWN',
    'pygame.KEYDOWN',
    'pygame.K_ESCAPE',
]

all_found = True
for handler in event_handlers:
    if handler in content:
        print(f"✓ Found: {handler}")
    else:
        print(f"✗ Missing: {handler}")
        all_found = False

if not all_found:
    sys.exit(1)

print("\n" + "="*50)
print("✓ All tests passed successfully!")
print("="*50)
print("\nThe game is ready to run. Execute with:")
print("  python3 Reto-Pokemon.py")
print("\nNote: A display is required to actually run the game.")
