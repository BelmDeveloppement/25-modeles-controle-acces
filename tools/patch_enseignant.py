# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés. Correctifs de la tour de contrôle (TDC).
TDC_JS = r'''
/* ---------- jeu 25 : Questions à plusieurs réponses, sondage, signalements, nouvelle partie ---------- */
const isMulti = qid => AC.q(qid).type === 'multi';
function multiPanel(c, q) {
  const rep = SEC.q[c.qid][0], ex = SEC.q[c.qid][1], cnt = q.items.map(() => [0, 0, 0, 0]);
  Object.keys(c.ans).forEach(p => { const a = c.ans[p].a; if (Array.isArray(a)) a.forEach((x, i) => { if (x >= 0) cnt[i][x]++; }); });
  return q.items.map((it, ii) => `<div class="card" style="margin:6px 0;padding:8px 12px"><b>${ii + 1}. ${AC.esc(it.t)}</b>${it.o.map((o, i) => `<div class="opt" style="--oc:${AC.LCOL[i]};cursor:default;margin:4px 0;padding:6px 10px;${i === rep[ii] ? 'border-color:#56B4E9' : ''}"><span class="lt">${AC.LET[i]}</span><span style="flex:1">${AC.esc(o)} ${i === rep[ii] ? '<b class="ok">✔ bonne réponse</b>' : ''}</span><b class="mono">${cnt[ii][i]}</b></div>`).join('')}<div class="muted">${AC.esc(ex[ii])}</div></div>`).join('');
}
function revealMulti(c, q) {
  const rep = SEC.q[c.qid][0], mult = q.final ? 2 : 1, R0 = AC.rankList(G.pl), rk0 = {}; R0.forEach((x, i) => rk0[x.pid] = i + 1);
  c.res = {};
  Object.keys(G.pl).forEach(pid => {
    const P = G.pl[pid], a = c.ans[pid];
    if (!a) { P.streak = 0; c.res[pid] = [rep.map(() => -1), 0, 0, 0, 0, 0, mult, rk0[pid], 0, 0]; P.res[c.qid] = {a:null, ms:null, g:0, ok:0, n:rep.length}; return; }
    const nOK = a.a.reduce((t, x, i) => t + (x === rep[i] ? 1 : 0), 0), late = a.ms > c.dur * 1000 + AC.GRACE;
    const gain = Math.round(nOK * AC.BASE * (late ? AC.LATE : 1)) * mult;
    P.pts += gain; P.ok += nOK; if (nOK) P.tt += a.ms; P.streak = nOK === rep.length ? P.streak + 1 : 0;
    c.res[pid] = [a.a, gain, nOK === rep.length ? 1 : 0, gain / mult, 0, 0, mult, rk0[pid], late ? 1 : 0, nOK];
    P.res[c.qid] = {a:a.a, ms:a.ms, g:gain, ok:nOK, n:rep.length, late:late ? 1 : 0};
  });
  c.st = 'rev'; G.qdone[c.qid] = true; commit(true);
}
function revealSondage(c) {
  const R0 = AC.rankList(G.pl), rk0 = {}; R0.forEach((x, i) => rk0[x.pid] = i + 1);
  c.res = {};
  Object.keys(G.pl).forEach(pid => { const P = G.pl[pid], a = c.ans[pid]; c.res[pid] = [a ? a.a : -1, 0, 0, 0, 0, 0, 1, rk0[pid], 0]; P.res[c.qid] = {a:a ? a.a : -1, ms:a ? a.ms : null, g:0, ok:0, so:1}; });
  c.st = 'rev'; G.qdone[c.qid] = true; commit(true);
}
const ansTxt = (qq, r) => qq.type === 'multi' ? (Array.isArray(r.a) ? r.a.map(x => x >= 0 ? AC.LET[x] : '—').join('') : '—') : qq.type === 'cloud' ? cs((r.w || []).join(', ') || '—') : (r.a >= 0 ? AC.LET[r.a] : '—');
const keyTxt = (qq, q) => qq.type === 'multi' ? SEC.q[q][0].map(x => AC.LET[x]).join('') : qq.type === 'cloud' ? cs('(nuage de mots)') : qq.sondage ? '(sondage)' : AC.LET[SEC.q[q][0]];
window.toggleDet = qid => { ui.det = ui.det || {}; ui.det[qid] = !ui.det[qid]; render(true); };
function detBtn(qid) {
  const on = ui.det && ui.det[qid], L = SEC.q[qid][4] || [];
  return `<p style="margin:8px 0 0"><button class="btn alt sm" onclick="window.toggleDet('${qid}')">${on ? '▲ Masquer' : '📘 Afficher'} la correction très détaillée (enseignant)</button></p>${on ? `<div class="card" style="background:#0a1a30;margin-top:6px">${L.map(x => `<p style="margin:.35em 0">${AC.esc(x)}</p>`).join('')}</div>` : ''}`;
}
window.nouvellePartie = () => {
  if (!confirm('NOUVELLE PARTIE : remet tout à zéro (joueurs, points, Questions jouées, écran projeté et écrans des joueurs). Les signalements sont conservés (exportez-les avant si besoin). Continuer ?')) return;
  G.pl = {}; G.cur = null; G.played = {}; G.qdone = {}; G.ended = false; G.pend = null; G.lastSlide = null; G.gen = now();
  ui.note = 'Nouvelle partie : tout est remis à zéro. Les joueurs se réinscrivent automatiquement avec leur pseudo.'; tab = 'pilot'; commit(true);
};
const RST = {a:'● à approuver par l’enseignant', ok:'✓ approuvé', ko:'✗ rejeté'};
function signTab() {
  const L = G.reports || [], nA = L.filter(r => r.st === 'à approuver').length;
  let h = `<div class="card"><h2>Revue de backlog des signalements</h2><p class="muted">Signalements non anonymes, statut initial « à approuver par l’enseignant ». Faites la revue en fin de séance : approuvez ou rejetez chaque signalement, puis exportez. ${nA} à approuver sur ${L.length}.</p>
   <button class="btn alt sm" onclick="window.exportReports()">Exporter la revue (CSV)</button> <button class="btn alt sm" onclick="window.addReport()">+ Signaler (enseignant)</button></div>`;
  if (!L.length) return h + '<p class="muted">Aucun signalement pour le moment.</p>';
  L.slice().reverse().forEach(r => {
    const sym = r.st === 'approuvé' ? '✓ approuvé' : r.st === 'rejeté' ? '✗ rejeté' : '● à approuver par l’enseignant';
    h += `<div class="card" style="padding:10px 14px"><div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center"><span class="tag">${sym}</span><span class="tag">${r.qid ? 'Question ' + AC.num(r.qid) + ' · page ' + r.page : 'général'}</span><span class="tag">${AC.esc(r.type)}</span><span class="muted">${AC.avHtml((G.pl[r.pid] || {}).av)} ${AC.esc(r.n)} (${r.from})</span><span style="flex:1"></span>
      <button class="btn alt sm" onclick="window.setReport('${r.id}','approuvé')">✓ Approuver</button><button class="btn alt sm" onclick="window.setReport('${r.id}','rejeté')">✗ Rejeter</button><button class="btn alt sm" onclick="window.setReport('${r.id}','à approuver')">↺</button></div><p style="margin:.5em 0 0">${AC.esc(r.txt)}</p></div>`;
  });
  return h;
}
window.setReport = (id, st) => { const r = (G.reports || []).find(x => x.id === id); if (r) { r.st = st; commit(false); } };
window.addReport = () => {
  const txt = prompt('Signalement (enseignant) : décrivez le problème'); if (!txt) return;
  const c = G.cur, q = c && AC.q(c.qid); G.reports = G.reports || [];
  G.reports.push({id:'t' + AC.rid(8), pid:null, n:'Enseignant', qid:c ? c.qid : '', page:q ? q.sl : 0, type:'Remarque enseignant', txt:txt.slice(0, 500), ts:now(), from:'enseignant', st:'à approuver'}); commit(false);
};
window.exportReports = () => {
  const d = new Date().toISOString().slice(0, 10);
  dl('25_signalements_' + d + '.csv', ['Statut;Date;Auteur;Origine;Question;Page;Type;Texte'].concat((G.reports || []).map(r => [cs(r.st), new Date(r.ts).toLocaleString('fr-FR'), cs(r.n), r.from, r.qid ? AC.num(r.qid) : '', r.page || '', cs(r.type), cs(r.txt)].join(';'))).join('\r\n'));
};
function corrTab() {
  let h = `<p class="muted">Corrigés très détaillés (visibles seulement ici, avec votre code). Bonne réponse marquée ✔.</p>`, chap = '';
  AC.PUB.groups.forEach(g => {
    if (g.chap !== chap) { chap = g.chap; h += `<h2 style="margin-top:14px;color:#29D3FF">${AC.esc(chap)}</h2>`; }
    g.qs.forEach(qid => {
      const q = AC.q(qid), s = SEC.q[qid];
      h += `<div class="card"><b>Question ${AC.num(qid)} · page ${q.sl}</b> <span class="tag">${q.type === 'multi' ? q.items.length + ' réponses' : q.sondage ? 'sondage' : '1 réponse'} · ${q.t} s</span><p style="margin:.5em 0"><b>${AC.esc(q.txt)}</b></p>`;
      if (q.type === 'multi') h += q.items.map((it, ii) => `<div style="margin:6px 0"><b>${ii + 1}. ${AC.esc(it.t)}</b>${it.o.map((o, i) => `<div style="margin:2px 0 2px 10px;${i === s[0][ii] ? 'color:#56B4E9;font-weight:700' : 'color:#C9D8F2'}">${AC.LET[i]}. ${AC.esc(o)}${i === s[0][ii] ? ' ✔' : ''}</div>`).join('')}<div class="muted" style="margin-left:10px">${AC.esc(s[1][ii])}</div></div>`).join('');
      else h += q.opts.map((o, i) => `<div style="margin:2px 0;${i === s[0] ? 'color:#56B4E9;font-weight:700' : 'color:#C9D8F2'}">${AC.LET[i]}. ${AC.esc(o)}${i === s[0] ? ' ✔' : ''}</div>`).join('') + `<p class="muted">${AC.esc(s[1])}</p>`;
      h += `<div style="margin-top:8px;padding-top:8px;border-top:1px solid #1F3556">${(s[4] || []).map(x => `<p style="margin:.3em 0">${AC.esc(x)}</p>`).join('')}</div></div>`;
    });
  });
  return h;
}
'''
def patch_enseignant(s):
    # état : génération de partie ; protocole
    s = sub(s, "G = {v:Math.floor(now() / 1000),", "G = {gen:now(), reports:[], v:Math.floor(now() / 1000),", what='newGame')
    s = sub(s, "lb:R.slice(0, 10).map(x => [x.n, x.pts, Math.round(x.tt / 100) / 10, x.ok]), me:{}};",
            "lb:R.slice(0, 10).map(x => [x.n, x.pts, Math.round(x.tt / 100) / 10, x.ok, x.av || '']), me:{}, gen:G.gen || 0, rk:(G.reports || []).slice(-300).map(r => r.id)};", what='buildPub-head')
    s = sub(s, "    } else if (c.st === 'rev') {\n      const cnt = [0, 0, 0, 0];",
            "    } else if (c.st === 'rev' && q.type === 'multi') {\n      const cnt = q.items.map(() => [0, 0, 0, 0]); Object.keys(c.ans).forEach(p => c.ans[p].a.forEach((x, i) => { if (x >= 0) cnt[i][x]++; }));\n      P.rev = {rep:SEC.q[c.qid][0], exp:SEC.q[c.qid][1], cnt, r:c.res || {}, dt:DT};\n    } else if (c.st === 'rev') {\n      const cnt = [0, 0, 0, 0];", what='buildPub-rev')
    s = sub(s, "if (!P) { if (nPl() >= 40) return; G.pl[o.pid] = {n:uniqName(n, o.pid), pts:0, tt:0, ok:0, streak:0, res:{}, j:now()}; ch = true; imm = true; }",
            """if (!P) {
      const old = o.re ? Object.keys(G.pl).find(p => p !== o.pid && G.pl[p].n.toLowerCase() === n.toLowerCase()) : null;
      if (old) {   // reprise de partie sur un autre appareil : même joueur, pas compté deux fois
        G.pl[o.pid] = G.pl[old]; delete G.pl[old]; const c0 = G.cur;
        if (c0) { if (c0.ans[old]) { c0.ans[o.pid] = c0.ans[old]; delete c0.ans[old]; } if (c0.res && c0.res[old]) { c0.res[o.pid] = c0.res[old]; delete c0.res[old]; } }
        if (o.av) G.pl[o.pid].av = String(o.av).slice(0, 4); ch = true; imm = true;
      } else { if (nPl() >= 40) return; G.pl[o.pid] = {n:uniqName(n, o.pid), av:String(o.av || '').slice(0, 4), pts:0, tt:0, ok:0, streak:0, res:{}, j:now()}; ch = true; imm = true; }
    }""", what='join')
    s = sub(s, "else if (P.n.replace(/ \\d+$/, '') !== n) { P.n = uniqName(n, o.pid); ch = true; imm = true; }",
            "else if (P.n.replace(/ \\d+$/, '') !== n) { P.n = uniqName(n, o.pid); ch = true; imm = true; }\n    else if (o.av && P.av !== String(o.av).slice(0, 4)) { P.av = String(o.av).slice(0, 4); ch = true; }", what='join-av')
    s = sub(s, "const c = G.cur, P = G.pl[o.pid], a = +o.a;\n    if (!P || !c || c.st !== 'open' || o.q !== c.qid || o.ik !== c.k || c.ans[o.pid] || !(a >= 0 && a < 4)) return;\n    c.ans[o.pid] = {a, ms:now() - c.t0}; ch = true;",
            """const c = G.cur, P = G.pl[o.pid], mq = c && AC.q(c.qid).type === 'multi';
    let a = +o.a;
    if (mq) { const nI = AC.q(c.qid).items.length; a = Array.isArray(o.a) ? o.a.map(x => +x) : null; if (!a || a.length !== nI || !a.every(x => x >= -1 && x < 4) || a.every(x => x < 0)) return; }
    else if (!(a >= 0 && a < 4)) return;
    if (!P || !c || c.st !== 'open' || o.q !== c.qid || o.ik !== c.k || c.ans[o.pid]) return;
    c.ans[o.pid] = {a, ms:now() - c.t0}; ch = true;""", what='answer')
    s = sub(s, "  else if (o.k === 'W') {", """  else if (o.k === 'R') {   // signalement (non anonyme, à approuver par l'enseignant)
    const P = G.pl[o.pid]; G.reports = G.reports || [];
    if (o.id && !G.reports.some(r => r.id === o.id)) G.reports.push({id:String(o.id).slice(0, 20), pid:o.pid, n:String(o.n || (P && P.n) || '?').slice(0, 16), qid:String(o.qid || '').slice(0, 8), page:+o.page || 0, type:String(o.type || '').slice(0, 60), txt:String(o.txt || '').slice(0, 500), ts:+o.ts || now(), from:'joueur', st:'à approuver'});
    ch = true; imm = true;
  }
  else if (o.k === 'W') {""", what='report')
    # PowerPoint : page de correction « Qnn:c »
    s = sub(s, "function drive(n, tag) {", """function drive(n, tag) {
  const cm = tag && /^(Q\\d+):c$/.exec(tag);
  if (cm) {   // page de correction : ferme et corrige la Question en cours
    G.lastSlide = {n:n || null, gid:null, qid:cm[1], ts:now()};
    if (G.cur && G.cur.qid === cm[1] && G.cur.st !== 'rev') { reveal(); ui.note = 'Page ' + (n || '') + ' : Question ' + AC.num(cm[1]) + ' corrigée.'; commit(true); } else commit(false);
    return;
  }""", what='drive')
    # correction
    s = sub(s, "function reveal() {", "function revealPlaceholder() {}\nfunction reveal() {", what='reveal-anchor')
    s = sub(s, "  if (AC.q(c.qid).type === 'cloud') return revealCloud(c, AC.q(c.qid));", "  if (AC.q(c.qid).type === 'cloud') return revealCloud(c, AC.q(c.qid));\n  if (AC.q(c.qid).type === 'multi') return revealMulti(c, AC.q(c.qid));\n  if (AC.q(c.qid).sondage) return revealSondage(c);", what='reveal')
    # joueurs fictifs
    s = sub(s, "  Object.keys(G.pl).filter(p => G.pl[p].bot && !c.ans[p]).forEach(p => {\n    const good = Math.random() < 0.65,",
            "  if (AC.q(c.qid).type === 'multi') { Object.keys(G.pl).filter(p => G.pl[p].bot && !c.ans[p]).forEach(p => { c.ans[p] = {a:rep.map(x => Math.random() < 0.65 ? x : [0, 1, 2, 3].filter(y => y !== x)[Math.floor(Math.random() * 3)]), ms:Math.round(1500 + Math.random() * c.dur * 650)}; }); commit(true); return; }\n  Object.keys(G.pl).filter(p => G.pl[p].bot && !c.ans[p]).forEach(p => {\n    const good = rep >= 0 && Math.random() < 0.65,", what='bots')
    # exports
    s = sub(s, "+ text], {type:'text/csv;charset=utf-8'}", "+ text + '\\r\\n© 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés.'], {type:'text/csv;charset=utf-8'}", what='dl')
    s = sub(s, "qq.type === 'cloud' ? cs((r.w || []).join(', ') || '—') : (r.a >= 0 ? AC.LET[r.a] : '—'), qq.type === 'cloud' ? cs('(nuage de mots)') : AC.LET[SEC.q[q][0]],", "ansTxt(qq, r), keyTxt(qq, q),", what='csv-row')
    s = sub(s, "Object.keys(x.res).filter(q => x.res[q].a >= 0 ||", "Object.keys(x.res).filter(q => Array.isArray(x.res[q].a) || x.res[q].a >= 0 ||", what='csv-n')
    s = s.replace("LANLive_classement_", "25_classement_").replace("LANLive_detail_", "25_detail_")
    # interface
    s = sub(s, "['corr', 'Corrigés'], ['guide', 'Guide']];", "['corr', 'Corrigés'], ['sign', 'Signalements (' + (G.reports || []).length + ')'], ['guide', 'Guide']];", what='tabs')
    s = sub(s, "tab === 'corr' ? corrTab() : guideTab();", "tab === 'corr' ? corrTab() : tab === 'sign' ? signTab() : guideTab();", what='render')
    s = sub(s, '<h1 style="margin:0">LAN Live ${G.test', '<h1 style="margin:0">Jeu 25 · TDC ${G.test', what='h1')
    s = sub(s, '<button class="btn alt sm" onclick="window.exportCSV()">Exporter CSV</button></div>', '<button class="btn alt sm" onclick="window.exportCSV()">Exporter CSV</button><button class="btn red sm" onclick="window.nouvellePartie()">↺ Nouvelle partie</button></div>', what='np')
    s = sub(s, '<h1>LAN Live · Tour de contrôle</h1><p class="muted">Sécurité des accès : ACL, VLAN, annuaires, protocoles (UCUE-S5-4-1)</p>', '<h1>Jeu 25 · Tour de contrôle</h1><p class="muted">Modèles de contrôle d’accès (UCUE-S5-4-1, partie 2)</p>', what='start')
    s = sub(s, "<h2>Question ${AC.num(c.qid)} · diapo ${q.sl} / ${AC.PUB.total} · ${AC.esc(g.titre)}", "<h2>Question ${AC.num(c.qid)} · page ${q.sl} · ${AC.esc(g.titre)}", what='pilot-h2')
    s = sub(s, "${q.type === 'cloud' ? cloudPanel(c) : ''}${q.opts.map((o, i) =>", "${q.type === 'cloud' ? cloudPanel(c) : ''}${q.type === 'multi' ? multiPanel(c, q) : q.opts.map((o, i) =>", what='pilot-opts')
    s = sub(s, "${q.type === 'cloud' ? '' : `<span class=\"ok\">Bonne réponse :", "${q.type === 'cloud' || q.type === 'multi' || rep < 0 ? '' : `<span class=\"ok\">Bonne réponse :", what='pilot-ok')
    s = sub(s, "${AC.esc(SEC.q[c.qid][1])}${detHtml(SEC.q[c.qid][3], true)}</div></div>`;", "${q.type === 'multi' ? '' : AC.esc(SEC.q[c.qid][1])}${detHtml(SEC.q[c.qid][3], true)}${detBtn(c.qid)}</div></div>`;", what='pilot-det')
    s = sub(s, "ils scannent ce QR code ou tapent l’adresse", "ils ouvrent d’abord sur leur PC l’adresse", what='guide-li')
    s = sub(s, ", puis saisissent un pseudo. <b>${nPl()}</b>", ", puis choisissent un avatar et un pseudo (le QR code, étiqueté « secours téléphone », ne sert qu’en secours : un joueur n’est pas compté deux fois s’il change d’appareil). <b>${nPl()}</b>", what='guide-li2')
    s = sub(s, '<div style="width:190px;background:#fff;padding:8px;border-radius:10px">${qrSvg(u, 180)}</div>', '<div style="width:190px"><div style="background:#fff;padding:8px;border-radius:10px">${qrSvg(u, 180)}</div><div class="muted" style="text-align:center">▲ secours téléphone</div></div>', what='guide-qr')
    # fonctions nouvelles : remplace corrTab d'origine
    i = s.index('function corrTab() {'); j = s.index('function guideTab() {')
    s = s[:i] + TDC_JS + s[j:]
    return s
