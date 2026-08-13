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

## 5. Déploiement sur un VPS (ex. Hostinger) avec systemd

Ces étapes gardent le bot actif en permanence, même après un redémarrage du
serveur.

### 5.1 Connexion et dépendances

```bash
ssh root@ton_ip_vps

apt update && apt install -y python3 python3-venv python3-pip git
```

### 5.2 Récupérer le code

```bash
cd /opt
git clone https://github.com/nyayimga-debug/jojo-ia.git
cd jojo-ia
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # colle ton VRAI token (jamais dans .env.example / jamais commité)
deactivate
```

### 5.3 Créer le service systemd

```bash
nano /etc/systemd/system/jojo-bot.service
```

Colle ceci (adapte `WorkingDirectory` si tu as cloné ailleurs que `/opt/jojo-ia`) :

```ini
[Unit]
Description=Jojo ID Bot (Telegram)
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/jojo-ia
ExecStart=/opt/jojo-ia/venv/bin/python /opt/jojo-ia/bot.py
Restart=always
RestartSec=5
EnvironmentFile=/opt/jojo-ia/.env

[Install]
WantedBy=multi-user.target
```

### 5.4 Démarrer et activer au boot

```bash
systemctl daemon-reload
systemctl enable jojo-bot
systemctl start jojo-bot
```

### 5.5 Vérifier / dépanner

```bash
systemctl status jojo-bot     # état du service
journalctl -u jojo-bot -f     # logs en direct
```

### 5.6 Mettre à jour le bot plus tard

```bash
cd /opt/jojo-ia
git pull
source venv/bin/activate
pip install -r requirements.txt
deactivate
systemctl restart jojo-bot
```
