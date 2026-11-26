# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.
# Produit data/pub.json (public) et data/sec.json (corrigés) à partir de data/questions.json, puis chiffre sec.json.
# Usage : python3 tools/make_data.py [code_secret]   (sans argument : lit/crée le code dans $JEU25_SECRET_FILE)
import json, os, sys, base64, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(R, 'data', 'questions.json'), encoding='utf8'))['questions']
M = {q['qid']: q for q in json.load(open(os.path.join(R, 'data', 'manifest-v2.json'), encoding='utf8'))['q']}
TOTAL = 211
def short(s, n=64):
    s = s.strip().rstrip('?').strip()
    return s if len(s) <= n else s[:n].rsplit(' ', 1)[0] + '…'
groups, qs, sec = [], {}, {}
for o in D:
    qid, mq = o['qid'], M[o['qid']]
    gid = 'G' + qid[1:]
    first = o['items'][0]
    titre = short(o['situation'] if o['type'] == 'multi' else first['txt'])
    groups.append({'id': gid, 'slide': o['page'], 'so': 0, 'titre': titre, 'chap': o['part'], 'qs': [qid]})
    q = {'g': gid, 'ctx': None, 'final': False, 'sl': o['page'], 'ap': o['corr_page']}
    if o['type'] == 'multi':
        q.update({'type': 'multi', 'txt': o['situation'], 'items': [{'t': it['txt'], 'o': it['opts']} for it in o['items']], 'opts': [],
                  't': 60 + 30 * len(o['items']), 'rap': o['situation'] + '\n\n' + '\n'.join('%d. %s' % (i + 1, it['txt']) for i, it in enumerate(o['items']))})
        rep = [it['key'] for it in o['items']]
        exp = [it['ex'] for it in o['items']]
        det = ['But : ' + (o['but'] or ''), 'À retenir : ' + (o['retenir'] or '')] + ['Réponse %d : %s → %s' % (i + 1, it['opts'][it['key']], it['ex']) for i, it in enumerate(o['items'])]
        det += ['Corrigé du PowerPoint (page %d) : ' % o['corr_page'] + ' | '.join('%s : %s' % (r[0], r[1]) for r in mq['rows'])]
    else:
        it = first
        q.update({'type': 'single', 'txt': it['txt'], 'opts': it['opts'], 't': 60, 'rap': it['txt'] + '\n\n' + '\n'.join('%s. %s' % ('ABCD'[i], x) for i, x in enumerate(it['opts']))})
        if o.get('sondage'): q['sondage'] = True
        rep = it['key']; exp = it['exopts'][it['key']]
        det = ['But : ' + (o['but'] or ''), 'À retenir : ' + (o['retenir'] or '')] + ['%s. %s → %s' % ('ABCD'[i], x, it['exopts'][i]) for i, x in enumerate(it['opts'])]
    det += ['Source : ' + (o['source'] or '')]
    if o.get('cyber'): det += ['Rôle en cybersécurité : ' + o['cyber']]
    dt = ['', [] if o['type'] == 'multi' else [[it['opts'][i], it['exopts'][i]] for i in range(4) if i != it['key']] if o['type'] == 'single' else [], o.get('cyber') or '']
    if o['type'] == 'single': dt[0] = o.get('retenir') or ''
    qs[qid] = q
    sec[qid] = [rep, exp, None, dt, det]
pub = {'groups': groups, 'total': TOTAL, 'sid': 'mca25', 'qs': qs}
json.dump(pub, open(os.path.join(R, 'data', 'pub.json'), 'w', encoding='utf8'), ensure_ascii=False)
# chiffrement (PBKDF2-SHA256 200 000 itérations + AES-GCM), même format que le moteur du jeu 22
sf = os.environ.get('JEU25_SECRET_FILE', '/home/claude/jeu25_secret.txt')
code = sys.argv[1] if len(sys.argv) > 1 else (open(sf).read().strip() if os.path.exists(sf) else secrets.token_urlsafe(18))
open(sf, 'w').write(code)
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=200000).derive(code.encode())
ct = AESGCM(key).encrypt(iv, json.dumps({'q': sec}, ensure_ascii=False).encode('utf8'), None)
enc = {'salt': base64.b64encode(salt).decode(), 'iv': base64.b64encode(iv).decode(), 'ct': base64.b64encode(ct).decode(), 'it': 200000}
json.dump(enc, open(os.path.join(R, 'data', 'enc.json'), 'w'))
print('pub', len(groups), 'groupes', len(qs), 'questions ; sec chiffré', len(enc['ct']), 'octets ; code dans', sf)
