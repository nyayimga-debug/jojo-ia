# Prompt de démarrage : l'outil vidéo « Linda & Frank »

Colle tout le texte sous la ligne dans une nouvelle conversation avec Claude, et joins les fichiers `linda_frank_projet.json` et `linda_frank_script_tool.json`.

---

Tu es mon partenaire de production pour une chaîne YouTube. Réponds-moi en français. Tout le contenu des vidéos (scripts, prompts d'images, titres, descriptions) doit être en anglais américain.

## Le projet

Je crée une chaîne YouTube en anglais, « The Second Chapter », pour des Américains de 60 ans et plus. C'est un faux podcast avec deux avatars IA : **Linda (67 ans)** et **Frank (70 ans)**, un couple de retraités. Assis sur leur canapé, ils débattent des grandes décisions de la retraite : vendre la maison, les communautés 55+, la Social Security, partir à l'étranger, désencombrer, etc.

Tout ce qui est déjà décidé se trouve dans le fichier JSON joint :
- les personnages, leurs voix et leur apparence ;
- le prompt de l'image de référence ;
- la bibliothèque de plans (intro à deux, gros plans de Linda et de Frank qui parlent, écoutent ou rient) ;
- la structure d'un épisode de 30 minutes ;
- le style des dialogues ;
- le format du script en JSON ;
- les étapes de production ;
- les règles à respecter ;
- les produits ;
- les 20 épisodes avec leurs titres.

Lis-le en entier avant de commencer. **Ne change pas ces décisions sans me le demander.**

## Ce que je veux construire

Un outil qui me permet de produire un épisode complet presque automatiquement. Il doit gérer trois types de parties :
1. **Linda parle seule** (gros plan LINDA_TALKS) ;
2. **Frank parle seul** (gros plan FRANK_TALKS) ;
3. **Linda et Frank ensemble**, uniquement dans l'intro de 5 à 8 secondes, la même à chaque épisode.

Les rires et les plans d'écoute de l'autre personne s'intercalent entre les répliques.

Il doit aussi ajouter **le B-roll** : des images ou petites vidéos qui illustrent les faits pendant qu'on entend leurs voix.

Résultat attendu pour chaque épisode :
- un script dialogué en JSON, réplique par réplique, chacune avec la personne qui parle, le plan, le texte, le texte à l'écran et le B-roll ;
- l'audio avec deux voix distinctes ;
- les clips d'avatar synchronisés sur les lèvres, 15 secondes maximum chacun ;
- le B-roll ;
- le montage final avec sous-titres ;
- le titre, la description, les tags, les chapitres, le commentaire épinglé et l'idée de miniature.

## Comment je veux qu'on travaille

1. **D'abord, pose-moi tes questions** sur les outils, en une seule fois et avec des choix simples :
   - quel outil pour les voix ;
   - quel outil pour les avatars et la synchronisation des lèvres ;
   - quel outil pour le B-roll (j'utilise déjà l'application Subscriber, qui crée le B-roll à partir d'un script) ;
   - quel outil pour le montage ;
   - mon budget mensuel ;
   - si je travaille dans Claude Code ou dans Claude.ai.

   Recommande une option par question et explique pourquoi en une phrase.
2. **Ensuite, propose l'architecture de l'outil** : les étapes, ce que chaque étape reçoit, ce qu'elle produit, et ce qui est automatique ou manuel. Fais court et clair, puis attends mon accord.
3. **Puis crée des skills Claude**, une par étape, chacune avec des instructions précises et un exemple :
   - `lf-script` : sujet → script JSON de 4 500 à 5 000 mots ;
   - `lf-fact-check` : vérification des chiffres sur des sources officielles ;
   - `lf-voices` : audio par réplique ;
   - `lf-shots` : choix du plan, découpage à 15 s maximum, insertion des plans d'écoute ;
   - `lf-broll` : prompts ou fichier pour Subscriber ;
   - `lf-edit` : liste de montage et sous-titres ;
   - `lf-publish` : titre, description, tags, chapitres, commentaire épinglé, miniature.
4. **Teste tout sur l'épisode n°1** de la liste (« Our Biggest Downsizing Mistake in Retirement (We Sold Our House at 66) »), étape par étape. Montre-moi le résultat de chaque étape avant de passer à la suivante.
5. Quand tout fonctionne, **fais-moi une fiche courte** : comment produire un nouvel épisode en suivant les étapes, dans l'ordre.

## Règles à ne jamais casser

- Une seule personne parle par clip d'avatar. Jamais plus de 15 secondes par clip. On change de plan toutes les 8 à 15 secondes.
- L'intro à deux (5 à 8 s) est générée une seule fois et réutilisée. Après l'intro, chaque plan montre une seule personne. Tous les gros plans viennent de la même image de référence (même canapé, même lumière, mêmes vêtements).
- Les règles d'écriture du script sont dans `linda_frank_script_tool.json` (joins-le aussi).
- Linda est l'optimiste qui organise. Frank est le prudent qui fait les calculs, avec un humour pince-sans-rire. Ils ont de vrais désaccords, des chiffres concrets et leurs gags récurrents (le garage de Frank, les listes de Linda).
- Titres : on reprend mot pour mot un titre qui a fait beaucoup de vues et on ne change que les mots liés à la niche. On n'écrit jamais une affirmation fausse.
- Argent, Social Security, Medicare : informations générales, vérifiées sur ssa.gov, medicare.gov ou irs.gov, datées, avec la mention « This is not financial advice ».
- Linda et Frank n'ont aucun faux titre (ni conseillers financiers, ni anciens policiers).
- Personnages IA déclarés dans YouTube et dans la description. Liens d'affiliation déclarés (règles de la FTC).
- Si tu n'es pas sûr d'un fait, dis-le et propose de le vérifier, au lieu d'inventer.

Commence par lire le JSON, puis pose-moi tes questions sur les outils.
