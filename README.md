# Reconstituição com IA — dois casos

Portfólio que mostra, etapa por etapa, como fotos de inquérito e um relato
viram uma reconstituição.

**No ar:** https://mjdanielsouza.github.io/portifolioia/

## Os casos

| | Caso | Etapas | Imagens | Planos |
|---|---|---|---|---|
| 01 | Dívida de R$ 400 — homicídio e ocultação de cadáver | 5 | 60 | 14 |
| 02 | Confusão na Ilha do Mel — importunação e desacato | 4 | 42 | 11 |

Cada caso tem fonte pública linkada na própria página. **Nomes omitidos por
escolha editorial** — a imprensa não nomeia os envolvidos, e portfólio
comercial não é lugar para isso.

## O que tem na página

Seletor de casos · o caso · as etapas navegáveis · antes/depois arrastável
(só o caso 01, que tem chapa limpa) · da foto ao personagem · a sequência
dos fatos · comparativo com reconstituição filmada.

A **sequência dos fatos** é o material gerado colado na ordem, com cortes
secos — 45 s no caso 01, 35 s no caso 02. Não é montagem final.

## Sistema visual — portal por assinatura

Tokens medidos no cnnbrasil.com.br:

| | |
|---|---|
| Fundo | `#FFFFFF` · faixa `#FAFAFA` · leito `#F5F5F5` |
| Manchete | `#000000` — **preta**, tracking normal |
| Título de seção | `#DC2626` — o vermelho é da **seção**, não da manchete |
| Corpo | `#171717` · apoio `#525252` · fraco `#737373` |
| Barra do topo | `#000000`, grudada |
| Régua | `#E5E5E5` |

Tipografia **Inter** — a fonte do veículo (`cnnSans`) é proprietária; Inter é
a neutra livre mais próxima.

O que distingue este registro do g1, e por isso define o sistema: lá a
manchete é vermelha e com tracking apertado; aqui é **preta e com tracking
normal**, e o vermelho fica reservado a título de seção, chapéu, marcador
e quadradinho de lista.

**A gramática é de portal; a marca é do autor.** Nenhum logo, wordmark ou
nome de veículo aparece na página, e o rodapé declara que o site não tem
vínculo com imprensa.

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
