# Scènes de "Ah ! vous dirai-je, maman" : Lison, sa maman et son papa au pays des bonbons.
from papier import *
from papier import Scenes as Base

def rond(cx, cy, R):
    return [(cx + R * 1.02 * math.sin(i / 200 * 2 * math.pi), cy - R * .96 * math.cos(i / 200 * 2 * math.pi)) for i in range(200)]

def critter(R, c1, c2, ear, blink, mouth, bow=None, glasses=False, tie=None, flower=None, pointy=False):
    body = apple(R, c1, c2, True, blink, mouth, bow=bow, feet=True, leaf=False, tige=False, contour=rond)
    w, h = body.size; S = 3
    im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = w * S / 2, h * .54 * S; Rs = R * S
    inner = lerp(ear, (255, 255, 255), .45)
    for sg in (-1, 1):
        ex, ey = cx + sg * Rs * .62, cy - Rs * .78
        if pointy:
            d.polygon([(ex - Rs * .3, ey + Rs * .2), (ex + sg * Rs * .08, ey - Rs * .42), (ex + Rs * .3, ey + Rs * .2)], fill=ear + (255,))
            d.polygon([(ex - Rs * .15, ey + Rs * .12), (ex + sg * Rs * .05, ey - Rs * .2), (ex + Rs * .15, ey + Rs * .12)], fill=inner + (255,))
        else:
            d.ellipse((ex - Rs * .29, ey - Rs * .29, ex + Rs * .29, ey + Rs * .29), fill=ear + (255,))
            d.ellipse((ex - Rs * .15, ey - Rs * .15, ex + Rs * .15, ey + Rs * .15), fill=inner + (255,))
    ears = grain(im.resize((w, h), Image.LANCZOS))
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); out.alpha_composite(ears); out.alpha_composite(body)
    if glasses or tie or flower:
        im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if glasses:
            ey = cy - Rs * .08
            for sg in (-1, 1):
                X = cx + sg * Rs * .36
                d.ellipse((X - Rs * .25, ey - Rs * .25, X + Rs * .25, ey + Rs * .25), outline=INK + (255,), width=int(Rs * .045))
            d.line([(cx - Rs * .11, ey - Rs * .04), (cx + Rs * .11, ey - Rs * .04)], fill=INK + (255,), width=int(Rs * .045))
        if tie:
            ty = cy + Rs * .74
            d.polygon([(cx, ty), (cx - Rs * .26, ty - Rs * .14), (cx - Rs * .26, ty + Rs * .14)], fill=tie + (255,))
            d.polygon([(cx, ty), (cx + Rs * .26, ty - Rs * .14), (cx + Rs * .26, ty + Rs * .14)], fill=tie + (255,))
            d.ellipse((cx - Rs * .07, ty - Rs * .07, cx + Rs * .07, ty + Rs * .07), fill=lerp(tie, (0, 0, 0), .25) + (255,))
        if flower:
            fx, fy = cx + Rs * .62, cy - Rs * .78
            for k in range(5):
                a = k / 5 * 6.283
                d.ellipse((fx + math.cos(a) * Rs * .13 - Rs * .1, fy + math.sin(a) * Rs * .13 - Rs * .1, fx + math.cos(a) * Rs * .13 + Rs * .1, fy + math.sin(a) * Rs * .13 + Rs * .1), fill=flower + (255,))
            d.ellipse((fx - Rs * .07, fy - Rs * .07, fx + Rs * .07, fy + Rs * .07), fill=GOLD + (255,))
        out.alpha_composite(im.resize((w, h), Image.LANCZOS))
    return out

PERSOS['lison'] = lambda blink, mouth, R: critter(int(R * .78), hexc('#ffb9a0'), hexc('#f58c7a'), hexc('#e8735f'), blink, mouth, bow=hexc('#ff5a8a'))
PERSOS['maman'] = lambda blink, mouth, R: critter(R, hexc('#c9a8f0'), hexc('#a17fdc'), hexc('#8d68cf'), blink, mouth, flower=hexc('#fff4dc'))
PERSOS['papa'] = lambda blink, mouth, R: critter(R, hexc('#8fd6c4'), hexc('#5bb59f'), hexc('#4a9c88'), blink, mouth, glasses=True, tie=hexc('#e2453c'), pointy=True)

CANDY = ['#ff5a8a', '#ffb02e', '#7ccc6b', '#58b7f0', '#b47ef0', '#ff7b54']

def sprite(fn, w, h, sh=(4, 8, 7, .24)):
    S = 2; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); fn(ImageDraw.Draw(im), S)
    return shadowed(grain(im.resize((w, h), Image.LANCZOS)), *sh)

def wrapped(col, R=40):
    c = hexc(col); dk = lerp(c, (0, 0, 0), .2)
    def f(d, S):
        w, h = 4 * R * S, 2 * R * S; cx, cy = w / 2, h / 2
        for sg in (-1, 1):
            d.polygon([(cx + sg * R * .8 * S, cy), (cx + sg * R * 1.9 * S, cy - R * .62 * S), (cx + sg * R * 1.9 * S, cy + R * .62 * S)], fill=dk + (255,))
        d.ellipse((cx - R * S, cy - R * .78 * S, cx + R * S, cy + R * .78 * S), fill=c + (255,))
        for k in (-.4, 0, .4):
            d.line([(cx + (k - .2) * R * S, cy - R * .7 * S), (cx + (k + .2) * R * S, cy + R * .7 * S)], fill=(255, 255, 255, 150), width=int(R * .14 * S))
    return sprite(f, 4 * R, 2 * R, (3, 6, 5, .22))

def lolly(col, R=70, stick=150):
    c = hexc(col)
    def f(d, S):
        cx, cy = R * 1.1 * S, R * 1.1 * S
        d.rounded_rectangle((cx - R * .09 * S, cy, cx + R * .09 * S, cy + (R + stick) * S), int(R * .08 * S), fill=(255, 250, 240, 255))
        d.ellipse((cx - R * S, cy - R * S, cx + R * S, cy + R * S), fill=c + (255,))
        pts = [(cx + math.cos(t) * t / 12.6 * R * .95 * S, cy + math.sin(t) * t / 12.6 * R * .95 * S) for t in np.linspace(0, 12.6, 160)]
        d.line(pts, fill=(255, 255, 255, 235), width=int(R * .16 * S), joint='curve')
    return sprite(f, int(R * 2.2), int(R * 2.2 + stick + R * .1), (4, 8, 7, .24))

def gumdrop(col, R=34):
    c = hexc(col)
    def f(d, S):
        cx, by = R * 1.2 * S, R * 1.6 * S
        d.chord((cx - R * S, by - R * 1.5 * S, cx + R * S, by + R * .5 * S), 180, 360, fill=c + (255,))
        d.rectangle((cx - R * S, by - R * .5 * S, cx + R * S, by), fill=c + (255,))
        r = np.random.default_rng(len(col))
        for _ in range(9):
            x, y = cx + r.uniform(-.7, .7) * R * S, by - r.uniform(.15, 1) * R * S
            d.ellipse((x - 3 * S, y - 3 * S, x + 3 * S, y + 3 * S), fill=(255, 255, 255, 190))
    return sprite(f, int(R * 2.4), int(R * 1.8), (3, 5, 5, .2))

def heart(col, R=30):
    c = hexc(col)
    def f(d, S):
        cx, cy = R * 1.2 * S, R * 1.1 * S
        pts = [(cx + 16 * math.sin(t) ** 3 * R / 17 * S, cy - (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * R / 17 * S) for t in np.linspace(0, 6.283, 120)]
        d.polygon(pts, fill=c + (255,))
    return sprite(f, int(R * 2.4), int(R * 2.4), (2, 4, 4, .18))

def gradient(top, bot, k=1.1):
    a, b = np.array(hexc(top), np.float32), np.array(hexc(bot), np.float32)
    t = np.linspace(0, 1, H)[:, None, None] ** k
    return grain(Image.fromarray(np.repeat(a * (1 - t) + b * t, W, 1).astype(np.uint8), 'RGB').convert('RGBA'))

def candy_hill(col, base, amp, seed, stripes=False):
    r = np.random.default_rng(seed); x = np.arange(LW); ph = r.uniform(0, 6.28, 3)
    y = base + amp * (.6 * np.sin(2 * np.pi * x / LW * 2 + ph[0]) + .3 * np.sin(2 * np.pi * x / LW * 5 + ph[1]) + .1 * np.sin(2 * np.pi * x / LW * 9 + ph[2]))
    im = Image.new('RGBA', (LW, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = hexc(col)
    d.polygon([(0, H)] + [(int(a), float(b)) for a, b in zip(x[::8], y[::8])] + [(LW - 1, float(y[-1])), (LW - 1, H)], fill=c + (255,))
    if stripes:
        for i, xx in enumerate(range(0, LW, 46)):
            yy = float(y[min(xx, LW - 1)]) + 22
            d.ellipse((xx - 7, yy - 7, xx + 7, yy + 7), fill=hexc(CANDY[i % 6]) + (255,))
    return y, grain(shadowed(im, 0, -6, 8, .18))

class Scenes(Base):
    def prepare(self):
        n = self.name
        self.candies = [wrapped(c, 34) for c in CANDY]
        self.gums = [gumdrop(c) for c in CANDY]
        if n in ('intro', 'v2'):
            self.sky2 = gradient('#ffc8df', '#fff2e2')
            self.hl = [candy_hill('#f7b3d0', 620, 50, 3), candy_hill('#c7a6f2', 730, 40, 5), candy_hill('#a3e3cb', 850, 26, 8, True)]
            r = np.random.default_rng(9)
            self.lol = [(lolly(CANDY[i % 6], r.uniform(46, 70), r.uniform(120, 200)), r.uniform(0, LW), i % 2) for i in range(12)]
            self.floaters = [(self.candies[i % 6], r.uniform(0, W + 300), r.uniform(40, 330), r.uniform(18, 40), r.uniform(0, 6)) for i in range(6)]
        if n in ('intro', 'outro'):
            self.title = text_img(["Ah ! vous dirai-je,", "maman"], lora(112), RED, 10)
            self.sub = text_img(["Comptine à chanter ensemble"], font('Poppins-Medium.ttf', 40), INK)
            self.sign = paper_card(1180, 430)
            self.bye = text_img(["À bientôt !"], lora(118), RED)
            self.credit = text_img(["Comptine traditionnelle française · Arrangement original"], font('Poppins-Medium.ttf', 32), INK)
            self.card2 = paper_card(1160, 280)
        if n == 'v1': self.make_room()
        if n == 'inter':
            self.cloth = self.make_cloth()
            self.book = self.make_book(); self.jar = self.make_jar()
            f = font('Poppins-Bold.ttf', 40)
            self.lab1 = text_img(["la raison"], f, INK); self.lab2 = text_img(["les bonbons"], f, INK)
            self.q = text_img(["La grande balance"], lora(84), RED); self.qcard = paper_card(820, 150)
        if n in ('v3', 'outro'):
            self.sky3 = gradient('#ff9a6b', '#ffe0a8') if n == 'v3' else gradient('#5b4b9a', '#f6a6a0')
            self.sunset = sun(170, hexc('#ffcf5a')); self.blanket = self.make_blanket()
            self.hill3 = candy_hill('#e98aa8', 760, 30, 12)[1]; self.hill4 = candy_hill('#c76a9a', 860, 20, 14)[1]
            self.cake = self.make_cake(); self.hearts = [heart(c) for c in ('#ff5a8a', '#ff7b54', '#b47ef0')]
            self.stars = np.random.default_rng(2).uniform(0, 1, (120, 4))
    # --- éléments
    def make_room(self):
        bg = Image.new('RGBA', (W, H), hexc('#ffe9c9') + (255,)); d = ImageDraw.Draw(bg)
        for x in range(0, W, 120): d.rectangle((x, 0, x + 60, 760), fill=hexc('#ffdcb8') + (255,))
        for x in range(30, W, 120):
            for y in range(60, 740, 140): d.ellipse((x - 8, y - 8, x + 8, y + 8), fill=hexc('#ffb4c8') + (255,))
        d.rectangle((0, 760, W, H), fill=hexc('#d99a6c') + (255,))
        for x in range(-200, W, 160): d.line([(x, H), (x + 300, 760)], fill=hexc('#c7895d') + (255,), width=6)
        self.room = grain(bg)
        # fenêtre sur les collines de bonbons
        S = 2; w, h = 520, 400; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, w * S, h * S), 40 * S, fill=hexc('#fff4dc') + (255,))
        d.rounded_rectangle((22 * S, 22 * S, (w - 22) * S, (h - 22) * S), 28 * S, fill=hexc('#ffd3e6') + (255,))
        d.ellipse((60 * S, 230 * S, 420 * S, 520 * S), fill=hexc('#c7a6f2') + (255,)); d.ellipse((240 * S, 250 * S, 620 * S, 560 * S), fill=hexc('#a3e3cb') + (255,))
        d.rectangle((0, (h - 22) * S, w * S, h * S), fill=(0, 0, 0, 0))
        d.rectangle((22 * S, (h - 22) * S, (w - 22) * S, (h - 22) * S), fill=(0, 0, 0, 0))
        d.line([(w / 2 * S, 22 * S), (w / 2 * S, (h - 22) * S)], fill=hexc('#fff4dc') + (255,), width=16 * S)
        d.line([(22 * S, h / 2 * S), ((w - 22) * S, h / 2 * S)], fill=hexc('#fff4dc') + (255,), width=16 * S)
        self.window = shadowed(grain(im.resize((w, h), Image.LANCZOS)), 4, 9, 9, .22)
        # table ronde
        S = 2; w, h = 560, 300; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle((250 * S, 60 * S, 310 * S, 300 * S), fill=hexc('#a8693e') + (255,))
        d.ellipse((150 * S, 270 * S, 410 * S, 300 * S), fill=hexc('#8c5631') + (255,))
        d.ellipse((0, 0, w * S, 120 * S), fill=hexc('#b97a48') + (255,)); d.ellipse((0, 0, w * S, 100 * S), fill=hexc('#ffffff') + (255,))
        for i in range(14):
            x = (20 + i * 38) * S; d.ellipse((x, 40 * S, x + 26 * S, 66 * S), fill=hexc('#ff9fbf') + (255,))
        self.table = shadowed(grain(im.resize((w, h), Image.LANCZOS)), 4, 9, 9, .24)
        self.jar = self.make_jar(); self.book = self.make_book()
        self.lolli = lolly('#ff5a8a', 46, 110)
        self.hat = sprite(lambda d, S: (d.polygon([(70 * S, 0), (0, 150 * S), (140 * S, 150 * S)], fill=hexc('#58b7f0') + (255,)), d.ellipse((52 * S, -14 * S, 88 * S, 22 * S), fill=GOLD + (255,)),
                                         [d.ellipse(((30 + 22 * k) * S, (60 + 30 * k) * S, (44 + 22 * k) * S, (74 + 30 * k) * S), fill=(255, 255, 255, 220)) for k in range(3)]), 140, 152)
    def make_jar(self):
        S = 2; w, h = 260, 300; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((20 * S, 50 * S, 240 * S, 295 * S), 60 * S, fill=(220, 240, 255, 150))
        r = np.random.default_rng(4)
        for i in range(26):
            x, y = r.uniform(55, 205), r.uniform(120, 265); q = r.uniform(16, 22)
            d.ellipse(((x - q) * S, (y - q) * S, (x + q) * S, (y + q) * S), fill=hexc(CANDY[i % 6]) + (255,))
        d.rounded_rectangle((20 * S, 50 * S, 240 * S, 295 * S), 60 * S, outline=(255, 255, 255, 230), width=6 * S)
        d.rounded_rectangle((40 * S, 10 * S, 220 * S, 58 * S), 16 * S, fill=hexc('#ff5a8a') + (255,))
        d.ellipse((60 * S, 90 * S, 90 * S, 180 * S), fill=(255, 255, 255, 110))
        return shadowed(grain(im.resize((w, h), Image.LANCZOS)), 4, 8, 7, .24)
    def make_book(self):
        S = 2; w, h = 250, 200; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rounded_rectangle((10 * S, 20 * S, 240 * S, 195 * S), 12 * S, fill=hexc('#fff4dc') + (255,))
        d.rounded_rectangle((0, 0, 230 * S, 180 * S), 14 * S, fill=hexc('#3f6fb5') + (255,))
        d.rectangle((26 * S, 0, 46 * S, 180 * S), fill=hexc('#2c5592') + (255,))
        d.rounded_rectangle((70 * S, 50 * S, 200 * S, 120 * S), 10 * S, fill=hexc('#fff4dc') + (255,))
        for k in range(3): d.line([(85 * S, (68 + k * 18) * S), (185 * S, (68 + k * 18) * S)], fill=hexc('#9ab0d6') + (255,), width=5 * S)
        return shadowed(grain(im.resize((w, h), Image.LANCZOS)), 4, 8, 7, .24)
    def make_cloth(self):
        im = Image.new('RGBA', (W, H), hexc('#fff4dc') + (255,)); d = ImageDraw.Draw(im)
        for i in range(0, W, 120):
            d.rectangle((i, 0, i + 60, H), fill=hexc('#ffd6d8') + (255,))
        for j in range(0, H, 120):
            d.rectangle((0, j, W, j + 60), fill=hexc('#ffd6d8') + (255,))
        for i in range(0, W, 120):
            for j in range(0, H, 120): d.rectangle((i, j, i + 60, j + 60), fill=hexc('#ffb8c4') + (255,))
        return grain(im)
    def make_blanket(self):
        S = 2; w, h = 1300, 170; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon([(110 * S, 0), ((w - 110) * S, 0), (w * S, h * S), (0, h * S)], fill=hexc('#fff4dc') + (255,))
        for i in range(14):
            x0 = 110 + i * (w - 220) / 14; x1 = i * w / 14
            if i % 2 == 0:
                d.polygon([(x0 * S, 0), ((x0 + (w - 220) / 14) * S, 0), ((x1 + w / 14) * S, h * S), (x1 * S, h * S)], fill=hexc('#ff6f91') + (255,))
        return shadowed(grain(im.resize((w, h), Image.LANCZOS)), 3, 8, 8, .22)
    def make_cake(self):
        S = 2; w, h = 240, 210; im = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.ellipse((10 * S, 170 * S, 230 * S, 205 * S), fill=(255, 255, 255, 255))
        d.rectangle((30 * S, 80 * S, 210 * S, 185 * S), fill=hexc('#f7b3d0') + (255,))
        d.ellipse((30 * S, 165 * S, 210 * S, 200 * S), fill=hexc('#f7b3d0') + (255,))
        d.ellipse((30 * S, 60 * S, 210 * S, 100 * S), fill=hexc('#fff4dc') + (255,))
        for k in range(7):
            x = 40 + k * 26; d.ellipse((x * S, 90 * S, (x + 22) * S, 120 * S), fill=hexc('#fff4dc') + (255,))
        d.ellipse((100 * S, 30 * S, 140 * S, 70 * S), fill=hexc('#e2453c') + (255,))
        return shadowed(grain(im.resize((w, h), Image.LANCZOS)), 4, 8, 7, .24)
    # --- décor extérieur commun (intro, v2)
    def candyland(self, fr, tl, spd):
        fr.alpha_composite(self.sky2)
        for c, x, y, sp, ph in self.floaters:
            put(fr, c, (x - tl * sp) % (W + 400) - 250, y + 14 * math.sin(tl * 1.2 + ph))
        for i, (y, layer) in enumerate(self.hl):
            off = tl * spd * (.35, .6, 1)[i]
            if i == 1:
                for s_, x, back_ in self.lol:
                    if back_: continue
                    xx = (x - off) % LW
                    if xx > W + 200: continue
                    put(fr, s_, xx - s_.width / 2, y[int((x + 0) % LW)] - s_.height + 30)
            blit_scroll(fr, layer, off)
            if i == 1:
                for s_, x, back_ in self.lol:
                    if not back_: continue
                    xx = (x - off * 1.3) % LW
                    if xx > W + 200: continue
                    put(fr, s_, xx - s_.width / 2, 900 - s_.height + 40)
    # --- intro
    def do_intro(self, fr, t, tl, b):
        self.candyland(fr, tl, 30)
        draw_char(fr, 'maman', 230, 880, t, b, hop=26 * ease((b - 6) / 1), R=150)
        draw_char(fr, 'lison', 1700, 880, t, b, hop=34 * ease((b - 7) / 1), phase=.5, R=150)
        k = back((b - .4) / 2.2)
        if k > 0:
            sy = 90 - (1 - k) * 900 + 8 * math.sin(tl * 2)
            put(fr, self.sign, (W - self.sign.width) / 2, sy)
            put(fr, self.title, (W - self.title.width) / 2, sy + 70)
            put(fr, self.sub, (W - self.sub.width) / 2, sy + 372)
        if b < 1: put_fade(fr, 1 - b)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffe9c9'))
    # --- v1 : le salon de Lison
    def do_v1(self, fr, t, tl, b):
        fr.alpha_composite(self.room)
        put(fr, self.window, 160, 110)
        put(fr, self.table, 1360, 570)
        jk = back((b - 31) / 1.2)
        jy = 330 - 18 * max(0, math.sin(b * math.pi)) * (b > 32)
        put(fr, self.jar, 1510, jy)
        sing = self.ly.singing(b)
        # Lison grandit sur "comme une grande personne"
        g = ease((b - 24) / 2) * (1 - ease((b - 32) / 1.5))
        mk = ease((b - 1) / 2)
        draw_char(fr, 'maman', 560 - 900 * (1 - mk), 860, t, b, hop=14, sing=sing and b < 16, R=165)
        px = 1300 + 900 * (1 - ease((b - 15) / 1.5))
        if b > 14:
            draw_char(fr, 'papa', px, 860, t, b, hop=14, sing=sing and 16 <= b < 32, R=165, phase=.3)
            if b < 34:
                bk = ease((b - 16) / 1)
                put(fr, self.book, px - 125, 360 - 60 * bk + 6 * math.sin(tl * 3))
        lx = 920; sc = 1 + .55 * g
        if g > .05:
            put(fr, self.hat, lx - self.hat.width / 2, 860 - 300 * sc - self.hat.height * .7 - 30 * abs(math.sin(b * math.pi)))
        draw_char(fr, 'lison', lx, 868, t, b, hop=34, sing=sing, R=150, scale=sc, phase=.5)
        # pluie de bonbons sur "les bonbons"
        for i in range(18):
            st = 34 + i * .45; T = (b - st) * B
            if T < 0: continue
            r = np.random.default_rng(40 + i); x0 = 1640 + r.uniform(-40, 40); vx = r.uniform(-640, 240); vy = -r.uniform(900, 1200)
            tland = (-vy + math.sqrt(vy * vy + 4 * 1300 * 480)) / 2600; T = min(T, tland)
            x = x0 + vx * T; y = min(840, 360 + vy * T + 1300 * T * T) - (10 * (i % 3) if T >= tland else 0)
            put(fr, self.candies[i % 6], x - 68, y - 34)
        if b > 38:
            k = back((b - 38) / 1)
            put(fr, self.lolli, lx + 70, 868 - 260 - 60 * k + 10 * math.sin(tl * 4))
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ffe9c9'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#fff4dc'))
    # --- interlude : la grande balance (séquence inédite)
    def do_inter(self, fr, t, tl, b):
        fr.alpha_composite(self.cloth)
        put(fr, self.qcard, (W - self.qcard.width) / 2, 40)
        put(fr, self.q, (W - self.q.width) / 2, 64)
        n = int(clamp(b - 1, 0, 12)) if b > 1 else 0
        target = -16 + 30 * ease(n / 12)
        ang = math.radians(target + 3 * math.sin(tl * 5) * math.exp(-((b % 1) * 3)))
        cx, cy = W / 2, 400; L = 560
        d = ImageDraw.Draw(fr)
        d.polygon([(cx - 120, 900), (cx + 120, 900), (cx + 30, cy), (cx - 30, cy)], fill=hexc('#c7895d') + (255,))
        d.rounded_rectangle((cx - 200, 880, cx + 200, 920), 18, fill=hexc('#a8693e') + (255,))
        lx, ly = cx - L * math.cos(ang), cy - L * math.sin(ang)
        rx, ry = cx + L * math.cos(ang), cy + L * math.sin(ang)
        d.line([(lx, ly), (rx, ry)], fill=hexc('#8c5631') + (255,), width=26)
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=GOLD + (255,))
        for (px, py), item, lab in (((lx, ly), self.book, self.lab1), ((rx, ry), None, self.lab2)):
            d.line([(px, py), (px - 150, py + 230)], fill=INK + (255,), width=5); d.line([(px, py), (px + 150, py + 230)], fill=INK + (255,), width=5)
            d.chord((px - 190, py + 170, px + 190, py + 290), 0, 180, fill=hexc('#f1b92f') + (255,))
            if item is not None: put(fr, item, px - item.width / 2, py + 232 - item.height)
            put(fr, lab, px - lab.width / 2, py + 300)
        PILE = [(-120, 0), (-40, 0), (40, 0), (120, 0), (-80, -44), (0, -44), (80, -44), (-40, -88), (40, -88), (0, -132), (-120, -44), (120, -44)]
        gw, gh = self.gums[0].size
        for i in range(n):
            ox, oy = PILE[i]; put(fr, self.gums[i % 6], rx + ox - gw / 2, ry + 236 - gh + oy)
        if b > 1 and n < 12:
            T = (b % 1) * B; ox, oy = PILE[n]; yy = ry - 520 + 2600 * T * T
            if yy < ry + 236 - gh + oy: put(fr, self.gums[n % 6], rx + ox - gw / 2, yy)
        draw_char(fr, 'papa', 140, 1050, t, b, hop=10, R=150, scale=.72)
        draw_char(fr, 'lison', 1790, 1050, t, b, hop=30, R=150, scale=.8, phase=.5)
        sweep(fr, 1 - b / .5, hexc('#fff4dc'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffc8df'))
    # --- v2 : la promenade au pays des bonbons
    def do_v2(self, fr, t, tl, b):
        self.candyland(fr, tl, 120)
        sing = self.ly.singing(b)
        draw_char(fr, 'papa', 560, 880, t, b, hop=20, sing=sing, R=150, phase=.2)
        draw_char(fr, 'maman', 860, 880, t, b, hop=20, sing=sing, R=150, phase=.6)
        draw_char(fr, 'lison', 1180, 880, t, b, hop=40, sing=sing, R=150)
        # pluie de bonbons emballés sur "Moi, je dis que les bonbons..."
        k = clamp((b - 32) / 2) * (1 - clamp((b - 47) / 1))
        if k > 0:
            r = np.random.default_rng(3)
            for i in range(int(40 * k)):
                x = r.uniform(80, W - 80); sp = r.uniform(260, 420); ph = r.uniform(0, H)
                y = (ph + (tl - 32 * B) * sp) % (H + 200) - 150
                if y < 880: put(fr, self.candies[i % 6], x - 68 + 30 * math.sin(tl * 2 + i), y)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ffc8df'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffb38a'))
    # --- v3 : le goûter au soleil couchant
    def do_v3(self, fr, t, tl, b):
        fr.alpha_composite(self.sky3)
        put(fr, self.sunset, W / 2 - self.sunset.width / 2 + 420, 330 - tl * 2)
        blit_scroll(fr, self.hill3, 300); blit_scroll(fr, self.hill4, 900)
        put(fr, self.blanket, (W - self.blanket.width) / 2, 720)
        put(fr, self.cake, W / 2 - 120, 610)
        sing = self.ly.singing(b)
        draw_char(fr, 'maman', 440, 860, t, b, hop=16, sing=sing, R=150)
        draw_char(fr, 'lison', 1290, 860, t, b, hop=30, sing=sing, R=150, phase=.5)
        draw_char(fr, 'papa', 1660, 860, t, b, hop=16 + 14 * ease((b - 40) / 1), sing=sing, R=150, phase=.25)
        # Papa goûte enfin un bonbon : des cœurs s'envolent
        if b > 38:
            for i in range(10):
                T = (b - 38 - i * .6) * B
                if T < 0 or T > 3.2: continue
                put(fr, self.hearts[i % 3], 1640 + (i % 2 * 2 - 1) * (40 + 90 * T) + 30 * math.sin(T * 4 + i) - 36, 560 - T * 170)
        if 36 <= b < 40:
            k = ease((b - 36) / 1); put(fr, self.candies[0], 1560 + 60 * k - 68, 560 + 40 * k)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ffb38a'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#fff4dc'))
    # --- fin
    def do_outro(self, fr, t, tl, b):
        fr.alpha_composite(self.sky3)
        d = ImageDraw.Draw(fr)
        for x, y, ph, sz in self.stars:
            q = (1.4 + 3 * sz) * (.55 + .45 * math.sin(tl * 2 + ph * 6.28)); xx, yy = x * W, y * 520
            d.ellipse((xx - q, yy - q, xx + q, yy + q), fill=(255, 245, 205, 255))
        blit_scroll(fr, self.hill3, 300); blit_scroll(fr, self.hill4, 900)
        k = back((b - .4) / 1.6)
        sy = 170 + (1 - k) * 800
        put(fr, self.card2, (W - self.card2.width) / 2, sy)
        put(fr, self.bye, (W - self.bye.width) / 2, sy + 52)
        put(fr, self.credit, (W - self.credit.width) / 2, sy + 216)
        calm = b >= 12
        draw_char(fr, 'maman', 560, 900, t, b, hop=0 if calm else 30, R=150, tilt=8 * math.sin(tl * 3))
        draw_char(fr, 'lison', 960, 900, t, b, hop=0 if calm else 40, R=150, phase=.5, tilt=-8 * math.sin(tl * 3))
        draw_char(fr, 'papa', 1360, 900, t, b, hop=0 if calm else 30, R=150, phase=.25, tilt=8 * math.sin(tl * 3 + 1))
        sweep(fr, 1 - b / .5, hexc('#fff4dc'), rev=True)
        end = self.tend - t
        if end < .9: put_fade(fr, 1 - end / .9, CREAM)
