# Scènes de "Frère Jacques" : Jacques le hérisson dort dans sa maison-arbre,
# sa petite sœur Lili et la mésange Tiou font sonner les cloches de la forêt d'automne.
from papier import *
from papier import Scenes as Base

def rond(cx, cy, R):
    return [(cx + R * 1.02 * math.sin(i / 200 * 2 * math.pi), cy - R * .96 * math.cos(i / 200 * 2 * math.pi)) for i in range(200)]

def herisson(R, c1, c2, pique, blink, mouth, cap=False, bow=None, scarf=None):
    body = apple(R, c1, c2, True, blink, mouth, bow=bow, feet=True, leaf=False, tige=False, contour=rond)
    w, h = body.size; S = 3
    cx, cy = w * S / 2, h * .54 * S; Rs = R * S
    back_ = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(back_)
    dk = lerp(pique, (0, 0, 0), .22)
    for k, a in enumerate(np.linspace(-200, 20, 23)):
        r_ = math.radians(a); da = math.radians(7.5)
        col = pique if k % 2 else dk
        p0 = (cx + math.cos(r_ - da) * Rs * .86, cy + math.sin(r_ - da) * Rs * .86)
        p1 = (cx + math.cos(r_) * Rs * 1.3, cy + math.sin(r_) * Rs * 1.3)
        p2 = (cx + math.cos(r_ + da) * Rs * .86, cy + math.sin(r_ + da) * Rs * .86)
        d.polygon([p0, p1, p2], fill=col + (255,))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.alpha_composite(grain(back_.resize((w, h), Image.LANCZOS))); out.alpha_composite(body)
    top = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
    d.ellipse((cx - Rs * .08, cy + Rs * .12, cx + Rs * .08, cy + Rs * .24), fill=INK + (255,))
    if scarf:
        y = cy + Rs * .78
        d.rounded_rectangle((cx - Rs * .62, y - Rs * .1, cx + Rs * .62, y + Rs * .1), int(Rs * .1), fill=scarf + (255,))
        d.polygon([(cx + Rs * .22, y), (cx + Rs * .42, y + Rs * .26), (cx + Rs * .16, y + Rs * .24)], fill=lerp(scarf, (0, 0, 0), .15) + (255,))
    if cap:
        blue, white = hexc('#5b7fd6'), hexc('#fff4dc')
        base_y = cy - Rs * .62
        pts = [(cx - Rs * .78, base_y), (cx + Rs * .78, base_y), (cx + Rs * 1.15, cy - Rs * 1.45)]
        d.polygon(pts, fill=blue + (255,))
        for t in (.3, .6):
            a0 = (pts[0][0] + (pts[2][0] - pts[0][0]) * t, pts[0][1] + (pts[2][1] - pts[0][1]) * t)
            a1 = (pts[1][0] + (pts[2][0] - pts[1][0]) * t, pts[1][1] + (pts[2][1] - pts[1][1]) * t)
            d.line([a0, a1], fill=white + (255,), width=int(Rs * .09))
        d.rounded_rectangle((cx - Rs * .84, base_y - Rs * .06, cx + Rs * .84, base_y + Rs * .14), int(Rs * .08), fill=white + (255,))
        q = Rs * .16; d.ellipse((pts[2][0] - q, pts[2][1] - q, pts[2][0] + q, pts[2][1] + q), fill=white + (255,))
    out.alpha_composite(top.resize((w, h), Image.LANCZOS))
    return out

def oiseau(R, c1, c2, blink, mouth):
    body = apple(R, c1, c2, True, blink, mouth, feet=True, leaf=False, tige=False, contour=rond)
    w, h = body.size; S = 3; cx, cy = w * S / 2, h * .54 * S; Rs = R * S
    back_ = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(back_)
    wing = lerp(c2, (0, 0, 0), .15)
    for sg in (-1, 1):
        d.ellipse((cx + sg * Rs * .95 - Rs * .3, cy - Rs * .05, cx + sg * Rs * .95 + Rs * .3, cy + Rs * .55), fill=wing + (255,))
    for k in range(3):
        d.ellipse((cx - Rs * .1 + (k - 1) * Rs * .16, cy - Rs * 1.22 + abs(k - 1) * Rs * .1, cx + Rs * .1 + (k - 1) * Rs * .16, cy - Rs * .8), fill=wing + (255,))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.alpha_composite(grain(back_.resize((w, h), Image.LANCZOS))); out.alpha_composite(body)
    top = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(top)
    d.polygon([(cx - Rs * .13, cy + Rs * .1), (cx + Rs * .13, cy + Rs * .1), (cx, cy + Rs * .3)], fill=hexc('#f6a23a') + (255,))
    d.rounded_rectangle((cx - Rs * .7, cy - Rs * .62, cx + Rs * .7, cy - Rs * .48), int(Rs * .07), fill=hexc('#fff4dc') + (255,))
    out.alpha_composite(top.resize((w, h), Image.LANCZOS))
    return out

PERSOS['jacques'] = lambda blink, mouth, R: herisson(R, hexc('#e3b98c'), hexc('#c4925f'), hexc('#7a5236'), blink, mouth)
PERSOS['dodo'] = lambda blink, mouth, R: herisson(R, hexc('#e3b98c'), hexc('#c4925f'), hexc('#7a5236'), True, False, cap=True)
PERSOS['reveil'] = lambda blink, mouth, R: herisson(R, hexc('#e3b98c'), hexc('#c4925f'), hexc('#7a5236'), blink, True, cap=True)
PERSOS['lili'] = lambda blink, mouth, R: herisson(int(R * .76), hexc('#f6cfae'), hexc('#e3a37f'), hexc('#b0785a'), blink, mouth, bow=hexc('#ff6f91'), scarf=hexc('#f1b92f'))
PERSOS['tiou'] = lambda blink, mouth, R: oiseau(int(R * .62), hexc('#8fd0f4'), hexc('#4b9ddb'), blink, mouth)

AUT = ['#e8652f', '#f1a53a', '#d8452e', '#f4c84a', '#b7562d']

def sprite(fn, w, h, sh=(4, 8, 7, .24)):
    S = 2; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), S)
    return shadowed(grain(im.resize((w, h), Image.LANCZOS)), *sh)

def gradient(top, bot, k=1.1):
    a, b = np.array(hexc(top), np.float32), np.array(hexc(bot), np.float32)
    t = np.linspace(0, 1, H)[:, None, None] ** k
    return grain(Image.fromarray(np.repeat(a * (1 - t) + b * t, W, 1).astype(np.uint8), 'RGB').convert('RGBA'))

def leaf(col, R=26):
    c = hexc(col)
    def f(d, S):
        cx, cy = R * 1.2 * S, R * 1.2 * S
        pts = [(cx + math.cos(t) * R * S, cy + math.sin(t) * R * .55 * S * (1 - .25 * math.cos(t))) for t in np.linspace(0, 6.283, 60)]
        d.polygon(pts, fill=c + (255,))
        d.line([(cx - R * S, cy), (cx + R * S, cy)], fill=lerp(c, (0, 0, 0), .25) + (255,), width=max(2, int(R * .1 * S)))
    return sprite(f, int(R * 2.4), int(R * 2.4), (2, 4, 4, .16))

def autumn_tree(seed, sc=1., pine=False, cols=None):
    r = np.random.default_rng(seed)
    def f(d, S):
        w, h = 360 * sc * S, 520 * sc * S; c = w / 2
        tr = hexc('#7b4a2d')
        if pine:
            g = [hexc('#3f7a52'), hexc('#4f9160'), hexc('#5fa36c')]
            d.rectangle((c - 16 * sc * S, h * .78, c + 16 * sc * S, h), fill=tr + (255,))
            for k in range(4):
                y0 = h * (.06 + k * .18); y1 = y0 + h * .34; hw = (60 + k * 38) * sc * S
                d.polygon([(c, y0), (c - hw, y1), (c + hw, y1)], fill=g[k % 3] + (255,))
            return
        d.polygon([(c - 26 * sc * S, h), (c - 14 * sc * S, h * .5), (c + 14 * sc * S, h * .5), (c + 26 * sc * S, h)], fill=tr + (255,))
        cs = [hexc(x) for x in (cols or AUT)]
        for i in range(11):
            x, y, q = c + r.uniform(-110, 110) * sc * S, h * .36 + r.uniform(-90, 70) * sc * S, r.uniform(70, 110) * sc * S
            d.ellipse((x - q, y - q, x + q, y + q), fill=cs[i % len(cs)] + (255,))
    return sprite(f, int(360 * sc), int(520 * sc), (3, 6, 6, .2))

def forest_layer(col, base, amp, seed, ntrees, tsc, pine_every=3, cols=None):
    r = np.random.default_rng(seed); x = np.arange(LW); ph = r.uniform(0, 6.28, 3)
    y = base + amp * (.6 * np.sin(2 * np.pi * x / LW * 2 + ph[0]) + .3 * np.sin(2 * np.pi * x / LW * 5 + ph[1]) + .1 * np.sin(2 * np.pi * x / LW * 9 + ph[2]))
    im = Image.new('RGBA', (LW, H), (0, 0, 0, 0))
    for i in range(ntrees):
        tx = int((i + .5 + r.uniform(-.3, .3)) / ntrees * LW) % LW
        t_ = autumn_tree(seed * 10 + i, tsc * r.uniform(.8, 1.15), pine=(i % pine_every == 0), cols=cols)
        im.alpha_composite(t_, (max(0, min(LW - t_.width, tx - t_.width // 2)), int(y[tx] - t_.height + 20)))
    d = Image.new('RGBA', (LW, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(d)
    dd.polygon([(0, H)] + [(int(a), float(b)) for a, b in zip(x[::8], y[::8])] + [(LW - 1, float(y[-1])), (LW - 1, H)], fill=hexc(col) + (255,))
    im.alpha_composite(shadowed(d, 0, -6, 8, .18))
    return y, grain(im)

class Leaves:
    def __init__(self, n, seed, spr):
        r = np.random.default_rng(seed); self.spr = spr
        self.p = [(r.uniform(0, W), r.uniform(0, H + 200), r.uniform(70, 140), r.uniform(0, 6.28), r.uniform(30, 80), int(r.integers(len(spr)))) for _ in range(n)]
    def draw(self, fr, tl, k=1., ymax=H):
        for x, y0, sp, ph, sw, i in self.p[:int(len(self.p) * k)]:
            y = (y0 + tl * sp) % (H + 200) - 100
            if y > ymax: continue
            xx = x + math.sin(tl * 1.3 + ph) * sw
            s = self.spr[i].rotate(math.degrees(math.sin(tl * 1.7 + ph)) * .8 + ph * 40, Image.BILINEAR, expand=True)
            put(fr, s, xx - s.width / 2, y - s.height / 2)

def bell(R, col):
    c = hexc(col); dk = lerp(c, (0, 0, 0), .25); lt = lerp(c, (255, 255, 255), .45)
    def f(d, S):
        cx = R * 1.3 * S; top = R * .35 * S
        d.ellipse((cx - R * .18 * S, top - R * .3 * S, cx + R * .18 * S, top + R * .05 * S), outline=dk + (255,), width=int(R * .08 * S))
        pts = []
        for t in np.linspace(0, 1, 40):
            hw = R * (.42 + .58 * t ** 2.2) * S; pts.append((cx - hw, top + t * R * 1.5 * S))
        pts += [(2 * cx - x, y) for x, y in pts[::-1]]
        d.polygon(pts, fill=c + (255,))
        d.ellipse((cx - R * 1.02 * S, top + R * 1.36 * S, cx + R * 1.02 * S, top + R * 1.64 * S), fill=dk + (255,))
        d.ellipse((cx - R * .2 * S, top + R * 1.48 * S, cx + R * .2 * S, top + R * 1.78 * S), fill=lerp(c, (0, 0, 0), .45) + (255,))
        d.ellipse((cx - R * .45 * S, top + R * .25 * S, cx - R * .25 * S, top + R * .95 * S), fill=lt + (200,))
    return sprite(f, int(R * 2.6), int(R * 2.3), (3, 7, 6, .22))

def swing_angle(onsets, b, amp=16):
    last = None
    for i, o in enumerate(onsets):
        if o <= b: last = (i, o)
    if last is None: return 0.
    i, o = last; dt = (b - o) * B
    return (1 if i % 2 else -1) * amp * math.sin(min(dt * 7, math.pi * .5) + max(0, dt * 7 - math.pi * .5)) * math.exp(-dt * 1.6)

def put_rot(fr, s, ang, px, py):
    """Pose un sprite suspendu par son point haut-centre (px, py), incliné de ang degrés."""
    big = Image.new('RGBA', (s.width * 2, s.height * 2), (0, 0, 0, 0)); big.alpha_composite(s, (s.width // 2, s.height))
    rot = big.rotate(ang, Image.BICUBIC)
    put(fr, rot, px - rot.width / 2, py - rot.height / 2)

def zzz(fr, x, y, tl, f):
    for k in range(3):
        ph = (tl * .45 + k / 3) % 1
        a = int(255 * min(1, ph * 4) * (1 - ph))
        im = f[k % 2].copy(); im.putalpha(im.getchannel('A').point(lambda v: v * a // 255))
        put(fr, im, x + 70 * ph + 18 * math.sin(ph * 9), y - 190 * ph)

class Scenes(Base):
    def prepare(self):
        n = self.name
        self.leafs = [leaf(c, 24) for c in AUT]
        self.zf = [text_img(["z"], lora(64), hexc('#5b7fd6')), text_img(["Z"], lora(84), hexc('#5b7fd6'))]
        if n in ('intro', 'v2', 'v3', 'outro'):
            self.sky_dawn = gradient('#f7a98a', '#ffe9c4') if n in ('intro', 'v2') else gradient('#8fd3f0', '#fff0d2')
            self.fl = [forest_layer('#d98b4c', 640, 46, 4, 9, .7), forest_layer('#bf6f3a', 750, 36, 6, 7, .95, 4),
                       forest_layer('#9a5a33', 870, 22, 9, 0, 1)]
            self.sunrise = sun(110, hexc('#ffd35a'), hexc('#ffc23f'))
            self.lv = Leaves(26, 3, self.leafs)
        if n in ('intro', 'outro'):
            self.title = text_img(["Frère Jacques"], lora(128), RED)
            self.sub = text_img(["Comptine à chanter ensemble"], font('Poppins-Medium.ttf', 40), INK)
            self.sign = paper_card(1080, 330)
            self.bye = text_img(["À bientôt !"], lora(118), RED)
            self.credit = text_img(["Comptine traditionnelle française · Arrangement original"], font('Poppins-Medium.ttf', 32), INK)
            self.card2 = paper_card(1160, 280)
        if n == 'v1': self.make_room()
        if n == 'v2': self.make_belfry(); self.make_trunk()
        if n == 'canon': self.make_canon()
        if n == 'v3':
            self.belfry_small = self.make_belfry(.55)
            self.basket = self.make_basket()
    # --- éléments
    def make_room(self):
        bg = Image.new('RGBA', (W, H), hexc('#7b4a2d') + (255,)); d = ImageDraw.Draw(bg)
        d.ellipse((-140, -260, W + 140, 1010), fill=hexc('#f7dcb0') + (255,))
        for k in range(7):
            d.arc((-140 + k * 60, -260 + k * 60, W + 140 - k * 60, 1010 - k * 60), 200, 340, fill=hexc('#efcb98') + (255,), width=14)
        d.rectangle((0, 840, W, H), fill=hexc('#a8693e') + (255,))
        for x in range(0, W, 180): d.line([(x, 840), (x, H)], fill=hexc('#93582f') + (255,), width=5)
        self.room = grain(bg)
        # fenêtre ronde sur l'aube
        S = 2; R = 170
        def win(d, S):
            d.ellipse((0, 0, 2 * R * S, 2 * R * S), fill=hexc('#9a5a33') + (255,))
            d.ellipse((18 * S, 18 * S, (2 * R - 18) * S, (2 * R - 18) * S), fill=hexc('#ffc49a') + (255,))
            d.ellipse((90 * S, 150 * S, 250 * S, 310 * S), fill=hexc('#ffd35a') + (255,))
            d.ellipse((-40 * S, 220 * S, 230 * S, 420 * S), fill=hexc('#d98b4c') + (255,))
            d.ellipse((150 * S, 240 * S, 420 * S, 440 * S), fill=hexc('#bf6f3a') + (255,))
            d.ellipse((0, 0, 2 * R * S, 2 * R * S), outline=hexc('#7b4a2d') + (255,), width=20 * S)
            d.line([(R * S, 10 * S), (R * S, (2 * R - 10) * S)], fill=hexc('#7b4a2d') + (255,), width=12 * S)
            d.line([(10 * S, R * S), ((2 * R - 10) * S, R * S)], fill=hexc('#7b4a2d') + (255,), width=12 * S)
        self.window = sprite(win, 2 * R, 2 * R)
        # hamac de feuille
        def ham(d, S):
            d.line([(0, 20 * S), (120 * S, 150 * S)], fill=hexc('#6e4a32') + (255,), width=6 * S)
            d.line([(780 * S, 20 * S), (660 * S, 150 * S)], fill=hexc('#6e4a32') + (255,), width=6 * S)
            d.chord((100 * S, 30 * S, 680 * S, 260 * S), 0, 180, fill=hexc('#7cae4a') + (255,))
            for k in range(1, 6):
                d.line([(390 * S, 150 * S), ((110 + k * 95) * S, 220 * S)], fill=hexc('#5f9038') + (255,), width=4 * S)
        self.hammock = sprite(ham, 780, 270)
        self.lamp = sprite(lambda d, S: (d.line([(40 * S, 0), (40 * S, 60 * S)], fill=INK + (255,), width=3 * S),
                                          d.ellipse((5 * S, 55 * S, 75 * S, 125 * S), fill=hexc('#ffd35a') + (255,)),
                                          d.rectangle((25 * S, 50 * S, 55 * S, 62 * S), fill=hexc('#6e4a32') + (255,))), 80, 130)
        self.door = sprite(lambda d, S: (d.rounded_rectangle((0, 0, 260 * S, 520 * S), 130 * S, fill=hexc('#6e4a32') + (255,)),
                                          d.rounded_rectangle((18 * S, 18 * S, 242 * S, 520 * S), 112 * S, fill=hexc('#ffe3b3') + (255,))), 260, 520)
        self.shelf = sprite(lambda d, S: (d.rectangle((0, 70 * S, 420 * S, 86 * S), fill=hexc('#8c5631') + (255,)),
                                           [d.ellipse(((20 + k * 70) * S, (18 + (k % 2) * 8) * S, (70 + k * 70) * S, 72 * S), fill=hexc(['#c4925f', '#e8652f', '#7a5236'][k % 3]) + (255,)) for k in range(6)]), 420, 90)
    def make_belfry(self, sc=1.):
        def f(d, S):
            s = sc * S
            d.polygon([(110 * s, 760 * s), (150 * s, 200 * s), (330 * s, 200 * s), (370 * s, 760 * s)], fill=hexc('#a8693e') + (255,))
            for k in range(6): d.line([((150 + k * 36) * s, 220 * s), ((120 + k * 50) * s, 760 * s)], fill=hexc('#93582f') + (255,), width=int(5 * s))
            d.rectangle((150 * s, 200 * s, 330 * s, 420 * s), fill=hexc('#ffe3b3') + (255,))
            d.rectangle((140 * s, 190 * s, 340 * s, 215 * s), fill=hexc('#7b4a2d') + (255,))
            d.polygon([(90 * s, 200 * s), (240 * s, 30 * s), (390 * s, 200 * s)], fill=hexc('#d8452e') + (255,))
            d.polygon([(90 * s, 200 * s), (240 * s, 30 * s), (240 * s, 200 * s)], fill=hexc('#c23a27') + (255,))
        im = sprite(f, int(480 * sc), int(770 * sc))
        if sc == 1.: self.belfry = im; self.bigbell = bell(70, '#f1b92f')
        return im
    def make_trunk(self):
        def f(d, S):
            d.polygon([(60 * S, 900 * S), (110 * S, 0), (420 * S, 0), (470 * S, 900 * S)], fill=hexc('#8c5631') + (255,))
            for k in range(5): d.line([((140 + k * 60) * S, 0), ((110 + k * 75) * S, 900 * S)], fill=hexc('#7b4a2d') + (255,), width=6 * S)
            d.ellipse((150 * S, 260 * S, 390 * S, 500 * S), fill=hexc('#6e4a32') + (255,))
            d.ellipse((168 * S, 278 * S, 372 * S, 482 * S), fill=hexc('#f7dcb0') + (255,))
        self.trunk = sprite(f, 520, 900)
        cs = [hexc(x) for x in AUT]
        def crown(d, S):
            r = np.random.default_rng(12)
            for i in range(14):
                x, y, q = r.uniform(80, 620), r.uniform(60, 300), r.uniform(80, 130)
                d.ellipse(((x - q) * S, (y - q) * S, (x + q) * S, (y + q) * S), fill=cs[i % 5] + (255,))
        self.crown = sprite(crown, 700, 420)
    def make_canon(self):
        bg = Image.new('RGBA', (W, H), hexc('#fff4dc') + (255,)); d = ImageDraw.Draw(bg)
        for i, x in enumerate(range(-200, W + 200, 110)):
            d.polygon([(x, 0), (x + 55, 0), (x - 145, H), (x - 200, H)], fill=hexc('#ffe7c2') + (255,))
        d.rectangle((0, 930, W, H), fill=hexc('#e8b48a') + (255,))
        self.cbg = grain(bg)
        self.beam = sprite(lambda d, S: (d.rounded_rectangle((0, 0, 1600 * S, 46 * S), 20 * S, fill=hexc('#8c5631') + (255,)),
                                          d.rectangle((0, 18 * S, 1600 * S, 26 * S), fill=hexc('#7b4a2d') + (255,))), 1600, 46)
        self.bells = [bell(64, '#f1b92f'), bell(90, '#e8873a'), bell(46, '#f4d36b')]
        f = font('Poppins-Bold.ttf', 58)
        self.nums = [text_img([str(k + 1)], f, CREAM) for k in range(3)]
        self.badge = sprite(lambda d, S: d.ellipse((0, 0, 96 * S, 96 * S), fill=RED + (255,)), 96, 96, (2, 4, 4, .2))
        self.ctitle = text_img(["Chantons en canon !"], lora(84), RED); self.ccard = paper_card(900, 150)
        self.notes_spr = [text_img(["♪"], ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 70), hexc(c)) for c in ('#d8452e', '#5b7fd6', '#7cae4a')]
    def make_basket(self):
        def f(d, S):
            d.arc((30 * S, 0, 190 * S, 150 * S), 180, 360, fill=hexc('#8c5631') + (255,), width=10 * S)
            d.ellipse((50 * S, 40 * S, 110 * S, 100 * S), fill=hexc('#d8452e') + (255,))
            d.ellipse((100 * S, 35 * S, 165 * S, 100 * S), fill=hexc('#c4925f') + (255,))
            d.rounded_rectangle((10 * S, 70 * S, 210 * S, 170 * S), 30 * S, fill=hexc('#c98a4e') + (255,))
            for k in range(4): d.line([(20 * S, (90 + k * 20) * S), (200 * S, (90 + k * 20) * S)], fill=hexc('#a8693e') + (255,), width=4 * S)
        return sprite(f, 220, 175)
    # --- forêt extérieure
    def forest(self, fr, tl, spd, sunx=1450, suny=150):
        fr.alpha_composite(self.sky_dawn)
        put(fr, self.sunrise.rotate(tl * 8, Image.BILINEAR), sunx, suny)
        for i, (y, layer) in enumerate(self.fl):
            blit_scroll(fr, layer, 400 * i + tl * spd * (.3, .6, 1)[i])
    # --- intro : l'aube sur la forêt d'automne
    def do_intro(self, fr, t, tl, b):
        self.forest(fr, tl, 0, suny=330 - 140 * ease(b / 14))
        self.lv.draw(fr, tl, .6)
        draw_char(fr, 'lili', 300, 900, t, b, hop=34 * ease((b - 4) / 1), R=160)
        tx = 1640; ty = 820 - 140 * abs(math.sin(tl * 2.2))
        draw_char(fr, 'tiou', tx, ty, t, b, hop=0, R=160, tilt=10 * math.sin(tl * 4))
        k = back((b - .4) / 2.2)
        if k > 0:
            sy = 130 - (1 - k) * 900 + 8 * math.sin(tl * 2)
            put(fr, self.sign, (W - self.sign.width) / 2, sy)
            put(fr, self.title, (W - self.title.width) / 2, sy + 70)
            put(fr, self.sub, (W - self.sub.width) / 2, sy + 240)
        if b < 1: put_fade(fr, 1 - b)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#f7dcb0'))
    # --- v1 : Jacques dort dans sa maison-arbre
    def do_v1(self, fr, t, tl, b):
        fr.alpha_composite(self.room)
        put(fr, self.window, 1420, 120)
        put(fr, self.shelf, 980, 300)
        put(fr, self.door, 70, 330)
        put(fr, self.lamp, 860, 40 + 4 * math.sin(tl * 2))
        sw = 10 * math.sin(tl * 1.6)
        hx, hy = 880, 520
        put(fr, self.hammock, hx, hy + sw * .3)
        sing = self.ly.singing(b)
        # Jacques ronfle : il gonfle doucement
        breathe = 1 + .04 * math.sin(tl * 2.4)
        draw_char(fr, 'dodo', hx + 390 + sw, hy + 200 + sw * .3, t, b, hop=0, R=150, scale=breathe, tilt=-8 + sw * .3)
        zzz(fr, hx + 470, hy - 20, tl, self.zf)
        # Lili entre par la porte et l'appelle
        lk = ease((b - 1) / 2)
        lx = 200 + 380 * lk
        knock = 24 <= b < 32 and (b % 1) < .3
        draw_char(fr, 'lili', lx, 890, t, b, hop=30 if b > 3 else 0, sing=sing, R=165, tilt=-10 if knock else 0)
        # Tiou arrive par la fenêtre sur "Sonnez les matines"
        if b > 15:
            k = ease((b - 15) / 2.5)
            draw_char(fr, 'tiou', 1610 - 90 * k, 290 + 600 * k - 120 * math.sin(k * math.pi), t, b, hop=20 * (k >= 1), sing=sing and b >= 16, R=150, phase=.3)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#f7dcb0'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffd9b8'))
    # --- v2 : le clocher de la forêt
    def do_v2(self, fr, t, tl, b):
        self.forest(fr, tl, 0, sunx=1120, suny=170)
        self.lv.draw(fr, tl, .5, ymax=900)
        # maison-arbre de Jacques à droite, fenêtre avec Jacques endormi
        put(fr, self.trunk, 1380, 180); put(fr, self.crown, 1300, -60)
        wx, wy = 1380 + 270, 180 + 370
        s = char('dodo', True, False, 110)
        win = Image.new('RGBA', (204, 204), (0, 0, 0, 0)); win.alpha_composite(s, (102 - s.width // 2, 40 - int(s.height * .2) + int(4 * math.sin(tl * 2.4))))
        m = Image.new('L', (204, 204), 0); ImageDraw.Draw(m).ellipse((0, 0, 203, 203), fill=255)
        win.putalpha(Image.fromarray(np.minimum(np.array(win.getchannel('A')), np.array(m))))
        put(fr, win, wx - 102, wy - 102)
        zzz(fr, wx + 40, wy - 90, tl, self.zf)
        # clocher et grosse cloche
        bx, by = 260, 160
        put(fr, self.belfry, bx, by)
        on = [24, 25, 26, 28, 29, 30]
        ang = swing_angle([o for o in on], b, 22)
        put_rot(fr, self.bigbell, ang, bx + 240, by + 225)
        if 24 <= b < 33:
            for o in on:
                ph = (b - o) / 1.4
                if 0 <= ph < 1:
                    d = ImageDraw.Draw(fr); r_ = 140 + 160 * ph; a = int(220 * (1 - ph))
                    d.arc((bx + 240 - r_, by + 330 - r_, bx + 240 + r_, by + 330 + r_), -60, 60, fill=GOLD + (a,), width=8)
                    d.arc((bx + 240 - r_, by + 330 - r_, bx + 240 + r_, by + 330 + r_), 120, 240, fill=GOLD + (a,), width=8)
        # corde : Lili tire dessus
        pull = max(0, math.sin((b - 24) * math.pi)) * (24 <= b < 32)
        d = ImageDraw.Draw(fr)
        d.line([(bx + 240, by + 330), (bx + 240, 700 + 40 * pull)], fill=hexc('#f4e2bf') + (255,), width=8)
        sing = self.ly.singing(b)
        draw_char(fr, 'lili', bx + 240, 900 + 20 * pull, t, b, hop=0 if 24 <= b < 32 else 28, sing=sing, R=165)
        draw_char(fr, 'tiou', 860, 900, t, b, hop=40, sing=sing, R=150, phase=.5)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ffd9b8'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#fff4dc'))
    # --- canon : trois cloches qui chantent l'une après l'autre (séquence inédite)
    def do_canon(self, fr, t, tl, b):
        fr.alpha_composite(self.cbg)
        put(fr, self.ccard, (W - self.ccard.width) / 2, 30)
        put(fr, self.ctitle, (W - self.ctitle.width) / 2, 58)
        put(fr, self.beam, (W - self.beam.width) / 2, 260)
        entree = [0, 8, 16]
        mel = [n[1] for l in SEC['v1']['lignes'] for n in l]
        voix = [[o + e for o in mel if o + e < 32] for e in entree]
        xs = [960, 470, 1450]
        who = ['lili', 'tiou', 'reveil']
        for k in range(3):
            if b < entree[k] - 1.5: continue
            ak = back((b - entree[k] + 1.5) / 1.2)
            ang = swing_angle(voix[k], b, 18)
            put_rot(fr, self.bells[k], ang, xs[k], 300 - (1 - ak) * 50)
            # pastille du numéro de voix
            put(fr, self.badge, xs[k] - 48 - 150, 300 - (1 - ak) * 50 + 10)
            put(fr, self.nums[k], xs[k] - self.nums[k].width / 2 - 150 + 1, 300 - (1 - ak) * 50 + 16)
            # petites notes qui s'envolent
            for o in voix[k]:
                ph = (b - o) / 2
                if 0 <= ph < 1:
                    s = self.notes_spr[k]
                    put(fr, s, xs[k] + 60 + 90 * ph + 20 * math.sin(ph * 8), 560 - 260 * ph)
        # les sonneurs
        draw_char(fr, 'lili', xs[0], 900, t, b, hop=26, R=150, sing=True)
        if b > 6.5: draw_char(fr, 'tiou', xs[1], 900 - 30 * (1 - ease((b - 6.5) / 1.5)) * 10, t, b, hop=30, R=150, sing=True, phase=.4)
        # Jacques se réveille et arrive en courant pour la troisième cloche
        if b > 13:
            k = ease((b - 13) / 2.5)
            draw_char(fr, 'reveil', W + 200 - (W + 200 - xs[2]) * k, 900, t, b, hop=40, R=150, phase=.2, tilt=-8 * (1 - k))
        sweep(fr, 1 - b / .5, hexc('#fff4dc'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#bfe6f5'))
    # --- v3 : la promenade du matin, tous réveillés
    def do_v3(self, fr, t, tl, b):
        self.forest(fr, tl, 130, sunx=1500, suny=60)
        put(fr, self.belfry_small, 1330, 300)
        self.lv.draw(fr, tl, 1., ymax=930)
        sing = self.ly.singing(b)
        jump = 24 <= b < 32 and (b - 24) % 4 < 3
        h = 60 if jump else 26
        draw_char(fr, 'lili', 520, 900, t, b, hop=h, sing=sing, R=160, phase=.5)
        draw_char(fr, 'jacques', 840, 900, t, b, hop=h, sing=sing, R=160)
        put(fr, self.basket, 840 + 90, 800 - 18 * abs(math.sin(b * math.pi)))
        draw_char(fr, 'tiou', 1150, 900, t, b, hop=h + 20, sing=sing, R=160, phase=.25)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#bfe6f5'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#fff4dc'))
    # --- fin
    def do_outro(self, fr, t, tl, b):
        self.forest(fr, tl, 0, sunx=1500, suny=60)
        self.lv.draw(fr, tl, .7)
        k = back((b - .4) / 1.6)
        sy = 140 + (1 - k) * 800
        put(fr, self.card2, (W - self.card2.width) / 2, sy)
        put(fr, self.bye, (W - self.bye.width) / 2, sy + 52)
        put(fr, self.credit, (W - self.credit.width) / 2, sy + 216)
        calm = b >= 12
        draw_char(fr, 'lili', 560, 920, t, b, hop=0 if calm else 34, R=150, tilt=8 * math.sin(tl * 3))
        draw_char(fr, 'jacques', 960, 920, t, b, hop=0 if calm else 30, R=150, phase=.5, tilt=-8 * math.sin(tl * 3))
        draw_char(fr, 'tiou', 1360, 920, t, b, hop=0 if calm else 40, R=150, phase=.25, tilt=8 * math.sin(tl * 3 + 1))
        sweep(fr, 1 - b / .5, hexc('#fff4dc'), rev=True)
        end = self.tend - t
        if end < .9: put_fade(fr, 1 - end / .9, CREAM)
