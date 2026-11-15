"""Genera texturas provisionales 16x16 de JockBall. Uso: python3 tools/gen_textures.py"""
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "src/main/resources/assets/jockball/textures/item")
os.makedirs(OUT, exist_ok=True)

# nivel: (principal, sombra, detalle)
LEVELS = {
    1: ((139, 94, 60), (92, 60, 36), (200, 170, 120)),     # cuero viejo
    2: ((150, 150, 155), (100, 100, 108), (200, 60, 50)),  # lona gris / rojo
    3: ((50, 100, 200), (30, 60, 130), (240, 240, 240)),   # equipo de colegio azul
    4: ((40, 160, 90), (20, 100, 55), (220, 225, 230)),    # profesional verde/plata
    5: ((235, 190, 40), (160, 120, 20), (25, 25, 30)),     # capitan oro/negro
}

SHAPES = {
 "helmet": ["................",
            "....########....",
            "..############..",
            ".##############.",
            ".##############.",
            ".##..######..##.",
            ".##..######..##.",
            ".##..######..##.",
            ".##..######..##.",
            ".##..........##.",
            ".##..........##.",
            "................",
            "................",
            "................",
            "................",
            "................"],
 "chestplate": ["................",
               "..####....####..",
               ".######..######.",
               ".##############.",
               ".##############.",
               "..############..",
               "..############..",
               "..############..",
               "..############..",
               "..############..",
               "...##########...",
               "................",
               "................",
               "................",
               "................",
               "................"],
 "leggings": ["................",
             "..############..",
             "..############..",
             "..############..",
             "..###......###..",
             "..###......###..",
             "..###......###..",
             "..###......###..",
             "..###......###..",
             "..###......###..",
             "..###......###..",
             "..###......###..",
             "................",
             "................",
             "................",
             "................"],
 "boots": ["................",
          "................",
          "................",
          "................",
          "..###......###..",
          "..###......###..",
          "..###......###..",
          ".####......####.",
          ".#####....#####.",
          ".#####....#####.",
          ".#.#.#....#.#.#.",
          "................",
          "................",
          "................",
          "................",
          "................"],
}

def render(shape, lv):
    main, dark, acc = LEVELS[lv]
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    px = img.load()
    rows = SHAPES[shape]
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            if c != "#":
                continue
            below = y + 1 < 16 and rows[y + 1][x] == "#"
            side = x + 1 < 16 and rows[y][x + 1] == "#"
            col = main if (below and side) else dark
            if y == 2 and shape != "boots":
                col = acc
            px[x, y] = col + (255,)
    # numero de nivel como puntos de detalle abajo
    for i in range(lv):
        px[1 + i * 2, 14] = acc + (255,)
    return img

names = {"helmet": "helmet", "chestplate": "shoulder_pads", "leggings": "pants", "boots": "cleats"}
for lv in LEVELS:
    for shape, n in names.items():
        render(shape, lv).save(os.path.join(OUT, f"{n}_l{lv}.png"))

# Mineral "Trofeo": pepita dorada con copa
t = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); p = t.load()
gold, dk, hi = (245, 200, 50), (170, 120, 20), (255, 245, 170)
cup = ["....########....",
       "...##########...",
       "..############..",
       "..############..",
       "..############..",
       "...##########...",
       "....########....",
       ".....######.....",
       "......####......",
       "......####......",
       ".....######.....",
       "....########...."]
for y, r in enumerate(cup):
    for x, c in enumerate(r):
        if c == "#":
            p[x, y + 2] = gold + (255,) if (x + y) % 5 else hi + (255,)
for x in range(4, 12):
    p[x, 14] = dk + (255,)
t.save(os.path.join(OUT, "trophy.png"))
# Plantilla de mejora: pizarra de jugadas
tp = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); q = tp.load()
board, edge, line, red, blue = (235, 235, 225), (90, 60, 35), (60, 60, 60), (200, 50, 45), (45, 90, 200)
for y in range(1, 15):
    for x in range(2, 14):
        q[x, y] = (edge if x in (2, 13) or y in (1, 14) else board) + (255,)
for (x, y) in [(5, 4), (6, 5), (9, 4), (10, 5), (5, 5), (10, 4)]:
    pass
for (x, y) in [(4, 4), (5, 5), (6, 6), (4, 6), (6, 4)]:      # X
    q[x, y] = red + (255,)
for i in range(5):                                           # flecha de jugada
    q[6 + i, 9] = line + (255,)
q[10, 8] = q[10, 10] = line + (255,)
for (x, y) in [(10, 5), (11, 5), (10, 6), (11, 6), (9, 12), (10, 12), (9, 11), (10, 11)]:  # O
    q[x, y] = blue + (255,)
tp.save(os.path.join(OUT, "upgrade_template.png"))
print("Texturas generadas en", os.path.abspath(OUT))
