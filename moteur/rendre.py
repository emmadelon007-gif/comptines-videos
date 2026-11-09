#!/usr/bin/env python3
"""Fabrique la vidéo finale : python3 moteur/rendre.py episodes/<slug>. Sortie : videos/<slug>.mp4 et .jpg"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.path.abspath(sys.argv[1]); slug = os.path.basename(EP.rstrip('/')); BUILD = os.path.join(EP, '.build'); os.makedirs(BUILD, exist_ok=True)
env = dict(os.environ, EPISODE=EP)
E = json.load(open(os.path.join(EP, 'episode.json'), encoding='utf-8'))
M = os.path.join(ROOT, 'moteur')
def run(*a): subprocess.run(a, check=True, env=env)
wav = os.path.join(BUILD, 'music.wav')
run(sys.executable, os.path.join(M, 'musique.py'), wav)
noms = [s['nom'] for s in E['sections']]
with ThreadPoolExecutor(os.cpu_count() or 2) as ex: list(ex.map(lambda n: run(sys.executable, os.path.join(M, 'scene.py'), n), noms))
lst = os.path.join(BUILD, 'list.txt')
open(lst, 'w').write(''.join(f"file '{os.path.join(BUILD, n + '.mp4')}'\n" for n in noms))
os.makedirs(os.path.join(ROOT, 'videos'), exist_ok=True)
v_tmp = os.path.join(BUILD, 'video.mp4'); out_tmp = os.path.join(BUILD, 'final.mp4'); out = os.path.join(ROOT, 'videos', slug + '.mp4')
run('ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', v_tmp)
run('ffmpeg', '-y', '-loglevel', 'error', '-i', v_tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out_tmp)
os.replace(out_tmp, out)
m = E.get('miniature', {'section': noms[0], 'temps': 5})
run(sys.executable, os.path.join(M, 'scene.py'), 'still', f"{m['section']}:{float(m['temps'])}")
from PIL import Image
Image.open(os.path.join(BUILD, f"{m['section']}_{float(m['temps']):.1f}.png")).resize((1280, 720), Image.LANCZOS).convert('RGB').save(os.path.join(ROOT, 'videos', slug + '.jpg'), quality=92)
# Contrôles bloquants : image, son, durée, niveau
p = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', out]))
v = next(s for s in p['streams'] if s['codec_type'] == 'video'); au = [s for s in p['streams'] if s['codec_type'] == 'audio']
err = []
if (v['codec_name'], v['width'], v['height']) != ('h264', 1920, 1080): err.append('format vidéo inattendu')
if not au: err.append('piste audio absente')
elif abs(float(v['duration']) - float(au[0]['duration'])) > .2: err.append('image et son de durées différentes')
log = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', out, '-map', '0:a', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True, env=env).stderr
lufs = re.findall(r'I:\s+(-?[\d.]+) LUFS', log)
if not lufs or float(lufs[-1]) < -30: err.append('son absent ou presque muet')
print(json.dumps({'video': out, 'duree': float(p['format']['duration']), 'taille_mo': round(int(p['format']['size']) / 1e6, 1), 'lufs': lufs[-1] if lufs else None, 'erreurs': err}, ensure_ascii=False))
sys.exit(1 if err else 0)
