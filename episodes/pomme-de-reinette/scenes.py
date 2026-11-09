# Scènes de "Pomme de reinette et pomme d'api" : exemple de référence pour les épisodes suivants.
from papier import *
from papier import Scenes as Base

PERSOS['reinette'] = lambda blink, mouth, R: apple(R, R_C1, R_C2, True, blink, mouth, freckle=(170, 118, 42), bow=hexc('#f07a2a'))
PERSOS['api'] = lambda blink, mouth, R: apple(int(R * .74), A_C1, A_C2, True, blink, mouth)

class Scenes(Base):
    def prepare(self):
        name = self.name
        if name == 'intro' or name == 'outro':
            self.title = text_img(["Pomme de reinette", "et pomme d'api"], lora(118), RED, 10)
            self.sub = text_img(["Comptine à chanter ensemble"], font('Poppins-Medium.ttf', 40), INK)
            self.sign = paper_card(1180, 430)
            self.bye = text_img(["À bientôt au Verger !"], lora(110), RED)
            self.credit = text_img(["Comptine traditionnelle française · Arrangement original"], font('Poppins-Medium.ttf', 32), INK)
            self.card2 = paper_card(1160, 280)
        if name == 'inter':
            self.badge = paper_card(620, 660, rad=40)
            f = lora(76)
            self.n1 = text_img(["La reinette"], f, hexc('#b78312')); self.n2 = text_img(["La pomme d'api"], f, RED)
            f2 = font('Poppins-Medium.ttf', 32)
            self.d1 = text_img(["Dorée et mouchetée"], f2, INK); self.d2 = text_img(["Toute petite, rouge et jaune"], f2, INK)
        if name == 'v3': self.basket = self.make_basket(); self.fire = np.random.default_rng(4).uniform(0, 1, (46, 4))
        if name == 'v4': self.stars = np.random.default_rng(1).uniform(0, 1, (160, 4)); self.conf = Confetti(); self.bunt = self.make_bunting()
        if name == 'outro': self.stars = np.random.default_rng(1).uniform(0, 1, (160, 4)); self.conf = Confetti()
        if name == 'v2': self.balloon = self.make_balloon()
    def make_basket(self):
        S = 2; w, h = 620 * S, 300 * S; im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.polygon([(30 * S, 40 * S), (590 * S, 40 * S), (520 * S, 290 * S), (100 * S, 290 * S)], fill=hexc('#a56a35') + (255,))
        for y in range(52, 290, 36):
            x_off = (y - 40) / 250 * 70
            for x in range(int(30 + x_off), int(590 - x_off), 62):
                d.rounded_rectangle(((x + (y % 2) * 12) * S, y * S, (x + 44) * S, (y + 20) * S), 8, fill=hexc('#c68a4a') + (255,))
        d.rounded_rectangle((16 * S, 24 * S, 604 * S, 66 * S), 18 * S, fill=hexc('#7e4c25') + (255,))
        return shadowed(grain(im.resize((w // S, h // S), Image.LANCZOS)), 5, 10, 10, .26)
    def make_bunting(self):
        S = 2; im = Image.new('RGBA', (W * S, 300 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); cs = ['#ef3b34', '#f1b92f', '#7ccc6b', '#fff4dc', '#ffa23b']
        pts = [(x * S, (40 + 90 * math.sin(x / W * math.pi)) * S) for x in range(0, W + 20, 20)]
        d.line(pts, fill=(230, 220, 200, 255), width=5 * S)
        for i in range(0, 48):
            x = i * 40 + 20; y = 40 + 90 * math.sin(x / W * math.pi)
            d.polygon([((x - 22) * S, y * S), ((x + 22) * S, y * S), (x * S, (y + 50) * S)], fill=hexc(cs[i % 5]) + (255,))
        return shadowed(grain(im.resize((W, 300), Image.LANCZOS)), 3, 6, 6, .2)
    def make_balloon(self):
        a = apple(130, hexc('#ef3b34'), hexc('#c42530'), feet=False); S = 2
        im = Image.new('RGBA', (a.width, a.height + 150), (0, 0, 0, 0)); im.alpha_composite(a, (0, 0)); d = ImageDraw.Draw(im); c = a.width // 2; by = a.height + 40
        for sg in (-1, 1): d.line([(c + sg * 60, a.height - 62), (c + sg * 30, by)], fill=(90, 60, 40, 255), width=4)
        d.rounded_rectangle((c - 44, by, c + 44, by + 62), 10, fill=hexc('#a56a35') + (255,))
        return im
    # --- intro
    def do_intro(self, fr, t, tl, b):
        self.bg(fr, t, (1, 1, 1), 180 + tl * 12)
        falling(fr, 1, b, 9, 77, 840, B)
        draw_char(fr, 'reinette', 190, 870, t, b, hop=30 * ease((b - 6) / 1), R=165)
        draw_char(fr, 'api', 1730, 870, t, b, hop=30 * ease((b - 7) / 1), phase=.5, R=165)
        k = back((b - .4) / 2.2)
        if k > 0:
            sy = 90 - (1 - k) * 900 + 8 * math.sin(tl * 2)
            put(fr, self.sign, (W - self.sign.width) / 2, sy)
            put(fr, self.title, (W - self.title.width) / 2, sy + 72)
            put(fr, self.sub, (W - self.sub.width) / 2, sy + 372)
        if b < 1: put_fade(fr, 1 - b)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#fff4dc'))
    # --- v1 : le verger
    def do_v1(self, fr, t, tl, b):
        self.bg(fr, t, (1, 1, 1), 180 + tl * 12)
        k_r = ease((b - 8) / 4); k_g = ease((b - 24) / 4)
        if k_r > 0: put(fr, self.red.crop((0, 0, int(self.red.width * k_r), self.red.height)), -40, 758)
        falling(fr, 15.5, b, 14, 12, 846, B)
        sing = self.ly.singing(b)
        draw_char(fr, 'reinette', 680, 842, t, b, sing=sing, R=165)
        draw_char(fr, 'api', 1230, 842, t, b, sing=sing, phase=.5, R=165)
        if k_g > 0:
            cw = int(self.gray.width * k_g)
            put(fr, self.gray.crop((self.gray.width - cw, 0, self.gray.width, self.gray.height)), W + 40 - cw, 836)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#fff4dc'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ecf9dc'))
    # --- v2 : le tapis volant
    def do_v2(self, fr, t, tl, b):
        self.bg(fr, t, (.5, .85, 1.3), 180 + 400 + tl * 170, clouds=False)
        for i, (c, x, y) in enumerate(self.clouds):
            xx = (x - tl * (70 + 24 * i)) % (W + 600) - 460
            put(fr, c, xx, y)
        bx = W + 240 - tl * 92
        put(fr, self.balloon, bx, 150 + 26 * math.sin(tl * .9))
        gk = ease((b - 24) / 1.3)
        base = self.fly_r if gk <= 0 else self.fly_g if gk >= 1 else Image.blend(self.fly_r, self.fly_g, gk)
        wv = wavy(base, t, amp=13)
        bob = 18 * math.sin(tl * 1.7)
        cy = 655 + bob
        sing = self.ly.singing(b)
        draw_char(fr, 'reinette', 760, cy + 46, t, b, hop=22, sing=sing, R=165, tilt=-3)
        draw_char(fr, 'api', 1150, cy + 46, t, b, hop=22, sing=sing, phase=.5, R=165, tilt=3)
        put(fr, wv, (W - wv.width) / 2, cy + 8)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ecf9dc'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffd98c'))
    # --- interlude : qui est qui
    def do_inter(self, fr, t, tl, b):
        r = rays(hexc('#ffc36b'), hexc('#ffb257'), tl * .08); fr.alpha_composite(r)
        for side, st, x, key, name, desc, sc in [(0, .6, 500, 'reinette', self.n1, self.d1, 1.), (1, 7.6, 1420, 'api', self.n2, self.d2, 1.14)]:
            k = back((b - st) / 1.3)
            if k <= 0: continue
            y0 = 170 + (1 - k) * 900
            put(fr, self.badge, x - self.badge.width / 2, y0)
            draw_char(fr, key, x, y0 + 450, t, b, hop=22, R=165, phase=side * .5, scale=sc * 1.0)
            put(fr, name, x - name.width / 2, y0 + 472)
            put(fr, desc, x - desc.width / 2, y0 + 590)
        sweep(fr, 1 - b / .5, hexc('#ffd98c'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#ffb257'))
    # --- v3 : la récolte au soleil couchant
    def do_v3(self, fr, t, tl, b):
        self.bg(fr, t, (1, 1, 1), 1400 + tl * 8)
        # nuages gris sur "gris"
        gk = ease((b - 28) / 2)
        for i, (c, x, y) in enumerate(self.clouds[:4]):
            pass
        bw = self.basket.width; bx = (W - bw) / 2; by = 610
        r = np.random.default_rng(99)
        beats = int(b) + 1
        pop = []
        for i in range(0, 32):
            if i >= beats + 4: break
            T = (b - i) * B
            if T < 0: continue
            rr = np.random.default_rng(1000 + i)
            vx = rr.uniform(-560, 560); vy = -rr.uniform(1050, 1420); g = 2500
            for j, (dx, delay) in enumerate([(0, 0), (70, .12)]):
                T2 = T - delay
                if T2 < 0 or T2 > 1.55: continue
                x = W / 2 + dx - 35 + vx * T2; y = by + 30 + vy * T2 + .5 * g * T2 * T2
                if y > by + 60 and vy + g * T2 > 0: continue
                put(fr, small((i + j) % 4, 34), x - 58, y - 58)
        put(fr, self.basket, bx, by)
        sing = self.ly.singing(b)
        draw_char(fr, 'reinette', 360, 860, t, b, sing=sing, R=165)
        draw_char(fr, 'api', 1560, 860, t, b, sing=sing, phase=.5, R=165)
        for x, y, ph, sp in self.fire:
            a = .5 + .5 * math.sin(tl * 3 * (1 + sp) + ph * 6.28)
            xx = x * W + 28 * math.sin(tl * .8 + ph * 7); yy = 250 + y * 560 + 18 * math.cos(tl + ph * 9)
            q = 3 + 4 * a; glow = Image.new('RGBA', (1, 1))
            ImageDraw.Draw(fr).ellipse((xx - q, yy - q, xx + q, yy + q), fill=(255, 241, 150, 255))
        if gk > 0:
            for i, (c, x, y) in enumerate(self.clouds):
                sgn = -1 if i % 2 else 1; xx = W / 2 + sgn * (1500 - 1100 * gk) + sgn * i * 100 - c.width / 2
                g_ = c.copy(); a_ = np.array(g_).astype(np.float32); a_[..., :3] = a_[..., :3] * .55 + np.array([60, 66, 80], np.float32)
                put(fr, Image.fromarray(a_.clip(0, 255).astype(np.uint8), 'RGBA'), xx, 40 + 26 * i)
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#ffb257'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#26305e'))
    # --- v4 : la fête sous la lune
    def do_v4(self, fr, t, tl, b):
        self.bg(fr, t, (1, 1, 1), 2300 + tl * 5)
        d = ImageDraw.Draw(fr); pulse = 1 - (b % 1)
        for x, y, ph, sz in self.stars:
            a = .55 + .45 * math.sin(tl * 2 + ph * 6.28) + .3 * pulse * (int(ph * 10) % 2)
            q = (1.4 + 3 * sz) * clamp(a, .2, 1.3); xx, yy = x * W, y * 500
            d.ellipse((xx - q, yy - q, xx + q, yy + q), fill=(255, 245, 205, 255))
        put(fr, self.bunt, 0, 18)
        put(fr, self.red.crop((0, 0, self.red.width, self.red.height)), -40, 774)
        for i in range(5):
            x = 150 + i * 405; sc = .34
            if 1 < i < 3: continue
            draw_char(fr, ['api', 'reinette', 'x', 'api', 'reinette'][i], x, 800, t, b, hop=26, phase=i * .25, scale=.42, R=165, sing=self.ly.singing(b))
        sing = self.ly.singing(b)
        draw_char(fr, 'reinette', 760, 880, t, b, sing=sing, scale=1.14, hop=42, R=165)
        draw_char(fr, 'api', 1160, 880, t, b, sing=sing, phase=.5, scale=1.14, hop=42, R=165)
        self.conf.draw(fr, tl, clamp(b / 4))
        self.ly.draw(fr, b)
        sweep(fr, 1 - b / .5, hexc('#26305e'), rev=True)
        sweep(fr, (b - (self.len - .5)) / .5, hexc('#fff4dc'))
    # --- fin
    def do_outro(self, fr, t, tl, b):
        self.bg(fr, t, (1, 1, 1), 2300 + tl * 5)
        d = ImageDraw.Draw(fr)
        for x, y, ph, sz in self.stars:
            q = (1.4 + 3 * sz) * (.55 + .45 * math.sin(tl * 2 + ph * 6.28)); xx, yy = x * W, y * 500
            d.ellipse((xx - q, yy - q, xx + q, yy + q), fill=(255, 245, 205, 255))
        self.conf.draw(fr, tl, .5 if b > 12 else .75)
        k = back((b - .4) / 1.6)
        sy = 170 + (1 - k) * 800
        put(fr, self.card2, (W - self.card2.width) / 2, sy)
        put(fr, self.bye, (W - self.bye.width) / 2, sy + 62)
        put(fr, self.credit, (W - self.credit.width) / 2, sy + 216)
        calm = b >= 12
        draw_char(fr, 'reinette', 720, 880, t, b, hop=0 if calm else 34, scale=1.1, R=165, tilt=8 * math.sin(tl * 3))
        draw_char(fr, 'api', 1200, 880, t, b, hop=0 if calm else 34, phase=.5, scale=1.1, R=165, tilt=-8 * math.sin(tl * 3))
        sweep(fr, 1 - b / .5, hexc('#fff4dc'), rev=True)
        end = self.tend - t
        if end < .9: put_fade(fr, 1 - end / .9, CREAM)
