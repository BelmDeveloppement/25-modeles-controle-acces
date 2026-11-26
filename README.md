# Jeu 25 : Modèles de contrôle d'accès

© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.

Application d'interaction couplée au PowerPoint « 25 Modèles de contrôle d'accès » (v2, 211 pages, 66 Questions).
Moteur de départ : jeu 22 LAN Live (relais Cloudflare en voie principale, ntfy en secours).

## État
- Étape 0 (faite) : dépôt créé, licence « tous droits réservés ».
- Étape 1 (faite) : données structurées des 66 Questions (clé par réponse pour les 23 Questions à plusieurs réponses).
- Étape 2 (faite, à valider en séance réelle) : moteur étendu (plusieurs réponses, 1 point par réponse exacte ; Signaler, Rappel, Nouvelle partie, avatars et classement, correction détaillée en TDC).
- Étape 3 (faite, testée en local avec un relais simulé) : test final noté (règle 33) : 50 questions tirées d'une banque de 600 (12 thèmes, tirage ± 1 par thème, niveaux ≈ 20/55/25 %), ordre mélangé par étudiant, « Je ne sais pas », note /20, nom et prénom chiffrés (ECDH + AES-GCM) pour la seule TDC, export ZIP (CSV par étudiant, synthèse, classement). Banque : `data/bank/t01..t12.py` (sources ⚠ à vérifier), `tools/build_bank.py` (génère `data/bank.json`, `data/bank_enc.json`, `data/bank_sources.json`), code dans `tools/test_player.js` et `tools/test_tdc.js`. Pages PowerPoint : `TEST` ouvre le test, `TEST:c` le clôt.

Adresse prévue : https://belmdeveloppement.github.io/25-modeles-controle-acces/

## Régénération
`python3 tools/make_data.py` (données chiffrées ; nécessite le code secret hors dépôt), puis `python3 tools/build_bank.py   # banque du test (nécessite le code secret hors dépôt)
python3 tools/build_app.py` (joueur.html, enseignant.html, classement.html, index.html).
Le code secret de la tour de contrôle n'est jamais versé dans le dépôt.
