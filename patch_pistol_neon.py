#!/usr/bin/env python3
"""Usage:  python3 patch_pistol_neon.py index.html
Creates index_new.html next to it (the original is left untouched)."""
import re, sys, os

src = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(src, encoding='utf-8').read()
miss = []

def R(old, new, all_=True):
    global s
    if old not in s:
        miss.append(old[:70]); return
    s = s.replace(old, new) if all_ else s.replace(old, new, 1)

def RX(pat, new):
    global s
    s, n = re.subn(pat, new, s)
    if not n: miss.append(pat[:70])

# ---------- 1) emojis: replace the useful ones with text, strip the rest ----------
R('title="Pause (P)">⏸</div>', 'title="Pause (P)">II</div>')
R('<span class="ai">📺</span>', '<span class="ai">▶</span>')
R('id="td">⚡<small>Q</small>', 'id="td">»<small>Q</small>')
R('id="tf">🔫<small>ENTER</small>', 'id="tf">●<small>ENTER</small>')
R('.tile::before{content:"👆";position:absolute;bottom:2px;right:8px;font-size:18px;animation:hand 1.2s ease-in-out infinite}', '')
R('<p class="tap"><span>👆</span> Tap a weapon to choose it</p>', '<p class="tap">Tap a weapon to equip it instantly</p>')
R("' · 👁 '", "' · HAKI '")
R("['👆','TAP TO FIRE'", "['TAP','TAP TO FIRE'")
RX(r"\['🖱\uFE0F?','CLICK TO FIRE'", "['CLICK','CLICK TO FIRE'")
R("['💥','USE RECOIL'", "['KICK','USE RECOIL'")
R("['🔴','DODGE THE LASER'", "['LASER','DODGE THE LASER'")
R("['⚡','DASH'", "['Q','DASH'")
R('Q or the ⚡ button', 'Q or the » button')
R('⏸ pause.', 'II pause.')
R('⭐', '★')
R("lk?'🔒'", "lk?'—'")
R('<div class="ti">📋</div>', '<div class="ti">≡</div>')
R("' ☠ '+BN[", "' · '+BN[")
RX(r"<h2>[^A-Za-z<]{1,6}NEW: '\+WP\[nl\]", "<h2>NEW: '+WP[nl]")
R('🔒', '×')
KEEP = set('♥★⛶')
emo = re.compile('[\U0001F000-\U0001FAFF\u2600-\u26FF\u2700-\u27BF\u2B50\u23E9-\u23FA\uFE0F\u200D\uFFFD]')
s = emo.sub(lambda m: m.group(0) if m.group(0) in KEEP else '', s)

# ---------- 2) weapons sorted by unlock level + tap = equip ----------
R('function weapons(from,sel){',
  "const ulv=i=>{const w=WP[i];return w.ul||(w.bx?14:2*i)},WORD=()=>WP.map((w,i)=>i).sort((a,b)=>ulv(a)-ulv(b)||a-b);\n"
  "function weapons(from,sel){", False)
R('const tiles=WP.map((x,i)=>{const u=ok(i);return', 'const tiles=WORD().map(i=>{const x=WP[i],u=ok(i);return', False)
R('<small>${x.n}</small></button>', "<small>${u?x.n:x.n+' · Lv '+ulv(i)}</small></button>", False)
R("PN.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>weapons(from,+b.dataset.s));",
  "PN.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{const q=+b.dataset.s;"
  "if(ok(q)&&(q!==SV.wp||(TW&&TW.lvl===lvl&&from==='pause'))){au();tone(700,.08,'triangle',.12,1000);"
  "SV.wp=q;SV.seen=Math.max(SV.seen,q+1);sw(q);save();"
  "if(from==='pause'){TW=null;hide();loadLevel(lvl);return}bg()}weapons(from,q)});", False)
R("""<button class="o" id="eqp"${un&&!cur?'':' disabled'}>${cur?'EQUIPPED':un?'EQUIP':'LOCKED'}</button>""",
  """<div class="eqs">${un?'EQUIPPED':'LOCKED'}</div>""", False)
RX(r"\s*\$\('eqp'\)\.onclick=.*?renderMenu\(\)\}\}\}", "}")
R('</style>', '.eqs{flex:1;display:flex;align-items:center;justify-content:center;font-weight:800;letter-spacing:1px;color:var(--gd);border:2px solid var(--ln);border-radius:10px}\n</style>', False)

# ---------- 3) bosses: much more health, gradual, damage capped per hit ----------
R('hp=10+6*(t-1),bt=', 'hp=Math.round(60+40*(t-1)+4*(t-1)*(t-1)),bt=', False)
R('let dd=e.boss&&b.bd?b.bd:(b.dm||1);', 'let dd=e.boss&&b.bd?b.bd:(b.dm||1);if(e.boss)dd=Math.min(dd,7);', False)
R('if(q.boss)q.hp-=(bdm==null?2:bdm);', 'if(q.boss)q.hp-=Math.min(7,bdm==null?2:bdm);', False)
R('Math.ceil(e.mh*.3)', 'Math.ceil(e.mh*.15)', False)
R('hits bosses for 30% of their health', 'hits bosses for 15% of their health', False)
R('if(e.pz>0&&(e.pz-=dt,',
  "if(e.boss&&!e.en2&&e.hp<=e.mh*.5){e.en2=1;e.iv*=.72;e.sf*=1.2;msg('BOSS ENRAGED!',1.3,'gold');addRing(e.x,e.y,6,0xff2a55);spawn(e.x,e.y,0xff2a55,30,14,.22);shake=1;tone(70,.6,'sawtooth',.3,30)}"
  "if(e.pz>0&&(e.pz-=dt,", False)
R('gain(e);spawn(e.x,e.y,0xff7b3d,22,9);', 'gain(e);if(e.boss)bossDrop(e);spawn(e.x,e.y,0xff7b3d,22,9);', False)

# ---------- 4) better pacing: more drops, level modifiers, music ----------
R('k=r<.07&&P.hp<3?0:r<.14?1:r<.22?2:-1', 'k=r<.1&&P.hp<3?0:r<.2?1:r<.3?2:-1', False)
R('P.vy-=20*dt;const sp=', 'P.vy-=(window.GRV||20)*dt;const sp=', False)

EXTRA = r"""
<script>
/* ===== EXPERIENCE PACK: level modifiers, boss rewards, music ===== */
var GRV=20;
(function(){
const _ll=loadLevel;
loadLevel=function(n,retry){_ll.apply(this,arguments);GRV=20;let t='';
 if(n>=5&&n%10){const m=n%4;
  if(m===1){GRV=13;t='LOW GRAVITY'}
  else if(m===3){en.forEach(e=>{if(e.t!==5&&e.t!==10)e.iv*=.82});t='FAST ENEMIES'}}
 if(t)msg('LEVEL '+n+' · '+t,1.8)};
window.dropPk=function(x,y,k){const m=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color:[0xff5470,0x4dfff0,0xffd166][k]}));m.scale.setScalar(.3);m.position.set(x,y,0);scene.add(m);pk.push({m:m,x:x,y:y,l:12,k:k})};
window.bossDrop=function(e){dropPk(e.x-1,e.y,0);dropPk(e.x,e.y,2);dropPk(e.x+1,e.y,1)};
// procedural music (follows the Sound setting, speeds up on boss levels)
const N=[0,3,7,10,12,10,7,3],B=[55,55,65.4,49];let i=0;
(function tick(){
 try{if(st==='play'&&AC&&P.alive){const s=i++,bass=B[(s>>3)%4],f=bass*4*Math.pow(2,N[s%8]/12);
  if(s%2===0)tone(bass,.16,'triangle',.05,bass*.98);
  tone(f,.1,'square',.012,f*.99);if(s%4===0)noise(.05,.05)}}catch(e){}
 setTimeout(tick,lvl%10===0?135:170)})();
})();
</script>
"""
i = s.rfind('</body>')
if i < 0: miss.append('</body>')
else: s = s[:i] + EXTRA + s[i:]

out = os.path.splitext(src)[0] + '_new.html'
open(out, 'w', encoding='utf-8').write(s)
print('Saved:', out)
if miss:
    print('WARNING - patterns not found (that part was skipped):')
    for m in miss: print('  -', m)

