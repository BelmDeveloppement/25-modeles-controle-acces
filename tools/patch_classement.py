# © 2026 SAS BELM DEVELOPPEMENT. Tous droits réservés. Correctifs de l'écran PROJECTION.
def patch_classement(s):
    # classement : avatars + barres de progression (symbole ● / rang en plus de la couleur)
    i = s.index('function board() {'); j = s.index('const flag = c =>')
    s = s[:i] + r'''function board() {
  if (!pub || !pub.lb.length) return `<div class="card"><h2>Classement</h2><p class="muted">En attente des premiers points…</p></div>`;
  const medal = ['🥇', '🥈', '🥉'], mx = Math.max(1, ...pub.lb.map(x => x[1])), COL = ['#56B4E9', '#FF8A3D', '#F0E442'];
  return `<div class="card"><h2>Classement</h2>${pub.lb.map((x, i) => `<div style="margin:7px 0"><div style="display:flex;align-items:center;gap:10px;font-size:22px"><span style="width:40px;text-align:center">${medal[i] || '<b>' + (i + 1) + '</b>'}</span><span style="font-size:30px">${AC.avHtml(x[4])}</span><b style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${AC.esc(x[0])}</b><span class="muted">${x[3]} ✔</span><b class="pts mono">${x[1]}</b></div><div style="height:14px;background:#10203a;border:1px solid #1F3556;border-radius:8px;overflow:hidden"><div style="height:100%;width:${Math.max(2, Math.round(100 * x[1] / mx))}%;background:${COL[i % 3]};${i % 3 === 2 ? '' : ''}"></div></div></div>`).join('')}</div>`;
}
''' + s[j:]
    # en-tête : Question N · page p
    old = '<span class="tag" style="font-size:18px">diapo ${c.sl} / ${c.tot}</span>'
    assert s.count(old) == 1; s = s.replace(old, '<span class="tag" style="font-size:18px">page ${c.sl} / ${c.tot}</span>')
    # Questions à plusieurs réponses et sondage
    old = "  const rev = c.st === 'rev' && pub.rev, mx = rev ? Math.max(1, ...pub.rev.cnt) : 1;\n"
    assert s.count(old) == 1
    s = s.replace(old, r'''  if (q.type === 'multi') {
    const rv = c.st === 'rev' && pub.rev;
    h += q.items.map((it, ii) => `<div style="margin:8px 0"><b style="font-size:22px">${ii + 1}. ${AC.esc(it.t)}</b>${it.o.map((o, i) => { const g = rv && i === pub.rev.rep[ii], tot = rv ? Math.max(1, ...pub.rev.cnt[ii]) : 1; return `<div class="opt ${rv ? (g ? 'good' : 'dim') : ''}" style="--oc:${AC.LCOL[i]};font-size:19px;cursor:default;padding:4px 10px;margin:3px 0"><span class="lt">${AC.LET[i]}</span><span style="flex:1">${AC.esc(o)} ${g ? '<b>✔</b>' : ''}</span>${rv ? `<span class="bar" style="width:${Math.round(110 * pub.rev.cnt[ii][i] / tot)}px;background:${AC.LCOL[i]}"></span><b class="mono">${pub.rev.cnt[ii][i]}</b>` : ''}</div>`; }).join('')}</div>`).join('');
    if (c.st !== 'rev') h += flag(c) + `<p style="font-size:24px"><b>${c.done.length}</b> / ${pub.np} réponses reçues</p>`;
    return h + '</div>';
  }
  const rev = c.st === 'rev' && pub.rev, mx = rev ? Math.max(1, ...pub.rev.cnt) : 1;
''')
    old = "${rev ? (i === pub.rev.rep ? 'good' : 'dim') : ''}"
    assert s.count(old) == 1; s = s.replace(old, "${rev && pub.rev.rep >= 0 ? (i === pub.rev.rep ? 'good' : 'dim') : ''}")
    # QR : PC d'abord, QR « secours téléphone »
    i = s.index("  if (!c) return `<div class=\"card\" style=\"text-align:center\"><h1 style=\"font-size:40px\">Rejoignez la séance</h1>")
    j = s.index('  const q = AC.q(c.qid);', i)
    s = s[:i] + r'''  if (!c) return `<div class="card" style="text-align:center"><h1 style="font-size:40px">Rejoignez la séance</h1><p style="font-size:24px;margin:.3em 0">Sur votre <b>PC</b>, ouvrez cette adresse :</p>
    <p class="mono" style="font-size:26px;color:#29D3FF;word-break:break-all"><b>${AC.esc(joinUrl())}</b></p><p style="font-size:22px">Choisissez un avatar, saisissez votre pseudo.</p>
    <div style="width:170px;margin:10px auto 0;background:#fff;padding:6px;border-radius:10px">${qrSvg(joinUrl(), 158)}</div><p class="muted" style="font-size:18px;margin:4px 0">▲ secours téléphone (le PC d’abord)</p><p style="font-size:30px"><b>${pub.np}</b> connecté${pub.np > 1 ? 's' : ''}</p></div>`;
''' + s[j:]
    return s
# --- test final (règle 33) : la projection n'affiche qu'un compteur et le classement par pseudos, jamais de noms
_pc = patch_classement
def patch_classement(s):
    s = _pc(s)
    s = sub(s, "function render() { $('root').innerHTML", "const tfBanner = () => pub && pub.tf && pub.tf.st ? `<div class=\"card\" style=\"font-size:26px;margin-bottom:12px\"><b>Test final ${pub.tf.st === 'open' ? '● en cours' : '■ clos'}</b> · ✓ ${(pub.tf.done || []).length} terminé(s) sur ${pub.tf.np}</div>` : '';\nfunction render() { $('root').innerHTML", what='tf-banner')
    s = sub(s, "<div>${left()}</div>", "<div>${tfBanner()}${left()}</div>", what='tf-left')
    return s
