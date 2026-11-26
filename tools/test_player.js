/* ---------- jeu 25 : test final noté (règle 33), côté JOUEUR ---------- */
/* © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés. */
const tb64e = u => btoa(String.fromCharCode.apply(null, new Uint8Array(u)));
const tb64d = s => Uint8Array.from(atob(s), c => c.charCodeAt(0));
const tseed = str => { let h = 1779033703 ^ str.length; for (let i = 0; i < str.length; i++) { h = Math.imul(h ^ str.charCodeAt(i), 3432918353); h = h << 13 | h >>> 19; } return h >>> 0; };
const trng = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const tshuf = (arr, r) => { const a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const LST = LS + '_t';
let TST = {}; try { TST = JSON.parse(localStorage.getItem(LST) || '{}'); } catch (e) {}
const tsave = () => { try { localStorage.setItem(LST, JSON.stringify(TST)); } catch (e) {} };
AC.BANKI = {}; AC.BANK.q.forEach(q => { AC.BANKI[q[0]] = q; });
let tLastSend = 0, tTimer = null;
async function tEnc(obj) {   // chiffrement ECDH P-256 + AES-GCM vers la clé publique du TDC : le relais ne voit rien
  const pk = await crypto.subtle.importKey('raw', tb64d(pub.tf.pk), {name:'ECDH', namedCurve:'P-256'}, false, []);
  const kp = await crypto.subtle.generateKey({name:'ECDH', namedCurve:'P-256'}, true, ['deriveKey']);
  const k = await crypto.subtle.deriveKey({name:'ECDH', public:pk}, kp.privateKey, {name:'AES-GCM', length:256}, false, ['encrypt']);
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = await crypto.subtle.encrypt({name:'AES-GCM', iv}, k, new TextEncoder().encode(JSON.stringify(obj)));
  return {e:tb64e(await crypto.subtle.exportKey('raw', kp.publicKey)), iv:tb64e(iv), c:tb64e(ct)};
}
const tAnswered = () => Object.keys(TST.r || {}).length;
async function tSend(fin) {
  if (!pub || !pub.tf || !pub.tf.pk) return;
  tLastSend = Date.now();
  try { const m = await tEnc({ts:Date.now(), idn:TST.idn, r:TST.r || {}, fin:fin ? 1 : 0}); send(Object.assign({k:fin ? 'T' : 'TP', n:tAnswered()}, m)); } catch (e) {}
}
const tLater = () => { clearTimeout(tTimer); tTimer = setTimeout(() => tSend(false), 1500); };
const tOrder = () => tshuf(pub.tf.ids, trng(tseed(pub.tf.seed + ':' + me.pid + ':q')));
const tOpts = id => tshuf([0, 1, 2, 3], trng(tseed(pub.tf.seed + ':' + me.pid + ':' + id)));
window.tStart = () => {
  const a = ($('idn1').value || '').trim().slice(0, 40), b = ($('idn2').value || '').trim().slice(0, 40);
  if (!a || !b) { $('terr').textContent = 'Saisissez votre nom et votre prénom.'; return; }
  TST.idn = [a, b]; TST.i = 0; tsave(); tSend(false); render();
};
window.tPick = (id, v) => { if (TST.fin) return; TST.r = TST.r || {}; TST.r[id] = v; tsave(); tLater(); render(); };
window.tGo = i => { TST.i = i; tsave(); render(); window.scrollTo(0, 0); };
window.tValid = () => {
  const n = pub.tf.ids.length, got = tAnswered();
  if (!confirm('Valider le test est DÉFINITIF : vous ne pourrez plus modifier vos réponses.\n' + got + ' réponse(s) sur ' + n + ' (les autres compteront comme « Je ne sais pas »).\nValider ?')) return;
  TST.fin = 1; tsave(); tSend(true); render();
};
function tRender() {   // retourne true si l'écran est géré par le test final
  const t = pub.tf; if (!t || !t.st) return false;
  const a = document.activeElement; if (a && /^idn[12]$/.test(a.id)) { tinyStatus(); return true; }
  if (TST.seed !== t.seed) { TST = {seed:t.seed, r:{}, i:0, idn:TST.idn || null, fin:0}; tsave(); }
  const n = t.ids.length, done = (t.done || []).indexOf(me.pid) >= 0, act = (t.act || []).indexOf(me.pid) >= 0;
  if (done && !TST.fin) { TST.fin = 1; tsave(); }
  let h = topbar();
  if (TST.fin) {
    if (!done && Date.now() - tLastSend > 6000) tSend(true);
    h += `<div style="padding:12px"><div class="card" style="text-align:center"><h1 class="mono">Test final</h1><p style="font-size:1.3em"><b class="ok">✓ Test terminé</b></p>
      <p>${done ? '✓ Vos réponses sont bien enregistrées chez l’enseignant.' : '● Envoi de vos réponses à l’enseignant…'}</p><p class="muted">Votre note vous sera communiquée par l’enseignant. Vous pouvez fermer cette page.</p></div></div>`;
  } else if (t.st === 'closed') {
    h += `<div style="padding:12px"><div class="card" style="text-align:center"><h1 class="mono">Test final</h1><p>⏱ Le test est clos par l’enseignant.</p><p class="muted">Vos dernières réponses transmises ont été conservées.</p></div></div>`;
  } else if (!TST.idn) {
    h += `<div style="padding:12px"><div class="card"><h1 class="mono">Test final</h1>
      <p><b>${n} questions notées</b>, chacune avec 4 propositions et « Je ne sais pas ».</p>
      <ul><li>Bonne réponse : + 1 · mauvaise réponse : − 1/3 · « Je ne sais pas » : 0.</li><li>Pas de minuteur : travaillez à votre rythme.</li><li>Vous pouvez revenir sur vos réponses jusqu’au bouton « Valider le test », qui est <b>définitif</b>.</li><li>Le bouton « Rappel » est désactivé.</li></ul>
      <p>Pour la note, saisissez vos <b>nom et prénom</b> (distincts de votre pseudo). Ils ne sont ni affichés aux autres joueurs ni projetés : ils sont transmis chiffrés à l’enseignant seul.</p>
      <input id="idn1" maxlength="40" placeholder="Nom" style="width:100%;padding:12px;margin:4px 0;font-size:1.1em;background:#050A14;color:#E8F1FF;border:2px solid #1F3556;border-radius:10px">
      <input id="idn2" maxlength="40" placeholder="Prénom" style="width:100%;padding:12px;margin:4px 0;font-size:1.1em;background:#050A14;color:#E8F1FF;border:2px solid #1F3556;border-radius:10px" onkeydown="if(event.key==='Enter')tStart()">
      <p id="terr" class="ko"></p><button class="btn go xl" onclick="tStart()">Commencer le test</button></div></div>`;
  } else {
    if (!act && Date.now() - tLastSend > 8000) tSend(false);   // l’enseignant ne nous connaît pas encore : on se représente
    const ord = tOrder(), i = Math.min(Math.max(+TST.i || 0, 0), n - 1), id = ord[i], q = AC.BANKI[id], r = TST.r || {}, v = r[id];
    h += `<div style="padding:12px"><div class="card"><div style="display:flex;justify-content:space-between;flex-wrap:wrap"><b>Test final · Question ${i + 1} / ${n}</b><span class="muted">${tAnswered()} répondue(s) sur ${n}</span></div>
      <p style="font-size:1.1em;margin:.7em 0"><b>${AC.esc(q[3])}</b></p>`;
    tOpts(id).forEach((o, k) => { h += `<button class="opt${v === o ? ' sel' : ''}" style="--oc:${AC.LCOL[k]}" onclick="tPick('${id}',${o})"><span class="lt">${AC.LET[k]}</span><span style="flex:1">${AC.esc(q[4][o])}</span>${v === o ? '<b>✓</b>' : ''}</button>`; });
    h += `<button class="opt${v === -1 ? ' sel' : ''}" style="--oc:#9fb3d1" onclick="tPick('${id}',-1)"><span class="lt">?</span><span style="flex:1">Je ne sais pas (0 point)</span>${v === -1 ? '<b>✓</b>' : ''}</button>
      <div style="display:flex;gap:8px;margin-top:10px"><button class="btn alt" ${i ? '' : 'disabled'} onclick="tGo(${i - 1})">◀ Précédente</button><button class="btn alt" ${i < n - 1 ? '' : 'disabled'} onclick="tGo(${i + 1})">Suivante ▶</button></div></div>
      <div class="card" style="margin-top:10px"><b>Mes réponses</b> <span class="muted">(✓ répondue · ? je ne sais pas · ○ pas encore)</span><div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px">`;
    ord.forEach((x, j) => { const y = r[x]; h += `<button class="btn alt sm" style="${j === i ? 'outline:3px solid #F0E442;' : ''}" onclick="tGo(${j})">${j + 1} ${y === undefined ? '○' : y === -1 ? '?' : '✓'}</button>`; });
    h += `</div></div><button class="btn go xl" style="margin-top:10px" onclick="tValid()">Valider le test (${tAnswered()} réponse(s) sur ${n}) · définitif</button></div>`;
  }
  $('app').innerHTML = h + `<div class="foot" style="padding-bottom:64px">${AC.FOOT}<br><span id="st">${status}</span></div><div id="fx">${fxHtml()}</div>`;
  return true;
}
