"""Rend une section en MP4, ou des images de contrôle : scene.py <nom> | scene.py still nom:temps ..."""
import importlib.util, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from papier import FPS, W, H, DURATION, SECTIONS, B
EP = os.environ['EPISODE']; BUILD = os.path.join(EP, '.build'); os.makedirs(BUILD, exist_ok=True)
spec = importlib.util.spec_from_file_location('scenes_ep', os.path.join(EP, 'scenes.py'))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
def bounds(name):
    s = next(x for x in SECTIONS if x[0] == name); i = SECTIONS.index(s); bar = SECTIONS[0][2] * 0 + 4
    a = round(s[1] * bar * B * FPS)
    e = round(DURATION * FPS) if i == len(SECTIONS) - 1 else round(SECTIONS[i + 1][1] * bar * B * FPS)
    return a, e
if sys.argv[1] == 'still':
    by = {}
    for arg in sys.argv[2:]:
        sec, tt = arg.split(':'); tt = float(tt)
        sc = by.setdefault(sec, mod.Scenes(sec)); f0, _ = bounds(sec)
        sc.frame(f0 / FPS + tt).convert('RGB').save(os.path.join(BUILD, f'{sec}_{tt:.1f}.png'))
else:
    name = sys.argv[1]; sc = mod.Scenes(name); a, e = bounds(name)
    tmp = os.path.join(BUILD, name + '.tmp.mp4'); final = os.path.join(BUILD, name + '.mp4')
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-crf', '21', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    for i in range(a, e): p.stdin.write(sc.frame(i / FPS).convert('RGB').tobytes())
    p.stdin.close()
    if p.wait() != 0: sys.exit(f'ffmpeg a échoué sur {name}')
    os.replace(tmp, final); print(name, e - a, 'images')
