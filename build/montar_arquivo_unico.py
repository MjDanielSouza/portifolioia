# -*- coding: utf-8 -*-
"""Embute imagens e videos no HTML como data URIs, gerando um arquivo unico."""
import base64, io, os, re, sys, json
import os as _os
# Caminhos relativos ao proprio script. Antes apontavam para a pasta
# temporaria da sessao, que nao sobrevive a uma conversa nova.
SP = _os.path.dirname(_os.path.abspath(__file__))   # .../SITE_GITHUB/build
G  = _os.path.dirname(SP)                           # .../SITE_GITHUB

TPL  = os.path.join(SP, "template.html")
WEB  = os.path.join(SP, "web")
OUT  = r"E:/PORTIFOLIO_IA/EXEMPLO_02/OUT_SITE/reconstituicao-com-ia.html"

media = {}
for sub, mime in (("img", "image/jpeg"), ("vid", "video/mp4")):
    d = os.path.join(WEB, sub)
    for fn in sorted(os.listdir(d)):
        key = os.path.splitext(fn)[0]
        with open(os.path.join(d, fn), "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode("ascii")
        media[key] = "data:%s;base64,%s" % (mime, b64)

html = io.open(TPL, encoding="utf-8").read()

# --- confere que toda chave citada no template existe ---
citadas = set(re.findall(r'MEDIA\[\s*["\']([A-Za-z0-9_]+)["\']\s*\]', html))
citadas |= set(re.findall(r'"([a-z]_[A-Za-z0-9_]+)"\s*,', html))
faltando = sorted(k for k in citadas if k not in media and re.match(r'^[rcpft]_', k))
if faltando:
    print("CHAVES SEM ARQUIVO:", faltando); sys.exit(1)

usadas = sorted(k for k in media if k in html)
sobrando = sorted(k for k in media if k not in html)

bloco = "const MEDIA = " + json.dumps(media, ensure_ascii=False) + ";"
html = html.replace("/*__MEDIA__*/", bloco)

fcss = io.open(os.path.join(SP, "fonts", "embed.css"), encoding="utf-8").read()
if "/*__FONTS__*/" not in html:
    print("SEM placeholder de fontes"); sys.exit(1)
html = html.replace("/*__FONTS__*/", fcss)
print("fontes embutidas    : %.0f KB" % (len(fcss)/1024))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, "w", encoding="utf-8", newline="").write(html)

mb = os.path.getsize(OUT) / (1024 * 1024)
print("arquivos embutidos : %d  (%d imagens, %d videos)" %
      (len(media), sum(1 for k in media if not k.startswith("t_")),
       sum(1 for k in media if k.startswith("t_"))))
print("referenciados      : %d" % len(usadas))
if sobrando:
    print("nao referenciados  : %s" % ", ".join(sobrando))
print("saida              : %s" % OUT)
print("tamanho            : %.1f MB" % mb)
