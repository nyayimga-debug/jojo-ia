# Reprise : analyse des chaînes avatar IA (avatarchannels.com)

## Prompt à coller dans la nouvelle session

> Réponds-moi en français. Lis d'abord `analyse_avatar_channels/REPRISE.md` dans le dépôt.
> Ensuite, va sur https://avatarchannels.com et récupère **toutes** les chaînes listées (toutes les pages, tous les filtres), avec toutes les données affichées : nom, lien, niche, abonnés, vues, revenus, date de création.
> Puis analyse ces chaînes US et trouve-moi des alternatives dans la niche **allemande** et **française** où il n'y a pas encore de concurrence, c'est-à-dire où personne n'a encore copié le concept.
> Fais une recherche très approfondie avec l'API YouTube. Mes clés sont à mettre dans la variable `YT_KEYS` (je te les donne dans le chat, ne les écris jamais dans le dépôt). Si tu manques de quota, dis-le-moi et je t'en fournis d'autres.
> Livre le résultat dans une page HTML (artifact + copie dans le dépôt), comme pour les analyses précédentes.

## Ce qui est déjà collecté (12 octobre 2026)

Les fichiers sont dans `data/`. Ils ont été produits avec les scripts de `scripts/`.

| Fichier | Contenu |
|---|---|
| `us_raw.json` | Recherche YouTube US, 25 types de personnages (médecin seniors, infirmière, grand-mère cuisine, pasteur, retraite, fermier, mécanicien, avocat, Amish, etc.). Vidéos de 4 min et plus publiées depuis le 1er mai 2026, triées par vues : 3 856 vidéos, 2 775 chaînes. Format : `{"vids": {id: {arch, q, ch, t, k (vues), al, pub}}, "ch": {id: {t, h, created, country, subs, views, nv, desc}}}` |
| `de_raw.json` | Les mêmes 24 types de personnages, recherchés en allemand (publiés depuis le 1er janvier 2026). Même format. |
| `fr_raw.json` | Les mêmes 24 types de personnages, recherchés en français (publiés depuis le 1er janvier 2026). Même format. |
| `nexlev_ai.json` | Base Nexlev, filtre « chaîne IA », triée par vues moyennes. Clés `en` (créées depuis oct. 2025), `de` et `fr` (créées depuis juin 2025). Attention : ce sont surtout des documentaires en voix off, pas des avatars qui parlent. |
| `nexlev_persona_en.json` | Base Nexlev, recherche « avatar personnage âgé qui donne des conseils aux seniors », chaînes anglaises créées depuis oct. 2025. |

## Ce qui ressort déjà (à confirmer avec la liste du site)

- Le plus gros groupe d'avatars IA US qui marche : les **« Dr. X Senior Health »**. Exemples :
  - Dr. Ares Senior : 75 k abonnés, médiane 54 k vues, environ 34 000 $/mois selon Nexlev.
  - Dr. Elias Senior Health : médiane 47 k vues.
  - Également : Dr. Atlas Senior Health, Dr. Aven Royce, Doctor Laura.
- Autres personnages US :
  - Uncle John Financial (retraite, médiane 24 k vues).
  - Old Lion Stories (histoires pour les 50 ans et plus, RPM environ 12 $).
  - The Heart Compass (psychologie pour les femmes âgées, RPM environ 12 $).
  - Stylish60plus (mode après 60 ans).
  - Senior Meal Coach.
- Déjà vérifié dans les sessions précédentes, côté français et allemand :
  - Cuisine en français : « Papy Fernand » est un avatar IA confirmé.
  - Pâtisserie en français : aucun avatar trouvé.
  - Pâtisserie en allemand : seulement Hermines Backstube (petite chaîne).
  - Mécanique en allemand : Horst, notre projet.

## Étapes restantes

1. Récupérer la liste complète de avatarchannels.com.
2. Pour chaque chaîne du site : stats sur les vidéos de 8 min et plus (médiane, P25, part des vidéos à 100 k et plus, date de création). Utiliser `scripts/stats.py`, fonction `chstats`.
3. Regrouper les chaînes par type de personnage ou niche.
4. Pour chaque niche :
   - chercher en allemand et en français des chaînes avec un personnage, créées depuis 2025, à partir de `de_raw.json` et `fr_raw.json`, complétés par de nouvelles recherches ;
   - mesurer la demande (médiane des vues sur le sujet) ;
   - classer la niche en **libre / 1 petit concurrent / occupée**.
5. Classement final des opportunités, avec les chiffres et les liens cliquables.
