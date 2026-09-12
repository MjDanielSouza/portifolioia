# Reconstituição de cenas com IA

Peça de venda. O argumento é um só: **pouca referência entra, muita cena sai.**

**No ar:** https://mjdanielsouza.github.io/portifolioia/

| Caso | Entra | Sai |
|---|---|---|
| 01 · Dívida de R$ 400 | 12 fotos + relato | 94 quadros · **14 cenas** |
| 02 · Confusão na Ilha do Mel | 13 fotos + relato | 25 quadros · **11 cenas** |

## A página

1. **Manchete + vídeo** — o resultado antes de qualquer explicação
2. **O que entra e o que sai** — as fotos de um lado, as cenas do outro
3. **Tudo sai do que já existe** — antes/depois arrastável e foto → personagem
4. **As cenas** — player com todas, na ordem dos fatos
5. **Rodapé** — prazo, contato, aviso de uso

Página inteira: **~240 palavras.** Foi deliberado. A versão anterior explicava
o método em cinco etapas com nota em cada uma, narrava o caso em três
parágrafos e trazia tabela comparativa de sete linhas — e isso tirava o foco
do que o cliente compra.

Saíram: narrativa do caso, stepper de etapas, tabela comparativa, seção de
derivação isolada. O prazo virou uma linha no rodapé.

## Estrutura

```
index.html               página inteira (CSS e JS embutidos)
assets/manifest.json     inventário: etapas e arquivos de cada caso
assets/c1/{img,vid,poster}
assets/c2/{img,vid,poster}
assets/fonts/            Inter, subconjunto latin
robots.txt  .nojekyll
```

Caminhos relativos — funciona na raiz ou em `usuario.github.io/repo/`. Sem
dependência externa.

Os números da manchete e das contagens **saem do `manifest.json`**, não de
texto escrito à mão: trocar um vídeo ou uma referência atualiza a página
sozinho.

## Sistema visual

Registro de portal de notícia, tokens medidos no cnnbrasil.com.br: fundo
`#FFFFFF`, manchete `#000000` com tracking normal, vermelho `#DC2626` em
título de seção e marcador, barra do topo preta, corpo `#171717`. Fonte
**Inter** (a do veículo é proprietária).

**A gramática é de portal; a marca é do autor.** Nenhum logo ou nome de
veículo aparece, e o rodapé declara que não há vínculo com imprensa.

## Publicar

```bash
python montar_v6.py && git add -A && git commit -m "atualiza" && git push
```

Deploy em ~20 s. O Pages serve com `max-age=600` — se não vir a mudança,
é cache de 10 minutos.

## Sobre o conteúdo

Casos reais com reportagem pública, linkada em cada um. `noindex` e
`robots.txt` mantêm a página fora de buscadores. **Isso vale para o site:**
os arquivos seguem visíveis em `github.com/MjDanielSouza/portifolioia`, que
é público, e permanecem no histórico do git.

---

Daniel Souza · [@7danielsouza](https://instagram.com/7danielsouza)
