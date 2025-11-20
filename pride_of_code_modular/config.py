# Game window settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
GAME_TITLE = "Code of Pride: Marching Band Director"

# Save system version
SAVE_VERSION = 1

# Pride of Casa Grande Colors (Blue and Gold)
COLOR_BLUE = (46, 94, 170)  # Primary blue - Casa Grande High School Blue
COLOR_GOLD = (255, 184, 28)  # Primary gold - Casa Grande High School Gold
COLOR_BG = (20, 20, 30)  # Dark background for contrast
COLOR_TEXT = (240, 240, 240)  # White text for readability
COLOR_FIELD_GREEN = (34, 139, 34)  # Field grass - classic green
COLOR_FIELD_LINES = (255, 255, 255)  # Yard lines - white for visibility

# Band Section Colors (for easy identification)
SECTION_COLORS = {
    'brass': (255, 215, 0),      # Gold/Yellow - Brass instruments
    'woodwind': (144, 238, 144), # Light Green - Woodwind instruments
    'percussion': (220, 20, 60), # Crimson Red - Percussion instruments
    'guard': (186, 85, 211)      # Medium Orchid Purple - Color guard
}

# Field dimensions (in yards)
FIELD_LENGTH = 100  # 100 yards
FIELD_WIDTH = 53.33  # 53.33 yards (160 feet)
FIELD_HASH_WIDTH = 13.33  # Distance between hash marks

# Pixel dimensions for field view
FIELD_PIXEL_WIDTH = 600
FIELD_PIXEL_HEIGHT = 400
FIELD_OFFSET_X = 750  # Position on screen
FIELD_OFFSET_Y = 80

# Grid settings
GRID_STEPS = 4  # 4 steps per 5 yards

# Editor defaults
EDITOR_FONT = "consolas"
EDITOR_FONT_SIZE = 16
EDITOR_WIDTH = 680
EDITOR_HEIGHT = 600
EDITOR_X = 20
EDITOR_Y = 140

# Paths
ASSETS_DIR = "assets"

# Animation settings
MARCHER_MOVE_SPEED = 2.0  # pixels per frame
MARCHER_SIZE = 8  # 8x8 pixel sprite (Retro Bowl style)

# Scoring
MAX_PRIDE_POINTS = 100.0
MIN_PRIDE_POINTS = 0.0

# Game branding elements
BRAND_NAME = "Pride of Casa Grande"
BRAND_MASCOT = "Cougar"
BRAND_MOTTO = "Strike Gold!"

# Audio settings
AUDIO_ENABLED = True
DEFAULT_VOLUME = 0.7

# Difficulty settings
DIFFICULTY_LEVELS = {
    'beginner': {'description': 'Perfect for first-time programmers', 'band_size': 8},
    'intermediate': {'description': 'For those with some coding experience', 'band_size': 16},
    'advanced': {'description': 'Challenging exercises for experienced coders', 'band_size': 24}
}