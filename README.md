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

## Estrutura

```
index.html               página inteira (CSS e JS embutidos)
assets/manifest.json     inventário: etapas e arquivos de cada caso
assets/c1/{img,vid,poster}
assets/c2/{img,vid,poster}
assets/fonts/            Montserrat e Roboto Mono, subconjunto latin
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

## Pendência

A linha **"Prazo"** do comparativo está em branco — procure por
`preencha com seu número`. É o único dado que depende de número real.

## Sobre o conteúdo

As imagens integram processos criminais com reportagem pública. Uso restrito
à demonstração do método.

`noindex` e `robots.txt` mantêm a página fora de buscadores. **Isso vale para
o site.** Os arquivos seguem visíveis em `github.com/MjDanielSouza/portifolioia`
porque o repositório é público, e permanecem no histórico do git mesmo se
removidos depois.

---

Daniel Souza · [@7danielsouza](https://instagram.com/7danielsouza)
