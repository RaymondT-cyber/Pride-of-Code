# Game window settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
GAME_TITLE = "Code of Pride: Marching Band Director"

# Save system version
SAVE_VERSION = 1

# Pride of Casa Grande Colors (Blue and Gold)
COLOR_BLUE = (46, 94, 170)  # Primary blue
COLOR_GOLD = (255, 184, 28)  # Primary gold
COLOR_BG = (20, 20, 30)  # Dark background
COLOR_TEXT = (240, 240, 240)  # White text
COLOR_FIELD_GREEN = (34, 139, 34)  # Field grass
COLOR_FIELD_LINES = (255, 255, 255)  # Yard lines

# Band Section Colors (for easy identification)
SECTION_COLORS = {
    'brass': (255, 215, 0),      # Gold/Yellow
    'woodwind': (144, 238, 144), # Light Green
    'percussion': (220, 20, 60), # Crimson Red
    'guard': (186, 85, 211)      # Medium Orchid Purple
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