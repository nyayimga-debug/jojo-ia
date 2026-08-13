# Jojo ID Bot

Bot Telegram qui donne l'ID :

- de ton propre compte utilisateur ;
- de n'importe quel groupe ou supergroupe ;
- de n'importe quel canal, **public ou privé**.

## 1. Créer le bot sur Telegram

1. Ouvre une conversation avec [@BotFather](https://t.me/BotFather).
2. Envoie `/newbot` et suis les instructions.
3. Récupère le token fourni (ex. `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).

## 2. Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Ouvre `.env` et remplace `ton_token_ici` par le token obtenu à l'étape 1.

## 3. Lancer le bot

```bash
python bot.py
```

## 4. Utilisation

- **Ton propre ID** : envoie `/start` ou `/id` au bot en message privé.
- **ID d'un groupe/supergroupe** : ajoute le bot au groupe (simple membre suffit),
  puis envoie `/id` dans le groupe. Le bot annonce aussi l'ID automatiquement
  dès qu'il est ajouté.
- **ID d'un canal (public ou privé)** : ajoute le bot comme **administrateur**
  du canal (les bots ne peuvent lire un canal que s'ils sont admins). Le bot
  poste alors automatiquement l'ID du canal, et `/id` fonctionne aussi si un
  admin le poste dans le canal.
- **Sans ajouter le bot nulle part** : transfère (forward) n'importe quel
  message provenant du groupe/canal qui t'intéresse vers une conversation
  privée avec le bot. Il te renvoie l'ID de la source, même pour un groupe
  ou un canal privé — à condition que l'expéditeur n'ait pas masqué
  l'identité de la source de transfert (option de confidentialité Telegram).

## Notes

- Les IDs de canaux et de supergroupes commencent généralement par `-100`.
- Les IDs de groupes classiques (non "super") sont négatifs (ex. `-123456789`).
- Les IDs d'utilisateurs et de canaux/groupes "normaux" sont positifs.
