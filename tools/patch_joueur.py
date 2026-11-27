# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés. Correctifs de l'écran JOUEUR.
JOUEUR_JS = r'''
/* ---------- jeu 25 : Questions à plusieurs réponses ---------- */
window.pickM = (ii, i) => { const k = key(); if (sent[k] !== undefined) return; const a = draft[k] = draft[k] || []; a[ii] = i; render(); };
window.validM = () => {
  const k = key(); if (sent[k] !== undefined || !pub || !pub.cur || pub.cur.st !== 'open') return;
  const q = AC.q(pub.cur.qid), n = q.items.length, d = draft[k] || [], a = q.items.map((_, i) => d[i] === undefined ? -1 : d[i]), got = a.filter(x => x >= 0).length;
  if (!got) return;
  if (got < n && !confirm('Vous avez répondu à ' + got + ' demande(s) sur ' + n + '. Valider quand même ? Les autres ne rapporteront aucun point.')) return;
  sent[k] = a; save(); send({k:'A', q:pub.cur.qid, ik:pub.cur.k, a}); render();
};
function multiBody(c, q, k, already) {
  const n = q.items.length, sv = sent[k], ch = Array.isArray(sv) ? sv : (draft[k] || []);
  const rev = c.st === 'rev' && pub.rev, rep = rev ? pub.rev.rep : [], my = rev ? pub.rev.r[me.pid] : null, mine = my ? my[0] : ch;
  let h = `<p class="muted" style="margin:0 0 4px">${n} réponses à donner : 1 point par réponse exacte (${AC.BASE} points chacune).</p>`;
  q.items.forEach((it, ii) => {
    h += `<div class="card" style="margin:8px 0;padding:10px 12px"><b>${ii + 1}. ${AC.esc(it.t)}</b>`;
    it.o.forEach((o, i) => {
      let cls = 'opt';
      if (rev) cls += i === rep[ii] ? ' good' : (i === mine[ii] ? ' bad' : ' dim'); else if (ch[ii] === i) cls += ' sel';
      const dis = rev || c.st !== 'open' || already;
      h += `<button class="${cls}" style="--oc:${AC.LCOL[i]};padding:8px 10px;margin:5px 0" ${dis ? 'disabled' : ''} onclick="pickM(${ii},${i})"><span class="lt">${AC.LET[i]}</span><span style="flex:1">${AC.esc(o)}</span>${rev && i === rep[ii] ? '<b class="ok">✔ bonne réponse</b>' : ''}${rev && i === mine[ii] && i !== rep[ii] ? '<b class="ko">✗ votre réponse</b>' : ''}</button>`;
    });
    if (rev) h += `<div class="muted" style="margin-top:4px">${AC.esc(pub.rev.exp[ii])}</div>`;
    h += '</div>';
  });
  if (c.st === 'open') {
    const got = (ch || []).filter(x => x !== undefined && x >= 0).length;
    h += already ? `<p class="ok" style="margin:10px 0 0">✔ Réponses envoyées. Attendez la correction.</p>`
      : `<button id="vb" class="btn go xl" style="margin-top:8px" ${got ? '' : 'disabled'} onclick="validM()">Valider mes réponses (${got} sur ${n})</button>`;
  } else if (c.st === 'closed') h += `<p class="muted" style="margin:10px 0 0">${already ? '✔ Réponses envoyées.' : '⏱ Temps écoulé : pas de réponse de votre part.'} Correction en attente…</p>`;
  else if (rev) {
    const R = my;
    if (!R) h += `<p class="muted" style="margin-top:10px">Vous n’aviez pas encore rejoint la séance pour cette Question.</p>`;
    else {
      const now_ = myRec() ? myRec()[0] : null, mv = R[7] && now_ ? R[7] - now_ : 0;
      h += `<div class="card" style="background:${R[9] ? '#0a2133;border-color:#56B4E9' : '#2b1806;border-color:#FF8A3D'};margin-top:10px"><b class="${R[9] ? 'ok' : 'ko'}" style="font-size:1.2em">${R[9] ? '✔' : '✗'} ${R[9]} bonne${R[9] > 1 ? 's' : ''} réponse${R[9] > 1 ? 's' : ''} sur ${n} <span class="gain">+${R[1]} pts</span></b></div>`;
      if (now_) h += `<p class="muted">Rang ${now_}${mv > 0 ? ' · ▲ +' + mv : mv < 0 ? ' · ▼ ' + mv : ' · ='}</p>`;
    }
    h += dtHtml(pub.rev.dt) ? `<div class="card" style="margin-top:8px"><h2>Pour retenir</h2>${dtHtml(pub.rev.dt)}</div>` : '';
  }
  return h;
}
/* ---------- jeu 25 : Rappel, Signaler ---------- */
const RQK = LS + '_rq';
let RQ = []; try { RQ = JSON.parse(localStorage.getItem(RQK) || '[]'); } catch (e) {}
const saveRQ = () => { try { localStorage.setItem(RQK, JSON.stringify(RQ.slice(-60))); } catch (e) {} };
function flushRQ() { if (!me.n) return; RQ.filter(r => !r.ack).slice(0, 10).forEach(r => send(Object.assign({k:'R'}, r, {ack: undefined}))); }
setInterval(flushRQ, 8000);
function lastQid() { return pub && pub.cur ? pub.cur.qid : (me.lq || ''); }
function rappelHtml() {
  const qid = lastQid(); if (!qid || !AC.q(qid)) return '<p class="muted">Aucune Question en cours : le rappel s’affichera dès qu’une Question est ouverte.</p>';
  const q = AC.q(qid);
  return `<p class="muted">Question ${AC.num(qid)} · page ${q.sl}</p><pre class="ctx" style="white-space:pre-wrap;font-size:15px">${AC.esc(q.rap || q.txt)}</pre>`;
}
function signalHtml() {
  const qid = lastQid(), q = qid && AC.q(qid), mine = RQ.slice(-5).reverse();
  return `<p>Signaler un problème (erreur, réponse discutable, énoncé ambigu). Votre <b>pseudo est joint</b> (${AC.esc(me.n || '?')}). L’enseignant approuve ou rejette chaque signalement en fin de séance. Fonctionne même avec une connexion instable : l’envoi est retenté.</p>
   <p class="muted">${q ? 'Question ' + AC.num(qid) + ' · page ' + q.sl : 'Aucune Question en cours : le signalement sera général.'}</p>
   <select id="sg_t" style="width:100%;padding:10px;background:#050A14;color:#E8F1FF;border:2px solid #1F3556;border-radius:10px"><option>Erreur dans l’énoncé ou la correction</option><option>Réponse discutable</option><option>Énoncé ambigu ou incomplet</option><option>Problème d’affichage ou de connexion</option><option>Autre</option></select>
   <textarea id="sg_x" rows="4" maxlength="500" placeholder="Décrivez le problème en une ou deux phrases" style="width:100%;margin-top:8px;padding:10px;background:#050A14;color:#E8F1FF;border:2px solid #1F3556;border-radius:10px"></textarea>
   <p><button class="btn go" onclick="sendSignal()">Envoyer le signalement</button></p>
   ${mine.length ? `<h3>Mes signalements</h3>${mine.map(r => `<div class="muted" style="margin:4px 0">${r.ack ? '✔ reçu par l’enseignant' : '● envoi en attente'} · ${AC.esc(r.type)} · ${AC.esc(r.txt.slice(0, 60))}</div>`).join('')}` : ''}`;
}
window.sendSignal = () => {
  const txt = ($('sg_x').value || '').trim(); if (!txt) { $('sg_x').focus(); return; }
  const qid = lastQid(), q = qid && AC.q(qid);
  RQ.push({id:'r' + AC.rid(8), pid:me.pid, n:me.n, qid:qid || '', page:q ? q.sl : 0, type:$('sg_t').value, txt, ts:Date.now()}); saveRQ(); flushRQ(); renderFx();
};
function fxHtml() {
  const S = sheet === 'rappel' ? {t:'Rappel', h:rappelHtml()} : sheet === 'signal' ? {t:'Signaler', h:signalHtml()} : sheet ? AC.INFO[sheet] : null;
  const dis = pub && pub.test_final;
  const B = (k, t) => `<button class="btn alt ${sheet === k ? 'on' : ''}" ${k === 'rappel' && dis ? 'disabled' : ''} onclick="sheetTo('${k}')">${t}</button>`;
  return `${S ? `<div class="sheet"><h2 class="mono" style="color:#29D3FF">${AC.esc(S.t)}</h2>${S.h}<p><button class="btn alt" onclick="sheetTo('${sheet}')">Fermer</button></p></div>` : ''}
   <div class="fxbar" style="flex-wrap:wrap">${B('rappel', '↩ Rappel')}${B('signal', '⚑ Signaler')}${B('translor', '🏢 TransLor')}${B('jeu', '🎮 Le jeu')}${B('aide', '❓ Aide')}</div>`;
}
function lb() {
  if (!pub || !pub.lb || !pub.lb.length) return '';
  const r = myRec(), mx = Math.max(1, ...pub.lb.map(x => x[1]));
  const row = (rk, x, me_) => `<tr class="${me_ ? 'me' : ''}"><td class="rk">${rk}</td><td>${AC.avHtml(x[4])} ${AC.esc(x[0])}${me_ ? ' (vous)' : ''}<div class="cable" style="margin-top:3px;height:10px"><div style="width:${Math.max(4, Math.round(100 * x[1] / mx))}%"></div></div></td><td class="muted">${x[3]} ✔</td><td class="pts">${x[1]}</td></tr>`;
  const rows = pub.lb.map((x, i) => row(i + 1, x, r && r[0] === i + 1)).join('');
  const extra = r && r[0] > pub.lb.length ? row(r[0], [me.n, r[1], 0, '', me.av], true) : '';
  return `<div class="card"><h2>Classement</h2><table class="lb">${rows}${extra}</table></div>`;
}
'''
def patch_joueur(s):
    # inscription : avatar, reprise de partie (changement d'appareil)
    s = sub(s, '<h1 class="mono" style="color:#29D3FF">LAN LIVE</h1><p>Sécurité des accès : ACL, VLAN, annuaires, protocoles.</p>',
            '<h1 class="mono" style="color:#29D3FF">JEU 25</h1><p>Modèles de contrôle d’accès : DAC, MAC, RBAC, ABAC…</p>', what='accueil')
    s = sub(s, '<p>Votre pseudo :</p>', '''<p>Votre avatar :</p><div id="avs" style="display:flex;flex-wrap:wrap;gap:6px">${AC.AV.map(a => `<button class="btn alt sm" style="font-size:1.5em;padding:.15em .4em;${(me.av || AC.AV[0]) === a ? 'outline:3px solid #56B4E9' : ''}" onclick="setAv('${a}')">${a}</button>`).join('')}</div><p>Votre pseudo :</p>''', what='avatar')
    s = sub(s, '<input id="nm" maxlength="16"', '<input id="nm" value="${AC.esc(me.last || \'\')}" maxlength="16"', what='nm-prefill')
    s = sub(s, '<p id="err" class="ko"></p>', '<label class="muted" style="display:block;margin:8px 0"><input type="checkbox" id="re"> Je reprends ma partie (j’ai changé d’appareil : même pseudo)</label><p id="err" class="ko"></p>', what='reprise')
    s = sub(s, "me.n = n; save(); send({k:'J', n});", "me.n = n; me.av = me.av || AC.AV[0]; save(); send({k:'J', n, av:me.av, re:$('re') && $('re').checked ? 1 : 0});", what='join')
    s = sub(s, "window.join = () => {", "window.setAv = a => { me.av = a; save(); const n = $('nm') ? $('nm').value : ''; render(); if ($('nm')) $('nm').value = n; };\nwindow.join = () => {", what='setAv')
    s = sub(s, "send({k:'J', n:me.n}); }   // le PC enseignant", "send({k:'J', n:me.n, av:me.av || ''}); }   // le PC enseignant", what='rejoin')
    # réception : nouvelle partie, accusés de signalement
    s = sub(s, "AC.Assembler(s => { pub = s; recvAt = Date.now(); status = 'connecté'; render(); })",
            "AC.Assembler(s => { pub = s; recvAt = Date.now(); status = 'connecté'; if (pub.gen && me.gen !== pub.gen) { if (me.gen && me.n) { me.last = me.n; me.n = ''; } me.gen = pub.gen; sent = {}; draft = {}; save(); } if (pub.cur) { me.lq = pub.cur.qid; } (pub.rk || []).forEach(id => { const r = RQ.find(x => x.id === id); if (r && !r.ack) { r.ack = 1; saveRQ(); } }); render(); })", what='assembler')
    # bandeau : Question N · page p
    s = sub(s, '<span class="tag" style="font-size:1.05em"><b>Question ${AC.num(c.qid)}</b> · ${AC.esc(c.gt)}</span><span class="tag">diapo ${c.sl} / ${c.tot}</span>',
            '<span class="tag" style="font-size:1.05em"><b>Question ${AC.num(c.qid)}</b> · page ${c.sl}</span>', what='bandeau')
    s = sub(s, "if (q.type === 'cloud') return h + cloudBody(c, q, k, already) + '</div>';", "if (q.type === 'cloud') return h + cloudBody(c, q, k, already) + '</div>';\n  if (q.type === 'multi') return h + multiBody(c, q, k, already) + '</div>';", what='multi')
    # sondage (Question 1) : pas de bonne réponse
    s = sub(s, "if (rev) { cls += i === rep ? ' good' : (i === mine ? ' bad' : ' dim'); }", "if (rev) { cls += i === rep ? ' good' : (rep < 0 ? (i === mine ? ' sel' : ' dim') : (i === mine ? ' bad' : ' dim')); }", what='sondage-cls')
    s = sub(s, 'h += R[2] ? `<div class="card" style="background:#0a2133;border-color:#56B4E9;margin-top:10px">', 'h += q.sondage ? `<div class="card" style="margin-top:10px"><b>● Sondage : pas de bonne réponse, pas de points.</b></div>` : R[2] ? `<div class="card" style="background:#0a2133;border-color:#56B4E9;margin-top:10px">', what='sondage-card')
    s = sub(s, '<b class="mono" style="color:#29D3FF">LAN LIVE</b>', '<b class="mono" style="color:#29D3FF">JEU 25</b>', what='topbar')
    s = sub(s, '<div class="muted">${AC.esc(me.n || \'\')}</div>', "<div class=\"muted\">${AC.avHtml(me.av)} ${AC.esc(me.n || '')}</div>", what='topbar-name')
    # fonctions nouvelles : avant lb() / fxHtml() d'origine (remplacées)
    i = s.index('function fxHtml() {'); j = s.index('function renderFx()')
    s = s[:i] + s[j:]
    i = s.index('function lb() {'); j = s.index('function qView() {')
    s = s[:i] + JOUEUR_JS + s[j:]
    return s
# --- test final (règle 33)
_pj = patch_joueur
def patch_joueur(s):
    s = _pj(s)
    i = s.index('function lb() {')
    s = s[:i] + open(os.path.join(R, 'tools', 'test_player.js'), encoding='utf8').read() + '\n' + s[i:]
    s = sub(s, "  if (sheet) { dirty = true; return; }\n", "  if (sheet) { dirty = true; return; }\n  if (me.n && pub && pub.tf && pub.tf.st && tRender()) return;\n", what='render-test')
    return s
