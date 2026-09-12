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

## Sistema visual — portal

Registro de site de notícia brasileiro. Tokens medidos no g1.globo.com:

| | |
|---|---|
| Chão | `#F9F9F9` · card `#FFFFFF` · leito `#EFEFEF` |
| Texto | corpo `#333333` · apoio `#555555` · fraco `#888888` |
| Régua | `#E4E4E4` |
| Vermelho | `#C4170C` |
| Faixa superior | `#1A1A1A` |

Tipografia **Open Sans** (400/600/700/800). A assinatura do gênero é a
manchete em **700 com tracking negativo apertado** (−0,035em) e entrelinha
1,1 — é o que faz a página ser reconhecida como portal antes de qualquer
leitura.

Estrutura: faixa preta de seções, barra vermelha da marca, nav grudada no
topo, conteúdo em cards brancos sobre cinza, rodapé escuro.

**A gramática é de portal; a marca é do autor.** Nenhum logo, wordmark ou
nome de veículo de imprensa aparece na página — copiar marca alheia num
portfólio queima justamente com o cliente que se quer atender. O rodapé
declara que o site não tem vínculo com nenhum veículo.

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
