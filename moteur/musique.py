"""Compose la piste instrumentale d'un épisode à partir de episode.json (aucun enregistrement externe)."""
import os, sys
import numpy as np
from scipy.signal import lfilter, fftconvolve, butter, sosfilt
from scipy.io import wavfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from song import *
SR = 44100
N = int(DURATION * SR)
rng = np.random.default_rng(7)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
def bus(): return np.zeros((N, 2))
def add(b, x, t, gain=1., pan=0.):
    i = int(t * SR)
    if i >= N: return
    x = x[:N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    b[i:i + len(x), 0] += x * gain * l * 1.414
    b[i:i + len(x), 1] += x * gain * r * 1.414
def tine(m, dur=1.6):
    n = int(SR * dur); t = np.arange(n) / SR; f = hz(m)
    mod = 1.6 * np.exp(-t * 9) * np.sin(2 * np.pi * f * 3.5 * t)
    x = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 3.2)
    x += .22 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 6) + .10 * np.sin(2 * np.pi * f * 5.02 * t) * np.exp(-t * 16)
    x[:30] *= np.linspace(0, 1, 30)
    return x
_ks = {}
def pluck(m, dur=1.4):
    if m in _ks: return _ks[m]
    n = int(SR * dur); p = int(round(SR / hz(m)))
    ex = np.zeros(n); ex[:p] = lfilter([.5, .5], [1], rng.uniform(-1, 1, p))
    a = np.zeros(p + 2); a[0] = 1; a[p] = -.4965; a[p + 1] = -.4965
    y = lfilter([1], a, ex); y /= np.abs(y).max()
    _ks[m] = y
    return y
def bass(m, dur):
    n = int(SR * dur); t = np.arange(n) / SR; f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + .28 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 2.2)
    a = min(300, n // 4); x[:a] *= np.linspace(0, 1, a); x[-400:] *= np.linspace(1, 0, 400)
    return x
def flute(m, dur):
    n = int(SR * (dur + .15)); t = np.arange(n) / SR; f = hz(m)
    vib = .006 * np.minimum(1, t / .35) * np.sin(2 * np.pi * 5.2 * t)
    ph = 2 * np.pi * np.cumsum(f * (1 + vib)) / SR
    x = np.sin(ph) + .16 * np.sin(2 * ph) + .05 * np.sin(3 * ph)
    x += .05 * sosfilt(butter(2, [f * .9, min(f * 3.5, 20000)], 'bp', fs=SR, output='sos'), rng.normal(0, 1, n))
    return x * np.minimum(1, t / .05) * np.minimum(1, (n / SR - t) / .13)
def noise_hit(dur, lo, hi, decay):
    n = int(SR * dur); t = np.arange(n) / SR
    return sosfilt(butter(2, [lo, hi], 'bp', fs=SR, output='sos'), rng.normal(0, 1, n)) * np.exp(-t * decay)
def wood(f=900):
    t = np.arange(int(SR * .09)) / SR
    return (np.sin(2 * np.pi * f * t) + .5 * np.sin(2 * np.pi * f * 2.6 * t)) * np.exp(-t * 55)
def kick():
    t = np.arange(int(SR * .28)) / SR
    return np.sin(2 * np.pi * (58 * t + 18 * (1 - np.exp(-t * 32)))) * np.exp(-t * 11)

PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def parse(ch):
    root = PC[ch[0]]; i = 1
    if ch[i:i + 1] == '#': root += 1; i += 1
    elif ch[i:i + 1] == 'b': root -= 1; i += 1
    return root % 12, ch[i:i + 1] == 'm'
def voicing(ch):
    r, mi = parse(ch)
    tones = sorted(60 + (r + d) % 12 for d in (0, 3 if mi else 4, 7))
    return tones + [60 + r % 12 + 12]

lead, pad, rhythm, low, perc_bus = bus(), bus(), bus(), bus(), bus()
PATTERNS = {4: [(0, 0), (1, 0), (1.5, 1), (2.5, 1), (3, 0), (3.5, 1)], 3: [(0, 0), (1, 1), (2, 1)], 2: [(0, 0), (.5, 1), (1, 0), (1.5, 1)], 6: [(0, 0), (1, 1), (2, 1), (3, 0), (4, 1), (5, 1)]}
def strum(t0, ch, tr, gain):
    for off, up in PATTERNS.get(BAR, PATTERNS[4]):
        st = voicing(ch)[::-1 if up else 1]
        for k, m in enumerate(st):
            add(rhythm, pluck(m + tr), (t0 + off) * B + k * .012, gain * (.55 if up else 1), pan=(k - 1.5) * .18)
def bassline(t0, ch, tr, g):
    r, _ = parse(ch); root = 48 + r; fifth = root + 7 - (12 if root + 7 > 59 else 0)
    add(low, bass(root + tr, B * 1.8), t0 * B, g)
    if BAR >= 4: add(low, bass(fifth + tr, B * 1.8), (t0 + BAR / 2) * B, g * .85)
def percs(t0, sh, ta, ki):
    if sh:
        for i in range(int(BAR * 2)): add(perc_bus, noise_hit(.07, 6000, 13000, 70), (t0 + i / 2) * B, .05 if i % 2 else .09, pan=.35)
    if ta:
        for b_ in range(1, int(BAR), 2): add(perc_bus, wood(), (t0 + b_) * B, .14, pan=-.25)
    if ki:
        for b_ in range(0, int(BAR), 2): add(perc_bus, kick(), (t0 + b_) * B, .42)

for s in E['sections']:
    t0 = s['mesure'] * BAR; tr = s.get('transpo', 0)
    notes = [n[1:] for l in s.get('lignes', []) for n in l] + s.get('notes', [])
    for ins in s.get('instruments', [{'son': 'tine', 'gain': .46}]):
        for t, d, m in notes:
            mm = m + tr + ins.get('oct', 0)
            if ins['son'] == 'tine': add(lead, tine(mm), (t0 + t) * B, ins['gain'], pan=.05)
            else: add(lead, flute(mm, d * B * .94), (t0 + t) * B, ins['gain'], pan=-.08)
    acc = s['accords']
    for k in range(s['mesures']):
        tb = t0 + k * BAR; ch = acc[k % len(acc)]
        last = s.get('fin') and k == s['mesures'] - 1
        if last: continue
        if s.get('strum'): strum(tb, ch, tr, s['strum'])
        if s.get('basse'): bassline(tb, ch, tr, s['basse'])
        percs(tb, s.get('shaker'), s.get('taps'), s.get('kick'))
    if s.get('fin'):
        tb = t0 + (s['mesures'] - 1) * BAR; ch = acc[(s['mesures'] - 1) % len(acc)]; r, mi = parse(ch)
        base = 62 - 2 + r if False else 60 + r
        for k, d in enumerate((0, 3 if mi else 4, 7, 12, 16 if not mi else 15, 19, 24)):
            add(pad, tine(base + tr + d, 3.2), tb * B + k * .03, .2, pan=(k - 3) * .12)
        add(low, bass(36 + r + tr, 2.6), tb * B, .5); add(perc_bus, kick(), tb * B, .4)
        for k in range(14):
            add(pad, tine(base + tr + 24 + [0, 2, 4, 7, 9, 12, 14][k % 7], .9), tb * B + .25 + k * .07, .05 + k * .004, pan=np.sin(k) * .6)

irn = int(1.5 * SR); tt = np.arange(irn) / SR
ir = np.stack([rng.normal(0, 1, irn) * np.exp(-tt * 3.6) for _ in range(2)], 1)
ir = sosfilt(butter(1, 5200, 'lp', fs=SR, output='sos'), ir, axis=0); ir /= np.sqrt((ir ** 2).sum(0))
def verb(x, amt): return x + np.stack([fftconvolve(x[:, c], ir[:, c])[:N] for c in range(2)], 1) * amt
mix = verb(lead, .34) + verb(pad, .4) + verb(rhythm, .16) + low * .95 + verb(perc_bus, .1)
fl = int(.5 * SR); fade = np.ones(N); fade[-fl:] = np.linspace(1, 0, fl); mix *= fade[:, None]
mix -= mix.mean(0)
mix = np.tanh(mix / np.abs(mix).max() * .9); mix = mix / np.abs(mix).max() * .775
wavfile.write(sys.argv[1], SR, (mix * 32767).astype(np.int16))
