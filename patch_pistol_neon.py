#!/usr/bin/env python3
# Usage:  python patch_pistol_neon.py index.html
# Makes index.html.bak, then patches index.html in place.
import sys, shutil
f = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
s = open(f, encoding='utf-8').read()
shutil.copy(f, f + '.bak')

def R(old, new):
    global s
    if s.count(old) != 1:
        sys.exit('PATCH FAILED (found %d times): %s' % (s.count(old), old[:70]))
    s = s.replace(old, new)

# ---------- 1) NEW ENEMIES, BOSSES, HELPERS ----------
R("const EC=[0xe63946,0x3dd6a0,0xffa23d,0xc77dff,0xb8c4ff];", r'''const EC=[0xe63946,0x3dd6a0,0xffa23d,0xc77dff,0xb8c4ff,0,0x39e6ff,0xff3df0,0xa8ff3d,0xa8ff3d];
const BC=[0xffd23d,0xff4d6d,0x7cfc9a,0xb23bff,0x3dd6ff,0xffffff],BN=['IRON WARDEN','CRIMSON HYDRA','VENOM KING','VOID TYRANT','FROST EMPEROR','SOLAR GOD'];
const HT={13:'New: BLINKER - it teleports next to you, then fires.',16:'New: SNIPER - slow warning, very fast shot. Keep moving!',21:'New: SPIRAL - sprays a rotating stream of bullets.',25:'New: DRONE - it chases you and explodes on contact. Shoot it!'};
const typesFor=n=>{const a=[0,1,2,3,4];n>=13&&a.push(6);n>=16&&a.push(7);n>=21&&a.push(8);n>=25&&a.push(9);return a};
function bossLevel(n){const t=n/10|0,hp=10+6*(t-1),bt=[2,4,6,3,1][(t-1)%5],ty=typesFor(n),m=Math.min(6,t+1),e=[[0,9,bt,Math.max(.9,2.3-.15*t),2.5,hp,t]];
 for(let i=0;i<m;i++)e.push([(i%2?1:-1)*(3+i),4+(i*2.3)%7,ty[i%ty.length],2.8,2.5]);
 return{p:[[-4,5,3,.6],[4,5,3,.6]],e}}
function mkBoss(t){const c=BC[(t-1)%BC.length],g=mkGun(c,1.2,t>1);box(.5,.5,.3,0xffffff,-.2,.45,0,g);for(let i=0;i<Math.min(t,6);i++)box(.12,.35+.05*i,.12,c,-.35+i*.18,.65+.05*i,0,g);return g}
function mkDrone(){const g=new THREE.Group(),c=new THREE.Mesh(geo,M(0xa8ff3d,0x2a4400));c.scale.setScalar(.5);g.add(c);for(let i=0;i<4;i++){const q=box(.5,.1,.1,0x222831,0,0,0,g);q.rotation.z=i*Math.PI/4}return g}''')

R("k=Math.min(9,3+Math.floor((n-12)/3))", "k=Math.min(11,3+Math.floor((n-12)/3)),ty=typesFor(n)")
R("e.push([ex,ey,Math.floor(r()*5),2.6,2+r()*2])", "e.push([ex,ey,ty[Math.floor(r()*ty.length)],2.6,2+r()*2])")
R("if(n%10===0)e.push([0,9,3,2.2,2,10]);return{p,e}}", "const I={13:6,16:7,21:8,25:9};if(I[n]&&e.length)e[0][2]=I[n];return{p,e}}")
R("const L=LV[n-1]||gen(n),hue", "const L=n%10===0?bossLevel(n):(LV[n-1]||gen(n)),hue")
R("L.e.forEach(d=>{const hp=d[5]||(n>=9&&d[2]>0&&d[2]<5?2:1),m=d[2]===5?mkBomb():mkGun(hp>1?0xffd23d:EC[d[2]]||0xe63946,1,d[2]===4);LG.add(m);",
  "L.e.forEach(d=>{const hp=d[5]||((n>=9&&d[2]>0&&d[2]<5)||(n>=18&&d[2]>5&&d[2]<9)?2:1),m=d[2]===5?mkBomb():d[2]===9?mkDrone():d[5]?mkBoss(d[6]||1):mkGun(hp>1?0xffd23d:EC[d[2]]||0xe63946,1,d[2]===4);LG.add(m);")
R("d[2]===4?1.1:.75)", "d[2]===4?1.1:d[2]===9?1.5:.75)")
R("iv:d[3]*(1-.32*D)", "iv:d[3]*(d[2]===7?1.35:1)*(1-.32*D)")
R("sc:d[5]?2:hp>1?1.3:1.1,boss:!!d[5],alive:true}", "sc:d[5]?1.7+.12*Math.min(d[6]||1,8):hp>1?1.3:1.1,tr:d[6]||0,mh:hp,hr:d[5]?1.05+.06*Math.min(d[6]||1,8):.7,boss:!!d[5],alive:true}")
R("msg('LEVEL '+n+(n%10===0?' ☠ BOSS':''),1.2)", "msg('LEVEL '+n+(n%10===0?' ☠ '+BN[((n/10|0)-1)%BN.length]:''),1.6)")
R("Dodge the red laser!':'';hud()}", "Dodge the red laser!':HT[n]||'';hud()}")

# ---------- 2) ENEMY BEHAVIOUR ----------
R("P.gt-=dt;P.inv-=dt;P.jb-=dt;P.dc-=dt;", "P.gt-=dt;P.inv-=dt;P.jb-=dt;P.dc-=dt;P.rp-=dt;")
R("const s=e.sf*(e.lock?.15:e.dash>0?0:1);", "if(e.t===9){e.gx=P.x;e.gy=P.y}const s=e.sf*(e.lock?.15:e.dash>0?0:1);")
R("if(e.t===5){e.m.position.set(e.x,e.y,0);e.m.userData.c.scale.setScalar(.6+.06*Math.sin(time*8));return}",
  "if(e.t===5){e.m.position.set(e.x,e.y,0);e.m.userData.c.scale.setScalar(.6+.06*Math.sin(time*8));return}"
  "if(e.t===9){e.m.position.set(e.x,e.y,0);e.m.rotation.z+=dt*9;if(P.alive&&st==='play'&&Math.hypot(P.x-e.x,P.y-e.y)<.95){hitP({vx:e.vx});addRing(e.x,e.y,2,0xa8ff3d);e.hp=1;hurt(e)}return}")
R("e.tm+=dt;if(!e.lock&&e.tm>e.iv-tele){e.lock=true;sEn()}", "e.tm+=dt;const tl=e.t===7?tele*1.9:tele;if(!e.lock&&e.tm>e.iv-tl){e.lock=true;sEn()}")
R("if(e.tm>=e.iv){e.lock=false;e.tm=0;e.b=e.t===2?3+(D>.5?1:0):1;e.bt=0;",
  "if(e.tm>=e.iv){e.lock=false;e.tm=0;if(e.t===6){spawn(e.x,e.y,0xff3df0,12,8,.12);e.x=clamp(P.x+(Math.random()*2-1)*6,-8.6,8.6);e.y=clamp(P.y+1+(Math.random()*2-1)*3,2,10.8);e.vx=e.vy=0;e.gx=e.x;e.gy=e.y;spawn(e.x,e.y,0xff3df0,12,8,.12);tone(700,.15,'sine',.1,200)}e.b=e.boss?1+(e.tr>>1):e.t===2?3+(D>.5?1:0):e.t===8?8:1;e.bt=0;")
R("if(e.t===3){for(let i=-1;i<=1;i++)bullet(ox,oy,e.aim+i*.26,bs,0)}else bullet(ox,oy,e.aim,bs,0);",
  "if(e.boss){const k=Math.min(11,2+e.tr*2);for(let i=0;i<k;i++)bullet(ox,oy,e.aim+(i-(k-1)/2)*.2,bs,0);if(e.tr>=2&&(e.rv=(e.rv||0)+1)%3===0){const m=10+e.tr*2;for(let j=0;j<m;j++)bullet(e.x,e.y,j/m*6.283+time,bs*.7,0)}}"
  "else if(e.t===3){for(let i=-1;i<=1;i++)bullet(ox,oy,e.aim+i*.26,bs,0)}else bullet(ox,oy,e.aim,bs*(e.t===7?2.2:e.t===8?.8:1),0);if(e.t===8)e.aim+=.55;")

# ---------- 3) BULLET FEATURES (pierce / homing / damage) ----------
R("if(b.bm)b.vy-=14*dt;b.x+=b.vx*dt;",
  "if(b.hm2){let t=null,bd=1e9;for(const e of en)if(e.alive&&e.t!==5){const d=Math.hypot(e.x-b.x,e.y-b.y);if(d<bd){bd=d;t=e}}if(t){const sp=Math.hypot(b.vx,b.vy),a=Math.atan2(b.vy,b.vx),na=a+nrm(Math.atan2(t.y-b.y,t.x-b.x)-a)*Math.min(1,dt*5);b.vx=Math.cos(na)*sp;b.vy=Math.sin(na)*sp}}if(b.bm)b.vy-=14*dt;b.x+=b.vx*dt;")
R("for(const e of en)if(e.alive&&Math.hypot(b.x-e.x,b.y-e.y)<.7){if(b.bm)dead=true;else{if(b.dm>1)e.hp-=b.dm-1;hurt(e);dead=true}break}",
  "for(const e of en)if(e.alive&&Math.hypot(b.x-e.x,b.y-e.y)<(e.hr||.7)){if(b.hs){if(b.hs.includes(e))continue;b.hs.push(e)}if(b.bm)dead=true;else{if(b.dm>1)e.hp-=b.dm-1;hurt(e);if(!b.pr)dead=true}if(!b.pr||b.bm)break}")
R("for(let i=0;i<W.pel;i++)bullet(P.x+dx*.8*W.len,P.y+dy*.8*W.len,a0+(Math.random()-.5)*2*W.sp,32,1);",
  "for(let i=0;i<W.pel;i++)bullet(P.x+dx*.8*W.len,P.y+dy*.8*W.len,a0+(W.ring?i/W.pel*6.2832:(Math.random()-.5)*2*W.sp),W.spd?32*W.spd:32,1);"
  "for(const b of bl.slice(-W.pel)){if(W.pierce){b.pr=1;b.hs=[];b.rc=0;b.m.scale.setScalar(.2)}if(W.dmg)b.dm=W.dmg;if(W.hm)b.hm2=1;if(W.big)b.m.scale.setScalar(W.big)}")
R("P.cd=W.cd+(W.burst?W.burst*.07:0);", "P.cd=(W.cd+(W.burst?W.burst*.07:0))*(P.rp>0?.5:1);")
R("hu:0,am:W.mag", "hu:0,rp:0,am:W.mag")

# ---------- 4) NEW WEAPONS ----------
R("burst:0,bx:1}];", r'''burst:0,bx:1},
{n:'Rail Cannon',d:'Piercing shot that goes through every enemy in line. Heavy recoil.',c:0x2ee6d6,rec:17,tq:9,cd:.7,mag:4,rel:1.3,pel:1,sp:0,len:1.6,auto:0,burst:0,pierce:1,dmg:3,spd:1.9,ul:16},
{n:'Plasma Rifle',d:'Fast heavy bolts with double damage. Hold to fire.',c:0xff3df0,rec:5,tq:3.5,cd:.11,mag:36,rel:1.4,pel:1,sp:.03,len:1.3,auto:1,burst:0,dmg:2,big:.2,ul:24},
{n:'Seeker',d:'Fires two homing missiles that hunt enemies.',c:0xffe14d,rec:7,tq:5,cd:.35,mag:12,rel:1.2,pel:2,sp:.5,len:1.2,auto:0,burst:0,hm:1,spd:.62,dmg:2,ul:32},
{n:'Nova Blaster',d:'Blasts a full ring of bullets in every direction. Great against crowds.',c:0xff5470,rec:7,tq:3,cd:.5,mag:6,rel:1.3,pel:12,sp:0,len:1.1,auto:0,burst:0,ring:1,ul:40}];
function ok(i){const w=WP[i];return w.ul?SV.best>w.ul:w.bx?SV.best>=15:i<SV.un}''')
R("if(SV.wp>=SV.un&&!(WP[SV.wp].bx&&SV.best>=15))SV.wp=0;", "if(!ok(SV.wp))SV.wp=0;")
R("if(w.bx?SV.best<15:i>=SV.un)return", "if(!ok(i))return")
R("Clear level ${w.bx?14:2*i}", "Clear level ${w.ul||(w.bx?14:2*i)}")
R("<b>${un}/${WP.length-1}</b>", "<b>${WP.filter((w,i)=>ok(i)).length}/${WP.length}</b>")
R("const nu=Math.min(WP.length-1,1+Math.floor(lvl/2)),nw=nu>SV.un;", "const nu=Math.min(7,1+Math.floor(lvl/2)),nw=nu>SV.un;")
R("const bn=lvl===14&&SV.best<15;", "const bn=lvl===14&&SV.best<15,nl=WP.findIndex(w=>w.ul===lvl);")
R("'</p></div>':'')+(hxn?", "'</p></div>':'')+(nl>=0?'<div class=\"new\"><h2>�� NEW: '+WP[nl].n+' unlocked!</h2><p>'+WP[nl].d+'</p></div>':'')+(hxn?")
R("<path d='M10 19h9l-3 10h-8z' fill='#2c3440'/>`];", r'''<path d='M10 19h9l-3 10h-8z' fill='#2c3440'/>`,
c=>`<rect x='4' y='12' width='56' height='5' fill='${c}'/><rect x='6' y='9' width='16' height='11' rx='2' fill='#2c3440'/><circle cx='56' cy='14.5' r='3' fill='#fff'/>`,
c=>`<rect x='6' y='9' width='34' height='10' rx='3' fill='${c}'/><circle cx='50' cy='14' r='6' fill='${c}' opacity='.7'/><rect x='38' y='12' width='8' height='4' fill='#111'/><path d='M10 19h9l-3 10h-8z' fill='#2c3440'/>`,
c=>`<rect x='6' y='10' width='26' height='9' rx='3' fill='#2c3440'/><path d='M32 11l20 3-20 4z' fill='${c}'/><circle cx='54' cy='14' r='3' fill='${c}'/>`,
c=>`<circle cx='32' cy='16' r='5' fill='${c}'/><g stroke='${c}' stroke-width='2'><path d='M32 2v6M32 24v6M12 16h6M46 16h6M18 6l4 4M42 22l4 4M46 6l-4 4M22 22l-4 4'/></g>`];''')

# ---------- 5) POWER-UP DROPS (shield / rapid fire / heart) ----------
R("if(P.hp<3&&Math.random()<.12){const m=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color:0xff5470}));m.scale.setScalar(.3);m.position.set(e.x,e.y,0);scene.add(m);pk.push({m,x:e.x,y:e.y,l:10})}}",
  "{const r=Math.random(),k=r<.07&&P.hp<3?0:r<.14?1:r<.22?2:-1;if(k>=0){const m=new THREE.Mesh(geo,new THREE.MeshBasicMaterial({color:[0xff5470,0x4dfff0,0xffd166][k]}));m.scale.setScalar(.3);m.position.set(e.x,e.y,0);scene.add(m);pk.push({m,x:e.x,y:e.y,l:10,k})}}}")
R("if(P.alive&&P.hp<3&&Math.hypot(q.x-P.x,q.y-P.y)<.9){P.hp++;hud();spawn(q.x,q.y,0xff5470,8,6,.12);tone(880,.15,'triangle',.15,1200);q.l=0}",
  "if(P.alive&&(q.k||P.hp<3)&&Math.hypot(q.x-P.x,q.y-P.y)<.9){if(q.k===1){P.inv=Math.max(P.inv,5);msg('SHIELD!',.8,'gold')}else if(q.k===2){P.rp=7;P.am=cw().mag;P.rl=0;msg('RAPID FIRE!',.8,'gold')}else P.hp++;hud();spawn(q.x,q.y,[0xff5470,0x4dfff0,0xffd166][q.k||0],8,6,.12);tone(880,.15,'triangle',.15,1200);q.l=0}")

# ---------- 6) NO MUSIC: remove it, use plain wind ambience + sound effects ----------
R("sUnlock=()=>[523,659,784,1047].forEach((f,i)=>setTimeout(()=>tone(f,.3,'triangle',.22,f*1.01),i*110));",
  "sUnlock=()=>{noise(.6,.35);tone(200,.5,'sawtooth',.18,900);tone(400,.4,'sine',.15,1500)};")
a = s.index('// procedural synthwave music')
b = s.index('function hot_t(){return 135}') + len('function hot_t(){return 135}')
s = s[:a] + r'''// plain wind ambience (no melody, no rhythm, no instruments) - respects the mute setting
let amb=null;
setInterval(()=>{if(!AC||SV.mu||document.hidden||(st!=='play'&&st!=='menu')){if(amb)amb.g.gain.setTargetAtTime(0,AC.currentTime,.2);return}
 if(AC.state!=='running')return;
 if(!amb){const bf=AC.createBuffer(1,AC.sampleRate*2,AC.sampleRate),d=bf.getChannelData(0);for(let i=0;i<d.length;i++)d[i]=Math.random()*2-1;const sr=AC.createBufferSource(),f=AC.createBiquadFilter(),g=AC.createGain();sr.buffer=bf;sr.loop=true;f.type='lowpass';f.frequency.value=420;g.gain.value=0;sr.connect(f).connect(g).connect(AC.destination);sr.start();amb={f,g}}
 const hot=st==='play'&&(lvl%10===0||en.some(q=>q.alive&&q.boss));
 amb.f.frequency.setTargetAtTime((hot?300:420)+160*Math.sin(time*.7),AC.currentTime,.3);amb.g.gain.setTargetAtTime(hot?.07:.035,AC.currentTime,.3)},200);''' + s[b:]

# ---------- 7) BOSS HEALTH BAR ----------
R("cmE.innerHTML='<b></b><i></i>';", "cmE.innerHTML='<b></b><i></i>';const bb=ce('div','bb');bb.style.cssText='position:fixed;top:calc(88px + env(safe-area-inset-top,0px));left:50%;transform:translateX(-50%);width:min(60vw,360px);height:10px;border:1px solid #ff5470;border-radius:6px;background:#1a0a10;display:none;pointer-events:none;overflow:hidden';bb.innerHTML='<i style=\"display:block;height:100%;background:linear-gradient(90deg,#ff5470,#ffd166)\"></i>';")
R("const on=cb>1&&time-ct<3&&st==='play';", "const bo=en.find(q=>q.alive&&q.boss);bb.style.display=bo&&st==='play'?'block':'none';if(bo)bb.firstChild.style.width=Math.max(0,bo.hp/bo.mh*100)+'%';const on=cb>1&&time-ct<3&&st==='play';")

open(f, 'w', encoding='utf-8').write(s)
print('OK - patched', f, '(backup:', f + '.bak)')
