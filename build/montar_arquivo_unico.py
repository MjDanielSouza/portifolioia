# -*- coding: utf-8 -*-
"""Arquivo unico: o mesmo site, com a midia embutida em data URI.

A versao anterior montava de um template proprio (template_arquivo_unico.html)
com midia de uma pasta build/web/ que morava na pasta temporaria da sessao.
As duas coisas se perderam, e a pagina em dossie ficou duas geracoes atras do
site. Este gerador parte do index.html JA CONSTRUIDO: o arquivo unico passa a
ser, por construcao, a mesma pagina — rode montar.py, rode este, e pronto.

O que ele faz:
  · descobre a midia referenciada a partir do manifesto e do meta_casos,
    que sao a mesma fonte de verdade da pagina
  · embute cada arquivo como data URI
  · troca os literais assets/... do HTML e do CSS (fontes inclusive)
  · aponta os tres atalhos de caminho do JS para o mapa MEDIA

Nao entra: assets/og.jpg. E meta tag de compartilhamento, nao carrega na
pagina, e embutir so engordaria o arquivo.
"""
import base64, io, json, mimetypes, os, re, sys

SP = os.path.dirname(os.path.abspath(__file__))     # .../SITE_GITHUB/build
G  = os.path.dirname(SP)                            # .../SITE_GITHUB
OUT = os.path.join(os.path.dirname(os.path.dirname(G)),
                   "EXEMPLO_02", "OUT_SITE", "reconstituicao-com-ia.html")
if not os.path.isdir(os.path.dirname(OUT)):         # se a arvore mudar de lugar
    OUT = os.path.join(G, "OUT_SITE", "reconstituicao-com-ia.html")

sys.path.insert(0, SP)
from meta_casos import CASOS

IDX = os.path.join(G, "index.html")
if not os.path.exists(IDX):
    sys.exit("index.html nao existe. Rode montar.py antes.")
html = io.open(IDX, encoding="utf-8").read()
MAN = json.load(io.open(os.path.join(G, "assets", "manifest.json"), encoding="utf-8"))

# ---- o que a pagina referencia, pela mesma fonte de verdade que a monta ----
alvo = set()
for c in MAN["casos"]:
    cid = c["id"]; m = CASOS[cid]
    ref   = c["etapas"][0]
    video = [e for e in c["etapas"] if e["tipo"] == "video"][0]
    for k, _ in ref["itens"]:
        alvo.add("assets/%s/img/%s.jpg" % (cid, k))
    for k, _ in video["itens"]:
        alvo.add("assets/%s/poster/%s.jpg" % (cid, k))
        alvo.add("assets/%s/vid/%s.mp4"   % (cid, k))
    for p in m["ba"]:
        alvo.add("assets/%s/img/%s.jpg" % (cid, p["a"]))
        alvo.add("assets/%s/img/%s.jpg" % (cid, p["b"]))
    for d in m["deriv"]:
        alvo.add("assets/%s/img/%s.jpg" % (cid, d["de"]))
        alvo.add("assets/%s/img/%s.jpg" % (cid, d["para"]))
    alvo.add(m["seq"]["poster"]); alvo.add(m["seq"]["arquivo"])

# As fontes sao caso a parte: moram em url() dentro do CSS, e CSS nao enxerga
# o mapa MEDIA. Elas sao as unicas que entram como literal trocado no texto.
# Todo o resto vive so no mapa, senao o arquivo embute duas vezes — foi o que
# inchou a primeira geracao em 11 MB, com os dois sequencia.mp4 em dobro.
fontes = sorted(set(re.findall(r"assets/fonts/[A-Za-z0-9_-]+\.woff2", html)))

# assets/og.jpg fica de fora: e meta tag de compartilhamento, nao carrega.
# meta_casos.capa tambem: e campo morto, nenhum JS le.

faltando = sorted(p for p in alvo if not os.path.exists(os.path.join(G, p)))
if faltando:
    sys.exit("ARQUIVO NAO ENCONTRADO:\n  " + "\n  ".join(faltando))

# ---- embute ----
def datauri(p):
    fp = os.path.join(G, p)
    mime = mimetypes.guess_type(p)[0] or "application/octet-stream"
    if p.endswith(".woff2"):
        mime = "font/woff2"
    dados = open(fp, "rb").read()
    return len(dados), "data:%s;base64,%s" % (mime, base64.b64encode(dados).decode("ascii"))

MEDIA, bruto = {}, 0
for p in sorted(alvo):
    n, uri = datauri(p)
    bruto += n; MEDIA[p] = uri

# ---- so as fontes entram trocadas no texto ----
trocados = 0
for p in fontes:
    n, uri = datauri(p)
    bruto += n
    html = html.replace(p, uri); trocados += 1

# ---- e os caminhos que o JS monta em tempo de execucao ----
def troca(a, b):
    global html
    if html.count(a) != 1:
        sys.exit("esperava 1 ocorrencia de: %s (achei %d)" % (a, html.count(a)))
    html = html.replace(a, b, 1)

troca("const MANIFESTO = ", "const MEDIA = %s;\nconst MANIFESTO = "
      % json.dumps(MEDIA, ensure_ascii=False))
troca("const img=(c,k)=>'assets/'+c+'/img/'+k+'.jpg';",
      "const img=(c,k)=>MEDIA['assets/'+c+'/img/'+k+'.jpg']||'';")
troca("const vid=(c,k)=>'assets/'+c+'/vid/'+k+'.mp4';",
      "const vid=(c,k)=>MEDIA['assets/'+c+'/vid/'+k+'.mp4']||'';")
troca("const pos=(c,k)=>'assets/'+c+'/poster/'+k+'.jpg';",
      "const pos=(c,k)=>MEDIA['assets/'+c+'/poster/'+k+'.jpg']||'';")
# seq.poster e seq.arquivo ja viraram data URI na troca de literais acima,
# entao aqui a busca no mapa falha e o ||s.x devolve o proprio data URI
troca("sv.poster=s.poster; sv.src=s.arquivo;",
      "sv.poster=MEDIA[s.poster]||s.poster; sv.src=MEDIA[s.arquivo]||s.arquivo;")

# ---- nao pode sobrar caminho relativo, senao quebra offline ----
sobrou = sorted(set(re.findall(r'(?:src|href)="(assets/[^"]+)"|url\((assets/[^)]+)\)', html)))
sobrou = [p for t in sobrou for p in t if p and not p.endswith("og.jpg")]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write(html)

print("embutidos     : %d arquivos, %.2f MB de midia" % (len(MEDIA), bruto/1048576))
print("  imagens     : %d" % sum(1 for p in MEDIA if "/img/" in p))
print("  posteres    : %d" % sum(1 for p in MEDIA if "/poster/" in p))
print("  videos      : %d" % sum(1 for p in MEDIA if p.endswith(".mp4")))
print("  fontes      : %d" % sum(1 for p in MEDIA if p.endswith(".woff2")))
print("fontes trocadas: %d" % trocados)
print("caminho solto : %s" % (", ".join(sobrou) if sobrou else "nenhum"))
print("saida         : %s" % OUT)
print("tamanho       : %.1f MB" % (os.path.getsize(OUT)/1048576))
