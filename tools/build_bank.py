# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.
# Construit la banque de 600 questions du test final (règle 33) à partir de data/bank/t01..t12.py (+ bank_fixes, bank_edits).
# Sorties : data/bank.json (public : énoncés et propositions, SANS la clé), data/bank_enc.json (clés + explications chiffrées avec le
# code secret, même schéma que enc.json), data/bank_sources.json (sources par thème, pour la page « Sources et références »).
import json, os, sys, base64, random, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))
import bank_load
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = bank_load.load()
rng = random.Random(25600)          # déterministe : même banque à chaque génération
# 1) contrôles
themes, rows, stems = [], [], set()
for ti, (th, src, qs) in enumerate(T):
    themes.append([th[0], th[1]])
    for q in qs:
        d, stem, good, b1, b2, b3, ex = q
        opts = [good, b1, b2, b3]
        assert len(set(o.strip().lower() for o in opts)) == 4, ('propositions identiques', th[0], stem)
        assert stem not in stems, ('énoncé en double', stem); stems.add(stem)
        assert d in (1, 2, 3) and ex.strip(), (th[0], stem)
        rows.append([ti, d, stem, opts, ex])
assert len(rows) == 600, len(rows)
# 2) niveaux : les énoncés de pure définition passent au niveau 1, les longs scénarios chiffrés au niveau 3, jusqu'à ≈ 20 / 55 / 25 %
dfn = re.compile(r"^(Que signifie|Qu.est-ce qu|Que désigne|Que veut dire|Que représente|Quel sigle|Que contient|Que traite)")
def cnt(): return [sum(1 for r in rows if r[1] == k) for k in (1, 2, 3)]
for r in rows:
    if cnt()[0] >= 120: break
    if r[1] == 2 and dfn.search(r[2]): r[1] = 1
cand = sorted([r for r in rows if r[1] == 2], key=lambda r: -len(r[2]))
for r in cand:
    if cnt()[2] >= 150: break
    r[1] = 3
cand = sorted([r for r in rows if r[1] == 2], key=lambda r: len(r[2]))
for r in cand:
    if cnt()[0] >= 120: break
    r[1] = 1
# 3) positions : bonne réponse équilibrée (150 par lettre), sans série de plus de 2 identiques, mélange déterministe des distracteurs
pos = [0, 1, 2, 3] * 150
rng.shuffle(pos)
def runs(): return [i for i in range(len(pos) - 2) if pos[i] == pos[i + 1] == pos[i + 2]]
for _ in range(100000):
    r = runs()
    if not r: break
    i = r[0] + 2; j = rng.randrange(600); pos[i], pos[j] = pos[j], pos[i]
assert not runs()
order = list(range(600)); rng.shuffle(order)       # les questions ne sont pas rangées par thème dans l'ordre d'identifiant
pub, key = {'themes': themes, 'q': []}, {}
for n, ri in enumerate(order):
    ti, d, stem, opts, ex = rows[ri]
    good, bad = opts[0], opts[1:]; rng.shuffle(bad)
    o = bad[:]; o.insert(pos[n], good)
    qid = 'B%03d' % (n + 1)
    pub['q'].append([qid, ti, d, stem, o]); key[qid] = [pos[n], ex]
json.dump(pub, open(os.path.join(R, 'data', 'bank.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
json.dump({th[0]: [th[1], src] for th, src, _ in T}, open(os.path.join(R, 'data', 'bank_sources.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
sf = os.environ.get('JEU25_SECRET_FILE', '/home/claude/jeu25_secret.txt')
code = open(sf).read().strip()
salt, iv = os.urandom(16), os.urandom(12)
k = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200000).derive(code.encode())
ct = AESGCM(k).encrypt(iv, json.dumps({'k': key}, ensure_ascii=False).encode('utf8'), None)
json.dump({'salt': base64.b64encode(salt).decode(), 'iv': base64.b64encode(iv).decode(), 'ct': base64.b64encode(ct).decode(), 'it': 200000}, open(os.path.join(R, 'data', 'bank_enc.json'), 'w'))
L = [sum(1 for r in rows if r[1] == x) for x in (1, 2, 3)]; P = [pos.count(i) for i in range(4)]
lon = sum(1 for q in pub['q'] if len(q[4][key[q[0]][0]]) == max(len(x) for x in q[4]))
print('banque', len(pub['q']), 'questions ; niveaux', L, '; positions', P, '; bonne réponse la plus longue %d %%' % round(100 * lon / 600))
