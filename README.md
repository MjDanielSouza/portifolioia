# Reconstituição com IA — dois casos

Portfólio que mostra, etapa por etapa, como fotos de inquérito e um relato
viram uma reconstituição.

**No ar:** https://mjdanielsouza.github.io/portifolioia/

## Os casos

| | Caso | Etapas | Imagens | Planos |
|---|---|---|---|---|
| 01 | Dívida de R$ 400 — homicídio e ocultação de cadáver | 5 | 60 | 14 |
| 02 | Confusão na Ilha do Mel — importunação e desacato | 4 | 42 | 15 |

Cada caso tem fonte pública linkada na própria página. **Nomes omitidos por
escolha editorial** — a imprensa não nomeia os envolvidos, e portfólio
comercial não é lugar para isso.

## O que tem na página

Seletor de casos · o caso · as etapas navegáveis · antes/depois arrastável
(só o caso 01, que tem chapa limpa) · da foto ao personagem · a sequência
dos fatos · comparativo com reconstituição filmada.

A **sequência dos fatos** é o material gerado colado na ordem, com cortes
secos — 45 s no caso 01, 48 s no caso 02. Não é montagem final.

## Sistema visual — dossiê

Registro de documento, não de interface. A paleta:

Paleta medida no g1.globo.com e adotada aqui:

| | |
|---|---|
| Chão | `#F9F9F9` · chapa `#FFFFFF` · leito `#EFEFEF` |
| Texto | título `#1A1A1A` · corpo `#333333` · apoio `#666666` |
| Régua | `#E4E4E4` |
| Acento | `#C4170C` — o vermelho do g1, **só em marcação** |

Foi adotada a **lógica de cor** do g1, não a tipografia: o portal é todo em
Open Sans porque é feed, e isto é portfólio.

Tipografia: **Archivo** no título, **Newsreader** (serifa) no texto corrido,
**JetBrains Mono** só em metadado real.

As regras que sustentam: a cor vem só das fotografias; nada de glow, nada de
vidro, raio de 3px; fio de 1px separa e sombra não; grade assimétrica com
trilho de metadado à esquerda.

## Estrutura

```
index.html               página inteira (CSS e JS embutidos)
assets/manifest.json     inventário: etapas e arquivos de cada caso
assets/c1/{img,vid,poster}
assets/c2/{img,vid,poster}
assets/fonts/            Archivo, Newsreader e JetBrains Mono, subconjunto latin
robots.txt  .nojekyll
```

Caminhos relativos em tudo — funciona na raiz ou em `usuario.github.io/repo/`.
Sem dependência externa: as fontes estão no repositório.

A página é gerada a partir do `manifest.json` mais um arquivo de texto, e
não de listas escritas à mão dentro do HTML. Para trocar imagem, substitua
o arquivo mantendo o nome.

## Publicar

```bash
git add -A && git commit -m "atualiza site" && git push
```

Deploy em ~20 s.

## Sobre o conteúdo

As imagens integram processos criminais com reportagem pública. Uso restrito
à demonstração do método.

`noindex` e `robots.txt` mantêm a página fora de buscadores. **Isso vale para
o site.** Os arquivos seguem visíveis em `github.com/MjDanielSouza/portifolioia`
porque o repositório é público, e permanecem no histórico do git mesmo se
removidos depois.

---

Daniel Souza · [@7danielsouza](https://instagram.com/7danielsouza)
