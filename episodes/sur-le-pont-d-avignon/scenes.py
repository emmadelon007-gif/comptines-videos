# Scènes de "Sur le pont d'Avignon" : un matin de Provence, Rosette la cigale, Zélie la grenouille
# et Firmin le canard dansent sur le vieux pont de pierre. Le pont s'arrête au milieu du fleuve :
# ils traversent en sautant de nénuphar en nénuphar jusqu'à l'île, dansent sous les arches,
# puis font la grande ronde au soleil couchant.
from papier import *
from papier import Scenes as Base

# ---------- Outils de dessin ----------
def rond(cx, cy, R):
    return [(cx + R * 1.02 * math.sin(i / 200 * 2 * math.pi), cy - R * .96 * math.cos(i / 200 * 2 * math.pi)) for i in range(200)]

def sprite(fn, w, h, sh=(4, 8, 7, .24)):
    S = 2; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), S)
    return shadowed(grain(im.resize((w, h), Image.LANCZOS)), *sh)

def gradient(top, bot, k=1.1):
    a, b = np.array(hexc(top), np.float32), np.array(hexc(bot), np.float32)
    t = np.linspace(0, 1, H)[:, None, None] ** k
    return grain(Image.fromarray(np.repeat(a * (1 - t) + b * t, W, 1).astype(np.uint8), 'RGB').convert('RGBA'))

def eyes(d, cx, cy, Rs, blink):
    ex, ey = Rs * .36, cy - Rs * .1
    for sg in (-1, 1):
        X = cx + sg * ex
        if blink:
            d.arc((X - Rs * .17, ey - Rs * .1, X + Rs * .17, ey + Rs * .16), 200, 340, fill=INK + (255,), width=int(Rs * .05))
        else:
            d.ellipse((X - Rs * .18, ey - Rs * .23, X + Rs * .18, ey + Rs * .23), fill=(255, 255, 255, 255))
            d.ellipse((X - Rs * .115, ey - Rs * .13, X + Rs * .115, ey + Rs * .16), fill=INK + (255,))
            d.ellipse((X - Rs * .05, ey - Rs * .09, X + Rs * .03, ey - Rs * .01), fill=(255, 255, 255, 255))
        d.ellipse((X + sg * Rs * .2 - Rs * .13, ey + Rs * .28, X + sg * Rs * .2 + Rs * .13, ey + Rs * .41), fill=(255, 120, 120, 140))

def mouth_(d, cx, cy, Rs, open_, wide=1.):
    my = cy + Rs * .38
    if open_:
        d.ellipse((cx - Rs * .15 * wide, my - Rs * .08, cx + Rs * .15 * wide, my + Rs * .22), fill=(120, 26, 38, 255))
        d.ellipse((cx - Rs * .09 * wide, my + Rs * .08, cx + Rs * .09 * wide, my + Rs * .21), fill=(238, 96, 96, 255))
    else:
        d.arc((cx - Rs * .2 * wide, my - Rs * .18, cx + Rs * .2 * wide, my + Rs * .14), 25, 155, fill=INK + (255,), width=int(Rs * .05))

def critter(R, c1, c2, blink, mouth, back=None, front=None, beak=False, wide=1., feet=True):
    """Personnage rond en papier : back(d, cx, cy, Rs) dessine derrière le corps, front(...) devant."""
    body = apple(R, c1, c2, False, feet=feet, leaf=False, tige=False, contour=rond)
    w, h = body.size; S = 3; cx, cy = w * S / 2, h * .54 * S; Rs = R * S
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if back:
        bl = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); back(ImageDraw.Draw(bl), cx, cy, Rs)
        out.alpha_composite(grain(bl.resize((w, h), Image.LANCZOS)))
    out.alpha_composite(body)
    top = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
    if front: front(d, cx, cy, Rs)
    eyes(d, cx, cy, Rs, blink)
    if beak:
        o = .1 if mouth else 0
        d.ellipse((cx - Rs * .26, cy + Rs * .1, cx + Rs * .26, cy + Rs * .3), fill=hexc('#f6a23a') + (255,))
        if mouth:
            d.ellipse((cx - Rs * .22, cy + Rs * .24, cx + Rs * .22, cy + Rs * (.42 + o)), fill=hexc('#d9822a') + (255,))
            d.ellipse((cx - Rs * .12, cy + Rs * .26, cx + Rs * .12, cy + Rs * .34), fill=(120, 26, 38, 255))
    else:
        mouth_(d, cx, cy, Rs, mouth, wide)
    out.alpha_composite(top.resize((w, h), Image.LANCZOS))
    return out

def flower(d, x, y, r, col, heart=(255, 214, 90)):
    for k in range(5):
        a = k / 5 * 2 * math.pi - math.pi / 2
        d.ellipse((x + math.cos(a) * r * .8 - r * .55, y + math.sin(a) * r * .8 - r * .55, x + math.cos(a) * r * .8 + r * .55, y + math.sin(a) * r * .8 + r * .55), fill=col + (255,))
    d.ellipse((x - r * .42, y - r * .42, x + r * .42, y + r * .42), fill=heart + (255,))

# ---------- Personnages ----------
# Rosette, cigale dorée aux ailes de papier calque, foulard rouge à pois jaunes
def rosette(blink, mouth, R, flap=0.):
    R = int(R * .86); c1, c2 = hexc('#f2c55c'), hexc('#b9832f')
    def back(d, cx, cy, Rs):
        for sg in (-1, 1):
            a = .55 + flap * .5
            px, py = cx + sg * Rs * .55, cy - Rs * .35
            tip = (px + sg * Rs * 1.15 * math.cos(a), py - Rs * 1.15 * math.sin(a))
            mid = (px + sg * Rs * .9 * math.cos(a - .5), py - Rs * .5 * math.sin(a - .5))
            d.polygon([(px, py), tip, mid], fill=(214, 238, 248, 215))
            d.line([(px, py), tip], fill=(140, 170, 190, 255), width=int(Rs * .03))
            d.line([(px, py), mid], fill=(140, 170, 190, 200), width=int(Rs * .02))
        for sg in (-1, 1):
            d.line([(cx + sg * Rs * .2, cy - Rs * .85), (cx + sg * Rs * .45, cy - Rs * 1.3)], fill=INK + (255,), width=int(Rs * .04))
            q = Rs * .07; x, y = cx + sg * Rs * .45, cy - Rs * 1.3
            d.ellipse((x - q, y - q, x + q, y + q), fill=INK + (255,))
    def front(d, cx, cy, Rs):
        for k in range(3):
            y = cy + Rs * (.62 + k * .13)
            d.arc((cx - Rs * .55, y - Rs * .3, cx + Rs * .55, y + Rs * .1), 30, 150, fill=hexc('#9e6c25') + (255,), width=int(Rs * .035))
        r = hexc('#d63a33')
        d.polygon([(cx - Rs * .62, cy + Rs * .5), (cx + Rs * .62, cy + Rs * .5), (cx, cy + Rs * .95)], fill=r + (255,))
        for u, v in ((-.3, .58), (.3, .58), (0, .72), (-.12, .84), (.14, .84)):
            q = Rs * .045; d.ellipse((cx + u * Rs - q, cy + v * Rs - q, cx + u * Rs + q, cy + v * Rs + q), fill=hexc('#ffd35a') + (255,))
    return critter(R, c1, c2, blink, mouth, back, front)

# Zélie, grenouille verte à la fleur de lavande
def zelie(blink, mouth, R):
    R = int(R * .9); c1, c2 = hexc('#9ad96b'), hexc('#4f9c45')
    def back(d, cx, cy, Rs):
        for sg in (-1, 1):
            x, y = cx + sg * Rs * .45, cy - Rs * .72
            d.ellipse((x - Rs * .36, y - Rs * .36, x + Rs * .36, y + Rs * .36), fill=c2 + (255,))
    def front(d, cx, cy, Rs):
        d.ellipse((cx - Rs * .55, cy + Rs * .45, cx + Rs * .55, cy + Rs * .95), fill=hexc('#d9f2b4') + (255,))
        x, y = cx + Rs * .62, cy - Rs * .62
        for k in range(5):
            q = Rs * .07; d.ellipse((x - q + k * Rs * .03, y - q - k * Rs * .1, x + q + k * Rs * .03, y + q - k * Rs * .1), fill=hexc('#9a6fd0') + (255,))
        d.line([(x, y + Rs * .05), (x - Rs * .1, y + Rs * .3)], fill=hexc('#4f8a3c') + (255,), width=int(Rs * .03))
    return critter(R, c1, c2, blink, mouth, back, front, wide=1.5)

# Firmin, petit canard jaune au foulard bleu
def firmin(blink, mouth, R):
    R = int(R * .82); c1, c2 = hexc('#fff1a6'), hexc('#efc244')
    def back(d, cx, cy, Rs):
        for k in range(3):
            a = -.4 + k * .4
            d.ellipse((cx + math.sin(a) * Rs * .25 - Rs * .1, cy - Rs * 1.12 - Rs * .1, cx + math.sin(a) * Rs * .25 + Rs * .1, cy - Rs * .82), fill=c2 + (255,))
        for sg in (-1, 1):
            d.ellipse((cx + sg * Rs * .95 - Rs * .3, cy + Rs * .05, cx + sg * Rs * .95 + Rs * .3, cy + Rs * .5), fill=lerp(c2, (200, 120, 20), .2) + (255,))
    def front(d, cx, cy, Rs):
        b = hexc('#3f7fd6')
        d.polygon([(cx - Rs * .6, cy + Rs * .48), (cx + Rs * .6, cy + Rs * .48), (cx, cy + Rs * .92)], fill=b + (255,))
        d.ellipse((cx - Rs * .1, cy + Rs * .44, cx + Rs * .1, cy + Rs * .6), fill=hexc('#2c5fa8') + (255,))
    return critter(R, c1, c2, blink, mouth, back, front, beak=True)

# Invités de la ronde : une coccinelle et un papillon bleu
def coccinelle(blink, mouth, R):
    R = int(R * .7); c1, c2 = hexc('#f0473c'), hexc('#b8222a')
    def front(d, cx, cy, Rs):
        for u, v in ((-.62, -.35), (.62, -.35), (-.7, .3), (.7, .3), (-.35, .72), (.35, .72)):
            q = Rs * .13; d.ellipse((cx + u * Rs - q, cy + v * Rs - q, cx + u * Rs + q, cy + v * Rs + q), fill=hexc('#3d2a24') + (255,))
    def back(d, cx, cy, Rs):
        for sg in (-1, 1):
            d.line([(cx + sg * Rs * .25, cy - Rs * .85), (cx + sg * Rs * .5, cy - Rs * 1.25)], fill=INK + (255,), width=int(Rs * .05))
            q = Rs * .08; x, y = cx + sg * Rs * .5, cy - Rs * 1.25; d.ellipse((x - q, y - q, x + q, y + q), fill=INK + (255,))
    return critter(R, c1, c2, blink, mouth, back, front)

def papillon(blink, mouth, R):
    R = int(R * .66); c1, c2 = hexc('#9fd0f5'), hexc('#4a8fd8')
    def back(d, cx, cy, Rs):
        for sg in (-1, 1):
            d.ellipse((cx + sg * Rs * 1.0 - Rs * .55, cy - Rs * 1.05, cx + sg * Rs * 1.0 + Rs * .55, cy + Rs * .05), fill=hexc('#f5a3c7') + (255,))
            d.ellipse((cx + sg * Rs * .9 - Rs * .4, cy - Rs * .1, cx + sg * Rs * .9 + Rs * .4, cy + Rs * .6), fill=hexc('#ffd35a') + (255,))
            q = Rs * .16; x, y = cx + sg * Rs * 1.05, cy - Rs * .55; d.ellipse((x - q, y - q, x + q, y + q), fill=CREAM + (255,))
    return critter(R, c1, c2, blink, mouth, back, None)

PERSOS['rosette'] = lambda blink, mouth, R: rosette(blink, mouth, R)
PERSOS['rosette_vol'] = lambda blink, mouth, R: rosette(blink, mouth, R, flap=.6)
PERSOS['zelie'] = lambda blink, mouth, R: zelie(blink, mouth, R)
PERSOS['firmin'] = lambda blink, mouth, R: firmin(blink, mouth, R)
PERSOS['coccinelle'] = lambda blink, mouth, R: coccinelle(blink, mouth, R)
PERSOS['papillon'] = lambda blink, mouth, R: papillon(blink, mouth, R)

# ---------- Décors de Provence ----------
SKY = {'day': ('#86cdee', '#fdf1cf'), 'sunset': ('#e86a6f', '#ffd38a')}
def landscape(mode):
    """Ciel, soleil, collines de lavande, cyprès et petite ville fortifiée au loin."""
    im = gradient(*SKY[mode]); d = ImageDraw.Draw(im)
    S = 2; L = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    dk = 0 if mode == 'day' else .25
    town = lerp(hexc('#e6c79a'), hexc('#c0605a'), dk); roof = lerp(hexc('#d07a4f'), hexc('#8a3d4a'), dk)
    # ville fortifiée (à gauche, au loin)
    r = np.random.default_rng(4); x = 40
    while x < 820:
        w = r.uniform(70, 130); h = r.uniform(70, 160)
        d.rectangle((x * S, (560 - h) * S, (x + w) * S, 620 * S), fill=lerp(town, (255, 255, 255), r.uniform(0, .15)) + (255,))
        d.polygon([((x - 8) * S, (560 - h) * S), ((x + w / 2) * S, (560 - h - w * .35) * S), ((x + w + 8) * S, (560 - h) * S)], fill=roof + (255,))
        x += w - 6
    for tx, th in ((140, 250), (470, 300), (700, 220)):
        d.rectangle(((tx - 38) * S, (560 - th) * S, (tx + 38) * S, 620 * S), fill=lerp(town, (120, 80, 60), .12) + (255,))
        for k in range(4):
            d.rectangle(((tx - 38 + k * 22) * S, (548 - th) * S, (tx - 24 + k * 22) * S, (562 - th) * S), fill=lerp(town, (120, 80, 60), .12) + (255,))
        d.rounded_rectangle(((tx - 10) * S, (590 - th) * S, (tx + 10) * S, (625 - th) * S), 10 * S, fill=lerp(town, (60, 40, 40), .45) + (255,))
    d.rectangle((0, 560 * S, 860 * S, 630 * S), fill=lerp(town, (120, 80, 60), .18) + (255,))
    for k in range(40):
        d.rectangle(((k * 22) * S, 548 * S, (k * 22 + 13) * S, 562 * S), fill=lerp(town, (120, 80, 60), .18) + (255,))
    # collines de lavande (à droite)
    hill = lerp(hexc('#b08ad8'), hexc('#8a5a9a'), dk); stripe = lerp(hexc('#8a62c2'), hexc('#6a3a7a'), dk)
    pts = [(xx * S, (520 + 60 * math.sin(xx / 380) - 40 * math.cos(xx / 170)) * S) for xx in range(760, W + 41, 20)]
    d.polygon([(760 * S, 640 * S)] + pts + [(W * S, 640 * S)], fill=hill + (255,))
    for k in range(18):
        x0 = 800 + k * 66
        d.line([(x0 * S, 630 * S), ((x0 + 120) * S, 520 * S)], fill=stripe + (255,), width=10 * S)
    L2 = L.copy(); m = Image.new('L', L.size, 0); ImageDraw.Draw(m).polygon([(760 * S, 640 * S)] + pts + [(W * S, 640 * S)], fill=255)
    # cyprès
    for cx_, cy_, hh in ((880, 600, 210), (930, 610, 160), (1580, 560, 230), (1640, 575, 170), (1860, 580, 200)):
        d.ellipse(((cx_ - 26) * S, (cy_ - hh) * S, (cx_ + 26) * S, cy_ * S), fill=lerp(hexc('#3d6b3a'), hexc('#2a3a3a'), dk) + (255,))
    L = L.resize((W, H), Image.LANCZOS)
    im.alpha_composite(shadowed(grain(L), 3, 6, 6, .2))
    return im

def river_layer(mode):
    """Bande de fleuve (largeur 2W) avec vaguelettes, défilée horizontalement."""
    S = 2; w = 2 * W; im = Image.new('RGBA', (w * S, 460 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = hexc('#4fa6d6') if mode == 'day' else hexc('#c4708a')
    a = np.array(c, np.float32); b = np.array(hexc('#2f6fa8') if mode == 'day' else hexc('#7a4a7a'), np.float32)
    for y in range(0, 460 * S, 4):
        k = y / (460 * S); d.rectangle((0, y, w * S, y + 4), fill=tuple(int(v) for v in a * (1 - k) + b * k) + (255,))
    r = np.random.default_rng(8); lite = lerp(c, (255, 255, 255), .45)
    for _ in range(90):
        x = r.uniform(0, w); y = r.uniform(20, 440); q = r.uniform(30, 70)
        d.arc(((x - q) * S, (y - 10) * S, (x + q) * S, (y + 14) * S), 200, 340, fill=lite + (255,), width=4 * S)
    return grain(im.resize((w, 460), Image.LANCZOS))

STONE = hexc('#e2bf8a'); STONE_D = hexc('#c59a62'); STONE_T = hexc('#efd3a4')
def bridge(x0, x1, deck, water, arches, broken=False):
    """Pont de pierre : tablier en haut (deck), arches jusqu'à l'eau. Renvoie une couche W x H."""
    S = 2; im = Image.new('RGBA', (W * S, H * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((x0 * S, deck * S, x1 * S, water * S), fill=STONE + (255,))
    d.rectangle((x0 * S, (deck - 14) * S, x1 * S, (deck + 22) * S), fill=STONE_T + (255,))
    # pierres
    r = np.random.default_rng(2)
    for y in range(deck + 34, water - 30, 34):
        off = 0 if (y // 34) % 2 else 40
        for x in range(int(x0) - off, int(x1), 80):
            d.rectangle((x * S, y * S, (x + 76) * S, (y + 30) * S), outline=STONE_D + (255,), width=2 * S)
    span = (x1 - x0) / arches
    for k in range(arches):
        cx = x0 + span * (k + .5); hw = span * .36; top = deck + 70
        if broken and k == arches - 1: continue
        d.rectangle(((cx - hw) * S, (top + hw * .5) * S, (cx + hw) * S, (water + 2) * S), fill=(0, 0, 0, 0))
        d.ellipse(((cx - hw) * S, top * S, (cx + hw) * S, (top + hw) * S), fill=(0, 0, 0, 0))
        d.arc(((cx - hw - 12) * S, (top - 12) * S, (cx + hw + 12) * S, (top + hw + 12) * S), 180, 360, fill=STONE_D + (255,), width=10 * S)
    if broken:
        # le pont s'arrête net, pierres en escalier
        xe = x1
        for k in range(7):
            d.rectangle(((xe - 10 - [0, 30, 12, 46, 26, 60, 40][k]) * S, (deck - 16 + k * 40) * S, (xe + 70) * S, (deck + 24 + k * 40) * S), fill=(0, 0, 0, 0))
    out = im.resize((W, H), Image.LANCZOS)
    return shadowed(grain(out), 5, 9, 9, .26)

def lily(sc=1., fl=False):
    def f(d, S):
        w, h = 220 * sc, 70 * sc
        d.pieslice((10 * S, 10 * S, (10 + w) * S, (10 + h) * S), 300, 240, fill=hexc('#5aa84a') + (255,))
        d.arc((30 * S, 18 * S, (w - 10) * S, (h + 2) * S), 200, 340, fill=hexc('#7cc35e') + (255,), width=3 * S)
        if fl: flower(d, (10 + w * .35) * S, (14 + h * .3) * S, 20 * sc * S, hexc('#f7b6cf'))
    return sprite(f, int(240 * sc), int(100 * sc), (2, 4, 4, .2))

def fish(col):
    def f(d, S):
        d.ellipse((20 * S, 14 * S, 100 * S, 66 * S), fill=col + (255,))
        d.polygon([(90 * S, 40 * S), (126 * S, 14 * S), (126 * S, 66 * S)], fill=col + (255,))
        d.ellipse((34 * S, 28 * S, 48 * S, 42 * S), fill=(255, 255, 255, 255)); d.ellipse((38 * S, 31 * S, 46 * S, 39 * S), fill=INK + (255,))
    return sprite(f, 132, 80, (2, 4, 4, .2))

def bunting(y0=40, sag=70, col_n=0):
    S = 2; im = Image.new('RGBA', (W * S, 220 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cs = ['#d63a33', '#ffd35a', '#9a6fd0', '#fff4dc', '#4fa6d6']
    pts = [(x * S, (y0 + sag * math.sin(x / W * math.pi)) * S) for x in range(0, W + 20, 20)]
    d.line(pts, fill=(240, 230, 210, 255), width=4 * S)
    for i in range(46):
        x = i * 42 + 21; y = y0 + sag * math.sin(x / W * math.pi)
        d.polygon([((x - 18) * S, y * S), ((x + 18) * S, y * S), (x * S, (y + 44) * S)], fill=hexc(cs[(i + col_n) % 5]) + (255,))
    return shadowed(grain(im.resize((W, 220), Image.LANCZOS)), 3, 6, 6, .2)

def lantern(col):
    def f(d, S):
        d.line([(30 * S, 0), (30 * S, 14 * S)], fill=INK + (255,), width=2 * S)
        d.ellipse((6 * S, 12 * S, 54 * S, 70 * S), fill=col + (255,))
        d.rectangle((18 * S, 8 * S, 42 * S, 16 * S), fill=INK + (255,)); d.rectangle((18 * S, 66 * S, 42 * S, 74 * S), fill=INK + (255,))
        d.ellipse((20 * S, 24 * S, 34 * S, 44 * S), fill=(255, 255, 255, 90))
    return sprite(f, 60, 80, (2, 4, 4, .2))

class Petals:
    """Pétales de lavande qui tombent en tournoyant."""
    def __init__(self, n=70, seed=3):
        r = np.random.default_rng(seed)
        self.p = [(r.uniform(0, W), r.uniform(-H, 0), r.uniform(90, 170), r.uniform(0, 6.28), r.uniform(6, 11), hexc(['#9a6fd0', '#b48ae0', '#fff4dc', '#ffd35a'][int(r.integers(4))])) for _ in range(n)]
    def draw(self, fr, tl, k=1.):
        d = ImageDraw.Draw(fr)
        for x, y0, sp, ph, q, col in self.p[:int(len(self.p) * k)]:
            y = (y0 + tl * sp) % (H + 80) - 40; xx = x + 30 * math.sin(tl * 1.5 + ph)
            w_ = q * (.4 + .6 * abs(math.sin(tl * 3 + ph)))
            d.ellipse((xx - w_, y - q * .55, xx + w_, y + q * .55), fill=col + (255,))

def put_alpha(fr, s, x, y, a):
    if a <= 0: return
    if a < 1:
        s = s.copy(); s.putalpha(s.getchannel('A').point(lambda v: int(v * a)))
    put(fr, s, x, y)

def jump(b, start, dur, x0, y0, x1, y1, h=160):
    """Position d'un saut de (x0,y0) à (x1,y1) commencé au temps start, durée dur (en temps)."""
    k = clamp((b - start) / dur)
    return x0 + (x1 - x0) * k, y0 + (y1 - y0) * k - h * 4 * k * (1 - k), k

# ---------- Scènes ----------
class Scenes(Base):
    def prepare(self):
        n = self.name
        mode = 'sunset' if n in ('r3', 'outro') else 'day'
        self.mode = mode
        self.land = landscape(mode)
        self.river = river_layer(mode)
        self.sunimg = sun(86, hexc('#ffd84d'), hexc('#ffc533')) if mode == 'day' else sun(105, hexc('#ffb347'))
        self.cl = [cloud(i + 3, np.random.default_rng(i).uniform(.5, .9), (255, 252, 240) if mode == 'day' else (255, 220, 200)) for i in range(3)]
        if n in ('intro', 'r1', 'r3', 'outro'):
            self.br = bridge(-60, W + 60, 650, 900, 4)
        if n in ('intro', 'outro'):
            f2 = font('Poppins-Medium.ttf', 40)
            self.sign = paper_card(1320, 290)
            self.title = text_img(["Sur le pont d'Avignon"], lora(112), RED, 8)
            self.sub = text_img(["Comptine à chanter ensemble"], f2, INK)
            self.card2 = paper_card(1240, 280)
            self.bye = text_img(["À bientôt !"], lora(120), RED)
            self.credit = text_img(["Comptine traditionnelle française · Arrangement original"], font('Poppins-Medium.ttf', 32), INK)
        if n == 'r1':
            self.flags = bunting(560, 30)
        if n == 'danse':
            self.brk = bridge(-60, 760, 650, 900, 3, broken=True)
            self.pads = [lily(.75, i == 2) for i in range(4)]
            self.padx = [870, 1030, 1190, 1350]
            self.fishes = [fish(hexc(c)) for c in ('#ff9a4a', '#ffd35a', '#f4738a')]
            self.oops = paper_card(760, 120)
            self.oops_t = text_img(["Oh ! Le pont s'arrête !"], lora(64), RED)
        if n == 'r2':
            self.flags = bunting(30, 60)
            self.fishes = [fish(hexc(c)) for c in ('#ff9a4a', '#ffd35a', '#f4738a')]
            self.lant = [lantern(hexc(c)) for c in ('#d63a33', '#ffd35a', '#9a6fd0', '#4fa6d6')]
        if n in ('r3', 'outro'):
            self.pet = Petals()
            self.lant = [lantern(hexc(c)) for c in ('#d63a33', '#ffd35a', '#9a6fd0', '#4fa6d6')]

    def scenery(self, fr, tl, water=640, clouds=True):
        fr.alpha_composite(self.land)
        if self.mode == 'day': put(fr, self.sunimg.rotate(tl * 8, Image.BILINEAR), 1500, 30)
        else: put(fr, self.sunimg, 1130, 40)
        if clouds:
            for i, c in enumerate(self.cl):
                put(fr, c, (300 + i * 620 + tl * 18) % (W + 500) - 420, 60 + i * 70)
        x = int(tl * 40) % W
        fr.alpha_composite(self.river, (0, water), (x, 0, x + W, min(460, H - water)))

    def dancers_on_deck(self, fr, t, b, foot, keys, xs, sing, spin=False, hop=30, scale=1.):
        for i, (k, x) in enumerate(zip(keys, xs)):
            tilt = 0
            if spin: tilt = 360 * ease(spin) * (1 if i % 2 else -1)
            draw_char(fr, k, x, foot, t, b, hop=hop, sing=sing, phase=i * .33, tilt=tilt, scale=scale, R=165)

    # --- intro : le pont au matin, titre
    def do_intro(self, fr, t, tl, b):
        self.scenery(fr, tl)
        fr.alpha_composite(self.br)
        for i, (k, x0, x1) in enumerate((('zelie', -200, 560), ('rosette', W + 200, 960), ('firmin', -400, 1360))):
            k_ = ease((b - 6 - i * 1.5) / 3)
            draw_char(fr, k, x0 + (x1 - x0) * k_, 660, t, b, hop=30, phase=i * .33, R=150, scale=.85)
        k = back((b - .4) / 2.2)
        if k > 0:
            sy = 36 - (1 - k) * 900 + 6 * math.sin(tl * 2)
            put(fr, self.sign, (W - self.sign.width) / 2, sy)
            put(fr, self.title, (W - self.title.width) / 2, sy + 60)
            put(fr, self.sub, (W - self.sub.width) / 2, sy + 222)
        if b < 1: put_fade(fr, 1 - b)
        sweep(fr, (b - (self.len - .5)) / .5, CREAM)

    # --- r1 : on danse sur le pont
    def do_r1(self, fr, t, tl, b):
        self.scenery(fr, tl)
        fr.alpha_composite(self.br)
        put(fr, self.flags, 0, 0)
        sing = self.ly.singing(b)
        # « tous en rond » (temps 12-16 et 28-32) : chacun fait un tour sur lui-même
        sp = 0
        for st in (12, 28):
            if st <= b < st + 4: sp = (b - st) / 3.5
        xs = [560 + 40 * math.sin(tl * 1.4), 960, 1360 - 40 * math.sin(tl * 1.4)]
        self.dancers_on_deck(fr, t, b, 660, ['zelie', 'rosette', 'firmin'], xs, sing, spin=sp if sp else False)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, CREAM, rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#9ad96b'))

    # --- danse (séquence inédite) : le pont s'arrête, traversée de nénuphar en nénuphar
    def do_danse(self, fr, t, tl, b):
        self.scenery(fr, tl, water=640)
        # l'île à droite
        d = ImageDraw.Draw(fr)
        d.ellipse((1450, 700, 2450, 870), fill=hexc('#8cc76a') + (255,))
        d.ellipse((1470, 690, 2450, 830), fill=hexc('#a6d67a') + (255,))
        for i, x in enumerate(self.padx):
            put(fr, self.pads[i], x - self.pads[i].width / 2, 790 + 6 * math.sin(tl * 2 + i))
        # poissons qui sautent sur les temps forts
        for j, st in enumerate((5, 13, 21, 29)):
            ph = (b - st) / 1.6
            if 0 <= ph < 1:
                f_ = self.fishes[j % 3]; x = 900 + j * 230 + 200 * ph; y = 900 - 300 * 4 * ph * (1 - ph)
                put(fr, f_.rotate(-60 + 120 * ph, Image.BICUBIC, expand=True), x - 60, y - 40)
        fr.alpha_composite(self.brk)
        # Zélie saute d'un nénuphar à l'autre, un saut toutes les deux mesures
        stops = [(630, 660)] + [(x, 800) for x in self.padx] + [(1665, 755)]
        zx, zy = stops[0]; zk = 0
        for i in range(len(stops) - 1):
            st = 8 + i * 4
            if b >= st:
                zx, zy, zk = jump(b, st, 1.5, stops[i][0], stops[i][1], stops[i + 1][0], stops[i + 1][1], 200)
        inair = 0 < zk < 1
        draw_char(fr, 'zelie', zx, zy, t, b, hop=0 if inair else 22, R=150, scale=.85, tilt=-15 * math.sin(zk * math.pi) if inair else 0)
        # Firmin nage à côté des nénuphars
        fk = ease((b - 10.5) / 16.5); fx = 560 + (1660 - 560) * fk; fy = 1000 + 8 * math.sin(tl * 3)
        if b < 9: fx, fy = 400, 660
        if 9 <= b < 10.5: fx, fy, _ = jump(b, 9, 1.5, 400, 660, 560, 1000, 120)
        if b >= 27: fx, fy, _ = jump(b, 27, 1.5, 1660, 1000, 1505, 765, 200)
        draw_char(fr, 'firmin', fx, fy, t, b, hop=0 if 10.5 < b < 27 else 20, R=150, scale=.85, tilt=4 * math.sin(tl * 3))
        # Rosette s'envole en boucle au-dessus du fleuve
        rk = clamp((b - 10) / 18)
        if b < 10: rx, ry, key = 170, 660, 'rosette'
        else:
            rx = 170 + (1810 - 170) * ease(rk) - 120 * math.sin(rk * 2 * math.pi)
            ry = 640 - 290 * math.sin(rk * math.pi) + 40 * math.sin(rk * 4 * math.pi) + 110 * rk
            key = 'rosette_vol' if int(tl * 8) % 2 else 'rosette'
            if rk >= 1: rx, ry, key = 1810, 750, 'rosette'
        draw_char(fr, key, rx, ry, t, b, hop=0 if 10 < b < 28 else 22, R=150, scale=.85, tilt=8 * math.sin(tl * 4) if 10 < b < 28 else 0)
        # panneau « Oh ! Le pont s'arrête ! »
        k = back((b - 1.5) / 1.2) - ease((b - 7.5) / .8) * 1.2
        if k > 0:
            y = 70 - (1 - min(k, 1)) * 400
            put(fr, self.oops, (W - self.oops.width) / 2, y); put(fr, self.oops_t, (W - self.oops_t.width) / 2, y + 22)
        sweep(fr, 1 - b / .5, hexc('#9ad96b'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#e2bf8a'))

    # --- r2 : sous les arches, sur l'île
    def do_r2(self, fr, t, tl, b):
        self.scenery(fr, tl, water=620, clouds=False)
        d = ImageDraw.Draw(fr)
        # grande arche au premier plan qui encadre la scène
        S_ = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(S_)
        ds.rectangle((0, 0, W, H), fill=STONE + (255,))
        ds.rectangle((150, 360, W - 150, H), fill=(0, 0, 0, 0)); ds.ellipse((150, 40, W - 150, 680), fill=(0, 0, 0, 0))
        for y in range(0, 1080, 60):
            off = 0 if (y // 60) % 2 else 50
            for x in list(range(-off, 150, 100)) + list(range(W - 150 - off, W, 100)):
                ds.rectangle((x, y, x + 96, y + 56), outline=STONE_D + (255,), width=3)
        ds.arc((140, 30, W - 140, 690), 180, 360, fill=STONE_D + (255,), width=16)
        # sol de l'île
        d.ellipse((-300, 760, W + 300, 1300), fill=hexc('#93c96c') + (255,))
        d.ellipse((-200, 790, W + 200, 1300), fill=hexc('#a8d67e') + (255,))
        for x in range(120, W, 170):
            flower(d, x + 30 * math.sin(x), 820 + (x * 37) % 60, 12, hexc(['#f7b6cf', '#fff4dc', '#9a6fd0'][x % 3]))
        # poissons qui sautent dans le fleuve, au fond
        for j, st in enumerate((3, 11, 19, 27)):
            ph = (b - st) / 1.6
            if 0 <= ph < 1:
                f_ = self.fishes[j % 3]; x = 400 + j * 300 + 180 * ph; y = 760 - 200 * 4 * ph * (1 - ph)
                put(fr, f_.rotate(-60 + 120 * ph, Image.BICUBIC, expand=True), x - 60, y - 40)
        fr.alpha_composite(shadowed(grain(S_), 0, 6, 12, .3))
        put(fr, self.flags, 0, 300)
        for i in range(4):
            x = 520 + i * 300; y = 340 + 70 * math.sin((x - 150) / (W - 300) * math.pi) * 0 + 8 * math.sin(tl * 2 + i)
            put(fr, self.lant[i], x - 30, 330 + 40 * math.sin((x) / W * math.pi) + 6 * math.sin(tl * 2 + i))
        sing = self.ly.singing(b)
        # invités au fond, plus petits
        draw_char(fr, 'coccinelle', 430, 800, t, b, hop=26, phase=.2, scale=.62, sing=sing, R=165)
        draw_char(fr, 'papillon', 1490, 800, t, b, hop=26, phase=.7, scale=.62, sing=sing, R=165)
        # les trois amis se tiennent en file et avancent / reculent
        sway = 70 * math.sin(b / 8 * math.pi)
        for i, (k, x) in enumerate((('zelie', 640), ('rosette', 960), ('firmin', 1280))):
            draw_char(fr, k, x + sway, 880, t, b, hop=36, sing=sing, phase=i * .33, R=165)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#e2bf8a'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffb36b'))

    # --- r3 : la grande ronde au soleil couchant
    def do_r3(self, fr, t, tl, b):
        self.scenery(fr, tl)
        fr.alpha_composite(self.br)
        for i in range(7):
            x = 160 + i * 270
            put(fr, self.lant[i % 4], x - 30, 470 + 10 * math.sin(tl * 2 + i))
        ImageDraw.Draw(fr).line([(0, 470), (W, 470)], fill=(240, 230, 210, 255), width=3)
        sing = self.ly.singing(b)
        keys = ['zelie', 'coccinelle', 'rosette', 'papillon', 'firmin']
        ang0 = b / 16 * 2 * math.pi
        items = []
        for i, k in enumerate(keys):
            a = ang0 + i / len(keys) * 2 * math.pi
            x = 960 + 560 * math.sin(a); depth = math.cos(a)
            items.append((depth, k, x, i))
        for depth, k, x, i in sorted(items):
            sc = .74 + .24 * depth
            if k in ('coccinelle', 'papillon'): sc *= .8
            draw_char(fr, k, x, 650 + 45 * depth, t, b, hop=28, sing=sing, phase=i * .2, scale=sc, R=165)
        self.pet.draw(fr, tl, clamp(b / 6))
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ffb36b'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, CREAM)

    # --- fin
    def do_outro(self, fr, t, tl, b):
        self.scenery(fr, tl)
        fr.alpha_composite(self.br)
        self.pet.draw(fr, tl, .6)
        k = back((b - .4) / 1.6)
        sy = 40 + (1 - k) * 800
        put(fr, self.card2, (W - self.card2.width) / 2, sy)
        put(fr, self.bye, (W - self.bye.width) / 2, sy + 50)
        put(fr, self.credit, (W - self.credit.width) / 2, sy + 210)
        calm = b >= 12
        for i, (k_, x) in enumerate((('zelie', 560), ('rosette', 960), ('firmin', 1360))):
            draw_char(fr, k_, x, 660, t, b, hop=0 if calm else 30, phase=i * .33, R=150, scale=.85, tilt=8 * math.sin(tl * 3 + i))
        sweep(fr, 1 - b / .5, CREAM, rev=True)
        end = self.tend - t
        if end < .9: put_fade(fr, 1 - end / .9, CREAM)
