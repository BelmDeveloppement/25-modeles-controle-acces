# Jeu 25 : Modèles de contrôle d'accès

© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.

Application d'interaction couplée au PowerPoint « 25 Modèles de contrôle d'accès » (v2, 211 pages, 66 Questions).
Moteur de départ : jeu 22 LAN Live (relais Cloudflare en voie principale, ntfy en secours).

## État
- Étape 0 (faite) : dépôt créé, licence « tous droits réservés ».
- Étape 1 (faite) : données structurées des 66 Questions (clé par réponse pour les 23 Questions à plusieurs réponses).
- Étape 2 (faite, à valider en séance réelle) : moteur étendu (plusieurs réponses, 1 point par réponse exacte ; Signaler, Rappel, Nouvelle partie, avatars et classement, correction détaillée en TDC).
- Étape 3 (à faire) : test final (50 questions tirées d'une banque de 600), export ZIP.

Adresse prévue : https://belmdeveloppement.github.io/25-modeles-controle-acces/

## Régénération
`python3 tools/make_data.py` (données chiffrées ; nécessite le code secret hors dépôt), puis `python3 tools/build_app.py` (joueur.html, enseignant.html, classement.html, index.html).
Le code secret de la tour de contrôle n'est jamais versé dans le dépôt.
