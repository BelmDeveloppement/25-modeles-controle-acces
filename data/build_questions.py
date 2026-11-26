# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.
# Fusionne le manifeste du PowerPoint v2 et les sous-réponses structurées : produit questions.json (66 Questions).
import json, random, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from multi_items import MULTI
from multi_patch import PATCH
H = os.path.dirname(__file__)
m = json.load(open(os.path.join(H, 'manifest-v2.json'), encoding='utf8'))
rng = random.Random(2526)
seq = []                                    # positions cibles de la bonne réponse : blocs de 4 mélangés, jamais 3 fois la même de suite
def next_pos():
    global seq
    if not seq:
        for _ in range(50):
            b = [0, 1, 2, 3] * 3; rng.shuffle(b)
            if all(not (b[i] == b[i+1] == b[i+2]) for i in range(len(b)-2)): seq = b; break
    return seq.pop()
Q = []
for q in m['q']:
    o = {k: q.get(k) for k in ('n', 'qid', 'page', 'part', 'retenir', 'but', 'cyber', 'source')}
    o['corr_page'] = q['page'] + 1
    if 'multi' in q:
        o['type'] = 'multi'; o['situation'] = q['situation']; o['consigne'] = "Répondez à chaque demande : 1 point par réponse exacte."
        items = []
        last = None
        for ix, it in enumerate(MULTI[q['n']]):
            op = PATCH.get((q['n'], ix), it['opts'])
            ok, bad = op[0], op[1:]
            p = next_pos()
            if last is not None and False: pass
            opts = bad[:p] + [ok] + bad[p:]
            items.append({'txt': it['txt'], 'opts': opts, 'key': p, 'ex': it['ex']})
        o['items'] = items
    else:
        o['type'] = 'single'; o['situation'] = None; o['consigne'] = None
        L = 'ABCD'.index(q['correct'])
        o['items'] = [{'txt': q['enonce'], 'opts': q['opts'], 'key': L, 'exopts': q['expl']}]
        o['sondage'] = bool(q.get('sondage'))
    Q.append(o)
# contrôles
tot = sum(len(o['items']) for o in Q); pos = [0]*4; longest = 0
for o in Q:
    for it in o['items']:
        pos[it['key']] += 1
        if max(range(len(it['opts'])), key=lambda i: len(it['opts'][i])) == it['key']: longest += 1
json.dump({'copyright': '© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.', 'questions': Q}, open(os.path.join(H, 'questions.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('questions', len(Q), 'réponses', tot, 'positions A-D', pos, 'correcte la plus longue', longest, round(100*longest/tot), '%')
print('points max (hors sondage)', sum(len(o['items']) for o in Q if not o.get('sondage')))
