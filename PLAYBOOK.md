# Youpi karaoké : règles de production

Chaîne YouTube de comptines traditionnelles françaises en karaoké, instrumentales. Rythme : 2 vidéos par semaine, publiées en public sans relecture humaine. Ces règles remplacent donc le relecteur.

## 1. Choisir la comptine
- Traditionnelle et anonyme, ou auteur et compositeur morts depuis plus de 70 ans. En cas de doute, en prendre une autre.
- Jamais publiée : vérifier `journal.md` et `publie/`.
- Adaptée aux jeunes enfants. Écarter ce qui est violent ou cruel, ou retirer le couplet si la comptine reste entière sans lui.
- **Règle de mélodie, bloquante :** au moins deux sources indépendantes lues pendant la session doivent donner les mêmes notes et le même rythme pour chaque vers. Si elles divergent, choisir une autre comptine. Noter les liens dans `episodes/<slug>/sources.md`.
- Vérifier les paroles sur deux sources. Ne rien inventer.
- Ne jamais réutiliser un enregistrement, un arrangement moderne ou une illustration existante. Toute la musique est synthétisée par `moteur/musique.py`.

## 2. Créer l'épisode
Dossier `episodes/<slug>/` avec `episode.json`, `scenes.py`, `sources.md`. Prendre `episodes/pomme-de-reinette/` comme modèle de structure, pas comme modèle de contenu.

- `episode.json` : `bpm`, `temps_par_mesure`, et des `sections` (`nom`, `mesure`, `mesures`, `palette`, `accords`, `lignes` pour les vers chantés ou `notes` pour l'instrumental, `transpo`, `strum`, `basse`, `shaker`, `taps`, `kick`, `fin`, `instruments`). Une note de ligne vaut `[texte, temps, durée, midi]`, le temps partant du début de la section, et le texte peut commencer par une espace.
- `scenes.py` : une classe `Scenes(Base)` avec `prepare()` et une méthode `do_<nom>` par section. Enregistrer les personnages dans `PERSOS`. `apple(..., contour=fonction, tige=False)` permet d'autres silhouettes que la pomme.
- Durée visée : 60 à 120 secondes, en reprenant la comptine avec des variations.

## 3. Direction artistique, toujours la même
Papier découpé, texture de grain, ombres portées douces. Personnages ronds aux grands yeux. Titres en Lora gras italique rouge, sur carte crème. Karaoké en Poppins gras sur bandeau crème, avec la petite pomme rebondissante. Balayages de papier entre les scènes. Fin sur une carte « À bientôt ! » avec la mention « Comptine traditionnelle française · Arrangement original ».

## 4. Varier vraiment
YouTube ne monétise pas les vidéos produites en masse sur un même modèle. Chaque épisode doit avoir son propre univers lié au sens de la comptine, ses propres personnages, sa propre histoire et au moins une séquence inédite. Ne pas reprendre le décor ni le déroulé des 3 derniers épisodes. Ne jamais dessiner de personnage ou de marque existants.

## 5. Contrôler avant de publier
1. Dessiner des images clés (`EPISODE=episodes/<slug> python3 moteur/scene.py still nom:temps ...`) et les regarder : texte coupé, chevauchements, fautes de français.
2. `python3 moteur/rendre.py episodes/<slug>`. Ce script bloque si l'image, le son, la durée ou le niveau sont incorrects. **La musique doit toujours être intégrée au MP4.**
3. Extraire au moins 8 images de la vidéo finale et les regarder.
Si un contrôle échoue et ne peut pas être corrigé, ne rien publier et expliquer pourquoi.

## 6. Publier
Créer `a_publier/AAAA-MM-JJ-<slug>.json` :
`{"video":"videos/<slug>.mp4","miniature":"videos/<slug>.jpg","titre":"…","description":"…","tags":["comptine","karaoké"],"visibilite":"public","categorie":"1"}`
Le titre fait au plus 100 caractères. Commit et push sur `main` : l'action GitHub envoie la vidéo, marquée « conçue pour les enfants », et écrit le résultat dans `publie/`.

Limite gratuite : 10 envois par mois. Compter les fichiers de `publie/` du mois en cours et ne pas dépasser 10.

## 7. Journal
Ajouter à `journal.md` : date, comptine, univers, sources, résultat.
