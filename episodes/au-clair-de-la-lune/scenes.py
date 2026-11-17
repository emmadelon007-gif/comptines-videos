# Scènes de "Au clair de la lune" : sur les toits d'un petit village endormi,
# Lulu la souris n'a plus de lumière pour écrire un mot à la Lune. Elle frappe chez Pierrot
# le hibou, qui l'envoie chez Madame Lapine ; la chandelle rallumée, la lettre s'envole vers la Lune.
from papier import *
from papier import Scenes as Base

def rond(cx, cy, R):
    return [(cx + R * 1.02 * math.sin(i / 200 * 2 * math.pi), cy - R * .96 * math.cos(i / 200 * 2 * math.pi)) for i in range(200)]

def sprite(fn, w, h, sh=(4, 8, 7, .24)):
    S = 2; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), S)
    return shadowed(grain(im.resize((w, h), Image.LANCZOS)), *sh)

def gradient(top, bot, k=1.1):
    a, b = np.array(hexc(top), np.float32), np.array(hexc(bot), np.float32)
    t = np.linspace(0, 1, H)[:, None, None] ** k
    return grain(Image.fromarray(np.repeat(a * (1 - t) + b * t, W, 1).astype(np.uint8), 'RGB').convert('RGBA'))

def eyes(d, cx, cy, Rs, blink, ring=None):
    ex, ey = Rs * .36, cy - Rs * .1
    for sg in (-1, 1):
        X = cx + sg * ex
        if ring: d.ellipse((X - Rs * .3, ey - Rs * .32, X + Rs * .3, ey + Rs * .3), fill=ring + (255,))
        if blink:
            d.arc((X - Rs * .17, ey - Rs * .1, X + Rs * .17, ey + Rs * .16), 200, 340, fill=INK + (255,), width=int(Rs * .05))
        else:
            d.ellipse((X - Rs * .18, ey - Rs * .23, X + Rs * .18, ey + Rs * .23), fill=(255, 255, 255, 255))
            d.ellipse((X - Rs * .115, ey - Rs * .13, X + Rs * .115, ey + Rs * .16), fill=INK + (255,))
            d.ellipse((X - Rs * .05, ey - Rs * .09, X + Rs * .03, ey - Rs * .01), fill=(255, 255, 255, 255))
        d.ellipse((X + sg * Rs * .2 - Rs * .13, ey + Rs * .28, X + sg * Rs * .2 + Rs * .13, ey + Rs * .41), fill=(255, 120, 120, 140))

def mouth_(d, cx, cy, Rs, open_):
    my = cy + Rs * .38
    if open_:
        d.ellipse((cx - Rs * .15, my - Rs * .08, cx + Rs * .15, my + Rs * .22), fill=(120, 26, 38, 255))
        d.ellipse((cx - Rs * .09, my + Rs * .08, cx + Rs * .09, my + Rs * .21), fill=(238, 96, 96, 255))
    else:
        d.arc((cx - Rs * .2, my - Rs * .18, cx + Rs * .2, my + Rs * .14), 25, 155, fill=INK + (255,), width=int(Rs * .05))

def critter(R, c1, c2, blink, mouth, back=None, front=None, ring=None, beak=False, nose=None):
    """Personnage rond en papier : back(d, cx, cy, Rs) dessine derrière le corps, front(...) devant."""
    body = apple(R, c1, c2, False, feet=True, leaf=False, tige=False, contour=rond)
    w, h = body.size; S = 3; cx, cy = w * S / 2, h * .54 * S; Rs = R * S
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    if back:
        bl = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); back(ImageDraw.Draw(bl), cx, cy, Rs)
        out.alpha_composite(grain(bl.resize((w, h), Image.LANCZOS)))
    out.alpha_composite(body)
    top = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
    if front: front(d, cx, cy, Rs)
    eyes(d, cx, cy, Rs, blink, ring)
    if beak:
        o = .1 if mouth else 0
        d.polygon([(cx - Rs * .14, cy + Rs * .1), (cx + Rs * .14, cy + Rs * .1), (cx, cy + Rs * (.36 + o))], fill=hexc('#f6a23a') + (255,))
        if mouth: d.polygon([(cx - Rs * .1, cy + Rs * .3), (cx + Rs * .1, cy + Rs * .3), (cx, cy + Rs * .52)], fill=hexc('#d9822a') + (255,))
    else:
        if nose: d.ellipse((cx - Rs * .08, cy + Rs * .12, cx + Rs * .08, cy + Rs * .24), fill=nose + (255,))
        mouth_(d, cx, cy, Rs, mouth)
    out.alpha_composite(top.resize((w, h), Image.LANCZOS))
    return out

# --- Lulu, petite souris grise au nœud bleu
def lulu(blink, mouth, R):
    R = int(R * .78); pk = hexc('#f4a7b9'); g = hexc('#b9b2cc')
    def back(d, cx, cy, Rs):
        for sg in (-1, 1):
            ex, ey = cx + sg * Rs * .78, cy - Rs * .78
            d.ellipse((ex - Rs * .5, ey - Rs * .5, ex + Rs * .5, ey + Rs * .5), fill=g + (255,))
            d.ellipse((ex - Rs * .32, ey - Rs * .32, ex + Rs * .32, ey + Rs * .32), fill=pk + (255,))
        pts = [(cx + Rs * (.8 + .5 * t), cy + Rs * (.75 - .9 * t * t) + Rs * .15 * math.sin(t * 7)) for t in np.linspace(0, 1, 30)]
        d.line(pts, fill=hexc('#9d95b3') + (255,), width=int(Rs * .07), joint='curve')
    def front(d, cx, cy, Rs):
        bx, by = cx + Rs * .5, cy - Rs * .72; b = hexc('#4f8fe0')
        d.polygon([(bx, by), (bx - Rs * .26, by - Rs * .16), (bx - Rs * .26, by + Rs * .16)], fill=b + (255,))
        d.polygon([(bx, by), (bx + Rs * .26, by - Rs * .16), (bx + Rs * .26, by + Rs * .16)], fill=b + (255,))
        d.ellipse((bx - Rs * .07, by - Rs * .07, bx + Rs * .07, by + Rs * .07), fill=hexc('#3a6fc0') + (255,))
        for sg in (-1, 1):
            for k in (-1, 0, 1):
                d.line([(cx + sg * Rs * .2, cy + Rs * .2), (cx + sg * Rs * .62, cy + Rs * (.14 + k * .09))], fill=INK + (200,), width=max(2, int(Rs * .018)))
    return critter(R, hexc('#d6d0e4'), hexc('#a59cbd'), blink, mouth, back, front, nose=pk)

# --- Pierrot, hibou brun au bonnet vert étoilé
def pierrot(blink, mouth, R, cap=True):
    c1, c2 = hexc('#c99a6a'), hexc('#916442')
    def back(d, cx, cy, Rs):
        for sg in (-1, 1):
            d.polygon([(cx + sg * Rs * .35, cy - Rs * .8), (cx + sg * Rs * .85, cy - Rs * 1.25), (cx + sg * Rs * .8, cy - Rs * .55)], fill=c2 + (255,))
            d.ellipse((cx + sg * Rs * .92 - Rs * .26, cy - Rs * .1, cx + sg * Rs * .92 + Rs * .26, cy + Rs * .62), fill=lerp(c2, (0, 0, 0), .12) + (255,))
    def front(d, cx, cy, Rs):
        bel = hexc('#f3dfbd')
        d.ellipse((cx - Rs * .5, cy + Rs * .3, cx + Rs * .5, cy + Rs * .98), fill=bel + (255,))
        for row in range(2):
            for k in range(4 - row):
                x = cx + (k - (3 - row) / 2) * Rs * .2; y = cy + Rs * (.56 + row * .17)
                d.arc((x - Rs * .08, y - Rs * .08, x + Rs * .08, y + Rs * .08), 20, 160, fill=hexc('#d8b98c') + (255,), width=max(2, int(Rs * .025)))
        if cap:
            gr, ye = hexc('#3f9a6e'), hexc('#ffd35a')
            by = cy - Rs * .64
            pts = [(cx - Rs * .76, by), (cx + Rs * .76, by), (cx - Rs * 1.12, cy - Rs * 1.48)]
            d.polygon(pts, fill=gr + (255,))
            for (u, v) in ((.35, .25), (.55, .5), (.3, .62)):
                sx = pts[0][0] + (pts[1][0] - pts[0][0]) * u * (1 - v) + (pts[2][0] - pts[0][0]) * v
                sy = by + (pts[2][1] - by) * v
                star(d, sx, sy, Rs * .07, ye)
            d.rounded_rectangle((cx - Rs * .82, by - Rs * .06, cx + Rs * .82, by + Rs * .14), int(Rs * .08), fill=CREAM + (255,))
            q = Rs * .15; d.ellipse((pts[2][0] - q, pts[2][1] - q, pts[2][0] + q, pts[2][1] + q), fill=CREAM + (255,))
    return critter(R, c1, c2, blink, mouth, back, front, ring=hexc('#f3dfbd'), beak=True)

# --- Madame Lapine, lapine crème au tablier rouge
def lapine(blink, mouth, R):
    R = int(R * .9); c1, c2 = hexc('#fbf3e6'), hexc('#e2d2bb'); pk = hexc('#f4a7b9')
    def back(d, cx, cy, Rs):
        for sg, ang in ((-1, -.25), (1, .32)):
            ex = cx + sg * Rs * .38
            pts = [(ex + Rs * .26 * math.cos(a) + Rs * math.sin(ang) * (1 - math.sin(a)) * .0, cy - Rs * .7 - Rs * .75 * (1 + math.sin(a))) for a in np.linspace(-math.pi / 2, 3 * math.pi / 2, 40)]
            pts = [(ex + (x - ex) + Rs * ang * (cy - Rs * .7 - y) / Rs * .8, y) for x, y in pts]
            d.polygon(pts, fill=c2 + (255,))
            inner = [(ex + (x - ex) * .5 + Rs * ang * (cy - Rs * .7 - y) / Rs * .4, y + Rs * .1) for x, y in pts]
            d.polygon(inner, fill=pk + (255,))
    def front(d, cx, cy, Rs):
        r = hexc('#d9433b')
        d.rounded_rectangle((cx - Rs * .5, cy + Rs * .42, cx + Rs * .5, cy + Rs * .98), int(Rs * .12), fill=r + (255,))
        for k in range(3):
            x = cx + (k - 1) * Rs * .28; d.ellipse((x - Rs * .05, cy + Rs * .62, x + Rs * .05, cy + Rs * .72), fill=CREAM + (255,))
        d.line([(cx - Rs * .5, cy + Rs * .44), (cx - Rs * .7, cy + Rs * .2)], fill=r + (255,), width=int(Rs * .06))
        d.line([(cx + Rs * .5, cy + Rs * .44), (cx + Rs * .7, cy + Rs * .2)], fill=r + (255,), width=int(Rs * .06))
    return critter(R, c1, c2, blink, mouth, back, front, nose=pk)

def star(d, x, y, r, col, a=255):
    pts = []
    for i in range(10):
        q = r if i % 2 == 0 else r * .45; an = -math.pi / 2 + i * math.pi / 5
        pts.append((x + q * math.cos(an), y + q * math.sin(an)))
    d.polygon(pts, fill=col + (a,))

PERSOS['lulu'] = lambda blink, mouth, R: lulu(blink, mouth, R)
PERSOS['pierrot'] = lambda blink, mouth, R: pierrot(blink, mouth, R)
PERSOS['lapine'] = lambda blink, mouth, R: lapine(blink, mouth, R)

NIGHT = ('#0e1840', '#33397c')

def moon_face(R, smile=True, sleepy=False):
    """La Lune : disque crème, cratères doux, visage rond."""
    c1, c2 = hexc('#fff6c9'), hexc('#ffd77a')
    def f(d, S):
        c = R * 1.6 * S; Rs = R * S
        for k in range(10, 0, -1):
            q = Rs * (1 + k * .06); d.ellipse((c - q, c - q, c + q, c + q), fill=(255, 236, 160, 9))
        d.ellipse((c - Rs, c - Rs, c + Rs, c + Rs), fill=c2 + (255,))
        d.ellipse((c - Rs * .97, c - Rs * .99, c + Rs * .9, c + Rs * .9), fill=c1 + (255,))
        for (u, v, q) in ((.45, -.5, .14), (-.55, .35, .1), (.55, .45, .08), (-.2, -.62, .07)):
            d.ellipse((c + u * Rs - q * Rs, c + v * Rs - q * Rs, c + u * Rs + q * Rs, c + v * Rs + q * Rs), fill=hexc('#f6e3a0') + (255,))
        ey = c - Rs * .08
        for sg in (-1, 1):
            X = c + sg * Rs * .34
            if sleepy: d.arc((X - Rs * .14, ey - Rs * .08, X + Rs * .14, ey + Rs * .12), 200, 340, fill=INK + (255,), width=int(Rs * .045))
            else:
                d.ellipse((X - Rs * .1, ey - Rs * .14, X + Rs * .1, ey + Rs * .14), fill=INK + (255,))
                d.ellipse((X - Rs * .04, ey - Rs * .09, X + Rs * .02, ey - Rs * .03), fill=(255, 255, 255, 255))
            d.ellipse((X + sg * Rs * .14 - Rs * .12, ey + Rs * .2, X + sg * Rs * .14 + Rs * .12, ey + Rs * .32), fill=(255, 150, 140, 150))
        if smile: d.arc((c - Rs * .2, c + Rs * .02, c + Rs * .2, c + Rs * .36), 25, 155, fill=INK + (255,), width=int(Rs * .045))
        else: d.ellipse((c - Rs * .07, c + Rs * .2, c + Rs * .07, c + Rs * .32), fill=INK + (255,))
    return sprite(f, int(R * 3.2), int(R * 3.2), (2, 4, 8, .1))

class Stars:
    def __init__(self, n, seed, ymax=620):
        r = np.random.default_rng(seed)
        self.p = [(r.uniform(20, W - 20), r.uniform(20, ymax), r.uniform(4, 11), r.uniform(0, 6.28), r.uniform(1.5, 3.5)) for _ in range(n)]
    def draw(self, fr, tl, k=1.):
        d = ImageDraw.Draw(fr)
        for x, y, q, ph, sp in self.p[:int(len(self.p) * k)]:
            a = .55 + .45 * math.sin(tl * sp + ph)
            star(d, x, y, q * (.8 + .3 * a), (255, 240, 190), int(255 * a))

ROOF = ['#c2553f', '#3e5e93', '#8a4f7d', '#b0723f', '#4f7f6a']
WALL = ['#e9d8b8', '#d7c3a5', '#efe0c4', '#cdb795']

def houses(seed, base, sc, ncols, dark=0., lit=.5):
    """Rangée de maisons en papier sur une bande de LW px. Renvoie (couche, fenêtres[(x,y,w,h,allumée)])."""
    r = np.random.default_rng(seed); im = Image.new('RGBA', (LW, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    wins = []; x = -40
    while x < LW:
        w = int(r.uniform(200, 300) * sc); h = int(r.uniform(160, 300) * sc)
        wall = lerp(hexc(WALL[int(r.integers(len(WALL)))]), hexc('#1a2350'), dark)
        roof = lerp(hexc(ROOF[int(r.integers(len(ROOF)))]), hexc('#1a2350'), dark)
        top = base - h
        d.rectangle((x, top, x + w, H), fill=wall + (255,))
        rh = int(r.uniform(.45, .7) * w)
        d.polygon([(x - 14 * sc, top), (x + w / 2, top - rh), (x + w + 14 * sc, top)], fill=roof + (255,))
        if r.uniform() < .7:
            chx = x + w * r.uniform(.6, .75); cht = top - rh * .62
            d.rectangle((chx, cht - 46 * sc, chx + 30 * sc, top - rh * .3), fill=lerp(roof, (0, 0, 0), .25) + (255,))
            d.rectangle((chx - 6 * sc, cht - 54 * sc, chx + 36 * sc, cht - 42 * sc), fill=lerp(roof, (0, 0, 0), .35) + (255,))
        for row in range(max(1, int(h / (110 * sc)))):
            for col in range(2):
                wx = x + w * (.22 + .4 * col); wy = top + 40 * sc + row * 105 * sc; ww, wh = 50 * sc, 64 * sc
                if wy + wh > base - 10: continue
                on = r.uniform() < lit
                wins.append((wx, wy, ww, wh, on))
                d.rounded_rectangle((wx, wy, wx + ww, wy + wh), int(10 * sc), fill=(hexc('#ffd35a') if on else lerp(hexc('#2b3466'), (0, 0, 0), dark * .3)) + (255,))
                d.line([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], fill=lerp(wall, (0, 0, 0), .3) + (255,), width=max(2, int(4 * sc)))
                d.line([(wx, wy + wh / 2), (wx + ww, wy + wh / 2)], fill=lerp(wall, (0, 0, 0), .3) + (255,), width=max(2, int(4 * sc)))
        x += w + int(r.uniform(-10, 30) * sc)
    return grain(shadowed(im, 3, 6, 6, .22)), wins

def candle(lit, smoke_t=None):
    def f(d, S):
        d.ellipse((10 * S, 150 * S, 130 * S, 186 * S), fill=hexc('#c9a24a') + (255,))
        d.rounded_rectangle((44 * S, 70 * S, 96 * S, 170 * S), 10 * S, fill=hexc('#fff4dc') + (255,))
        d.ellipse((44 * S, 62 * S, 96 * S, 80 * S), fill=hexc('#f3e4c0') + (255,))
        d.line([(70 * S, 70 * S), (70 * S, 54 * S)], fill=INK + (255,), width=3 * S)
        d.arc((104 * S, 130 * S, 150 * S, 170 * S), 270, 90, fill=hexc('#c9a24a') + (255,), width=7 * S)
    return sprite(f, 160, 190)

def flame(sc=1.):
    def f(d, S):
        for k, col in enumerate(('#ffb347', '#ffd35a', '#fff4c0')):
            q = 1 - k * .3
            d.ellipse(((30 - 18 * q) * S, (70 - 60 * q) * S, (30 + 18 * q) * S, 72 * S), fill=hexc(col) + (255,))
            d.polygon([((30 - 17 * q) * S, (70 - 28 * q) * S), (30 * S, (70 - 80 * q) * S), ((30 + 17 * q) * S, (70 - 28 * q) * S)], fill=hexc(col) + (255,))
    return sprite(f, int(60 * sc), int(80 * sc), (0, 0, 1, 0))

def glow(R, col=(255, 214, 120), a=90):
    im = Image.new('RGBA', (R * 2, R * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(16, 0, -1):
        q = R * k / 16; d.ellipse((R - q, R - q, R + q, R + q), fill=col + (int(a / 16 * 1.6),))
    return im

def feather(sc=1.):
    def f(d, S):
        pts = [(20 * S + 200 * t * S, 60 * S - 40 * t * S - 30 * math.sin(t * math.pi) * S) for t in np.linspace(0, 1, 30)]
        up = [(x, y - (26 * math.sin(t * math.pi) + 4) * S) for (x, y), t in zip(pts, np.linspace(0, 1, 30))]
        dn = [(x, y + (22 * math.sin(t * math.pi) + 2) * S) for (x, y), t in zip(pts, np.linspace(0, 1, 30))]
        d.polygon(up[4:] + dn[4:][::-1], fill=hexc('#c99a6a') + (255,))
        for i in range(6, 28, 3):
            x, y = pts[i]; d.line([(x, y), (x - 10 * S, y - 18 * S)], fill=hexc('#916442') + (255,), width=2 * S)
        d.line(pts, fill=hexc('#7a5236') + (255,), width=3 * S)
    return sprite(f, int(240 * sc), int(130 * sc), (2, 5, 4, .2))

def letter(open_=False):
    def f(d, S):
        d.polygon([(10 * S, 20 * S), (170 * S, 20 * S), (170 * S, 120 * S), (10 * S, 120 * S)], fill=hexc('#fff4dc') + (255,))
        d.line([(10 * S, 20 * S), (90 * S, 78 * S), (170 * S, 20 * S)], fill=hexc('#d9c08c') + (255,), width=4 * S)
        d.ellipse((76 * S, 64 * S, 104 * S, 92 * S), fill=RED + (255,))
        star(d, 90 * S, 78 * S, 10 * S, hexc('#ffd35a'))
    return sprite(f, 180, 140, (3, 6, 5, .25))

def put_alpha(fr, s, x, y, a):
    if a <= 0: return
    if a < 1:
        s = s.copy(); s.putalpha(s.getchannel('A').point(lambda v: int(v * a)))
    put(fr, s, x, y)

class Sparks:
    """Étincelles du briquet de Madame Lapine."""
    def draw(self, fr, x, y, b, onsets, col=(255, 210, 90)):
        d = ImageDraw.Draw(fr)
        for o in onsets:
            ph = (b - o) / 1.2
            if not 0 <= ph < 1: continue
            r = np.random.default_rng(int(o * 10))
            for k in range(14):
                an = r.uniform(-math.pi, 0); sp = r.uniform(80, 220)
                px = x + math.cos(an) * sp * ph; py = y + math.sin(an) * sp * ph + 160 * ph * ph
                q = 7 * (1 - ph) + 2
                star(d, px, py, q, col, int(255 * (1 - ph)))

class Scenes(Base):
    def prepare(self):
        n = self.name
        self.nsky = gradient(*NIGHT)
        self.stars = Stars(70, 4)
        self.moon = moon_face(130)
        if n in ('intro', 'v1', 'v3', 'outro', 'lettre'):
            self.far, _ = houses(21, 760, .7, 0, dark=.55, lit=.35)
            self.near, self.nwins = houses(37, 900, 1.0, 0, dark=.25, lit=.0)
            self.litwin = {}
        if n in ('intro', 'outro'):
            self.title = text_img(["Au clair de la lune"], lora(124), RED)
            self.sub = text_img(["Comptine à chanter ensemble"], font('Poppins-Medium.ttf', 40), INK)
            self.sign = paper_card(1180, 330)
            self.bye = text_img(["À bientôt !"], lora(118), RED)
            self.credit = text_img(["Comptine traditionnelle française · Arrangement original"], font('Poppins-Medium.ttf', 32), INK)
            self.card2 = paper_card(1160, 280)
        self.candle = candle(False); self.flame = flame(); self.glow = glow(150)
        if n == 'v1': self.make_roofwalk()
        if n == 'v2': self.make_bedroom(); self.make_kitchen(); self.sparks = Sparks()
        if n == 'lettre': self.make_letter()
        if n in ('v3', 'outro'): self.make_terrace()
        self.smoke = [text_img(["~"], font(POP, 110), hexc('#c3c9e6'))]
    # ----- éléments
    def make_roofwalk(self):
        # toit de zinc en premier plan, lucarne de Lulu à gauche, tour ronde de Pierrot à droite
        def roof(d, S):
            d.polygon([(0, 220 * S), (W * S, 160 * S), (W * S, 420 * S), (0, 420 * S)], fill=hexc('#5d6a94') + (255,))
            for k in range(0, W, 90): d.line([(k * S, (220 - k / W * 60) * S), (k * S, 420 * S)], fill=hexc('#4f5b84') + (255,), width=4 * S)
            d.polygon([(0, 208 * S), (W * S, 148 * S), (W * S, 170 * S), (0, 230 * S)], fill=hexc('#7d89b3') + (255,))
        self.roof = sprite(roof, W, 420, (0, -6, 8, .25))
        def dormer(d, S):
            d.rectangle((40 * S, 140 * S, 340 * S, 520 * S), fill=hexc('#e9d8b8') + (255,))
            d.polygon([(10 * S, 150 * S), (190 * S, 0), (370 * S, 150 * S)], fill=hexc('#c2553f') + (255,))
            d.rounded_rectangle((90 * S, 190 * S, 290 * S, 440 * S), 90 * S, fill=hexc('#2b3466') + (255,))
            d.line([(190 * S, 190 * S), (190 * S, 440 * S)], fill=hexc('#a8693e') + (255,), width=10 * S)
            d.line([(90 * S, 320 * S), (290 * S, 320 * S)], fill=hexc('#a8693e') + (255,), width=10 * S)
        self.dormer = sprite(dormer, 380, 520)
        def tower(d, S):
            d.rectangle((40 * S, 220 * S, 400 * S, 900 * S), fill=hexc('#d7c3a5') + (255,))
            for k in range(6): d.line([(40 * S, (300 + k * 100) * S), (400 * S, (300 + k * 100) * S)], fill=hexc('#c6b08f') + (255,), width=4 * S)
            d.polygon([(0, 230 * S), (220 * S, 0), (440 * S, 230 * S)], fill=hexc('#3e5e93') + (255,))
            d.ellipse((150 * S, 250 * S, 290 * S, 390 * S), fill=hexc('#2b3466') + (255,))
            d.rounded_rectangle((120 * S, 480 * S, 320 * S, 800 * S), 100 * S, fill=hexc('#7b4a2d') + (255,))
            d.rounded_rectangle((138 * S, 498 * S, 302 * S, 800 * S), 82 * S, fill=hexc('#9a5a33') + (255,))
            d.ellipse((268 * S, 640 * S, 288 * S, 660 * S), fill=GOLD + (255,))
            star(d, 220 * S, 560 * S, 30 * S, hexc('#ffd35a'))
        self.tower = sprite(tower, 440, 900)
        self.knock = text_img(["toc", "toc !"], lora(56), CREAM, sp=0)
    def make_bedroom(self):
        bg = Image.new('RGBA', (W, H), hexc('#3b3f7a') + (255,)); d = ImageDraw.Draw(bg)
        for x in range(0, W, 120): d.rectangle((x, 0, x + 60, 860), fill=hexc('#363a72') + (255,))
        d.rectangle((0, 860, W, H), fill=hexc('#7b4a2d') + (255,))
        for x in range(0, W, 200): d.line([(x, 860), (x, H)], fill=hexc('#6b3f26') + (255,), width=5)
        self.room = grain(bg)
        def win(d, S):
            R = 230
            d.ellipse((0, 0, 2 * R * S, 2 * R * S), fill=hexc('#7b4a2d') + (255,))
            d.ellipse((20 * S, 20 * S, (2 * R - 20) * S, (2 * R - 20) * S), fill=hexc('#1a2556') + (255,))
            for (x, y) in ((90, 120), (330, 160), (140, 330), (300, 360), (220, 90)): star(d, x * S, y * S, 10 * S, hexc('#fff0b0'))
            d.ellipse((60 * S, 230 * S, 520 * S, 600 * S), fill=hexc('#2e3a6e') + (255,))
            d.ellipse((0, 0, 2 * R * S, 2 * R * S), outline=hexc('#6b3f26') + (255,), width=22 * S)
            d.line([(R * S, 10 * S), (R * S, (2 * R - 10) * S)], fill=hexc('#6b3f26') + (255,), width=12 * S)
        self.win = sprite(win, 460, 460)
        self.bigmoon = moon_face(70)
        def bed(d, S):
            d.rounded_rectangle((0, 0, 70 * S, 420 * S), 30 * S, fill=hexc('#a8693e') + (255,))
            d.rounded_rectangle((690 * S, 120 * S, 760 * S, 420 * S), 30 * S, fill=hexc('#a8693e') + (255,))
            d.rectangle((40 * S, 240 * S, 720 * S, 360 * S), fill=hexc('#8c5631') + (255,))
        self.bed = sprite(bed, 760, 420)
        def quilt(d, S):
            d.rounded_rectangle((0, 0, 640 * S, 170 * S), 40 * S, fill=hexc('#e8873a') + (255,))
            for i in range(8):
                for j in range(2):
                    if (i + j) % 2: d.rectangle(((20 + i * 76) * S, (20 + j * 66) * S, (90 + i * 76) * S, (80 + j * 66) * S), fill=hexc('#f1b92f') + (255,))
        self.quilt = sprite(quilt, 640, 170)
        self.pillow = sprite(lambda d, S: d.ellipse((0, 0, 220 * S, 110 * S), fill=CREAM + (255,)), 220, 110)
        self.zf = [text_img(["z"], lora(64), hexc('#9fb6ff')), text_img(["Z"], lora(84), hexc('#9fb6ff'))]
    def make_kitchen(self):
        bg = Image.new('RGBA', (W, H), hexc('#f3d39b') + (255,)); d = ImageDraw.Draw(bg)
        for y in range(0, 860, 70):
            for x in range(0 if (y // 70) % 2 else 35, W, 70):
                d.rectangle((x, y, x + 66, y + 66), fill=hexc('#efc98a') + (255,))
        d.rectangle((0, 860, W, H), fill=hexc('#b0723f') + (255,))
        self.kroom = grain(bg)
        def stove(d, S):
            d.rounded_rectangle((0, 120 * S, 520 * S, 560 * S), 30 * S, fill=hexc('#4f5b84') + (255,))
            d.rectangle((0, 100 * S, 520 * S, 150 * S), fill=hexc('#3e4870') + (255,))
            d.rounded_rectangle((90 * S, 260 * S, 430 * S, 470 * S), 30 * S, fill=hexc('#2b3466') + (255,))
            d.rectangle((380 * S, 0, 440 * S, 110 * S), fill=hexc('#3e4870') + (255,))
        self.stove = sprite(stove, 520, 560)
        def shelf(d, S):
            d.rectangle((0, 90 * S, 520 * S, 108 * S), fill=hexc('#8c5631') + (255,))
            for k, c in enumerate(('#d9433b', '#4f8fe0', '#7cae4a', '#f1b92f', '#d9433b')):
                x = 20 + k * 100
                d.rounded_rectangle((x * S, (20 + (k % 2) * 14) * S, (x + 70) * S, 92 * S), 14 * S, fill=hexc(c) + (255,))
                d.rectangle(((x + 10) * S, (14 + (k % 2) * 14) * S, (x + 60) * S, (30 + (k % 2) * 14) * S), fill=CREAM + (255,))
        self.kshelf = sprite(shelf, 520, 110)
        def pot(d, S):
            d.ellipse((0, 30 * S, 200 * S, 160 * S), fill=hexc('#d9433b') + (255,))
            d.rectangle((10 * S, 20 * S, 190 * S, 60 * S), fill=hexc('#b5352f') + (255,))
            d.ellipse((80 * S, 0, 120 * S, 30 * S), fill=hexc('#b5352f') + (255,))
        self.pot = sprite(pot, 200, 160)
        def flint(d, S):
            d.rounded_rectangle((0, 20 * S, 90 * S, 70 * S), 16 * S, fill=hexc('#8a8f9e') + (255,))
            d.rounded_rectangle((60 * S, 0, 150 * S, 40 * S), 10 * S, fill=hexc('#5b5f6d') + (255,))
        self.flint = sprite(flint, 150, 70)
        self.lcandle = candle(False)
    def make_letter(self):
        self.letter = letter(); self.feather = feather(1.)
        self.ltitle = text_img(["Un mot pour la Lune"], lora(84), RED); self.lcard = paper_card(940, 150)
        self.desk = sprite(lambda d, S: (d.rounded_rectangle((0, 0, 900 * S, 60 * S), 20 * S, fill=hexc('#a8693e') + (255,)),
                                          d.rectangle((60 * S, 50 * S, 110 * S, 330 * S), fill=hexc('#8c5631') + (255,)),
                                          d.rectangle((790 * S, 50 * S, 840 * S, 330 * S), fill=hexc('#8c5631') + (255,))), 900, 330)
        self.paper = sprite(lambda d, S: (d.rectangle((0, 0, 300 * S, 200 * S), fill=CREAM + (255,)),
                                           [d.line([(30 * S, (40 + k * 36) * S), (270 * S, (40 + k * 36) * S)], fill=hexc('#e6d3a8') + (255,), width=3 * S) for k in range(5)]), 300, 200, (2, 4, 4, .2))
        self.word = text_img(["Bonne nuit, Lune !"], lora(34), hexc('#3e5e93'))
    def make_terrace(self):
        def ledge(d, S):
            d.rectangle((0, 40 * S, W * S, 240 * S), fill=hexc('#6b77a3') + (255,))
            d.rectangle((0, 20 * S, W * S, 60 * S), fill=hexc('#8a95c0') + (255,))
            for x in range(0, W, 160): d.rectangle((x * S, 60 * S, (x + 8) * S, 240 * S), fill=hexc('#5d6a94') + (255,))
        self.ledge = sprite(ledge, W, 240, (0, -5, 8, .25))
        self.lan = sprite(lambda d, S: (d.line([(40 * S, 0), (40 * S, 40 * S)], fill=INK + (255,), width=3 * S),
                                         d.rounded_rectangle((8 * S, 36 * S, 72 * S, 120 * S), 20 * S, fill=hexc('#ffcf5a') + (255,)),
                                         d.rectangle((14 * S, 30 * S, 66 * S, 44 * S), fill=hexc('#7b4a2d') + (255,))), 80, 124, (2, 4, 4, .18))
        self.small_letter = letter()
        self.feather = feather(.6)
    # ----- décor commun : nuit sur les toits
    def town(self, fr, tl, spd=0., moonx=1460, moony=70, lit_k=None):
        fr.alpha_composite(self.nsky)
        self.stars.draw(fr, tl)
        put(fr, self.moon, moonx - self.moon.width / 2, moony + 6 * math.sin(tl * .9))
        blit_scroll(fr, self.far, 300 + tl * spd * .4)
        blit_scroll(fr, self.near, 900 + tl * spd)
        if lit_k is not None:
            d = ImageDraw.Draw(fr); off = (900 + tl * spd) % LW
            for i, (wx, wy, ww, wh, _) in enumerate(self.nwins):
                k = clamp(lit_k * len(self.nwins) - i * 1.0)
                if k <= 0: continue
                x = wx - off
                if x < -ww: x += LW
                if not -ww < x < W: continue
                col = lerp(hexc('#2b3466'), hexc('#ffd35a'), k)
                d.rounded_rectangle((x, wy, x + ww, wy + wh), 10, fill=col + (255,))
                d.line([(x + ww / 2, wy), (x + ww / 2, wy + wh)], fill=hexc('#8c7a5e') + (255,), width=4)
                d.line([(x, wy + wh / 2), (x + ww, wy + wh / 2)], fill=hexc('#8c7a5e') + (255,), width=4)
    # ----- intro : la Lune se lève sur le village
    def do_intro(self, fr, t, tl, b):
        self.town(fr, tl, 0, moonx=1720, moony=420 - 330 * ease(b / 12))
        k = back((b - .4) / 2.2)
        if k > 0:
            sy = 150 - (1 - k) * 900 + 8 * math.sin(tl * 2)
            put(fr, self.sign, (W - self.sign.width) / 2, sy)
            put(fr, self.title, (W - self.title.width) / 2, sy + 72)
            put(fr, self.sub, (W - self.sub.width) / 2, sy + 238)
        lx = -150 + 470 * ease((b - 3) / 3)
        draw_char(fr, 'lulu', lx, 1000, t, b, hop=30 if 3 < b < 6 else 0, R=150)
        put(fr, self.candle, lx + 70, 1000 - 190)
        if b < 1: put_fade(fr, 1 - b, hexc('#0e1840'))
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#2b3466'))
    # ----- v1 : Lulu traverse le toit jusqu'à la porte de Pierrot
    def do_v1(self, fr, t, tl, b):
        self.town(fr, tl, 0, moonx=960, moony=40)
        put(fr, self.tower, 1380, 60)
        put(fr, self.roof, 0, 660)
        put(fr, self.dormer, 60, 330)
        sing = self.ly.singing(b)
        # trajet : sort de la lucarne (0-14), marche le long du toit (14-46), frappe à la porte (48-64)
        k = ease((b - 12) / 34)
        x = 250 + (1390 - 250) * k
        foot = 880 - (880 - 838) * k
        draw_char(fr, 'lulu', x, foot, t, b, hop=26 if 12 < b < 46 else 0, sing=sing, R=160)
        cx, cy = x + 72, foot - 190
        put(fr, self.candle, cx, cy)
        # fumée de la chandelle éteinte, au moment de "Ma chandelle est morte"
        if 32 <= b < 48:
            for j in range(3):
                ph = ((b - 32) / 3 + j / 3) % 1
                put_alpha(fr, self.smoke[0], cx + 50 + 20 * math.sin(ph * 6), cy - 20 - 120 * ph, 1 - ph)
        # toc toc à la porte
        if b >= 48:
            for o in (48, 49, 52, 53, 56, 57):
                ph = (b - o) / 1.5
                if 0 <= ph < 1: put_alpha(fr, self.knock, 1520 - self.knock.width / 2 + 40 * ph, 470 - 60 * ph, 1 - ph)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#2b3466'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#3b3f7a'))
    # ----- v2 : Pierrot au lit, puis la cuisine de Madame Lapine
    def do_v2(self, fr, t, tl, b):
        sing = self.ly.singing(b)
        if b < 32:
            fr.alpha_composite(self.room)
            put(fr, self.win, 1340, 90)
            put(fr, self.bigmoon, 1340 + 230 - self.bigmoon.width / 2, 90 + 200 - self.bigmoon.height / 2)
            put(fr, self.bed, 160, 520)
            put(fr, self.pillow, 230, 560)
            # Pierrot répond depuis son lit
            awake = b >= 14
            s = 1 + (.03 * math.sin(tl * 2.2) if not awake else 0)
            draw_char(fr, 'pierrot', 400, 760, t, b, hop=0, sing=sing and b >= 6, R=150, scale=s, tilt=-6 if not awake else 4 * math.sin(tl * 2))
            put(fr, self.quilt, 220, 640)
            if not awake:
                for kk in range(3):
                    ph = (tl * .45 + kk / 3) % 1; a = min(1, ph * 4) * (1 - ph)
                    put_alpha(fr, self.zf[kk % 2], 480 + 70 * ph, 520 - 190 * ph, a)
            # Lulu à la porte (à droite), chandelle éteinte
            k = ease(b / 3)
            draw_char(fr, 'lulu', 1150 + 300 * (1 - k), 900, t, b, hop=0 if b > 3 else 26, R=160, tilt=-6 * math.sin(tl * 2))
            put(fr, self.candle, 1150 + 300 * (1 - k) + 72, 900 - 190)
            sweep(fr, 1 - b / .5, hexc('#3b3f7a'), rev=True)
            sweep(fr, (b - 31.5) / .5, hexc('#f3d39b'))
        else:
            bb = b - 32
            fr.alpha_composite(self.kroom)
            put(fr, self.kshelf, 160, 200)
            put(fr, self.stove, 1240, 330)
            put(fr, self.pot, 1340, 360)
            # Madame Lapine bat le briquet : étincelles sur chaque syllabe de la dernière ligne
            draw_char(fr, 'lapine', 1000, 900, t, b, hop=18, sing=sing, R=160, phase=.3)
            fx, fy = 1075, 790 + 10 * math.sin(tl * 6)
            put(fr, self.flint, fx, fy)
            ons = [n[1] for n in SEC['v2']['lignes'][3]]
            self.sparks.draw(fr, fx + 140, fy + 10, b, ons)
            # Lulu arrive, et sa chandelle se rallume sur "briquet"
            k = ease(bb / 4)
            lx = -150 + 560 * k
            draw_char(fr, 'lulu', lx, 900, t, b, hop=26 if bb < 4 else 0, sing=sing, R=160)
            put(fr, self.lcandle, lx + 72, 710)
            lit = clamp((b - 60) / 1.2)
            if lit > 0:
                put_alpha(fr, self.glow, lx + 72 + 70 - 150, 710 + 50 - 150, lit)
                fl = self.flame.resize((int(60 * (.6 + .4 * lit)), int(80 * (.6 + .4 * lit))))
                put(fr, fl, lx + 72 + 70 - fl.width / 2, 710 + 58 - fl.height)
            sweep(fr, 1 - bb / .5, hexc('#f3d39b'), rev=True)
            sweep(fr, (b - (self.len - .5)) / .5, hexc('#0e1840'))
        self.ly.draw(fr, b)
    # ----- lettre (séquence inédite) : Pierrot offre une plume, la lettre s'envole jusqu'à la Lune
    def do_lettre(self, fr, t, tl, b):
        if b < 12:
            # au bureau, sous la lune : Pierrot laisse tomber une plume, Lulu écrit
            self.town(fr, tl, 0, moonx=1680, moony=60)
            put(fr, self.desk, 520, 730)
            put(fr, self.paper, 860, 540)
            wk = clamp((b - 5) / 4)
            if wk > 0:
                wd = self.word.crop((0, 0, max(1, int(self.word.width * wk)), self.word.height))
                put(fr, wd, 1010 - self.word.width / 2, 600)
            draw_char(fr, 'pierrot', 1580, 900, t, b, hop=0, R=140, tilt=5 * math.sin(tl * 2))
            fk = ease(b / 3)
            if b < 5:
                fx = 1450 - 520 * fk + 30 * math.sin(b * 3); fy = 400 + 90 * fk
                put(fr, self.feather.rotate(20 * math.sin(b * 2.5), Image.BICUBIC, expand=True), fx, fy)
            else:
                put(fr, self.feather.rotate(-30 + 10 * math.sin(b * 6), Image.BICUBIC, expand=True), 880 + 170 * wk, 470)
            draw_char(fr, 'lulu', 360, 900, t, b, hop=0, R=150, tilt=4 * math.sin(tl * 3))
            put(fr, self.candle, 600, 556)
            put(fr, self.glow, 600 + 70 - 150, 556 + 50 - 150)
            put(fr, self.flame, 600 + 40, 556 - 20)
            put(fr, self.lcard, (W - self.lcard.width) / 2, 40)
            put(fr, self.ltitle, (W - self.ltitle.width) / 2, 66)
            sweep(fr, 1 - b / .5, hexc('#0e1840'), rev=True)
        else:
            # vol de la lettre au-dessus des toits, traîne d'étoiles, la Lune l'attrape et sourit
            bb = b - 12
            self.town(fr, tl, 220, moonx=1450, moony=90)
            p = clamp(bb / 16)
            def pos(q):
                return 160 + 1200 * q + 60 * math.sin(q * 9), 760 - 600 * q + 90 * math.sin(q * 6)
            d = ImageDraw.Draw(fr)
            for j in range(18):
                q = p - j * .012
                if q < 0: break
                x, y = pos(q); star(d, x, y + 40, 12 - j * .5, (255, 236, 160), int(230 * (1 - j / 18)))
            if p < .97:
                x, y = pos(p)
                put(fr, self.letter.rotate(-20 + 15 * math.sin(bb * 2), Image.BICUBIC, expand=True), x - 90, y - 40)
            if bb > 15:
                hk = clamp((bb - 15) / 2)
                put_alpha(fr, glow(260, (255, 230, 150), 140), 1450 - 260, 90 + self.moon.height / 2 - 260, hk)
                for k in range(8):
                    an = k / 8 * 6.283 + bb
                    star(d, 1450 + math.cos(an) * 260 * hk, 90 + self.moon.height / 2 + math.sin(an) * 260 * hk, 14, (255, 240, 190), int(255 * hk))
            sweep(fr, (b - (self.len - .5)) / .5, hexc('#33397c'))
    # ----- v3 : tous ensemble sur le toit, les fenêtres s'allument une à une
    def do_v3(self, fr, t, tl, b):
        self.town(fr, tl, 0, moonx=960, moony=50, lit_k=clamp(b / 60))
        put(fr, self.ledge, 0, 800)
        d = ImageDraw.Draw(fr)
        d.line([(0, 330), (W / 2, 420), (W, 330)], fill=hexc('#2a2f5c') + (255,), width=4)
        for k in range(9):
            u = (k + .5) / 9; x = u * W; y = 330 + 90 * (1 - abs(2 * u - 1)) ** 1
            on = b >= k * 6
            s = self.lan if on else None
            if s: put(fr, s.rotate(6 * math.sin(tl * 2 + k), Image.BICUBIC), x - 40, y)
        sing = self.ly.singing(b)
        draw_char(fr, 'lapine', 520, 840, t, b, hop=24, sing=sing, R=160, phase=.3)
        draw_char(fr, 'lulu', 960, 840, t, b, hop=30, sing=sing, R=165)
        put(fr, self.candle, 960 + 72, 650)
        put(fr, self.flame, 960 + 72 + 40, 650 - 20)
        draw_char(fr, 'pierrot', 1400, 840, t, b, hop=24, sing=sing, R=150, phase=.6)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#33397c'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#2b3466'))
    # ----- fin
    def do_outro(self, fr, t, tl, b):
        self.town(fr, tl, 0, moonx=1730, moony=40, lit_k=1.)
        put(fr, self.ledge, 0, 840)
        k = back((b - .4) / 1.6)
        sy = 150 + (1 - k) * 800
        put(fr, self.card2, (W - self.card2.width) / 2, sy)
        put(fr, self.bye, (W - self.bye.width) / 2, sy + 52)
        put(fr, self.credit, (W - self.credit.width) / 2, sy + 216)
        calm = b >= 12
        draw_char(fr, 'lapine', 560, 900, t, b, hop=0 if calm else 30, R=150, tilt=8 * math.sin(tl * 3))
        draw_char(fr, 'lulu', 960, 900, t, b, hop=0 if calm else 34, R=150, phase=.5, tilt=-8 * math.sin(tl * 3))
        draw_char(fr, 'pierrot', 1360, 900, t, b, hop=0 if calm else 30, R=140, phase=.25, tilt=8 * math.sin(tl * 3 + 1))
        sweep(fr, 1 - b / .5, hexc('#2b3466'), rev=True)
        end = self.tend - t
        if end < .9: put_fade(fr, 1 - end / .9, CREAM)
