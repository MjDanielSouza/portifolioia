# -*- coding: utf-8 -*-
"""Prepara a midia dos dois casos e escreve manifest.json.

assets/c1/{img,vid,poster}  caso 01
assets/c2/{img,vid,poster}  caso 02

A pagina e gerada a partir do manifesto, nao de listas escritas a mao.
"""
import json, os, subprocess, sys, glob
import os as _os
# Caminhos relativos ao proprio script. Antes apontavam para a pasta
# temporaria da sessao, que nao sobrevive a uma conversa nova.
SP = _os.path.dirname(_os.path.abspath(__file__))   # .../SITE_GITHUB/build
G  = _os.path.dirname(SP)                           # .../SITE_GITHUB

E2  = r"E:/PORTIFOLIO_IA/EXEMPLO_02"          # caso 01 (divida de R$400)
E1  = r"E:/PORTIFOLIO_IA/EXEMPLO_01"          # caso 02 (restaurante de praia)

def sh(*a):
    r = subprocess.run(a, capture_output=True)
    if r.returncode != 0:
        print("FALHOU:", " ".join(a[:3]), r.stderr.decode("utf8","ignore")[:200]); sys.exit(1)

def img(src, dst, larg=1000, q="4"):
    sh("ffmpeg","-y","-v","error","-i",src,"-vf","scale='min(%d,iw)':-2"%larg,"-q:v",q,dst)

def vid(src, dst, ini="1.0", dur="3.2", larg="800"):
    sh("ffmpeg","-y","-v","error","-ss",ini,"-t",dur,"-i",src,
       "-c:v","libx264","-preset","slow","-crf","26","-vf","scale=%s:-2"%larg,
       "-an","-movflags","+faststart","-pix_fmt","yuv420p",dst)

def poster(src, dst):
    sh("ffmpeg","-y","-v","error","-i",src,"-frames:v","1","-vf","scale=800:-2","-q:v","6",dst)

def limpa(caso):
    for sub in ("img","vid","poster"):
        d = os.path.join(G,"assets",caso,sub)
        os.makedirs(d, exist_ok=True)
        for f in glob.glob(os.path.join(d,"*")): os.remove(f)

# =====================================================================
#  CASO 01
# =====================================================================
limpa("c1")
c1 = {"id":"c1", "etapas":[]}

def add_img_etapa(caso, cid, tag, nome, conta, sub, nota, arquivos, cols="g4", tall=False, larg=1000):
    itens=[]
    for i,(origem, rotulo) in enumerate(arquivos, 1):
        chave = "%s_%02d" % (tag, i)
        dst = os.path.join(G,"assets",cid,"img",chave+".jpg")
        img(origem, dst, larg)
        itens.append([chave, rotulo])
    caso["etapas"].append({"tag":tag,"nome":nome,"conta":conta,"sub":sub,"nota":nota,
                           "tipo":"grid","cols":cols,"tall":tall,"itens":itens})

O = os.path.join(E2,"01_REFERENCIA","ORIGINAL")
add_img_etapa(c1,"c1","01","REFERÊNCIA","12 arquivos",
  "O que já existia: fotos do inquérito, do local e das pessoas envolvidas.",
  "<b>Só isto é matéria-prima real.</b> Tudo o que vem depois é derivado daqui — e é por isso que a reconstituição pode ser conferida contra o que está no processo.",
  [(os.path.join(O,"ACUSADO 1.png"),"Autor · frontal"),
   (os.path.join(O,"ACUSADO 1_01.png"),"Autor · corredor"),
   (os.path.join(O,"ACUSADO 1_02.png"),"Autor · perfil"),
   (os.path.join(O,"ACUSADO 1_03.png"),"Autor · três quartos"),
   (os.path.join(O,"ACUSADO 2_01.png"),"Segundo envolvido"),
   (os.path.join(O,"ACUSADO 2_02.png"),"Segundo envolvido · 02"),
   (os.path.join(O,"VITIMA.png"),"Vítima"),
   (os.path.join(O,"VITIMA_02.png"),"Local · onde o corpo estava"),
   (os.path.join(O,"LOCAL_01.png"),"Local · escada e garagem"),
   (os.path.join(O,"LOCAL_02_01.png"),"Local · remoção"),
   (os.path.join(O,"LOCAL_02_02.png"),"Local · fundos"),
   (os.path.join(O,"LOCAL_02_03.png"),"Local · terreno")])

D = os.path.join(E2,"01_REFERENCIA","EDITADOS")
add_img_etapa(c1,"c1","02","CENÁRIO","17 arquivos",
  "O local esvaziado de gente, e os objetos do caso isolados em chapa própria.",
  "A chapa limpa preserva a geometria e a luz do lugar real. A <b>frigideira</b> e o <b>cobertor</b> — os dois objetos que aparecem no relato — foram recortados para poderem ser recolocados em qualquer plano.",
  [(os.path.join(D,"LOCAL_01_LIMPO.png"),"Garagem · limpa"),
   (os.path.join(D,"LOCAL_02_01_LIMPO.png"),"Frente da casa"),
   (os.path.join(D,"LOCAL_02_02_LIMPO.png"),"Fundos · limpo"),
   (os.path.join(D,"LOCAL_02_03_LIMPO.png"),"Terreno"),
   (os.path.join(D,"LOCAL_02_04_LIMPO.png"),"Local da ocultação"),
   (os.path.join(D,"LOCAL.png"),"Terreno · original"),
   (os.path.join(D,"SALA.png"),"Sala · panorâmica"),
   (os.path.join(D,"SALA_01.png"),"Sala · variação"),
   (os.path.join(D,"SALA CM FRIGIDEIRA.png"),"Sala com o objeto"),
   (os.path.join(D,"Gemini_Generated_Image_8awjku8awjku8awj.png"),"Sala · reconstruída"),
   (os.path.join(D,"hf_20260116_162734_e686c780-0cb2-4e40-87d4-3c45513dd0.png"),"Sala · ampla"),
   (os.path.join(D,"interna.jpg"),"Interior · referência"),
   (os.path.join(D,"image.webp"),"Objetos · referência"),
   (os.path.join(D,"FRIGIDEIRA.png"),"Objeto isolado · 9 ângulos"),
   (os.path.join(D,"cobertor.png"),"Cobertor isolado")])

P = os.path.join(E2,"02_PERSONAGENS")
add_img_etapa(c1,"c1","03","PERSONAGENS","3 arquivos",
  "Cada envolvido vira um character sheet de três vistas, para não variar entre planos.",
  "<b>É a etapa que sustenta todas as outras.</b> Sem o sheet, o mesmo personagem sai com outro rosto a cada geração e a sequência deixa de ler como uma cena única.",
  [(os.path.join(P,"EMERSON SANTOS.jpeg"),"Personagem A · três vistas"),
   (os.path.join(P,"ELDER (VULGO PIRULITO).jpeg"),"Personagem B · três vistas"),
   (os.path.join(P,"IRACEMA_PS.jpeg"),"Personagem C · três vistas")],
  cols="g1", tall=True, larg=1280)

# 30 frames cobrindo a narrativa inteira
lista = sorted(glob.glob(os.path.join(E2,"03_STIL FRAME","*.jpeg")) +
               glob.glob(os.path.join(E2,"03_STIL FRAME","*.jpg")))
idx = [3,7,11,15,17,21,24,28,31,34,37,41,44,46,49,52,55,58,61,64,67,71,74,77,80,83,86,89,92,94]
add_img_etapa(c1,"c1","04","STILL FRAMES","94 arquivos",
  "A cena desenhada quadro a quadro, com continuidade de luz e timecode em quadro.",
  "Trinta dos 94 frames, cobrindo o percurso inteiro do relato — do encontro à ocultação. É o volume real do trabalho de storyboard.",
  [(lista[i-1], "Frame %03d" % i) for i in idx])

print("caso 01 — imagens: %d" % sum(len(e["itens"]) for e in c1["etapas"]))

# videos do caso 01
V = os.path.join(E2,"04_VIDEOS")
vids = sorted(glob.glob(os.path.join(V,"*.mp4")))
itens=[]
for i,src in enumerate(vids,1):
    k = "t_%02d" % i
    vid(src, os.path.join(G,"assets","c1","vid",k+".mp4"))
    poster(os.path.join(G,"assets","c1","vid",k+".mp4"), os.path.join(G,"assets","c1","poster",k+".jpg"))
    itens.append([k, "Take %02d" % i])
c1["etapas"].append({"tag":"05","nome":"VÍDEOS IA","conta":"14 planos",
  "sub":"Cada frame aprovado vira movimento. 24 fps, planos de cinco segundos.",
  "nota":"Estão aqui <b>os 14 planos gerados</b>, na ordem da narrativa, cortados em ~3 s e em loop. Os originais têm cinco segundos cheios.",
  "tipo":"video","itens":itens})
print("caso 01 — videos: %d" % len(itens))

# =====================================================================
#  CASO 02
# =====================================================================
limpa("c2")
c2 = {"id":"c2", "etapas":[]}

R = os.path.join(E1,"REFERENCIA")
add_img_etapa(c2,"c2","01","REFERÊNCIA","13 arquivos",
  "O ponto de partida: fotos do local, das pessoas e do contexto.",
  "<b>Nada aqui foi gerado.</b> São as imagens que existiam antes — o restaurante, a praia e os envolvidos.",
  [(os.path.join(R,"LOCAL_01.png"),"Restaurante · fachada"),
   (os.path.join(R,"LOCAL_02.png"),"Salão · balcão"),
   (os.path.join(R,"LOCAL_03.png"),"Salão · outro ângulo"),
   (os.path.join(R,"LOCAL_04.png"),"Praia · faixa de areia"),
   (os.path.join(R,"LOCAL_05.png"),"Praia · vista ampla"),
   (os.path.join(R,"LOCAL_06.jpg"),"Restaurante · aérea"),
   (os.path.join(R,"thiagodrudi 01.png"),"Envolvido A · 01"),
   (os.path.join(R,"thiagodrudi 02.png"),"Envolvido A · 02"),
   (os.path.join(R,"thiagodrudi 03.png"),"Envolvido A · 03"),
   (os.path.join(R,"thiagodrudi 04.jpg"),"Envolvido A · 04"),
   (os.path.join(R,"TIAGO GRUDE.jfif"),"Envolvido A · 05"),
   (os.path.join(R,"VITIMA.png"),"Envolvido B"),
   (os.path.join(R,"mulher da internete.jpg"),"Acompanhante")])

PP = os.path.join(E1,"PERSONAGEM")
add_img_etapa(c2,"c2","02","PERSONAGENS","4 arquivos",
  "Character sheets de três vistas, gerados a partir das referências.",
  "Mesma lógica do outro caso: o sheet é o que trava a aparência do personagem entre um plano e outro.",
  [(os.path.join(PP,"Homem A (Thiago).png"),"Personagem A · três vistas"),
   (os.path.join(PP,"Homem B (Márcio).png"),"Personagem B · três vistas"),
   (os.path.join(PP,"Mulher (esposa de Márcio).png"),"Personagem C · três vistas"),
   (os.path.join(PP,"operacaonatal1_0.jpg"),"Guarnição · referência")],
  cols="g1", tall=True, larg=1280)

F = os.path.join(E1,"FRAMES")
fr = sorted(glob.glob(os.path.join(F,"*.jpeg")) + glob.glob(os.path.join(F,"*.jpg")) +
            glob.glob(os.path.join(F,"*.png")))
add_img_etapa(c2,"c2","03","FRAMES","25 arquivos",
  "Storyboard e frames-chave: cada cena definida antes de animar.",
  "Os <b>25 frames</b> do caso, na ordem do storyboard — da chegada ao restaurante até a saída com a guarnição.",
  [(p, "Frame %02d" % i) for i,p in enumerate(fr,1)])

print("caso 02 — imagens: %d" % sum(len(e["itens"]) for e in c2["etapas"]))

VV = os.path.join(E1,"VIDEOS IA")
vv = sorted(glob.glob(os.path.join(VV,"*.mp4")))
itens=[]
for i,src in enumerate(vv,1):
    k = "t_%02d" % i
    vid(src, os.path.join(G,"assets","c2","vid",k+".mp4"))
    poster(os.path.join(G,"assets","c2","vid",k+".mp4"), os.path.join(G,"assets","c2","poster",k+".jpg"))
    itens.append([k, "Take %02d" % i])
c2["etapas"].append({"tag":"04","nome":"VÍDEOS IA","conta":"15 planos",
  "sub":"Cada frame vira movimento; depois, montagem e finalização.",
  "nota":"Os <b>15 planos gerados</b>, cortados em ~3 s e em loop.",
  "tipo":"video","itens":itens})
print("caso 02 — videos: %d" % len(itens))

# =====================================================================
manifesto = {"casos":[c1,c2]}
with open(os.path.join(G,"assets","manifest.json"),"w",encoding="utf-8") as f:
    json.dump(manifesto, f, ensure_ascii=False, indent=1)
print("manifest.json escrito")
