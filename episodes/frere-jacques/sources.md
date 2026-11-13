# Sources : Frère Jacques

Toutes les pages ci-dessous ont été lues pendant la session du 13 novembre 2026.

## Domaine public
- Chanson traditionnelle française du XVIIIe siècle. Plus ancienne trace de la mélodie : manuscrit n° 300 de la Bibliothèque nationale (vers 1775-1785) ; première publication de l'air en 1811, paroles et musique ensemble à partir de 1860 environ. Parfois attribuée à Jean-Philippe Rameau (mort en 1764), sinon anonyme : domaine public dans les deux cas.
  - https://ipfs.ssi.eecc.de/ipns/en.wikipedia-on-ipfs.org/wiki/Fr%C3%A8re_Jacques (miroir de l'article Wikipédia anglais)
  - https://frenchmoments.eu/frere-jacques/
  - https://www.lieder-archiv.de/bruder_jakob-notenblatt_100145.html

## Mélodie (notes et rythme, vers par vers)
Référence en fa majeur, 4/4, noire = 1 temps (croches notées /2) :
`F G A F | F G A F | A Bb C2 | A Bb C2 | c/ d/ c/ Bb/ A F | c/ d/ c/ Bb/ A F | F C, F2 | F C, F2`

1. ABC « Frère Jaques », transcription Frank Nordberg (musicaviva.com), sur Folk Tune Finder :
   https://folktunefinder.com/tunes/143754 — en ré majeur : `DEFD|DEFD|FGA2|FGA2|A/B/A/G/FD|A/B/A/G/FD|DA,D2|DA,D2|]` (M:C, L:1/4).
2. Partition LilyPond de l'article Wikipédia anglais « Frère Jacques » (miroir https://wiki.riteme.site/wiki/Frere_Jacque), en fa majeur, 4/4 :
   `f4 g a f` ×2, `a4 bes c2` ×2, `c8 d c bes a4 f` ×2, `f4 c f2` ×2 (\relative c').

Transposées dans la même tonalité, les deux sources donnent les mêmes notes et le même rythme pour chacun des quatre vers.
Remarque : le MusicXML allemand « Bruder Jakob » du Lieder-Archiv (https://www.lieder-archiv.de/lieder/xml/100145.xml) termine les cloches par sol-do-fa au lieu de fa-do-fa. C'est l'adaptation allemande, pas la comptine française ; elle n'a pas été utilisée.

## Paroles (couplet unique, chanté trois fois)
Frère Jacques, frère Jacques,
Dormez-vous ? Dormez-vous ?
Sonnez les matines, sonnez les matines !
Ding, daing, dong. Ding, daing, dong.

Vérifiées vers par vers sur :
- https://frenchmoments.eu/frere-jacques/
- https://lyricfluent.com/lyrics/comptines_frère_jacques_english
(Seule la ponctuation varie entre les sources. Une troisième page, teteamodeler.ouest-france.fr, écrit « Dig, ding, dong » : variante non retenue.)

## Musique
Instrumental entièrement synthétisé par `moteur/musique.py` à partir de `episode.json`. Aucun enregistrement ni arrangement existant. Le canon à trois voix (séquence inédite) superpose la même mélodie décalée de deux mesures, une octave plus bas puis une octave plus haut.

## Univers
Une forêt d'automne au lever du jour. Jacques, un hérisson rond, dort en bonnet de nuit dans son hamac-feuille, au creux de sa maison-arbre. Sa petite sœur Lili (hérissonne à nœud rose et écharpe jaune) et la mésange Tiou viennent le réveiller, puis sonnent la cloche du petit clocher de bois. Séquence inédite « Chantons en canon ! » : trois cloches numérotées entrent l'une après l'autre ; Jacques, enfin réveillé, arrive en courant pour sonner la troisième. Fin : promenade du matin sous les feuilles qui tombent, tous les trois ensemble.
