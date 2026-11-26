# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.
# Sous-réponses des 23 Questions à plusieurs réponses du cours 25 (jeu 25).
# Format : I(énoncé, bonne réponse, [3 distracteurs], explication). La bonne réponse est écrite en premier ;
# l'ordre d'affichage est tiré au build (équilibré, voir build_questions.py).
def I(t, ok, bad, ex): return {'txt': t, 'opts': [ok] + list(bad), 'ex': ex}

PRM = 'PERMIS'
MULTI = {
# ---------- BLP ----------
7: [
 I('Léa lit le planning des tournées.', PRM, ['REFUSÉ, règle NRU (lecture vers le haut)', 'REFUSÉ, règle NWD (écriture vers le bas)', 'REFUSÉ, aucune règle BLP mais le propriétaire doit valider'], 'Léa : Interne (1) ; planning : Interne (1). Lecture : 1 ≥ 1, vrai.'),
 I('Léa lit les contrats clients.', 'REFUSÉ, règle NRU (lecture vers le haut)', [PRM, 'REFUSÉ, règle NWD (écriture vers le bas)', 'PERMIS, car Léa est salariée'], 'Contrats : niveau 2. Lecture : 1 ≥ 2, faux. NRU.'),
 I('Marc lit le planning des tournées.', PRM, ['REFUSÉ, règle NRU (lecture vers le haut)', 'REFUSÉ, règle NWD (écriture vers le bas)', 'REFUSÉ, il doit d’abord demander au propriétaire'], 'Marc : Confidentiel (2) ; planning : 1. Lecture : 2 ≥ 1, vrai (lecture vers le bas).'),
 I('Marc écrit dans le planning des tournées.', 'REFUSÉ, règle NWD (écriture vers le bas)', [PRM, 'REFUSÉ, règle NRU (lecture vers le haut)', 'PERMIS, car il est gestionnaire'], 'Écriture : niveau objet (1) ≥ niveau sujet (2) ? Faux. NWD : Marc pourrait y recopier du Confidentiel.'),
 I('Léa écrit un compte rendu dans le plan stratégique.', PRM, ['REFUSÉ, règle NRU (lecture vers le haut)', 'REFUSÉ, règle NWD (écriture vers le bas)', 'REFUSÉ, car le plan est Secret'], 'Léa : 1 ; plan : 3. Écriture : 3 ≥ 1, vrai. Surprenant, mais c’est une limite de BLP : l’intégrité n’est pas protégée.'),
 I('La directrice écrit dans la plaquette commerciale.', 'REFUSÉ, règle NWD (écriture vers le bas)', [PRM, 'REFUSÉ, règle NRU (lecture vers le haut)', 'PERMIS, car elle est au plus haut niveau'], 'Directrice : 3 ; plaquette : 0. Écriture : 0 ≥ 3, faux. NWD : elle pourrait publier du Secret par erreur.'),
],
# ---------- Biba ----------
12: [
 I('Sonia (Haute) lit les relevés des tablettes (Basse).', 'REFUSÉ, no read down', [PRM, 'REFUSÉ, no write up', 'REFUSÉ, niveau de confidentialité insuffisant'], 'Lecture : intégrité de l’objet (Basse) ≥ celle du sujet (Haute) ? Faux. No read down.'),
 I('Marc (Moyenne) écrit dans le grand livre (Haute).', 'REFUSÉ, no write up', [PRM, 'REFUSÉ, no read down', 'PERMIS, car Marc est gestionnaire'], 'Écriture : intégrité de l’objet (Haute) ≤ celle du sujet (Moyenne) ? Faux. No write up.'),
 I('Sonia (Haute) lit le grand livre (Haute).', PRM, ['REFUSÉ, no read down', 'REFUSÉ, no write up', 'REFUSÉ, sauf accord du propriétaire'], 'Haute ≥ Haute : vrai.'),
 I('Un conducteur (Basse) lit le grand livre (Haute).', PRM, ['REFUSÉ, no read down', 'REFUSÉ, no write up', 'REFUSÉ, car le grand livre est confidentiel'], 'Haute ≥ Basse : vrai. Lecture vers le haut : il lit du fiable.'),
 I('Marc (Moyenne) lit un fichier téléchargé sur le Web (Basse).', 'REFUSÉ, no read down', [PRM, 'REFUSÉ, no write up', 'PERMIS après un antivirus'], 'Basse ≥ Moyenne ? Faux. No read down : le fichier pourrait polluer les saisies.'),
 I('Un conducteur (Basse) écrit dans les saisies des gestionnaires (Moyenne).', 'REFUSÉ, no write up', [PRM, 'REFUSÉ, no read down', 'PERMIS, car il est salarié'], 'Écriture : Moyenne ≤ Basse ? Faux. No write up.'),
],
# ---------- Clark-Wilson ----------
13: [
 I('Combien de triplets (utilisateur, TP, CDI) sont autorisés par les droits décrits ?', '4', ['3', '6', '9'], '(Léa, TP1, Livraisons) ; (Sonia, TP2, Factures) ; (Marc, TP1, Livraisons) ; (Marc, TP3, Tarifs).'),
 I('Léa modifie directement la table Factures avec un outil de base de données : autorisé ou refusé ?', 'REFUSÉ : aucun triplet ne l’autorise et une modification directe contourne les TP', ['AUTORISÉ : Léa est utilisatrice du TMS', 'AUTORISÉ si l’IVP est vérifié le soir', 'REFUSÉ : Léa n’est pas propriétaire de la table'], 'Dans Clark-Wilson, un CDI ne se modifie que par une procédure de transformation (TP).'),
 I('Marc lance TP2 « émettre une facture » : autorisé ou refusé ?', 'REFUSÉ : le triplet (Marc, TP2, Factures) n’existe pas', ['AUTORISÉ : Marc est gestionnaire', 'AUTORISÉ : TP2 est une procédure certifiée', 'REFUSÉ : TP2 est réservée aux administrateurs'], 'Marc émet des tarifs, pas des factures : séparation des tâches implicite.'),
 I('À quoi sert l’IVP en fin de journée ?', 'À recalculer le total des factures et à alerter si l’écart avec le total comptable n’est pas nul', ['À sauvegarder la table Factures', 'À vérifier le mot de passe de chaque utilisateur', 'À supprimer les saisies des tablettes déjà traitées'], 'Vérification d’intégrité : si l’écart n’est pas nul (par exemple une facture de 4 200 € absente du total comptable), alerte.'),
],
# ---------- ACL (risque, contrôle) ----------
16: [
 I('Quel est le risque principal quand chaque gestionnaire modifie librement les ACL ?', 'Les droits s’accumulent sans que personne ne les valide', ['Le serveur sature', 'Les noms de fichiers deviennent trop longs', 'Les sauvegardes échouent'], 'Dérive des privilèges : propagation, faible traçabilité, erreur humaine, fuite par copie.'),
 I('Quel contrôle est applicable dès demain par deux informaticiens ?', 'Journaliser les changements d’ACL et alerter à l’ajout d’un compte externe', ['Interdire tout partage', 'Racheter un serveur', 'Former chacun pendant un an'], 'Le journal et l’alerte se mettent en place en quelques heures. Interdire tout partage bloque l’activité.'),
 I('Combien d’autorisations ont été créées sans aucune validation ? (15 gestionnaires, 8 dossiers chacun, 3 personnes par dossier)', '360', ['120', '26', '45'], '15 × 8 = 120 dossiers ; 120 × 3 = 360 autorisations. 120 oublie le facteur 3 ; 26 additionne ; 45 oublie le nombre de dossiers.'),
 I('Quel contrôle mettez-vous en place en premier ?', 'Le journal et l’alerte, car rapides et sans gêne', ['La revue trimestrielle seule', 'Le ticket obligatoire seul', 'La suppression des ACL'], 'Rapides, sans gêne, et ils révèlent l’ampleur réelle avant d’imposer le ticket ou la revue.'),
],
# ---------- RBAC : matrice et calculs ----------
20: [
 I('Combien de croix compte la matrice rôles × permissions attendue (moindre privilège), sur 32 cases ?', '14', ['8', '20', '32'], 'Conducteur 2, Gestionnaire 4, Comptable 3, Responsable 5 : 14 croix sur 32 cases.'),
 I('Sans rôles, combien de cases à gérer (120 utilisateurs × 8 permissions) ?', '960', ['128', '480', '152'], '120 × 8 = 960.'),
 I('Avec rôles, combien d’éléments (4 × 8 cases + 120 affectations) ?', '152', ['960', '128', '32'], '4 × 8 + 120 = 152, soit environ 15,8 % de 960 : réduction de 84 %.'),
 I('Léa passe conductrice → gestionnaire : combien d’opérations avec rôles ?', '1 : changer son affectation de rôle', ['8 : une par permission', '4 : une par rôle', '960 : tout recalculer'], 'Avec rôles : 1 opération, contre jusqu’à 8 cases sans rôles.'),
],
# ---------- SoD ----------
21: [
 I('Quel principe la situation (Sonia crée le fournisseur, change le RIB et valide le paiement) viole-t-elle ?', 'La séparation des tâches', ['Le moindre privilège seul', 'La disponibilité', 'La non-répudiation'], 'Une seule personne initie et exécute : aucun regard extérieur.'),
 I('Quelle règle de séparation des tâches est la plus précise ?', 'Les rôles « Gestion des fournisseurs » et « Validation des paiements » sont incompatibles pour une même personne', ['Les comptables doivent être prudents', 'Sonia doit refuser les faux courriels', 'Tout paiement doit être signalé à la direction'], 'Règle des quatre yeux : tout changement de RIB est approuvé par une autre personne.'),
 I('Quel contrôle compensatoire convient à une petite équipe (2 informaticiens, pas de RSSI) ?', 'Un rappel téléphonique au numéro connu du fournisseur avant tout paiement vers un RIB modifié', ['Un antivirus plus récent', 'Un mot de passe plus long pour Sonia', 'Un pare-feu supplémentaire'], 'Rappel au numéro connu, journalisation des changements de RIB, revue hebdomadaire par la direction.'),
 I('Quel poids représente la fraude (18 400 €) dans la marge annuelle de 280 000 € ?', 'Environ 6,6 %', ['Environ 66 %', 'Environ 0,66 %', 'Environ 15 %'], '18 400 / 280 000 ≈ 6,6 %. Seuil de 10 % : 28 000 € ; deux fraudes identiques (36 800 €) le dépassent.'),
],
# ---------- Hiérarchie ----------
22: [
 I('Combien de permissions effectives pour le Responsable d’exploitation (propres + héritées) ?', '6', ['2', '4', '8'], 'Responsable : 2 propres + 4 héritées (Gestionnaire 4 : 2 propres + 2 de Conducteur) = 6.'),
 I('Combien de liens permission → rôle sans hiérarchie (tout recopié) ?', '12', ['6', '8', '4'], '2 + 4 + 6 = 12 liens.'),
 I('Combien de liens avec hiérarchie (propres + liens d’héritage) ?', '8', ['12', '6', '10'], '6 propres + 2 liens d’héritage = 8 : gain de 4 sur 12, soit 33 %.'),
 I('Un rôle par fonction et par agence (3 fonctions × 3 agences), puis « jour » et « nuit » : combien de rôles ?', '18', ['9', '6', '12'], '3 × 3 = 9 rôles ; × 2 = 18. C’est l’explosion de rôles.'),
 I('Que proposez-vous pour éviter cette explosion ?', '3 rôles de base, l’agence et l’horaire portés par des attributs évalués à la demande', ['Un rôle par personne', 'Supprimer la hiérarchie', 'Un rôle par agence, jour et nuit'], 'On combine RBAC et ABAC : Gestionnaire + condition « même agence » + condition « heure ouvrée ».'),
],
# ---------- MAC ----------
28: [
 I('Marc (Confidentiel, {Exploitation}) lit Planning tournées (Interne, {Exploitation}).', PRM, ['REFUSÉ : niveau insuffisant', 'REFUSÉ : compartiment manquant', 'REFUSÉ : niveau et compartiment insuffisants'], 'Confidentiel ≥ Interne et {Exploitation} ⊆ {Exploitation}.'),
 I('Léa (Interne, {Exploitation}) lit Tarifs clients (Confidentiel, {Exploitation}).', 'REFUSÉ : niveau insuffisant', [PRM, 'REFUSÉ : compartiment manquant', 'REFUSÉ : niveau et compartiment insuffisants'], 'Interne < Confidentiel : niveau insuffisant (le compartiment est correct).'),
 I('Sonia (Confidentiel, {Finance}) lit Bilan (Confidentiel, {Finance}).', PRM, ['REFUSÉ : niveau insuffisant', 'REFUSÉ : compartiment manquant', 'REFUSÉ : niveau et compartiment insuffisants'], 'Confidentiel ≥ Confidentiel et {Finance} ⊆ {Finance}.'),
 I('Marc (Confidentiel, {Exploitation}) lit Bilan (Confidentiel, {Finance}).', 'REFUSÉ : compartiment manquant', [PRM, 'REFUSÉ : niveau insuffisant', 'REFUSÉ : niveau et compartiment insuffisants'], 'Niveau suffisant, mais {Finance} ⊄ {Exploitation} : besoin d’en connaître absent.'),
 I('La directrice (Secret, {RH, Finance, Exploitation}) lit Tarifs clients (Confidentiel, {Exploitation}).', PRM, ['REFUSÉ : niveau insuffisant', 'REFUSÉ : compartiment manquant', 'REFUSÉ : niveau et compartiment insuffisants'], 'Secret ≥ Confidentiel et {Exploitation} ⊆ {RH, Finance, Exploitation}.'),
 I('Léa (Interne, {Exploitation}) lit Procédures chauffeurs (Public, {}).', PRM, ['REFUSÉ : niveau insuffisant', 'REFUSÉ : compartiment manquant', 'REFUSÉ : niveau et compartiment insuffisants'], 'Interne ≥ Public, et l’ensemble vide est inclus dans tout ensemble.'),
],
# ---------- ABAC : évaluer ----------
31: [
 I('Requête 1 : Marc, gestionnaire, PC géré, 10 h, dossier Confidentiel.', PRM, ['REFUSÉ : rôle', 'REFUSÉ : appareil', 'REFUSÉ : heure'], 'Rôle ✓ ; appareil géré ✓ ; 10 h dans 7 h – 20 h ✓ ; Confidentiel ≤ Confidentiel ✓.'),
 I('Requête 2 : Marc, gestionnaire, PC personnel, 10 h, dossier Confidentiel.', 'REFUSÉ : appareil', [PRM, 'REFUSÉ : rôle', 'REFUSÉ : heure'], 'Appareil personnel : la condition « géré » n’est pas remplie.'),
 I('Requête 3 : Marc, gestionnaire, PC géré, 23 h, dossier Confidentiel.', 'REFUSÉ : heure', [PRM, 'REFUSÉ : rôle', 'REFUSÉ : appareil'], '23 h est hors de la plage 7 h – 20 h.'),
 I('Requête 4 : Karim, intérimaire, PC géré, 10 h, dossier Interne.', 'REFUSÉ : rôle', [PRM, 'REFUSÉ : appareil', 'REFUSÉ : heure'], 'Karim n’est pas gestionnaire : la condition de rôle n’est pas remplie.'),
 I('Pourquoi cette politique est-elle difficile à exprimer en RBAC seul ?', 'L’appareil et l’heure sont des attributs de contexte, qu’un rôle ne porte pas', ['Il faudrait moins de rôles que d’utilisateurs', 'Le RBAC interdit les conditions de classification', 'Le RBAC ne gère pas les gestionnaires'], 'Sans attributs, il faudrait un rôle par combinaison (gestionnaire géré de jour, etc.) : explosion de rôles.'),
],
# ---------- ABAC : écrire ----------
34: [
 I('Quel élément de la règle « fiches de paie » est un attribut d’ENVIRONNEMENT ?', 'L’appareil = géré', ['Le service = RH', 'Le type = fiche de paie', 'L’agence du salarié concerné'], 'L’appareil est une condition de contexte, comme le jour et l’heure.'),
 I('Quelle politique traduit correctement la règle ?', 'PERMIS SI service = RH ET type = fiche de paie ET agence du sujet = agence de la ressource ET appareil = géré ET jour ouvré ET heure entre 8 h et 18 h', ['PERMIS SI service = RH OU appareil = géré OU jour ouvré', 'PERMIS SI service = RH ET appareil = géré', 'PERMIS SI type = fiche de paie ET heure entre 8 h et 18 h'], 'Elle contient toutes les conditions reliées par ET. Un OU laisserait passer l’accès dès qu’une seule est vraie.'),
 I('(a) Paul, RH Nancy, poste géré, mardi 10 h, fiche d’un salarié de Nancy : décision ?', PRM, ['REFUSÉ : agence différente', 'REFUSÉ : appareil non géré ou jour non ouvré', 'REFUSÉ : service non RH'], 'Toutes les conditions sont vraies.'),
 I('(b) Paul, RH Nancy, poste géré, mardi 10 h, fiche d’un salarié de Metz : décision ?', 'REFUSÉ : agence différente', [PRM, 'REFUSÉ : appareil non géré ou jour non ouvré', 'REFUSÉ : service non RH'], 'L’agence du sujet est différente de celle de la ressource.'),
 I('(c) Paul, RH Nancy, PC personnel, samedi 9 h, fiche d’un salarié de Nancy : décision ?', 'REFUSÉ : appareil non géré ou jour non ouvré', [PRM, 'REFUSÉ : agence différente', 'REFUSÉ : service non RH'], 'Deux conditions sont fausses : appareil non géré ET jour non ouvré.'),
 I('Quel attribut est le plus fragile ?', '« Appareil géré », qui dépend d’un inventaire à jour', ['Le jour de la semaine', 'Le type de document', 'L’heure du serveur'], 'Un attribut mal renseigné ou falsifié ouvre ou bloque l’accès : la source d’attributs (PIP) est critique.'),
],
# ---------- OrBAC ----------
38: [
 I('Quelle formule traduit la règle 1 (gestionnaire de Metz, heures ouvrées) ?', 'Permission(Metz, Gestionnaire, Modifier, Tournées, HeuresOuvrées)', ['Obligation(Metz, Gestionnaire, Modifier, Tournées, HeuresOuvrées)', 'Permission(TransLor, Comptable, Modifier, Tournées, HeuresOuvrées)', 'Interdiction(Metz, Gestionnaire, Modifier, Tournées, HeuresOuvrées)'], 'Permission accordée dans l’organisation Metz au rôle Gestionnaire.'),
 I('Quelle formule traduit la règle 2 (un comptable ne modifie jamais une tournée) ?', 'Interdiction(TransLor, Comptable, Modifier, Tournées, Toujours)', ['Permission(TransLor, Comptable, Modifier, Tournées, Toujours)', 'Obligation(TransLor, Comptable, Modifier, Tournées, Toujours)', 'Interdiction(Metz, Gestionnaire, Modifier, Tournées, Toujours)'], 'Interdiction pour le rôle Comptable, en tout temps.'),
 I('Quelle formule traduit la règle 3 (en urgence, le responsable doit être prévenu) ?', 'Obligation(TransLor, ResponsableExploitation, Être prévenu, Modifications de tournées, Urgence)', ['Permission(TransLor, ResponsableExploitation, Être prévenu, Modifications de tournées, Urgence)', 'Interdiction(TransLor, ResponsableExploitation, Modifier, Tournées, Urgence)', 'Obligation(TransLor, Gestionnaire, Modifier, Tournées, Toujours)'], 'Une obligation : le responsable doit être prévenu.'),
 I('Dans la règle 1, quel élément est le contexte ?', 'HeuresOuvrées', ['Gestionnaire', 'Modifier', 'Tournées'], 'HeuresOuvrées est évalué au moment de la requête. Gestionnaire est un rôle, Modifier une activité, Tournées une vue.'),
 I('Marc, gestionnaire à Metz, veut modifier la tournée T-1042 à 22 h un mardi : décision ?', 'REFUSÉ, car le contexte HeuresOuvrées est faux', ['PERMIS, car il est gestionnaire', 'PERMIS, car la tournée existe', 'REFUSÉ, car il est à Metz'], 'À 22 h le contexte est faux : la règle de permission ne s’applique pas.'),
],
# ---------- Choisir le modèle ----------
40: [
 I('Besoin A (partage Exploitation entre 15 gestionnaires) : quel modèle principal ?', 'DAC encadré', ['RBAC', 'MAC Bell-LaPadula', 'ABAC'], 'Équipe restreinte, souplesse utile, délégations contrôlées et revues d’ACL. RBAC serait lourd pour 15 personnes.'),
 I('Besoin B (droits du TMS pour 120 salariés) : quel modèle principal ?', 'RBAC', ['DAC', 'ABAC', 'MAC'], '120 utilisateurs, fonctions stables : administration centralisée et audit. Le DAC dériverait.'),
 I('Besoin C (fichiers de paie, poste géré, heures ouvrées) : quel modèle principal ?', 'ABAC', ['DAC', 'RBAC seul', 'MAC Bell-LaPadula'], 'La décision dépend de l’appareil et de l’heure : attributs de contexte. En pratique : RBAC pour l’accès de base, ABAC pour le contexte.'),
 I('Besoin D (archives juridiques, aucune fuite vers un niveau inférieur) : quel modèle principal ?', 'MAC avec Bell-LaPadula', ['DAC', 'RBAC', 'ABAC'], 'Étanchéité par étiquettes, interdiction d’écrire vers le bas : le seul besoin où la confidentialité absolue prime.'),
 I('Quel est le risque résiduel du besoin C ?', 'Un appareil « géré » en réalité compromis ou mal inventorié ouvre l’accès', ['L’heure du serveur est trop précise', 'Le fichier de paie est trop volumineux', 'Les rôles sont trop nombreux'], 'Un attribut falsifié ou mal inventorié ouvre l’accès : la fiabilité de la source d’attributs (PIP) est critique.'),
],
# ---------- ACL vs capabilities ----------
42: [
 I('Matrice : Marc (Tarifs R, Factures R, Script RX), Sonia (Tarifs R, Factures RW, Script aucun), Léa (Tarifs aucun, Factures aucun, Script X). Quelle est l’ACL de l’objet Factures ?', 'Marc : R ; Sonia : RW ; Léa : aucun droit', ['Marc : RW ; Sonia : R ; Léa : aucun droit', 'Marc : R ; Sonia : RW ; Léa : X', 'Marc : RX ; Sonia : RW ; Léa : aucun droit'], 'L’ACL est la colonne de l’objet : qui a quel droit sur lui.'),
 I('Quelle est la liste de capabilities de Marc ?', 'Tarifs : R ; Factures : R ; Script : RX', ['Tarifs : R ; Factures : RW ; Script : RX', 'Tarifs : R ; Factures : R ; Script : X', 'Tarifs : aucun ; Factures : R ; Script : RX'], 'Les capabilities sont la ligne du sujet : ce qu’il peut faire sur chaque objet.'),
 I('Quelle lecture est la plus pratique pour « qui peut modifier Factures ? » et pour « que peut faire Marc ? »', 'L’ACL pour la première, les capabilities pour la seconde', ['Les capabilities pour la première, l’ACL pour la seconde', 'L’ACL pour les deux', 'Les capabilities pour les deux'], '« Qui peut modifier Factures ? » : on lit l’ACL (Sonia). « Que peut faire Marc ? » : on lit sa liste.'),
],
# ---------- Retour sur la fraude ----------
44: [
 I('Qu’est-ce qui a failli côté DAC ?', 'Le propriétaire du partage a élargi les droits sans contrôle', ['Le serveur était trop ancien', 'Le RIB était trop long', 'La règle d’héritage était absente'], 'Le propriétaire du partage a élargi les droits sans contrôle.'),
 I('Qu’est-ce qui a failli côté RBAC ?', 'Le rôle Comptable cumulait gestion des fournisseurs et validation des paiements', ['Le nombre de rôles était trop faible', 'Aucun lien utilisateur–rôle n’existait', 'La hiérarchie des rôles était trop courte'], 'Le rôle Comptable était trop large et ne séparait pas gestion des fournisseurs et validation.'),
 I('Quel correctif ABAC est le plus pertinent ?', 'Refuser « valider un paiement » si l’âge du RIB est inférieur à 48 h et le montant au-dessus d’un seuil, sauf double validation', ['Bloquer tout paiement', 'Ajouter un rôle', 'Interdire les ACL'], 'La règle sur l’âge du RIB ajoute un attribut de contexte : elle bloque sans empêcher les paiements légitimes.'),
 I('Quelle perte aurait été évitée ?', '18 400 €', ['280 000 €', '6,6 % de 18 400 €', '0 €'], '280 000 € est la marge totale ; la perte évitée est de 18 400 €.'),
 I('Cette perte représente quel pourcentage de la marge annuelle (280 k€) ?', '6,6 %', ['66 %', '0,66 %', '15 %'], '18 400 / 280 000 ≈ 6,6 %. 66 % et 0,66 % décalent la virgule.'),
],
# ---------- Cycle de vie ----------
45: [
 I('Arrivée de Nadia (comptable) : quelle séquence est correcte ?', 'Créer un compte nominatif, affecter le rôle Comptable, faire valider par le manager, activer, informer', ['Copier le compte de Sonia', 'Donner un accès administrateur « le temps de voir »', 'Créer un compte partagé avec le service'], 'Compte nominatif ; rôle selon la fiche de poste ; validation du manager ; activation ; information sur les règles.'),
 I('Mutation de Léa (conductrice → gestionnaire) : quelle séquence est correcte ?', 'Retirer le rôle Conducteur, ajouter le rôle Gestionnaire, faire valider et journaliser', ['Ajouter le rôle Gestionnaire et garder Conducteur', 'Créer un second compte pour Gestionnaire', 'Ne rien changer jusqu’à la revue annuelle'], 'Sans retrait, Léa cumule des droits (accumulation de privilèges).'),
 I('Départ de Karim (intérimaire) : quelle séquence est correcte ?', 'Désactiver le compte le dernier jour, récupérer le matériel, retirer les rôles, archiver puis supprimer après la durée de conservation', ['Attendre la fin du mois', 'Changer son mot de passe seulement', 'Supprimer immédiatement toutes ses données'], 'Un compte non désactivé devient un compte orphelin.'),
 I('Quelle part des comptes actifs (120 + 12 = 132) est orpheline ?', '9,1 %', ['10 %', '12 %', '0,1 %'], '12 / 132 ≈ 9,1 %.'),
 I('Quel indicateur de suivi mensuel est le plus pertinent ?', 'Comptes actifs d’anciens salariés au dernier jour du mois (cible 0)', ['Nombre de connexions', 'Nombre de rôles créés', 'Nombre de courriels envoyés'], 'Il mesure directement le risque ; les autres mesurent de l’activité.'),
],
# ---------- Audit ----------
47: [
 I('Ligne 1 (Karim, parti il y a 2 mois, compte actif, rôle Conducteur) : verdict ?', 'Anomalie : compte orphelin, cycle de vie non respecté', ['Conforme', 'Anomalie : compte partagé', 'Anomalie : accès trop large'], 'Désactiver le compte.'),
 I('Ligne 2 (Sonia : rôles Comptable et Responsable d’exploitation) : verdict ?', 'Anomalie : cumul de rôles incompatibles, séparation des tâches violée', ['Conforme', 'Anomalie : compte orphelin', 'Anomalie : héritage de rôle'], 'Violation de la séparation des tâches et du moindre privilège. Séparer les rôles.'),
 I('Ligne 3 (admin_tms partagé par 3 informaticiens, mot de passe commun) : verdict ?', 'Anomalie : compte partagé, perte d’imputabilité', ['Conforme', 'Anomalie : cumul de rôles', 'Anomalie : compte orphelin'], 'Comptes nominatifs nécessaires.'),
 I('Ligne 4 (dossier « RH » lisible par « Tout le monde ») : verdict ?', 'Anomalie : sur-exposition de données RH, à restreindre au rôle RH', ['Conforme', 'Anomalie : compte orphelin', 'Anomalie : compte partagé'], 'Restreindre au rôle RH.'),
 I('Ligne 5 (Marc, gestionnaire, accède aux tarifs, nécessaire à son travail) : verdict ?', 'Conforme : accès justifié par la fonction', ['Anomalie : trop de droits', 'Anomalie : compte partagé', 'Anomalie : compte orphelin'], 'Le droit correspond à la fonction : pas d’anomalie.'),
],
# ---------- Fiche de synthèse ----------
49: [
 I('Quel modèle principal pour les droits courants d’une PME de 40 personnes ?', 'RBAC avec peu de rôles stables', ['MAC à niveaux', 'Un rôle pour chaque salarié', 'DAC pur'], 'Fonctions stables, administration centralisée. Un rôle par salarié revient à de la gestion individuelle.'),
 I('Quel modèle complémentaire pour la paie et les paiements ?', 'ABAC (appareil, heure, âge du RIB)', ['Bell-LaPadula', 'OrBAC', 'Biba'], 'ABAC pour les décisions dépendant du contexte. Bell-LaPadula et Biba sont des modèles de niveaux ; OrBAC est un modèle de recherche.'),
 I('Quelle mesure prioriser en premier ?', 'Désactiver les comptes d’anciens salariés et fixer un processus de départ', ['Installer un moteur de politiques ABAC', 'Rédiger 50 rôles', 'Chiffrer tous les postes'], 'Gain immédiat, coût faible.'),
 I('Quel indicateur de suivi est le plus pertinent ?', 'Nombre de comptes actifs d’anciens salariés (cible 0)', ['Nombre de rôles créés', 'Nombre de partages', 'Durée des réunions'], 'Mesurable et lié au risque.'),
],
# ---------- Unix ----------
51: [
 I('tarifs.csv (‑rw‑r‑‑‑‑‑, propriétaire marc, groupe exploit) : que peut faire Léa (groupe exploit) ?', 'Lire seulement', ['Lire et écrire', 'Lire et exécuter', 'Rien'], 'Propriétaire (Marc) : lire et écrire. Groupe (Léa) : lire. Autres (Karim) : rien.'),
 I('Quelle ligne est une anomalie ?', 'salaires.xlsx (‑rw‑rw‑rw‑) : tout le monde peut lire et modifier', ['tarifs.csv (‑rw‑r‑‑‑‑‑)', 'factures/ (drwxrwx‑‑‑)', 'sauvegarde.sh (‑rwxr‑xr‑x)'], 'Tout le monde peut lire et modifier : atteinte à la confidentialité et à l’intégrité. Principe violé : moindre privilège.'),
 I('Quelle est la valeur octale de tarifs.csv (rw‑r‑‑‑‑‑) ?', '640', ['644', '600', '750'], 'rw- = 6 ; r-- = 4 ; --- = 0 : 640.'),
 I('Quelle est la valeur octale de factures/ (rwxrwx‑‑‑) ?', '770', ['760', '777', '750'], 'rwx = 7 ; rwx = 7 ; --- = 0 : 770.'),
 I('Quelle valeur corrigée proposez-vous pour salaires.xlsx (666) ?', '660 ou 640, accès limité à la RH', ['777', '644', '666 avec un mot de passe'], 'Lecture et écriture réservées au propriétaire et au groupe RH (660), ou lecture seule du groupe (640).'),
 I('Pourquoi ce système est-il un DAC ?', 'Le propriétaire de chaque fichier fixe lui-même ses droits (chmod)', ['Un administrateur central fixe tous les droits', 'Les droits dépendent de l’heure et de l’appareil', 'Les droits dépendent d’étiquettes de sécurité'], 'Discrétionnaire : le propriétaire décide.'),
],
# ---------- AGDLP ----------
53: [
 I('Quelle chaîne AGDLP est correcte pour le partage Factures ?', 'Comptes → GG_Compta → DL_Factures_Modif → Modifier sur Factures', ['Comptes → DL_Factures_Modif → GG_Compta → Modifier sur Factures', 'Comptes → Modifier sur Factures → GG_Compta', 'GG_Compta → comptes → DL_Factures_Modif → Modifier'], 'A : comptes ; G : GG_Compta ; DL : DL_Factures_Modif ; P : Modifier.'),
 I('Combien de groupes faut-il au total pour les quatre partages ?', '7 : 3 globaux et 4 locaux', ['4', '12', '24'], 'Globaux : 3 (GG_Compta, GG_RH, GG_Exploitation) ; locaux : 4 (un par partage et par niveau de droit).'),
 I('Combien d’imbrications (groupe global dans groupe local) ?', '6', ['3', '9', '12'], '3 globaux dans leur partage de modification + 3 dans DL_Procedures_Lecture : 6.'),
 I('Un nouveau comptable arrive : combien d’opérations avec AGDLP ?', '1', ['2', '4', '8'], 'Avec AGDLP : ajouter le compte à GG_Compta. Sans AGDLP : 2 opérations (Factures et Procédures), et chaque nouveau partage en ajoute une.'),
],
# ---------- ISO 27001 ----------
56: [
 I('Revue annuelle des droits par les managers : quelle mesure ISO/IEC 27001:2022 ?', '5.18', ['5.15', '8.3', '5.3'], 'Mesure 5.18 (droits d’accès). Preuve : comptes rendus de revue signés, liste des retraits.'),
 I('Comptes administrateurs nominatifs et limités : quelle mesure ?', '8.2', ['5.3', '5.18', '8.3'], 'Mesure 8.2 (droits d’accès privilégiés). Preuve : liste des comptes à privilèges et de leurs titulaires.'),
 I('Règle « initier ≠ valider » pour les paiements : quelle mesure ?', '5.3', ['8.2', '5.15', '8.3'], 'Mesure 5.3 (séparation des tâches). Preuve : matrice de rôles incompatibles, journal des validations.'),
 I('Politique de contrôle d’accès rédigée et approuvée : quelle mesure ?', '5.15', ['5.18', '8.2', '5.3'], 'Mesure 5.15 (contrôle d’accès). Preuve : document daté, approuvé et diffusé.'),
 I('Restriction du dossier RH au seul rôle RH : quelle mesure ?', '8.3', ['5.3', '5.18', '8.2'], 'Mesure 8.3 (restriction d’accès à l’information). Preuve : ACL du dossier, revue.'),
],
# ---------- PAM ----------
58: [
 I('Quel est le principal problème du compte partagé « admin_tms » ?', 'La perte d’imputabilité : on ne sait pas qui a fait quoi', ['Le mot de passe est trop court', 'Le compte coûte une licence', 'Il est lent'], 'Plusieurs personnes (et d’anciens) connaissent le mot de passe : impossible de savoir qui a agi.'),
 I('Quelle mesure PAM convient à une équipe de 2 personnes ?', 'Des comptes nominatifs avec droits élevés à la demande, justifiés et limités dans le temps', ['Un deuxième compte partagé', 'Un compte administrateur par service', 'Un coffre-fort de mots de passe en accès libre'], 'Peu coûteux pour 2 personnes. Un deuxième compte partagé aggrave le défaut.'),
 I('Combien d’heures par an de droits élevés avec la mesure (2 × 1 h × 52 semaines) ?', '104', ['52', '208', '8 760'], '2 × 1 × 52 = 104 h par an, contre 8 760 h : environ 1,2 % (réduction d’environ 98,8 %).'),
 I('Si le Just-in-Time est impossible, quel contrôle compensatoire ?', 'Journaliser les sessions administrateur avec une revue hebdomadaire par la direction', ['Augmenter la taille des mots de passe', 'Autoriser le partage du compte', 'Supprimer les journaux pour gagner de la place'], 'On ne réduit pas l’exposition, on la rend visible.'),
],
# ---------- ReBAC ----------
62: [
 I('Sonia peut-elle lire Tarifs2026 ?', 'Oui : sonia → membre de groupe:compta → lecteur de Tarifs → parent de Tarifs2026, héritage de lecture', ['Non : Sonia n’est pas propriétaire', 'Non : Tarifs2026 n’a pas de lecteur direct', 'Oui, car Marc est propriétaire de Tarifs'], 'Chemin de relations complet ; la règle d’héritage donne le droit de lecture.'),
 I('Karim (membre d’aucun groupe) peut-il lire Tarifs ?', 'Non : aucune relation ne relie Karim à Tarifs', ['Oui : tout salarié lit Tarifs', 'Oui : Tarifs a un parent', 'Oui si Marc est absent'], 'Sans relation, pas de droit.'),
 I('Marc retire Sonia du groupe compta : que devient son droit ?', 'Elle perd le droit sur Tarifs et sur Tarifs2026 en une seule opération', ['Elle perd le droit sur Tarifs seulement', 'Elle garde le droit sur Tarifs2026', 'Il faut modifier chaque sous-dossier'], 'Le chemin est rompu en un point.'),
 I('Quel avantage par rapport à un RBAC pour des dossiers imbriqués ?', 'Un seul changement de relation se répercute sur tous les sous-dossiers', ['Les droits sont plus longs à écrire', 'Il faut créer un rôle par dossier', 'Il n’y a plus besoin de propriétaire'], 'Pas besoin de créer un rôle par dossier, donc pas d’explosion de rôles.'),
],
# ---------- Zero Trust ----------
65: [
 I('Score de la requête 1 (Marc, PC géré, multifacteur, bureau, 10 h) ?', '6', ['4', '5', '3'], '2 + 2 + 1 + 1 = 6.'),
 I('Score de la requête 2 (Marc, PC personnel, multifacteur, domicile, 14 h habituelle) ?', '3', ['2', '4', '5'], 'Appareil 0 + multifacteur 2 + lieu 0 + heure 1 = 3.'),
 I('Score de la requête 4 (Karim, PC géré, sans multifacteur, étranger, 3 h) ?', '2', ['0', '3', '4'], 'Appareil 2 + 0 + 0 + 0 = 2.'),
 I('Requête 2 (score 3) sur une ressource Confidentiel (seuil 5) : décision ?', 'REFUSÉ (3 < 5)', ['PERMIS', 'PERMIS si le multifacteur est réussi', 'PERMIS car 3 ≥ 3'], 'Le seuil Confidentiel est 5.'),
 I('Requête 3 (Léa, PC géré, sans multifacteur, bureau, 6 h : score 3) sur une ressource Interne (seuil 3) : décision ?', 'PERMIS (3 ≥ 3)', ['REFUSÉ', 'REFUSÉ car 6 h est inhabituelle', 'PERMIS seulement avec le multifacteur'], 'Appareil 2 + lieu 1 = 3 ; 3 ≥ 3.'),
 I('Quel composant ABAC calcule le score et décide ?', 'Le PDP (point de décision) ; le PEP (point d’application) applique la décision', ['Le PEP calcule, le PDP applique', 'Le PIP décide', 'Le PAP applique'], 'PDP décide, PEP applique, PIP fournit les attributs.'),
 I('Quel défaut du modèle « le VPN ouvre tout » ce système corrige-t-il ?', 'Une fois connecté, on avait accès à tout : ici chaque accès est évalué', ['Le VPN est trop lent', 'Le VPN coûte trop cher', 'Le VPN n’est pas chiffré'], 'Zero Trust : on évalue chaque accès, pas seulement l’entrée.'),
],
}
