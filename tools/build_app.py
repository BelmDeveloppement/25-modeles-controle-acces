# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.
# Génère joueur.html, enseignant.html, classement.html, index.html du jeu 25 à partir des pages du moteur LAN Live (jeu 22)
# conservées dans engine/, des données data/pub.json + data/enc.json et des correctifs ci-dessous.
# Chaque correctif échoue bruyamment si son ancre n'est pas trouvée exactement une fois.
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def rd(p): return open(os.path.join(R, p), encoding='utf8').read()
def wr(p, s): open(os.path.join(R, p), 'w', encoding='utf8').write(s)
def sub(s, old, new, n=1, what=''):
    c = s.count(old)
    if c != n: sys.exit('ANCRE %s : %d occurrence(s) au lieu de %d : %r' % (what, c, n, old[:90]))
    return s.replace(old, new)
def swap_json(s, marker, obj):
    i = s.index(marker) + len(marker); _, e = json.JSONDecoder().raw_decode(s[i:])
    return s[:i] + json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + s[i + e:]
PUB = json.load(open(os.path.join(R, 'data', 'pub.json'), encoding='utf8'))
ENC = json.load(open(os.path.join(R, 'data', 'enc.json')))
BANK = json.load(open(os.path.join(R, 'data', 'bank.json'), encoding='utf8'))
TENC = json.load(open(os.path.join(R, 'data', 'bank_enc.json')))
AVATARS = ['🦊', '🐼', '🦉', '🐙', '🦁', '🐢', '🦄', '🐧', '🐝', '🦅', '🐬', '🦋']

INFO = r'''AC.INFO = {
  aide: {t: 'Aide', h: `<p><b>Comment répondre ?</b></p><ul><li>Lisez l’énoncé en entier, puis repérez le mot qui compte (<i>Pourquoi, Quel, Que se passe-t-il…</i>).</li><li>Certaines Questions comportent plusieurs réponses : répondez à chacune, 1 point par réponse exacte.</li><li>Éliminez d’abord les propositions que vous savez fausses.</li><li>Choisissez, puis appuyez sur « Valider » : une fois validée, la réponse ne se change plus.</li><li>Le bouton « Rappel » réaffiche la situation de la page en cours.</li><li>Le bouton « Signaler » vous permet de signaler une erreur ou une ambiguïté (votre pseudo est joint).</li></ul><p class="muted">L’aide ne donne jamais la réponse ; pour une notion, demandez à l’enseignant.</p>`},
  translor: {t: 'TransLor', h: `<p><b>TransLor</b> est l’entreprise fictive du cours, fil rouge des Questions. Les chiffres sont inventés mais réalistes.</p>
   <table><tr><th>Dimension</th><th>TransLor</th></tr>
   <tr><td>Entreprise</td><td>Transport et logistique près de Nancy · 120 salariés · 3 agences (Nancy, Metz, Épinal)</td></tr>
   <tr><td>Personnes</td><td>Léa (conductrice) · Marc (gestionnaire) · Sonia (comptable) · Paul (RH) · Karim (intérimaire) · la directrice</td></tr>
   <tr><td>Outils</td><td>TMS (gestion des tournées) · serveur de fichiers · annuaire</td></tr></table>`},
  jeu: {t: 'Le jeu', h: `<p><b>Jeu 25</b> : une Question à la fois, projetée en classe et envoyée sur votre écran. Le PowerPoint pilote le jeu : la page de la Question ouvre la Question, la page suivante la corrige.</p>
   <h3>Les points</h3><ul>
   <li>Question à une réponse : <b>100 points</b> pour une bonne réponse, jusqu’à <b>+ 50</b> de bonus de rapidité, <b>+ 10</b> par bonne réponse consécutive (jusqu’à + 50).</li>
   <li>Question à plusieurs réponses : <b>100 points par réponse exacte</b>, sans bonus de rapidité.</li>
   <li>Le sondage de la Question 1 ne rapporte aucun point.</li>
   <li>Une bonne réponse tardive (après le chrono) ne rapporte que la moitié des points de base.</li></ul>
   <h3>Classement</h3><p>Il est individuel et affiché sous forme de barres avec votre avatar. À égalité, le temps cumulé le plus court sur les bonnes réponses départage.</p>
   <h3>Bon à savoir</h3><ul><li>Une seule réponse par Question : elle ne se modifie plus après validation.</li><li>Changement d’appareil : cochez « Je reprends ma partie » à l’inscription, avec le même pseudo : vous ne serez pas compté deux fois.</li><li>Choisissez un pseudo sérieux : il est visible de toute la classe.</li></ul>`}
};
AC.FOOT = '© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés. · Jeu 25 · Modèles de contrôle d’accès';
AC.AV = ''' + json.dumps(AVATARS, ensure_ascii=False) + r''';
AC.avHtml = a => a ? `<span style="font-size:1.25em;line-height:1" aria-hidden="true">${a}</span>` : '';
'''

def common(s, title, page):
    s = swap_json(s, 'AC.PUB=', PUB)
    if 'AC.ENC=' in s: s = swap_json(s, 'AC.ENC=', ENC)
    if page in ('joueur', 'enseignant'):   # banque du test final (publique, sans clé) ; clés chiffrées pour le TDC seul
        s = sub(s, '</script><script>AC.PUB=', '</script><script>AC.BANK=' + json.dumps(BANK, ensure_ascii=False, separators=(',', ':')) + (';AC.TENC=' + json.dumps(TENC) if page == 'enseignant' else '') + ';</script><script>AC.PUB=', what='bank')
    i = s.index('AC.INFO = {'); j = s.index("AC.FOOT = '", i); j = s.index('\n', j)
    s = s[:i] + INFO.rstrip('\n') + s[j:]
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % title, s, count=1)
    s = s.replace("LAN Live : application d'interaction (jeu 22), cours « Sécurité des accès ».", "Jeu 25 : application d'interaction (moteur LAN Live), cours « Modèles de contrôle d'accès ».")
    s = s.replace('(jeu 22)', '(jeu 25)')
    return s

exec(open(os.path.join(R, 'tools', 'patch_joueur.py'), encoding='utf8').read())
exec(open(os.path.join(R, 'tools', 'patch_enseignant.py'), encoding='utf8').read())
exec(open(os.path.join(R, 'tools', 'patch_classement.py'), encoding='utf8').read())

wr('joueur.html', patch_joueur(common(rd('engine/joueur.html'), 'JOUEUR · Jeu 25 · Modèles de contrôle d’accès', 'joueur')))
wr('enseignant.html', patch_enseignant(common(rd('engine/enseignant.html'), 'TDC · Jeu 25 · tour de contrôle', 'enseignant')).replace('diapo ', 'page '))
wr('classement.html', patch_classement(common(rd('engine/classement.html'), 'PROJECTION · Jeu 25 · classement', 'classement')))
idx = rd('engine/index.html')
import re as _re
idx = _re.sub(r'<title>[^<]*</title>', '<title>Jeu 25 · Modèles de contrôle d’accès</title>', idx, count=1)
i = idx.index('<body'); j = idx.index('>', i) + 1
idx = idx[:j] + '<div class="wrap"><h1 class="mono" style="color:#29D3FF">JEU 25</h1><div class="card"><p>Application d’interaction pour le cours « Modèles de contrôle d’accès » (UCUE-S5-4-1, partie 2).</p><p><b>Étudiants :</b> ouvrez sur votre PC l’adresse communiquée par l’enseignant (le QR code n’est qu’un secours téléphone).</p><p><b>Enseignant :</b> ouvrez votre lien secret de tour de contrôle.</p></div><div class="foot">© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.</div></div></body></html>'
wr('index.html', idx)
print('pages générées')
