/* ---------- jeu 25 : test final noté (règle 33), côté TDC ---------- */
/* © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés. */
const tb64e = u => btoa(String.fromCharCode.apply(null, new Uint8Array(u)));
const tb64d = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
AC.BANKI = {}; AC.BANK.q.forEach(q => { AC.BANKI[q[0]] = q; });
const T_N = 50, T_FORM = {name:'ECDH', namedCurve:'P-256'};
async function unlockBlob(E, code) {
  const km = await crypto.subtle.importKey('raw', new TextEncoder().encode(code), 'PBKDF2', false, ['deriveKey']);
  const key = await crypto.subtle.deriveKey({name:'PBKDF2', salt:tb64d(E.salt), iterations:E.it, hash:'SHA-256'}, km, {name:'AES-GCM', length:256}, false, ['decrypt']);
  return JSON.parse(new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM', iv:tb64d(E.iv)}, key, tb64d(E.ct))));
}
const trnd = () => { const a = new Uint32Array(1); crypto.getRandomValues(a); return a[0] / 4294967296; };
function tshuf(a) { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(trnd() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
function drawTest(n) {   // répartition par thème (± 1) et par difficulté (≈ 20 / 55 / 25 %), aléatoire à chaque séance
  const th = AC.BANK.themes.length, base = Math.floor(n / th), extra = n - base * th, order = tshuf(AC.BANK.themes.map((_, i) => i)), slots = [];
  order.forEach((ti, k) => { for (let j = 0; j < base + (k < extra ? 1 : 0); j++) slots.push(ti); });
  const d1 = Math.round(n * 0.2), d3 = Math.round(n * 0.25), diffs = tshuf([].concat(Array(d1).fill(1), Array(n - d1 - d3).fill(2), Array(d3).fill(3)));
  const used = {}, ids = [];
  slots.forEach((ti, k) => {
    const want = diffs[k];
    for (const d of [want, 2, want === 2 ? 3 : 2, 1, 3]) {
      const pool = AC.BANK.q.filter(q => q[1] === ti && q[2] === d && !used[q[0]]);
      if (pool.length) { const q = pool[Math.floor(trnd() * pool.length)]; used[q[0]] = 1; ids.push(q[0]); return; }
    }
  });
  return tshuf(ids);
}
window.testLaunch = async () => {
  if (G.T) return;
  const kp = await crypto.subtle.generateKey(T_FORM, true, ['deriveKey']);
  const seed = AC.rid(10), ids = drawTest(T_N);
  G.T = {st:'open', ids, seed, pk:tb64e(await crypto.subtle.exportKey('raw', kp.publicKey)), sk:await crypto.subtle.exportKey('jwk', kp.privateKey), t0:now(), res:{}, last:now(), exp:0};
  ui.note = 'Test final ouvert : ' + ids.length + ' questions tirées.'; tab = 'test'; commit(true);
};
window.testClose = () => { if (!G.T || G.T.st === 'closed') return; G.T.st = 'closed'; G.T.last = now(); ui.note = 'Test final clos.'; commit(true); };
window.testReopen = () => { if (!G.T || G.T.st === 'open') return; G.T.st = 'open'; commit(true); };
function testPub() {
  const T = G.T; if (!T) return null;
  const R = T.res, in_ = p => !!G.pl[p];
  return {st:T.st, n:T.ids.length, seed:T.seed, ids:T.ids, pk:T.pk, act:Object.keys(R).filter(in_), done:Object.keys(R).filter(p => R[p].fin && in_(p)), np:nPl()};
}
async function tDec(o) {
  const sk = await crypto.subtle.importKey('jwk', G.T.sk, T_FORM, false, ['deriveKey']);
  const epk = await crypto.subtle.importKey('raw', tb64d(o.e), T_FORM, false, []);
  const k = await crypto.subtle.deriveKey({name:'ECDH', public:epk}, sk, {name:'AES-GCM', length:256}, false, ['decrypt']);
  return JSON.parse(new TextDecoder().decode(await crypto.subtle.decrypt({name:'AES-GCM', iv:tb64d(o.iv)}, k, tb64d(o.c))));
}
async function testMsg(o) {   // 'TP' : progression ; 'T' : validation définitive (messages chiffrés pour ce TDC)
  const T = G.T; if (!T || T.st !== 'open' || !G.pl[o.pid] || !o.e || !o.iv || !o.c) return;
  let d; try { d = await tDec(o); } catch (e) { return; }
  const R = T.res[o.pid] = T.res[o.pid] || {r:{}, fin:0, ts:0};
  if (R.fin || (d.ts && d.ts < R.ts)) return;
  const r = {}; T.ids.forEach(id => { const v = d.r && d.r[id]; if (Number.isInteger(v) && v >= -1 && v <= 3) r[id] = v; });
  R.r = r; R.n = Object.keys(r).length; R.ts = d.ts || now(); R.t = now();
  R.idn = Array.isArray(d.idn) ? d.idn.map(x => String(x).slice(0, 40)) : R.idn || ['', ''];
  if (o.k === 'T' || d.fin) R.fin = now();
  T.last = now(); commit(true);
}
function tGrade(R) {
  const K = SEC.T.k; let g = 0, b = 0, s = 0;
  G.T.ids.forEach(id => { const v = R.r[id]; if (v === undefined || v < 0) s++; else if (v === K[id][0]) g++; else b++; });
  return {g, b, s, note:Math.max(0, 0.4 * (g - b / 3))};
}
const tF = x => (Math.round(x * 10) / 10).toFixed(1).replace('.', ',');
const tCs = s => '"' + String(s == null ? '' : s).replace(/"/g, '""') + '"';
const COPY = '© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.';
const tAscii = s => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '_').replace(/^_|_$/g, '') || 'x';
function crc32(u) {
  if (!crc32.t) { crc32.t = []; for (let n = 0, c; n < 256; n++) { c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; crc32.t[n] = c >>> 0; } }
  let c = -1; for (let i = 0; i < u.length; i++) c = crc32.t[(c ^ u[i]) & 255] ^ (c >>> 8); return (c ^ -1) >>> 0;
}
function makeZip(files) {   // ZIP « stocké » (sans compression), noms en UTF-8
  const enc = new TextEncoder(), parts = [], cd = []; let off = 0;
  const u16 = n => [n & 255, (n >> 8) & 255], u32 = n => [n & 255, (n >> 8) & 255, (n >> 16) & 255, (n >>> 24) & 255];
  files.forEach(f => {
    const nm = enc.encode(f.name), crc = crc32(f.data), sz = f.data.length;
    const lh = new Uint8Array([0x50, 0x4b, 3, 4, ...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0x21), ...u32(crc), ...u32(sz), ...u32(sz), ...u16(nm.length), ...u16(0)]);
    parts.push(lh, nm, f.data);
    cd.push(new Uint8Array([0x50, 0x4b, 1, 2, ...u16(20), ...u16(20), ...u16(0x0800), ...u16(0), ...u16(0), ...u16(0x21), ...u32(crc), ...u32(sz), ...u32(sz), ...u16(nm.length), ...u16(0), ...u16(0), ...u16(0), ...u16(0), ...u32(0), ...u32(off)]), nm);
    off += lh.length + nm.length + sz;
  });
  const cdSize = cd.reduce((a, b) => a + b.length, 0);
  const end = new Uint8Array([0x50, 0x4b, 5, 6, 0, 0, 0, 0, ...u16(files.length), ...u16(files.length), ...u32(cdSize), ...u32(off), 0, 0]);
  return new Blob(parts.concat(cd, [end]), {type:'application/zip'});
}
function tCsv(lines) { return new TextEncoder().encode('﻿' + lines.map(l => l.join(';')).join('\r\n') + '\r\n'); }
function testFiles() {
  const T = G.T, K = SEC.T.k, files = [], used = {}, syn = [['Nom', 'Prénom', 'Pseudo', 'Statut', 'Bonnes', 'Mauvaises', 'Sans réponse', 'Note sur 20', 'Réussite (seuil 10/20)'].map(tCs)], notes = [];
  const pids = Object.keys(G.pl).filter(p => T.res[p]).sort((a, b) => (T.res[a].idn || ['', ''])[0].localeCompare((T.res[b].idn || ['', ''])[0], 'fr'));
  pids.forEach(p => {
    const R = T.res[p], P = G.pl[p], gr = tGrade(R), idn = R.idn || ['', ''], st = R.fin ? 'Terminé' : 'En cours (non validé)';
    let nm = '25_test_' + tAscii(idn[0]) + '_' + tAscii(idn[1]); used[nm] = (used[nm] || 0) + 1; if (used[nm] > 1) nm += '_' + used[nm];
    const L = [['N°', 'Thème', 'Difficulté', 'Énoncé', 'Réponse de l’étudiant', 'Bonne réponse', 'Résultat', 'Points'].map(tCs)];
    T.ids.forEach((id, i) => {
      const q = AC.BANKI[id], v = R.r[id], ok = K[id][0], res = v === undefined || v < 0 ? '○ sans réponse' : v === ok ? '✓ bonne' : '✗ mauvaise';
      L.push([i + 1, tCs(AC.BANK.themes[q[1]][1]), q[2], tCs(q[3]), tCs(v === undefined ? '(non répondu)' : v < 0 ? 'Je ne sais pas' : q[4][v]), tCs(q[4][ok]), tCs(res), v === undefined || v < 0 ? '0' : v === ok ? '1' : '-0,3333']);
    });
    L.push([]); L.push([tCs('Nom'), tCs(idn[0])]); L.push([tCs('Prénom'), tCs(idn[1])]); L.push([tCs('Pseudo'), tCs(P.n)]); L.push([tCs('Statut'), tCs(st)]);
    L.push([tCs('Bonnes / Mauvaises / Sans réponse'), gr.g + ' / ' + gr.b + ' / ' + gr.s]); L.push([tCs('Note sur 20 = 0,4 × (bonnes − mauvaises ÷ 3), plancher 0'), tF(gr.note)]); L.push([tCs(COPY)]);
    files.push({name:nm + '.csv', data:tCsv(L)});
    syn.push([tCs(idn[0]), tCs(idn[1]), tCs(P.n), tCs(st), gr.g, gr.b, gr.s, tF(gr.note), tCs(gr.note >= 10 - 1e-9 ? '✓ réussi' : '✗ échec')]); notes.push(gr.note);
  });
  syn.push([]); syn.push([tCs('Étudiants'), notes.length]); if (notes.length) syn.push([tCs('Moyenne de la classe /20'), tF(notes.reduce((a, b) => a + b, 0) / notes.length)]);
  syn.push([tCs('Tirage'), tCs(T.ids.length + ' questions de la banque de ' + AC.BANK.q.length)]); syn.push([tCs(COPY)]);
  files.unshift({name:'25_test_synthese.csv', data:tCsv(syn)});
  const rk = [['Rang', 'Pseudo', 'Points', 'Bonnes réponses'].map(tCs)]; AC.rankList(G.pl).forEach((x, i) => rk.push([i + 1, tCs(x.n), x.pts, x.ok])); rk.push([]); rk.push([tCs(COPY)]);
  files.push({name:'25_classement_seance.csv', data:tCsv(rk)});
  return files;
}
window.testExport = () => {
  const T = G.T; if (!T || !Object.keys(T.res).length) { alert('Aucun résultat à exporter.'); return; }
  const blob = makeZip(testFiles()), a = document.createElement('a');
  a.href = URL.createObjectURL(blob); a.download = '25_test_final_' + new Date().toISOString().slice(0, 16).replace(/[-:T]/g, '') + '.zip'; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000); T.exp = now(); commit(true);
};
function testTab() {
  const T = G.T;
  let h = `<div class="card"><h2>Test final · ${T_N} questions notées</h2><p class="muted">Tirage dans la banque de ${AC.BANK.q.length} questions : réparti sur les ${AC.BANK.themes.length} thèmes (± 1), équilibré en difficulté, différent à chaque séance. Même test pour toute la classe, ordre des questions et des réponses mélangé par étudiant. Sans minuteur ; « Valider le test » est définitif ; Rappel désactivé. Barème : bonne + 1, mauvaise − 1/3, « Je ne sais pas » 0 ; note /20 = 0,4 × (bonnes − mauvaises ÷ 3), plancher 0 ; réussite dès 10/20. Nom et prénom restent dans ce navigateur : jamais sur le relais, jamais projetés.</p>`;
  if (!T) return h + `<button class="btn go" onclick="window.testLaunch()">▶ Lancer le test (tirage de ${T_N} questions)</button></div>`;
  const fin = Object.keys(T.res).filter(p => T.res[p].fin && G.pl[p]).length, np = nPl();
  h += `<p><b>${T.st === 'open' ? '● Test ouvert' : '■ Test clos'}</b> · ✓ ${fin} terminé(s) sur ${np} joueur(s)</p>
   ${T.st === 'open' ? '<button class="btn red sm" onclick="window.testClose()">■ Clore le test</button>' : '<button class="btn alt sm" onclick="window.testReopen()">▶ Rouvrir le test</button>'}
   <button class="btn alt sm" onclick="window.testExport()">⬇ Exporter les résultats (ZIP)</button>
   <p class="muted">${T.exp ? 'Dernier export : ' + new Date(T.exp).toLocaleTimeString('fr-FR') : '⚠ Aucun export effectué.'} La page PowerPoint « TEST » ouvre le test, « TEST:c » le clôt.</p></div>`;
  const th = {}, df = [0, 0, 0, 0]; T.ids.forEach(id => { const q = AC.BANKI[id]; th[q[1]] = (th[q[1]] || 0) + 1; df[q[2]]++; });
  h += `<div class="card"><b>Tirage</b> <span class="muted">· difficulté : ${df[1]} faciles · ${df[2]} moyennes · ${df[3]} difficiles · par thème : ${AC.BANK.themes.map((x, i) => x[1] + ' ' + (th[i] || 0)).join(' · ')}</span></div>`;
  h += `<div class="card"><table style="width:100%;border-collapse:collapse"><tr><th align="left">Pseudo</th><th align="left">Nom Prénom</th><th align="left">État</th><th>Répondues</th><th>Bonnes</th><th>Mauvaises</th><th>Note /20</th></tr>`;
  Object.keys(G.pl).map(p => [p, G.pl[p]]).sort((a, b) => a[1].n.localeCompare(b[1].n, 'fr')).forEach(([p, P]) => {
    const R = T.res[p], st = !R ? '○ pas commencé' : R.fin ? '✓ terminé' : '● en cours', gr = R && (R.fin || T.st === 'closed') ? tGrade(R) : null;
    h += `<tr style="border-top:1px solid #1F3556"><td>${AC.avHtml(P.av)} ${AC.esc(P.n)}</td><td>${R && R.idn ? AC.esc(R.idn.join(' ')) : '—'}</td><td><b>${st}</b></td><td align="center">${R ? R.n + ' / ' + T.ids.length : '—'}</td><td align="center">${gr ? gr.g : '—'}</td><td align="center">${gr ? gr.b : '—'}</td><td align="center">${gr ? '<b>' + tF(gr.note) + '</b> ' + (gr.note >= 10 - 1e-9 ? '✓' : '✗') + (R.fin ? '' : ' ⚠ non validé') : '—'}</td></tr>`;
  });
  return h + '</table></div>';
}
