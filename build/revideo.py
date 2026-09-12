# -*- coding: utf-8 -*-
"""Reprocessa os videos dos dois casos na ORDEM DOS FATOS.

As pastas de origem foram renomeadas para ordem numerica, e o caso 02
passou de 15 para 11 planos. Este script:
  · apaga todo take/poster/sequencia que estava no repo (inclusive os
    orfaos t_12..t_15 do caso 02, que ficariam para tras)
  · regera na ordem do nome do arquivo
  · remonta a sequencia editada na mesma ordem
  · atualiza a etapa de video no manifest.json e as contagens
"""
import glob, json, io, os, re, subprocess, sys
import os as _os
# Caminhos relativos ao proprio script. Antes apontavam para a pasta
# temporaria da sessao, que nao sobrevive a uma conversa nova.
SP = _os.path.dirname(_os.path.abspath(__file__))   # .../SITE_GITHUB/build
G  = _os.path.dirname(SP)                           # .../SITE_GITHUB

TMP = os.path.join(_os.environ.get("TEMP","."), "recon_seq")

FONTES = {
    "c1": r"E:/PORTIFOLIO_IA/EXEMPLO_02/04_VIDEOS",
    "c2": r"E:/PORTIFOLIO_IA/EXEMPLO_01/VIDEOS IA",
}

VF_BASE = ("scale=800:450:force_original_aspect_ratio=decrease,"
           "pad=800:450:(ow-iw)/2:(oh-ih)/2:color=#000000,setsar=1")
LIFT_FORTE = "curves=all='0/0 0.25/0.52 0.6/0.82 1/1',eq=saturation=1.06"
LIFT_MEDIO = "curves=all='0/0 0.30/0.44 0.70/0.84 1/1',eq=saturation=1.03"

def sh(*a):
    r = subprocess.run(a, capture_output=True)
    if r.returncode != 0:
        print("FALHOU:", " ".join(str(x) for x in a[:4]))
        print(r.stderr.decode("utf8","ignore")[-300:]); sys.exit(1)

def luma(src):
    r = subprocess.run(["ffmpeg","-v","error","-ss","2.5","-i",src,"-frames:v","1",
                        "-vf","scale=1:1","-f","rawvideo","-pix_fmt","gray","-"],
                       capture_output=True)
    return r.stdout[0] if r.stdout else 128

def vf_para(src):
    L = luma(src)
    if L < 30: return VF_BASE + "," + LIFT_FORTE, L, "forte"
    if L < 58: return VF_BASE + "," + LIFT_MEDIO, L, "medio"
    return VF_BASE, L, "-"

man = json.load(io.open(os.path.join(G,"assets","manifest.json"), encoding="utf-8"))
resumo = {}

for caso, pasta in FONTES.items():
    d_vid = os.path.join(G,"assets",caso,"vid")
    d_pos = os.path.join(G,"assets",caso,"poster")
    # limpa TUDO que e video/poster de take, inclusive orfaos de versoes antigas
    apagados = 0
    for p in glob.glob(os.path.join(d_vid,"t_*.mp4")) + glob.glob(os.path.join(d_vid,"sequencia.mp4")) \
           + glob.glob(os.path.join(d_pos,"t_*.jpg")) + glob.glob(os.path.join(d_pos,"sequencia.jpg")):
        os.remove(p); apagados += 1

    fontes = sorted(glob.glob(os.path.join(pasta,"*.mp4")))
    print("%s: apagados %d, reprocessando %d na ordem:" % (caso, apagados, len(fontes)))

    d_tmp = os.path.join(TMP, caso); os.makedirs(d_tmp, exist_ok=True)
    for f in glob.glob(os.path.join(d_tmp,"*")): os.remove(f)

    partes, itens = [], []
    for i, src in enumerate(fontes, 1):
        k = "t_%02d" % i
        alvo = os.path.join(d_vid, k + ".mp4")
        vf, L, tipo = vf_para(src)
        marca = ("  [lift %s, luma %d]" % (tipo, L)) if tipo != "-" else ""
        print("   %02d  %s%s" % (i, os.path.basename(src), marca))
        sh("ffmpeg","-y","-v","error","-ss","1.0","-t","3.2","-i",src,
           "-c:v","libx264","-preset","slow","-crf","26","-vf",vf,
           "-r","24","-g","48","-an","-movflags","+faststart","-pix_fmt","yuv420p", alvo)
        sh("ffmpeg","-y","-v","error","-i",alvo,"-frames:v","1","-q:v","6",
           os.path.join(d_pos, k + ".jpg"))
        partes.append(alvo); itens.append([k, "Cena %02d" % i])

    lista = os.path.join(d_tmp,"lista.txt")
    with open(lista,"w",encoding="utf-8") as fh:
        for p in partes: fh.write("file '%s'\n" % p.replace("\\","/"))
    saida = os.path.join(d_vid,"sequencia.mp4")
    sh("ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",lista,
       "-c","copy","-movflags","+faststart", saida)
    sh("ffmpeg","-y","-v","error","-ss","2","-i",saida,"-frames:v","1","-q:v","5",
       os.path.join(d_pos,"sequencia.jpg"))
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
          "-of","csv=p=0",saida], capture_output=True).stdout.decode().strip())
    print("   -> sequencia.mp4  %.1fs  %.2f MB\n" % (dur, os.path.getsize(saida)/1048576))
    resumo[caso] = (len(itens), dur)

    # atualiza a etapa de video no manifesto
    c = next(x for x in man["casos"] if x["id"] == caso)
    et = next(e for e in c["etapas"] if e["tipo"] == "video")
    et["itens"] = itens
    et["conta"] = "%d planos" % len(itens)
    et["nota"]  = ("Os <b>%d planos gerados</b>, <b>na ordem dos fatos</b>, cortados em "
                   "~3 s e em loop. Os originais têm cinco segundos cheios." % len(itens))

json.dump(man, io.open(os.path.join(G,"assets","manifest.json"),"w",encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("manifest.json atualizado")

# ---- contagens no texto dos casos ----
P = os.path.join(SP,"meta_casos.py")
s = io.open(P, encoding="utf-8").read()
s = s.replace('"texto":"Os 14 planos colados na ordem dos fatos, com cortes secos. "',
              '"texto":"Os %d planos colados na ordem dos fatos, com cortes secos. "' % resumo["c1"][0])
s = s.replace('"texto":"Os 15 planos colados na ordem dos fatos, com cortes secos. "',
              '"texto":"Os %d planos colados na ordem dos fatos, com cortes secos. "' % resumo["c2"][0])
io.open(P,"w",encoding="utf-8",newline="").write(s)

# ---- total de planos na abertura ----
P2 = os.path.join(SP,"montar_v5.py")
s2 = io.open(P2, encoding="utf-8").read()
total = resumo["c1"][0] + resumo["c2"][0]
s2 = re.sub(r"<dt>Planos gerados</dt><dd>\d+</dd>",
            "<dt>Planos gerados</dt><dd>%d</dd>" % total, s2)
io.open(P2,"w",encoding="utf-8",newline="").write(s2)
print("contagens atualizadas: c1=%d, c2=%d, total=%d" % (resumo["c1"][0], resumo["c2"][0], total))
