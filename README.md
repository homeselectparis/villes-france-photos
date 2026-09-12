# Villes France Photos

Bibliothèque publique de photos de villes de France, une photo par ville,
nommée par slug : `photos/{slug}.jpg`. Elle est consommable par n'importe quel
projet GitHub (ou tout autre projet) via de simples URLs publiques, sans
authentification.

Contenu :

- `photos/` : 33 photos de villes (largeur 3200 px pour les heroes), nommées
  `paris.jpg`, `lyon.jpg`, `aix-en-provence.jpg`, etc. Le nom du fichier
  identifie la ville, sans ambiguïté.
- `photos/galerie/` : deux photos secondaires par ville,
  `{slug}-1.jpg` et `{slug}-2.jpg` (1600 px), pour les galeries de pages.
- `photos/secteur/` : une photo par secteur géographique,
  `secteur-{region}.jpg` (3200 px), pour les hubs de région.
- `manifest.json` : la liste complète avec, pour chaque photo : slug, nom,
  région, fichier, dimensions, poids, source d'origine, licence et crédit.
- `index.js` : un petit helper JavaScript (sans dépendance) pour construire
  les URLs.

## Accès depuis un autre projet

Deux formes d'URL équivalentes, remplacez `{slug}` par le slug de la ville
(voir `manifest.json`) :

- Raw GitHub (toujours à jour après un push) :

```
https://raw.githubusercontent.com/homeselectparis/villes-france-photos/main/photos/{slug}.jpg
```

- CDN jsDelivr (mis en cache, recommandé pour un site web) :

```
https://cdn.jsdelivr.net/gh/homeselectparis/villes-france-photos@main/photos/{slug}.jpg
```

Exemples :

```
https://cdn.jsdelivr.net/gh/homeselectparis/villes-france-photos@main/photos/paris.jpg
https://cdn.jsdelivr.net/gh/homeselectparis/villes-france-photos@main/photos/saint-tropez.jpg
```

## Exemple de code

Avec le helper `index.js` (à copier dans votre projet) :

```js
import { photoUrl, manifestUrl, CDN_BASE, RAW_BASE } from "./index.js";

photoUrl("lyon");
// https://cdn.jsdelivr.net/gh/homeselectparis/villes-france-photos@main/photos/lyon.jpg

photoUrl("nice", { cdn: false });
// https://raw.githubusercontent.com/homeselectparis/villes-france-photos/main/photos/nice.jpg
```

Sans le helper, en listant tout dynamiquement :

```js
const manifest = await fetch(manifestUrl()).then((r) => r.json());

for (const ville of manifest.villes) {
  console.log(ville.nom, ville.region, photoUrl(ville.slug));
}
```

## Ajouter une ville

1. Déposez la photo dans `photos/` au format `{slug}.jpg` (slug ASCII, sans
   accents : `aix-en-provence`, `saint-cyr-sur-mer`). Largeur 1600 px
   recommandée, poids cible sous 1 Mo.
2. Ajoutez l'entrée correspondante dans `manifest.json` (slug, nom, région,
   dimensions, source, licence, crédit).
3. Commitez et poussez sur `main` : les URLs raw sont immédiatement
   disponibles, le CDN jsDelivr se rafraîchit en quelques minutes.

## Licences et crédits

- Les photos ajoutées ou remplacées le 12/09/2026 (heroes de villes, galeries,
  secteurs) proviennent d'un abonnement **Adobe Stock** du groupe Home Select,
  sous **licence standard** : usage commercial sans attribution obligatoire.
  L'identifiant Adobe de chaque photo est conservé dans le champ `credit` du
  manifeste (forme `Adobe Stock #id`), preuve de licence et traçabilité.
- Les photos Pexels antérieures restantes sont soumises à la
  [Pexels License](https://www.pexels.com/license/) : utilisation libre,
  commerciale incluse, sans attribution obligatoire. La page d'origine de
  chaque photo est conservée dans le champ `credit` du manifeste.
- `sanary-sur-mer.jpg` provient de Wikimedia Commons, auteur Tobi 87, licence
  [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) : attribution
  de l'auteur requise, republication de la photo sous la même licence.
- `paris.jpg` est un fichier interne du projet French Realty.

La liste exacte, photo par photo, avec source et licence, fait foi dans
`manifest.json`.
