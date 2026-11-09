"""Chronologie d'un épisode : tout vient de $EPISODE/episode.json."""
import json, os
E = json.load(open(os.path.join(os.environ['EPISODE'], 'episode.json'), encoding='utf-8'))
BPM = E['bpm']
B = 60 / BPM
BAR = E.get('temps_par_mesure', 4)
FPS = 30
W, H = 1920, 1080
TAIL = 2.6
SEC = {s['nom']: s for s in E['sections']}
SECTIONS = [(s['nom'], s['mesure'] * BAR / 4, s['mesures'] * BAR / 4) for s in E['sections']]
_last = E['sections'][-1]
TOTAL_BEATS = (_last['mesure'] + _last['mesures']) * BAR
DURATION = TOTAL_BEATS * B + TAIL
