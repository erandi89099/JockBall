"""Genera modelos, lang, equipo, recetas y texturas de armadura puesta. Uso: python3 tools/gen_assets.py"""
import json, os
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(ROOT, "src/main/resources")
A = os.path.join(RES, "assets/jockball")
D = os.path.join(RES, "data/jockball")
PIECES = ["helmet", "shoulder_pads", "pants", "cleats"]
LEVELS = {  # principal, sombra, detalle
    1: ((139, 94, 60), (92, 60, 36), (200, 170, 120)),
    2: ((150, 150, 155), (100, 100, 108), (200, 60, 50)),
    3: ((50, 100, 200), (30, 60, 130), (240, 240, 240)),
    4: ((40, 160, 90), (20, 100, 55), (220, 225, 230)),
    5: ((235, 190, 40), (160, 120, 20), (25, 25, 30)),
}

def w(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(data, str): f.write(data)
        else: json.dump(data, f, indent=2, ensure_ascii=False)

# ---------- modelos + client items ----------
for name in [f"{p}_l{l}" for p in PIECES for l in LEVELS] + ["trophy", "upgrade_template"]:
    w(f"{A}/models/item/{name}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"jockball:item/{name}"}})
    w(f"{A}/items/{name}.json", {"model": {"type": "minecraft:model", "model": f"jockball:item/{name}"}})

# ---------- equipment asset (que textura se ve puesta) ----------
for l in LEVELS:
    w(f"{A}/equipment/level_{l}.json", {"layers": {
        "humanoid": [{"texture": f"jockball:level_{l}"}],
        "humanoid_leggings": [{"texture": f"jockball:level_{l}"}]}})

# ---------- idiomas ----------
ES_LV = {1: ("Viejo", "Viejas", "Viejos"), 2: ("de Entrenamiento",) * 3, 3: ("de Colegio",) * 3,
         4: ("Profesional",) * 3, 5: ("del Capitán",) * 3}
EN_LV = {1: "Old", 2: "Training", 3: "College", 4: "Pro", 5: "Captain's"}
ES_P = {"helmet": ("Casco", 0), "shoulder_pads": ("Hombreras", 1), "pants": ("Fundas", 1), "cleats": ("Tachos", 2)}
EN_P = {"helmet": "Helmet", "shoulder_pads": "Shoulder Pads", "pants": "Pants", "cleats": "Cleats"}
es = {"item.jockball.trophy": "Trofeo", "item.jockball.upgrade_template": "Plantilla de Mejora"}
en = {"item.jockball.trophy": "Trophy", "item.jockball.upgrade_template": "Upgrade Template"}
for l in LEVELS:
    for p in PIECES:
        n, g = ES_P[p]
        es[f"item.jockball.{p}_l{l}"] = f"{n} {ES_LV[l][g]}"
        en[f"item.jockball.{p}_l{l}"] = f"{EN_LV[l]} {EN_P[p]}"
w(f"{A}/lang/es_es.json", es); w(f"{A}/lang/en_us.json", en)

# ---------- recetas de mejora (herreria): pieza + Trofeo ----------
for p in PIECES:
    for l in range(1, 5):
        w(f"{D}/recipe/upgrade_{p}_l{l+1}.json", {
            "type": "minecraft:smithing_transform",
            "template": "jockball:upgrade_template",
            "base": f"jockball:{p}_l{l}",
            "addition": "jockball:trophy",
            "result": {"id": f"jockball:{p}_l{l+1}"}})

# loot de los cofres de vestidores (solo equipo nivel 1-3 y plantillas; nivel 4-5 se ganan en el campo)
def item(name, weight, lo=1, hi=1):
    e = {"type": "minecraft:item", "name": name, "weight": weight}
    if hi > 1:
        e["functions"] = [{"function": "minecraft:set_count", "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]
    return e
gear = [item(f"jockball:{p}_l{l}", {1: 6, 2: 4, 3: 2}[l]) for p in PIECES for l in (1, 2, 3)]
w(f"{D}/loot_table/chests/locker_room.json", {"type": "minecraft:chest", "pools": [
    {"rolls": {"type": "minecraft:uniform", "min": 1, "max": 2}, "entries": [item("jockball:upgrade_template", 1, 1, 2), {"type": "minecraft:empty", "weight": 2}]},
    {"rolls": {"type": "minecraft:uniform", "min": 2, "max": 4}, "entries": gear + [{"type": "minecraft:empty", "weight": 20}]},
    {"rolls": {"type": "minecraft:uniform", "min": 2, "max": 5}, "entries": [item("minecraft:bread", 6, 1, 4), item("minecraft:cooked_beef", 4, 1, 3), item("minecraft:golden_apple", 1), item("minecraft:string", 3, 1, 3)]}
]})

# tag de reparacion (vacio por ahora)
w(f"{D}/tags/item/repairs_gear.json", {"values": []})

# ---------- texturas de armadura puesta (64x32) ----------
def box(img, x, y, W, H, Dp, col, dark, acc, detail=None, rows=None):
    """Pinta las 6 caras de una caja en el mapa UV vanilla."""
    px = img.load()
    def fill(x0, y0, w_, h_, c, only_rows=None):
        for j in range(h_):
            if only_rows is not None and j not in only_rows: continue
            for i in range(w_):
                px[x0 + i, y0 + j] = c + (255,)
    fill(x + Dp, y, W, Dp, acc)                  # arriba
    fill(x + Dp + W, y, W, Dp, dark)             # abajo
    fill(x, y + Dp, Dp, H, dark, rows)           # lado
    fill(x + Dp, y + Dp, W, H, col, rows)        # frente
    fill(x + Dp + W, y + Dp, Dp, H, dark, rows)  # lado
    fill(x + 2 * Dp + W, y + Dp, W, H, col, rows)  # espalda

def make(l):
    col, dark, acc = LEVELS[l]
    # capa 1: casco, torso, brazos (hombreras), botas
    a = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    box(a, 0, 0, 8, 8, 8, col, dark, acc, rows=range(0, 4))           # casco: solo parte alta de la cara
    px = a.load()
    for i in range(8, 16):                                             # rejilla de la mascara
        for j in (12, 14): px[i, j] = acc + (255,) if i % 2 == 0 else dark + (255,)
    box(a, 16, 16, 8, 12, 4, col, dark, acc)                           # torso
    for i in range(20, 28): px[i, 20] = acc + (255,)                   # franja
    box(a, 40, 16, 4, 12, 4, col, dark, acc, rows=range(0, 12))        # brazo (hombrera)
    for j in range(16 + 4, 16 + 12): pass
    box(a, 0, 16, 4, 12, 4, col, dark, acc, rows=range(8, 12))         # botas (parte baja de la pierna)
    a.save(os.path.join(A, f"textures/entity/equipment/humanoid/level_{l}.png"))
    # capa 2: fundas (cintura y piernas)
    b = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
    box(b, 16, 16, 8, 12, 4, col, dark, acc, rows=range(8, 12))        # cintura
    box(b, 0, 16, 4, 12, 4, col, dark, acc, rows=range(0, 8))          # muslos
    pb = b.load()
    for j in range(16 + 4, 16 + 12): pb[5, j] = acc + (255,)           # franja lateral
    b.save(os.path.join(A, f"textures/entity/equipment/humanoid_leggings/level_{l}.png"))

for sub in ("humanoid", "humanoid_leggings"):
    os.makedirs(os.path.join(A, f"textures/entity/equipment/{sub}"), exist_ok=True)
for l in LEVELS: make(l)
print("Assets generados.")
