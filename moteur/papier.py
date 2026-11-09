import sys, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song import *

FD = '/usr/share/fonts/truetype/google-fonts/'
def font(name, size): return ImageFont.truetype(FD + name, size)
POP = 'Poppins-Bold.ttf'
def lora(size):
    f = ImageFont.truetype(FD + 'Lora-Italic-Variable.ttf', size)
    f.set_variation_by_axes([700])
    return f
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lerp(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease(k): k = clamp(k); return k * k * (3 - 2 * k)
def back(k):
    k = clamp(k); c = 1.9; return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2
INK = hexc('#3d2a24'); RED = hexc('#d92f2b'); CREAM = hexc('#fff4dc'); GOLD = hexc('#f1b92f')

_rng = np.random.default_rng(3)
GRAIN = np.clip(_rng.normal(1, .022, (1200, 2200)), .9, 1.1)
def grain(img):
    """Texture papier sur une couche RGBA."""
    a = np.array(img).astype(np.float32); h, w = a.shape[:2]
    g = np.resize(GRAIN, (h, w))
    a[..., :3] = np.clip(a[..., :3] * g[..., None], 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')
def shadowed(img, dx=5, dy=8, blur=7, op=.28):
    a = img.getchannel('A').filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * op))
    sh = Image.new('RGBA', img.size, (40, 20, 30, 0)); sh.putalpha(a)
    out = Image.new('RGBA', img.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (max(dx, 0), max(dy, 0)))
    out.alpha_composite(img)
    return out
def put(fr, s, x, y):
    x, y = int(round(x)), int(round(y))
    sx, sy = max(0, -x), max(0, -y)
    if x + s.width <= 0 or y + s.height <= 0 or x >= W or y >= H: return
    r = min(s.width, W - x); b = min(s.height, H - y)
    fr.alpha_composite(s, (max(x, 0), max(y, 0)), (sx, sy, r, b))

# ---------- Pommes ----------
def apple_pts(cx, cy, R):
    pts = []
    for i in range(240):
        th = i / 240 * 2 * math.pi
        d = min(th, 2 * math.pi - th); db = abs(th - math.pi)
        x = math.sin(th) * (1.03 + .07 * math.cos(th))
        y = -math.cos(th) * .95 + .19 * math.exp(-(d / .42) ** 2) - .07 * math.exp(-(db / .34) ** 2)
        pts.append((cx + x * R, cy + y * R))
    return pts
def apple(R, c1, c2, face=False, blink=False, mouth=False, freckle=None, bow=None, feet=True, leaf=True, S=3, contour=None, tige=True):
    Rs = R * S; pad = int(Rs * .55); sz = int(2 * Rs + 2 * pad)
    cx = sz // 2; cy = int(sz * .54)
    img = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    if feet:
        for sgn in (-1, 1):
            fx = cx + sgn * Rs * .42; fy = cy + Rs * .98
            d.ellipse((fx - Rs * .26, fy - Rs * .13, fx + Rs * .26, fy + Rs * .15), fill=(120, 72, 44, 255))
    m = Image.new('L', (sz, sz), 0); ImageDraw.Draw(m).polygon((contour or apple_pts)(cx, cy, Rs), fill=255)
    yy, xx = np.mgrid[0:sz, 0:sz].astype(np.float32)
    k = np.clip((xx - cx) / Rs * .55 + .5, 0, 1)[..., None]
    arr = np.array(c1, np.float32) * (1 - k) + np.array(c2, np.float32) * k
    v = np.clip((yy - cy) / Rs, -1, 1)[..., None]
    arr = arr * (1 - .17 * np.clip(v, 0, 1))
    grad = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGB').convert('RGBA'); grad.putalpha(m)
    img.alpha_composite(grad); d = ImageDraw.Draw(img)
    if freckle:
        r2 = np.random.default_rng(int(R))
        for _ in range(70):
            a, rr = r2.uniform(0, 6.28), Rs * .9 * math.sqrt(r2.uniform(0, 1))
            px, py = cx + math.cos(a) * rr, cy + math.sin(a) * rr * .9
            if abs(py - cy) < Rs * .42 and abs(px - cx) < Rs * .66: continue
            q = r2.uniform(.012, .028) * Rs
            d.ellipse((px - q, py - q, px + q, py + q), fill=freckle + (170,))
    hl = Image.new('RGBA', (sz, sz), (0, 0, 0, 0))
    ImageDraw.Draw(hl).ellipse((cx - Rs * .72, cy - Rs * .68, cx - Rs * .22, cy - Rs * .12), fill=(255, 255, 255, 80))
    hl = hl.filter(ImageFilter.GaussianBlur(Rs * .05)); hl.putalpha(Image.fromarray(np.minimum(np.array(hl.getchannel('A')), np.array(m))))
    img.alpha_composite(hl); d = ImageDraw.Draw(img)
    top = cy - Rs * .72
    if tige: d.line([(cx, top + Rs * .1), (cx + Rs * .03, top - Rs * .2), (cx + Rs * .13, top - Rs * .38)], fill=(104, 66, 40, 255), width=max(2, int(Rs * .09)), joint='curve')
    if leaf:
        lx, ly = cx + Rs * .1, top - Rs * .16
        pts = [(lx + Rs * .62 * t, ly - Rs * .16 * math.sin(t * math.pi * 1.0) * 2.1 - Rs * .1 * t) for t in np.linspace(0, 1, 30)]
        pts += [(lx + Rs * .62 * t, ly + Rs * .10 * math.sin(t * math.pi) - Rs * .1 * t) for t in np.linspace(1, 0, 30)]
        d.polygon(pts, fill=(84, 158, 64, 255))
        d.line([(lx, ly), (lx + Rs * .55, ly - Rs * .09)], fill=(54, 116, 48, 255), width=max(1, int(Rs * .02)))
    if bow:
        bx, by = cx - Rs * .42, cy - Rs * .63
        d.polygon([(bx, by), (bx - Rs * .3, by - Rs * .17), (bx - Rs * .3, by + Rs * .17)], fill=bow + (255,))
        d.polygon([(bx, by), (bx + Rs * .3, by - Rs * .17), (bx + Rs * .3, by + Rs * .17)], fill=bow + (255,))
        d.ellipse((bx - Rs * .08, by - Rs * .08, bx + Rs * .08, by + Rs * .08), fill=lerp(bow, (0, 0, 0), .2) + (255,))
    if face:
        ex, ey = Rs * .36, cy - Rs * .08
        for sgn in (-1, 1):
            X = cx + sgn * ex
            if blink:
                d.arc((X - Rs * .17, ey - Rs * .1, X + Rs * .17, ey + Rs * .16), 200, 340, fill=INK + (255,), width=int(Rs * .05))
            else:
                d.ellipse((X - Rs * .18, ey - Rs * .23, X + Rs * .18, ey + Rs * .23), fill=(255, 255, 255, 255))
                d.ellipse((X - Rs * .115, ey - Rs * .13, X + Rs * .115, ey + Rs * .16), fill=INK + (255,))
                d.ellipse((X - Rs * .05, ey - Rs * .09, X + Rs * .03, ey - Rs * .01), fill=(255, 255, 255, 255))
            d.ellipse((X + sgn * Rs * .18 - Rs * .13, ey + Rs * .26, X + sgn * Rs * .18 + Rs * .13, ey + Rs * .39), fill=(255, 120, 120, 140))
        my = cy + Rs * .36
        if mouth:
            d.ellipse((cx - Rs * .17, my - Rs * .1, cx + Rs * .17, my + Rs * .26), fill=(120, 26, 38, 255))
            d.ellipse((cx - Rs * .1, my + Rs * .08, cx + Rs * .1, my + Rs * .25), fill=(238, 96, 96, 255))
        else:
            d.arc((cx - Rs * .22, my - Rs * .2, cx + Rs * .22, my + Rs * .16), 25, 155, fill=INK + (255,), width=int(Rs * .05))
    out = img.resize((sz // S, sz // S), Image.LANCZOS)
    return shadowed(grain(out), 4, 6, 6, .24)

R_C1, R_C2 = hexc('#f4cf49'), hexc('#a9bb3e')
A_C1, A_C2 = hexc('#ef3b34'), hexc('#f2a437')
PERSOS = {}   # nom -> fonction(blink, mouth, R) renvoyant un sprite RGBA ; à remplir par chaque épisode
CHARS = {}
def char(key, blink, mouth, R=165):
    k = (key, blink, mouth, R)
    if k not in CHARS: CHARS[k] = PERSOS[key](blink, mouth, R)
    return CHARS[k]
SMALL = {}
def small(i, R=38):
    k = (i, R)
    if k not in SMALL:
        cs = [(R_C1, R_C2), (A_C1, A_C2), (hexc('#e6463c'), hexc('#a31e2b')), (hexc('#b6cf52'), hexc('#7fae3c'))]
        c = cs[i % 4]; SMALL[k] = apple(R, c[0], c[1], feet=False)
    return SMALL[k]

def draw_char(fr, key, x, foot, t, b, hop=34, sing=False, scale=1., phase=0., tilt=0., R=165):
    p = (b + phase) % 1
    y = hop * 4 * p * (1 - p)
    land = max(0, 1 - p / .16) if hop else 0
    sq = .1 * land - .06 * math.sin(p * math.pi) * (1 if hop else 0)
    blink = ((t * .63 + sum(map(ord, key)) * .137) % 1) < .05
    s = char(key, blink, sing, R)
    w = int(s.width * scale * (1 + sq)); h = int(s.height * scale * (1 - sq))
    im = s.resize((w, h), Image.BILINEAR)
    ang = tilt + 5 * math.sin((b + phase) * math.pi)
    im2 = im.rotate(ang, Image.BICUBIC, expand=True)
    footline = int(h * .9)
    put(fr, im2, x - im2.width / 2, foot - y - footline - (im2.height - h) / 2)

# ---------- Décors ----------
PAL = {
    'day': dict(sky=('#7fd0ef', '#ecf9dc'), hills=('#c5e27f', '#97d05f', '#67b24a'), canopy=('#4f9f4b', '#65b552', '#3f8a44'), trunk='#8a5a39', fruit=True),
    'sunset': dict(sky=('#f46d6b', '#ffd98c'), hills=('#e0a860', '#b98a48', '#8a6a3c'), canopy=('#6a7c3c', '#80903f', '#566731'), trunk='#5d3d2b', fruit=True),
    'night': dict(sky=('#101c48', '#3f3f8b'), hills=('#37516b', '#284460', '#1c3550'), canopy=('#21505a', '#2a6068', '#1a4450'), trunk='#26303f', fruit=True),
}
def sky(pal):
    a, b = hexc(pal['sky'][0]), hexc(pal['sky'][1])
    k = np.linspace(0, 1, H)[:, None, None] ** 1.1
    arr = np.array(a, np.float32) * (1 - k) + np.array(b, np.float32) * k
    arr = np.repeat(arr, W, 1)
    return grain(Image.fromarray(arr.astype(np.uint8), 'RGB').convert('RGBA'))
def tree(pal, seed, sc=1.):
    S = 2; w, h = int(460 * sc) * S, int(560 * sc) * S; r = np.random.default_rng(seed)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = w / 2
    tr = hexc(pal['trunk'])
    d.polygon([(c - 34 * sc * S, h), (c - 20 * sc * S, h * .46), (c + 20 * sc * S, h * .46), (c + 34 * sc * S, h)], fill=tr + (255,))
    for sg in (-1, 1):
        d.line([(c, h * .62), (c + sg * 95 * sc * S, h * .4)], fill=tr + (255,), width=int(18 * sc * S))
    cs = [hexc(x) for x in pal['canopy']]
    blobs = [(c + r.uniform(-140, 140) * sc * S, h * .32 + r.uniform(-90, 90) * sc * S, r.uniform(85, 130) * sc * S) for _ in range(13)]
    for i, (x, y, q) in enumerate(blobs):
        col = cs[2] if i < 5 else cs[0] if i < 10 else cs[1]
        d.ellipse((x - q, y - q, x + q, y + q), fill=col + (255,))
    for _ in range(16):
        a, rr = r.uniform(0, 6.28), r.uniform(.15, 1) ** .5
        x, y = c + math.cos(a) * rr * 200 * sc * S, h * .32 + math.sin(a) * rr * 165 * sc * S
        q = 15 * sc * S; col = hexc(['#e63e36', '#f0b83a', '#e63e36'][int(r.integers(3))])
        if pal['sky'][0] == '#101c48': col = lerp(col, (30, 40, 90), .35)
        d.ellipse((x - q, y - q, x + q, y + q), fill=col + (255,))
        d.ellipse((x - q * .5, y - q * .6, x - q * .05, y - q * .15), fill=(255, 255, 255, 110))
    return im.resize((w // S, h // S), Image.LANCZOS)
LW = 3840
def hill(pal, idx, base, amp, seed, ntrees, tsc):
    col = hexc(pal['hills'][idx]); r = np.random.default_rng(seed)
    x = np.arange(LW); ph = r.uniform(0, 6.28, 4)
    y = base + amp * (.55 * np.sin(2 * np.pi * x / LW * 2 + ph[0]) + .3 * np.sin(2 * np.pi * x / LW * 5 + ph[1]) + .15 * np.sin(2 * np.pi * x / LW * 9 + ph[2]))
    im = Image.new('RGBA', (LW, H), (0, 0, 0, 0))
    for i in range(ntrees):
        tx = int((i + .5 + r.uniform(-.25, .25)) / ntrees * (LW - 700)) + 350
        t_ = tree(pal, seed * 10 + i, tsc * r.uniform(.85, 1.15))
        im.alpha_composite(t_, (tx - t_.width // 2, int(y[tx] - t_.height + 18)))
    m = Image.new('L', (LW, H), 0); d = ImageDraw.Draw(m)
    d.polygon([(0, H)] + [(int(a), float(b)) for a, b in zip(x[::4], y[::4])] + [(LW - 1, float(y[-1])), (LW - 1, H)], fill=255)
    arr = np.zeros((H, LW, 3), np.float32) + np.array(col, np.float32)
    yy = np.arange(H, dtype=np.float32)[:, None, None]
    arr = arr * (1 - .13 * np.clip((yy - base) / 400, 0, 1))
    body = Image.fromarray(arr.astype(np.uint8), 'RGB').convert('RGBA'); body.putalpha(m)
    im.alpha_composite(shadowed(body, 0, -6, 8, .2))
    return grain(im)
def blit_scroll(fr, layer, scroll, top=0):
    x = int(scroll) % LW
    r1 = min(LW, x + W)
    fr.alpha_composite(layer, (0, top), (x, top, r1, H))
    if r1 - x < W:
        fr.alpha_composite(layer, (r1 - x, top), (0, top, W - (r1 - x), H))
def cloud(seed, sc=1., col=(255, 252, 240)):
    S = 2; r = np.random.default_rng(seed); w, h = int(440 * sc) * S, int(190 * sc) * S
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(7):
        q = r.uniform(.2, .38) * h; x = w * (.18 + .64 * i / 6)
        d.ellipse((x - q * 1.4, h * .62 - q * 1.2, x + q * 1.4, h * .62 + q * .9), fill=col + (255,))
    d.rectangle((w * .1, h * .62, w * .9, h * .82), fill=col + (255,))
    return shadowed(grain(im.resize((w // S, h // S), Image.LANCZOS)), 3, 7, 7, .16)
def sun(R, col, ray=None):
    S = 2; sz = int(R * 3.4) * S; c = sz / 2; im = Image.new('RGBA', (sz, sz), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if ray:
        for i in range(14):
            a = i / 14 * 6.283; da = .09
            d.polygon([(c + math.cos(a - da) * R * 1.2 * S, c + math.sin(a - da) * R * 1.2 * S),
                       (c + math.cos(a) * R * 1.65 * S, c + math.sin(a) * R * 1.65 * S),
                       (c + math.cos(a + da) * R * 1.2 * S, c + math.sin(a + da) * R * 1.2 * S)], fill=ray + (255,))
    d.ellipse((c - R * S, c - R * S, c + R * S, c + R * S), fill=col + (255,))
    return shadowed(grain(im.resize((sz // S, sz // S), Image.LANCZOS)), 2, 4, 8, .14)
def carpet(col, length=1120, height=96):
    S = 2; w, h = (length + 90) * S, (height + 40) * S
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); y0, y1 = 20 * S, (height + 20) * S; x0, x1 = 45 * S, (length + 45) * S
    d.rounded_rectangle((x0, y0, x1, y1), 8 * S, fill=col + (255,))
    trim = lerp(col, (255, 225, 140), .75); dark = lerp(col, (20, 10, 20), .32)
    d.rectangle((x0, y0 + 10 * S, x1, y0 + 17 * S), fill=trim + (255,)); d.rectangle((x0, y1 - 17 * S, x1, y1 - 10 * S), fill=trim + (255,))
    my = (y0 + y1) / 2
    for i in range(int((x1 - x0) / (84 * S))):
        cx = x0 + (i + .5) * 84 * S; q = 19 * S
        d.polygon([(cx, my - q), (cx + q, my), (cx, my + q), (cx - q, my)], fill=(dark if i % 2 else trim) + (255,))
    for yy in range(y0, y1, 11 * S):
        for sg, ex in ((-1, x0), (1, x1)):
            d.line([(ex, yy + 3 * S), (ex + sg * 30 * S, yy + 6 * S)], fill=trim + (255,), width=4 * S)
    return shadowed(grain(im), 8, 12, 10, .24)
def wavy(img, t, amp=11, wl=420, spd=5.):
    a = np.array(img); h, w = a.shape[:2]; out = np.zeros_like(a)
    pad = int(amp * 2)
    canvas = np.zeros((h + 2 * pad, w, 4), np.uint8)
    ys = (amp * np.sin(np.arange(w) * 2 * np.pi / wl - t * spd) * np.clip(np.arange(w) / 120, .2, 1)).astype(int)
    for i in range(0, w, 2):
        y0 = pad + ys[i]; canvas[y0:y0 + h, i:i + 2] = a[:, i:i + 2]
    return Image.fromarray(canvas, 'RGBA').resize((w // 2, (h + 2 * pad) // 2), Image.BILINEAR)
def paper_card(w, h, col=CREAM, rad=26):
    S = 2; im = Image.new('RGBA', (w * S + 60, h * S + 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((30, 30, 30 + w * S, 30 + h * S), rad * S, fill=col + (255,))
    return shadowed(grain(im.resize((im.width // S, im.height // S), Image.LANCZOS)), 4, 9, 9, .26)
def text_img(lines, f, col=RED, sp=8, stroke=0, sc=None, align='center'):
    tmp = ImageDraw.Draw(Image.new('L', (4, 4)))
    bbs = [tmp.textbbox((0, 0), l, font=f, stroke_width=stroke) for l in lines]
    w = max(b[2] - b[0] for b in bbs) + 24; lh = f.size + sp; h = int(lh * len(lines) + 24 + f.size * .22)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, (l, b) in enumerate(zip(lines, bbs)):
        x = 12 + (w - 24 - (b[2] - b[0])) // 2 - b[0]
        d.text((x, 8 + i * lh), l, font=f, fill=col + (255,), stroke_width=stroke, stroke_fill=(sc or col) + (255,))
    return im

# ---------- Paroles ----------
class Lyrics:
    """Bandeau karaoké. lignes = [[[texte, temps, durée, midi], ...], ...] ; un texte peut commencer par une espace."""
    def __init__(self, lignes):
        self.lines = lignes
        self.toks = [[n[0] for n in l] for l in lignes]
        self.fin = max(l[-1][1] + l[-1][2] for l in lignes)
        size = 76
        while max(font(POP, size).getlength(''.join(t)) for t in self.toks) > 1430 and size > 40: size -= 2
        self.f = font(POP, size); self.card = paper_card(1530, 138)
        self.ball = small(1, 25); self.spr = []
        for tk in self.toks:
            txt = ''.join(tk); L = self.f.getlength(txt)
            w, h = int(L) + 8, 112
            b = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(b).text((4, 2), txt, font=self.f, fill=INK + (255,))
            hl = Image.new('RGBA', (w, h), (0, 0, 0, 0)); ImageDraw.Draw(hl).text((4, 2), txt, font=self.f, fill=RED + (255,))
            cum = [4 + self.f.getlength(''.join(tk[:i])) for i in range(len(tk) + 1)]
            start = [cum[i] + (self.f.getlength(' ') if tk[i].startswith(' ') else 0) for i in range(len(tk))]
            self.spr.append((b, hl, w, start, cum))
    def state(self, b):
        li = 0
        for i, l in enumerate(self.lines):
            if b >= l[0][1]: li = i
        line = self.lines[li]; tok, pr = -1, 0.
        for i, (s, t, d, m) in enumerate(line):
            if t <= b:
                tok = i; nxt = line[i + 1][1] if i + 1 < len(line) else t + d
                pr = clamp((b - t) / max(.01, nxt - t))
        return li, tok, pr
    def singing(self, b):
        li, tok, pr = self.state(b)
        if tok < 0 or b >= self.fin: return False
        s, t, d, m = self.lines[li][tok]
        return b < t + d * .78
    def draw(self, fr, b):
        if b > self.fin + .5: return
        cy = 978; k = 1 - ease((b - self.fin) / .45); yo = (1 - k) * 220
        put(fr, self.card, (W - self.card.width) / 2, cy - self.card.height / 2 + yo)
        li, tok, pr = self.state(b)
        base, hl, w, start, cum = self.spr[li]
        x0 = (W - w) / 2; y0 = cy - 60 + yo
        put(fr, base, x0, y0)
        if tok >= 0:
            cut = start[tok] + (cum[tok + 1] - start[tok]) * min(1, pr * 1.8)
            if cut >= 1: put(fr, hl.crop((0, 0, int(cut), hl.height)), x0, y0)
            cx_a = (start[tok] + cum[tok + 1]) / 2
            cx_b = (start[tok + 1] + cum[tok + 2]) / 2 if tok + 1 < len(self.toks[li]) else cx_a
            ball_x = x0 + cx_a + (cx_b - cx_a) * ease(pr)
            ball_y = y0 - 8 - 62 * 4 * pr * (1 - pr)
            put(fr, self.ball, ball_x - self.ball.width / 2, ball_y - self.ball.height * .72)

# ---------- Particules ----------
def falling(fr, t0, b, n, seed, ground, B_=B):
    r = np.random.default_rng(seed)
    for i in range(n):
        st = t0 + r.uniform(0, 6); x = r.uniform(120, W - 120); kind = int(r.integers(4)); g = 2600.
        T = (b - st) * B_
        if T < 0: continue
        y0 = r.uniform(120, 300); y = y0 + .5 * g * T * T; v = g * T; yg = ground - r.uniform(0, 30)
        rot = 0
        if y > yg:
            T1 = math.sqrt(2 * (yg - y0) / g); dt = T - T1; v0 = g * T1 * .42
            h = v0 * dt - .5 * g * dt * dt
            if dt > 2 * v0 / g: h = 0
            y = yg - max(0, h); x += min(dt, 1.) * 90 * (-1 if i % 2 else 1)
        put(fr, small(kind, 34), x - 58, y - 58)
class Confetti:
    def __init__(self, n=170, seed=5):
        r = np.random.default_rng(seed)
        self.p = [(r.uniform(0, W), r.uniform(-H, 0), r.uniform(120, 260), r.uniform(0, 6.28), r.uniform(8, 16), r.uniform(-40, 40),
                   hexc(['#f1b92f', '#ef3b34', '#7ccc6b', '#fff4dc', '#ffa23b'][int(r.integers(5))])) for _ in range(n)]
    def draw(self, fr, tl, intensity=1.):
        d = ImageDraw.Draw(fr)
        for x, y0, sp, ph, q, sw, col in self.p[:int(len(self.p) * intensity)]:
            y = (y0 + tl * sp) % (H + 120) - 60; xx = x + math.sin(tl * 2 + ph) * sw
            a = tl * 5 + ph; c, s = math.cos(a), math.sin(a); w_ = q * (.35 + .65 * abs(math.sin(tl * 4 + ph)))
            pts = [(xx + c * w_ - s * q * .5, y + s * w_ + c * q * .5), (xx - c * w_ - s * q * .5, y - s * w_ + c * q * .5), (xx - c * w_ + s * q * .5, y - s * w_ - c * q * .5), (xx + c * w_ + s * q * .5, y + s * w_ - c * q * .5)]
            d.polygon(pts, fill=col + (255,))

def rays(c1, c2, a):
    im = Image.new('RGB', (960, 540), c1); d = ImageDraw.Draw(im); cx, cy = 480, 330
    for i in range(20):
        a0 = a + i / 20 * 6.283; da = 6.283 / 40
        d.polygon([(cx, cy), (cx + 1300 * math.cos(a0), cy + 1300 * math.sin(a0)), (cx + 1300 * math.cos(a0 + da), cy + 1300 * math.sin(a0 + da))], fill=c2)
    return im.resize((W, H), Image.BILINEAR).convert('RGBA')

def sweep(fr, k, col, rev=False):
    """Feuille de papier qui balaie l'écran entre deux scènes."""
    k = clamp(k)
    if k <= 0: return
    d = ImageDraw.Draw(fr); pts = []
    for y in range(0, H + 30, 30):
        wob = 36 * math.sin(y * .012 + k * 7)
        if not rev: pts.append(((W + 180) * k - 90 + wob, y))
        else: pts.append((W - (W + 180) * k + 90 + wob, y))
    if not rev: poly = [(0, 0)] + pts + [(0, H)]
    else: poly = [(W, 0)] + pts + [(W, H)]
    d.polygon(poly, fill=col + (255,))

# ---------- Scènes ----------
class Scenes:
    def __init__(self, name):
        self.name = name
        sect = next(s for s in SECTIONS if s[0] == name)
        self.bar = sect[1]; self.t0 = sect[1] * 4 * B; self.len = sect[2] * 4
        self.tend = (sect[1] + sect[2]) * 4 * B + (TAIL if name == 'outro' else 0)
        pal = SEC[name].get('palette', 'day')
        self.pal = PAL[pal]; self.palname = pal
        self.sky = sky(self.pal)
        self.h = [hill(self.pal, 0, 610, 46, 11, 7, .62), hill(self.pal, 1, 720, 40, 22, 6, .85), hill(self.pal, 2, 835, 26, 33, 0, 1)]
        self.clouds = [(cloud(i, np.random.default_rng(i).uniform(.6, 1.15), (255, 252, 240) if pal == 'day' else (255, 226, 200) if pal == 'sunset' else (86, 96, 150)), np.random.default_rng(i * 7).uniform(0, W + 500), np.random.default_rng(i * 9).uniform(30, 300)) for i in range(5)]
        self.sun = sun(92, hexc('#ffd84d'), hexc('#ffc533')) if pal == 'day' else sun(170, hexc('#ffb347')) if pal == 'sunset' else None
        self.moon = apple(150, hexc('#fff0c2'), hexc('#ffd98a'), feet=False) if pal == 'night' else None
        if SEC[name].get('lignes'): self.ly = Lyrics(SEC[name]['lignes'])
        self.red = carpet(hexc('#d42d32'), 2200, 62); self.gray = carpet(hexc('#8d94a3'), 2200, 62)
        self.fly_r = carpet(hexc('#d42d32'), 1130, 88); self.fly_g = carpet(hexc('#8d94a3'), 1130, 88)
        self.prepare()
    def prepare(self):
        pass
    def bg(self, fr, t, spd=(1, 1, 1), offset=0, clouds=True):
        fr.alpha_composite(self.sky)
        tl = t - self.t0
        if self.sun is not None:
            if self.palname == 'day':
                r = self.sun.rotate(tl * 9, Image.BILINEAR); put(fr, r, 1480, 40)
            else: put(fr, self.sun, W / 2 - self.sun.width / 2 + 340, 300)
        if self.moon is not None: put(fr, self.moon, 1420, 40)
        if clouds:
            for c, x, y in self.clouds:
                xx = (x + tl * 22) % (W + 600) - 460
                put(fr, c, xx, y)
        for i, (l, s) in enumerate(zip(self.h, spd)):
            blit_scroll(fr, l, offset * s + tl * s * 0, top=100 if i < 2 else 480)
    def frame(self, t):
        fr = Image.new('RGBA', (W, H), (0, 0, 0, 255)); tl = t - self.t0; b = tl / B
        getattr(self, 'do_' + self.name)(fr, t, tl, b)
        return fr
def put_fade(fr, k, col=CREAM):
    k = clamp(k)
    if k <= 0: return
    fr.alpha_composite(Image.new('RGBA', (W, H), col + (int(255 * k),)))

def bounds(name):
    s = next(x for x in SECTIONS if x[0] == name)
    a = round(s[1] * 4 * B * FPS)
    i = SECTIONS.index(s)
    e = round(DURATION * FPS) if name == 'outro' else round(SECTIONS[i + 1][1] * 4 * B * FPS)
    return a, e

