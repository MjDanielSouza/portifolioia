# -*- coding: utf-8 -*-
"""Versão enxuta. O argumento da peça é UM: pouca referência entra,
muita cena sai. Tudo que não serve a isso foi cortado.

Saiu: narrativa do caso em três parágrafos, stepper de etapas com nota
explicativa em cada uma, tabela comparativa de sete linhas, seção de
derivação separada. Entrou: o resultado antes de qualquer explicação, e
o bloco entrou→saiu, que é a peça inteira em uma imagem.
"""
import io, json, os, sys
import os as _os
# Caminhos relativos ao proprio script. Antes apontavam para a pasta
# temporaria da sessao, que nao sobrevive a uma conversa nova.
SP = _os.path.dirname(_os.path.abspath(__file__))   # .../SITE_GITHUB/build
G  = _os.path.dirname(SP)                           # .../SITE_GITHUB

sys.path.insert(0, SP)
from meta_casos import CASOS

CSS = io.open(os.path.join(SP,"cnn.css"), encoding="utf-8").read()
MAN = json.load(io.open(os.path.join(G,"assets","manifest.json"), encoding="utf-8"))
faces = [l.split("|") for l in io.open(os.path.join(SP,"faces.txt"),encoding="utf-8").read().split("\n") if l]
FONTES = "\n".join(
    "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
    "src:url(assets/fonts/%s) format('woff2')}" % (fam,st,w,nome)
    for fam,w,st,nome in faces)

FAVICON = ("data:image/svg+xml,"
 "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
 "%3Crect width='32' height='32' fill='%23DC2626'/%3E"
 "%3Ctext x='16' y='23' font-family='Arial,sans-serif' font-size='19' font-weight='bold' "
 "fill='%23FFFFFF' text-anchor='middle'%3ER%3C/text%3E%3C/svg%3E")

# ---- numeros de cada caso, tirados do proprio manifesto ----
RESUMO = {}
for c in MAN["casos"]:
    et = {e["tag"]: e for e in c["etapas"]}
    ref   = c["etapas"][0]                      # etapa 01 = referencia
    frames= [e for e in c["etapas"] if "FRAME" in e["nome"].upper()][0]
    video = [e for e in c["etapas"] if e["tipo"]=="video"][0]
    RESUMO[c["id"]] = {
      "ref_total": int(ref["conta"].split()[0]),
      "ref_itens": [k for k,_ in ref["itens"]],
      "frames_total": int(frames["conta"].split()[0]),
      "cenas": len(video["itens"]),
      "cenas_itens": [k for k,_ in video["itens"]],
    }

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Reconstituição de cenas com IA</title>
<meta name="description" content="De poucas fotos e um relato a uma reconstituição com dezenas de cenas.">
<meta name="robots" content="noindex, nofollow">
<link rel="icon" href="__FAVICON__">
<meta property="og:type" content="website">
<meta property="og:title" content="Reconstituição de cenas com IA">
<meta property="og:description" content="De poucas fotos e um relato a uma reconstituição com dezenas de cenas.">
<meta property="og:image" content="assets/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<style>__FONTES__</style>
<style>__CSS__</style>
</head>
<body>

<header class="topo"><div class="wrap">
  <a class="logo" href="#resultado"><span><b>RECON</b><i>com IA</i></span></a>
  <div class="casos" id="casos" role="tablist" aria-label="Caso"></div>
  <a class="arroba" href="https://instagram.com/7danielsouza" target="_blank" rel="noopener">@7danielsouza</a>
</div></header>

<!-- Segunda barra grudada: a etapa do processo. Quem esta no fim da pagina
     troca de caso ou de etapa sem ter de subir. -->
<nav class="barra-etapas" aria-label="Etapa do processo"><div class="wrap">
  <div class="etapas-rol">
    <a class="etapa" href="#resultado" aria-current="true">A reconstituição</a>
    <a class="etapa" href="#salto">Material recebido</a>
    <a class="etapa" href="#prova">Origem das imagens</a>
    <a class="etapa" href="#cenas">As cenas, uma a uma</a>
  </div>
  <!-- Sao casos reais. A barra e o lugar onde se troca de caso, entao a
       identificacao e a reportagem publica tem de estar nela: quem troca
       no fim da pagina precisa saber que caso passou a ver e de onde vem. -->
  <span class="fonte-caso" id="fonteCaso"></span>
</div></nav>

<main>

<!-- O resultado primeiro. Explicação depois, e pouca. -->
<section id="resultado">
  <div class="wrap">
    <p class="chapeu">Reconstituição de cenas com IA</p>
    <h1 id="manchete"></h1>
    <p class="linha-fina">Você entrega as fotos que já existem no processo e o relato.
    O resto é reconstruído — sem locação, sem elenco, sem equipe em campo.</p>

    <div class="palco">
      <video id="seqVideo" playsinline muted loop autoplay controls preload="metadata"></video>
      <div class="barra"><em></em><b id="seqNome"></b> a reconstituição montada
        <span id="seqDur"></span></div>
    </div>
    <p class="resumo-linha" id="resumoLinha"></p>
  </div>
</section>

<!-- A peça inteira em uma imagem -->
<section id="salto" class="faixa-cinza">
  <div class="wrap rv">
    <h2 class="secao-titulo">O que foi recebido, o que foi produzido</h2>
    <div class="salto">
      <div class="lado">
        <div class="rot"><b>Recebido</b><span id="rotEntrou"></span></div>
        <div class="mini" id="entrou"></div>
        <p class="conta" id="contaEntrou"></p>
      </div>
      <div class="seta">→</div>
      <div class="lado">
        <div class="rot"><b>Produzido</b><span id="rotSaiu"></span></div>
        <div class="muitas" id="saiu"></div>
        <p class="conta" id="contaSaiu"></p>
      </div>
    </div>
  </div>
</section>

<!-- Prova visual, sem texto -->
<section id="prova">
  <div class="wrap rv">
    <h2 class="secao-titulo" id="tituloProva"></h2>
    <div class="batabs" id="batabs"></div>
    <div class="ba" id="ba">
      <img id="baBefore" alt="Foto do local"><img id="baAfter" class="after" alt="O mesmo local sem pessoas">
      <div class="handle"></div><div class="knob">↔</div>
      <span class="lbl l">Foto real</span><span class="lbl r">Cenário</span>
    </div>
    <div class="deriv" id="deriv"></div>
  </div>
</section>

<!-- As cenas -->
<section id="cenas" class="faixa-cinza">
  <div class="wrap rv">
    <h2 class="secao-titulo" id="tituloCenas"></h2>
    <div class="player">
      <div class="screen">
        <video id="vMain" playsinline muted loop autoplay preload="metadata"></video>
        <button class="playbtn" id="playbtn" type="button" aria-label="Reproduzir"><i>&#9654;</i></button>
        <div class="screenbar"><em></em><b id="vLabel"></b>
          <span>loop · sem áudio · toque para pausar</span></div>
      </div>
      <div class="takes" id="takes"></div>
    </div>
  </div>
</section>

</main>

<footer class="rodape">
  <div class="wrap">
    <h2 class="secao-titulo">Entrega em 3 a 4 dias<span class="thin">de poucas fotos e um relato a uma reconstituição que dá para assistir</span></h2>
    <div class="assin">
      <b>Daniel Souza</b>
      <a href="https://instagram.com/7danielsouza" target="_blank" rel="noopener">@7danielsouza</a>
    </div>
    <p class="aviso">Casos reais, com reportagem pública. As imagens integram processos
    criminais e o uso aqui é restrito à demonstração do método. Nomes omitidos por escolha
    editorial. Este site é portfólio pessoal e não tem vínculo com nenhum veículo de imprensa.</p>
  </div>
</footer>

<div class="lb" id="lb"><span class="x">fechar ✕</span><img id="lbImg" alt=""></div>

<script>
const MANIFESTO = __MANIFESTO__;
const META = __META__;
const RESUMO = __RESUMO__;
let casoAtual='c1';
const img=(c,k)=>'assets/'+c+'/img/'+k+'.jpg';
const vid=(c,k)=>'assets/'+c+'/vid/'+k+'.mp4';
const pos=(c,k)=>'assets/'+c+'/poster/'+k+'.jpg';

/* ---------- seletor de caso ---------- */
const elPil=document.getElementById('casos');
Object.keys(META).forEach(id=>{
  const m=META[id];
  const b=document.createElement('button');
  b.className='caso'; b.type='button'; b.setAttribute('role','tab');
  b.setAttribute('aria-selected', id===casoAtual?'true':'false');
  b.title=m.titulo;                      // o titulo nao cabe na barra
  b.textContent='Caso '+m.num;
  b.addEventListener('click',()=>trocar(id));
  elPil.appendChild(b);
});

function trocar(id){
  casoAtual=id;
  const m=META[id], r=RESUMO[id];
  [...elPil.children].forEach((b,i)=>
    b.setAttribute('aria-selected', Object.keys(META)[i]===id?'true':'false'));

  document.getElementById('manchete').textContent =
    r.ref_total+' fotos e um relato entraram. '+r.cenas+' cenas saíram.';
  document.getElementById('resumoLinha').innerHTML =
    '<b>'+m.titulo+'</b> — '+m.local+', '+m.quando+'. '+m.fonte_curta;
  document.getElementById('fonteCaso').innerHTML =
    '<b>Caso '+m.num+' · '+m.titulo+'</b><em>'+m.local+'</em>'+m.fonte_curta;

  // sequencia
  const s=m.seq, sv=document.getElementById('seqVideo');
  sv.poster=s.poster; sv.src=s.arquivo;
  document.getElementById('seqNome').textContent='Caso '+m.num;
  sv.addEventListener('loadedmetadata',()=>{
    document.getElementById('seqDur').textContent=Math.round(sv.duration)+' s';},{once:true});
  sv.play().catch(()=>{});

  montarSalto(r);
  montarBA(m);
  montarDeriv(m);
  // o subtitulo so promete arrastar quando existe chapa limpa para arrastar
  document.getElementById('tituloProva').innerHTML = m.ba.length
    ? 'Tudo sai do que já existe<span class="thin">o local real, esvaziado de gente — arraste</span>'
    : 'Tudo sai do que já existe<span class="thin">as pessoas do processo viram personagens consistentes</span>';
  montarCenas(r);
}

/* ---------- entrou -> saiu ---------- */
function montarSalto(r){
  const c=casoAtual;
  document.getElementById('rotEntrou').textContent='fotos do processo';
  document.getElementById('rotSaiu').textContent='cenas reconstruídas';
  document.getElementById('entrou').innerHTML =
    r.ref_itens.map(k=>'<img src="'+img(c,k)+'" alt="" loading="lazy">').join('');
  document.getElementById('saiu').innerHTML =
    r.cenas_itens.map(k=>'<img src="'+pos(c,k)+'" alt="" loading="lazy">').join('');
  document.getElementById('contaEntrou').innerHTML =
    '<em>'+r.ref_total+'</em> fotos e um relato';
  document.getElementById('contaSaiu').innerHTML =
    '<em>'+r.frames_total+'</em> quadros desenhados · <em>'+r.cenas+'</em> cenas em movimento';
}

/* ---------- antes / depois ---------- */
const secProva=document.getElementById('prova');
const ba=document.getElementById('ba'), baB=document.getElementById('baBefore'),
      baA=document.getElementById('baAfter'), baTabs=document.getElementById('batabs');
let baIdx=0, baPares=[];
function montarBA(m){
  baPares=m.ba;
  baTabs.style.display = baPares.length>1 ? '' : 'none';
  ba.style.display = baPares.length ? '' : 'none';
  if(!baPares.length) return;
  baIdx=0; baTabs.innerHTML='';
  baPares.forEach((p,i)=>{
    const b=document.createElement('button');
    b.className='batab'; b.type='button'; b.textContent=p.rot;
    b.setAttribute('aria-selected', i===0?'true':'false');
    b.addEventListener('click',()=>{ baIdx=i;
      [...baTabs.children].forEach((x,k)=>x.setAttribute('aria-selected',k===i?'true':'false'));
      carregarBA(); });
    baTabs.appendChild(b);
  });
  carregarBA();
}
function carregarBA(){ const p=baPares[baIdx];
  baB.src=img(casoAtual,p.a); baA.src=img(casoAtual,p.b); posic(50); }
function posic(p){ ba.style.setProperty('--pos', Math.max(0,Math.min(100,p))+'%'); }
function daEvento(ev){ const r=ba.getBoundingClientRect();
  posic(((ev.touches?ev.touches[0].clientX:ev.clientX)-r.left)/r.width*100); }
let arrastando=false;
ba.addEventListener('pointerdown',e=>{arrastando=true; ba.setPointerCapture(e.pointerId); daEvento(e);});
ba.addEventListener('pointermove',e=>{ if(arrastando) daEvento(e); });
ba.addEventListener('pointerup',()=>arrastando=false);
ba.addEventListener('pointercancel',()=>arrastando=false);

/* ---------- foto real -> personagem ---------- */
function montarDeriv(m){
  const c=casoAtual;
  document.getElementById('deriv').innerHTML = m.deriv.map(d=>
    '<div class="pair"><div class="from"><img src="'+img(c,d.de)+'" alt="" loading="lazy">'
    +'<div class="cap">Foto real</div></div><div class="arrow">→</div>'
    +'<div class="to"><img src="'+img(c,d.para)+'" alt="" loading="lazy">'
    +'<div class="cap">Personagem gerado, três vistas</div></div></div>').join('');
}

/* ---------- cenas ---------- */
function montarCenas(r){
  const c=casoAtual;
  document.getElementById('tituloCenas').innerHTML =
    'As '+r.cenas+' cenas<span class="thin">na ordem dos fatos · toque para trocar</span>';
  const v=document.getElementById('vMain'), lab=document.getElementById('vLabel'),
        box=document.getElementById('takes'), btn=document.getElementById('playbtn');
  box.innerHTML='';
  const sinc=()=>btn.classList.toggle('on', v.paused);
  if(!v.dataset.pronto){
    v.addEventListener('play',sinc); v.addEventListener('pause',sinc);
    btn.addEventListener('click',()=>v.play().catch(()=>{}));
    v.style.cursor='pointer';
    v.addEventListener('click',()=>{ v.paused?v.play().catch(()=>{}):v.pause(); });
    v.dataset.pronto='1';
  }
  const trocarCena=(k,t,b)=>{ v.poster=pos(c,k); v.src=vid(c,k); lab.textContent=t;
    v.play().catch(()=>{});
    [...box.children].forEach(x=>x.setAttribute('aria-current', x===b?'true':'false')); };
  r.cenas_itens.forEach((k,i)=>{
    const t='Cena '+String(i+1).padStart(2,'0');
    const b=document.createElement('button');
    b.className='take'; b.type='button'; b.title=t;
    b.setAttribute('aria-current', i===0?'true':'false');
    b.innerHTML='<img src="'+pos(c,k)+'" alt="'+t+'" decoding="async"><span>'+String(i+1).padStart(2,'0')+'</span>';
    b.addEventListener('click',()=>trocarCena(k,t,b));
    box.appendChild(b);
  });
  const k0=r.cenas_itens[0];
  v.poster=pos(c,k0); v.src=vid(c,k0); lab.textContent='Cena 01';
  v.play().catch(()=>{}); setTimeout(sinc,500);
}

/* ---------- lightbox ---------- */
const lb=document.getElementById('lb'), lbImg=document.getElementById('lbImg');
lb.addEventListener('click',()=>lb.classList.remove('on'));
document.addEventListener('keydown',e=>{ if(e.key==='Escape') lb.classList.remove('on'); });
document.addEventListener('click',e=>{
  const im=e.target.closest('.salto img, .pair img');
  if(im){ lbImg.src=im.src.replace('/poster/','/poster/'); lb.classList.add('on'); }
});

/* ---------- etapa corrente na segunda barra ----------
   Por handler de scroll, nao por IntersectionObserver: o observer nao
   dispara de forma confiavel nesta janela e a barra ficaria mentindo. */
const abas=[...document.querySelectorAll('.etapa')]
  .map(a=>({a, el:document.querySelector(a.getAttribute('href'))}))
  .filter(x=>x.el);
function marcarEtapa(){
  const limite=document.querySelector('.topo').offsetHeight
               +document.querySelector('.barra-etapas').offsetHeight+14;
  let atual=abas[0];
  for(const x of abas) if(x.el.getBoundingClientRect().top<=limite) atual=x;
  // o rodape nao tem aba: no fim da pagina a ultima etapa continua valendo
  if(innerHeight+scrollY>=document.documentElement.scrollHeight-4)
    atual=abas[abas.length-1];
  abas.forEach(x=>x.a.setAttribute('aria-current', x===atual?'true':'false'));
  // no celular a fileira rola: trazer a etapa corrente para a vista, mas so
  // quando ela muda, senao briga com quem esta arrastando a barra na mao
  if(atual && atual!==ultimaAba){
    ultimaAba=atual;
    const rol=document.querySelector('.etapas-rol'), e=atual.a;
    if(rol.scrollWidth>rol.clientWidth+1)
      rol.scrollTo({left:Math.max(0, e.offsetLeft-(rol.clientWidth-e.offsetWidth)/2),
                    behavior:'smooth'});
  }
}
let ultimaAba=null;
let agendado=false;
addEventListener('scroll',()=>{ if(agendado) return; agendado=true;
  requestAnimationFrame(()=>{ marcarEtapa(); agendado=false; }); },{passive:true});
addEventListener('resize',marcarEtapa,{passive:true});

const io2=new IntersectionObserver(es=>es.forEach(en=>{
  if(en.isIntersecting){ en.target.classList.add('in'); io2.unobserve(en.target); }
}),{threshold:.08});
document.querySelectorAll('.rv').forEach(el=>io2.observe(el));

trocar('c1');
marcarEtapa();
</script>
</body>
</html>
"""

# fonte curta por caso, para a linha de resumo
for cid, m in CASOS.items():
    import re as _re
    url = _re.search(r'href="(https://www\.bandab[^"]+)"', m["resumo"]).group(1)
    m["fonte_curta"] = '<a href="%s" target="_blank" rel="noopener">Ver a reportagem</a>' % url

html = (HTML.replace("__FONTES__", FONTES).replace("__CSS__", CSS)
            .replace("__FAVICON__", FAVICON)
            .replace("__MANIFESTO__", json.dumps(MAN, ensure_ascii=False))
            .replace("__META__", json.dumps(CASOS, ensure_ascii=False))
            .replace("__RESUMO__", json.dumps(RESUMO, ensure_ascii=False)))
io.open(os.path.join(G,"index.html"),"w",encoding="utf-8",newline="").write(html)
print("index.html: %.1f KB" % (len(html)/1024))
for cid,r in RESUMO.items():
    print("  %s: %d fotos -> %d quadros, %d cenas" % (cid, r["ref_total"], r["frames_total"], r["cenas"]))
