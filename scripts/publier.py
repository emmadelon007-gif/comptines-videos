#!/usr/bin/env python3
"""Envoie sur YouTube, via Upload-Post, chaque fiche de a_publier/ pas encore traitée. Lancé par GitHub Actions."""
import glob, json, os, subprocess, sys, time
KEY = os.environ.get('UPLOAD_POST_API_KEY', '').strip()
PROFIL = 'youpi-karaoke'
def curl(*a):
    r = subprocess.run(['curl', '-sS', '--max-time', '900', '-w', '\n%{http_code}', '-H', f'Authorization: Apikey {KEY}', *a], capture_output=True, text=True)
    corps, _, code = r.stdout.rpartition('\n')
    try:
        d = json.loads(corps)
        if not isinstance(d, dict): d = {'reponse': d}
    except ValueError:
        d = {'reponse_brute': corps[:2000]}
    d['http'] = code; d['curl_erreur'] = r.stderr[:500]; d['curl_code'] = r.returncode
    return d
echec = False
os.makedirs('publie', exist_ok=True)
for fiche in sorted(glob.glob('a_publier/*.json')):
    nom = os.path.basename(fiche); sortie = os.path.join('publie', nom)
    if os.path.exists(sortie): continue
    j = json.load(open(fiche, encoding='utf-8'))
    if not 0 < len(j['titre']) <= 100: sys.exit(f'{nom} : titre invalide')
    rid = 'youpi-' + nom[:-5]
    args = ['-X', 'POST', 'https://api.upload-post.com/api/upload', '-F', f"video=@{j['video']}", '-F', f"thumbnail=@{j['miniature']}",
            '-F', f'user={PROFIL}', '-F', 'platform[]=youtube', '-F', f"title={j['titre']}", '-F', f"description={j['description']}",
            '-F', f"privacyStatus={j.get('visibilite', 'public')}", '-F', 'selfDeclaredMadeForKids=true', '-F', 'containsSyntheticMedia=false',
            '-F', f"categoryId={j.get('categorie', '1')}", '-F', 'async_upload=true', '-F', f'request_id={rid}']
    for t in j.get('tags', []): args += ['-F', f'tags[]={t}']
    rep = curl(*args); print(nom, json.dumps(rep, ensure_ascii=False)[:800])
    if rep['http'] not in ('200', '201', '202'):
        os.makedirs('echecs', exist_ok=True)
        json.dump({'envoi': rep, 'cle_presente': bool(KEY)}, open(os.path.join('echecs', nom), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        echec = True; continue
    rid = rep.get('request_id', rid); etat = {'envoi': rep}
    for _ in range(90):
        time.sleep(20)
        etat = dict(curl(f'https://api.upload-post.com/api/uploadposts/status?request_id={rid}'), envoi=rep)
        if etat.get('status') in ('completed', 'failed', 'not_found'): break
    etat['fiche'] = j
    res = [r for r in etat.get('results', []) if r.get('platform') == 'youtube']
    ok = etat.get('status') == 'completed' and res and res[0].get('success')
    dest = sortie if ok else os.path.join('echecs', nom)
    os.makedirs('echecs', exist_ok=True)
    json.dump(etat, open(dest, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(nom, 'OK' if ok else 'ÉCHEC', json.dumps(res, ensure_ascii=False)[:800])
    echec = echec or not ok
sys.exit(1 if echec else 0)
