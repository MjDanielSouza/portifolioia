# Reconstituição com IA — estudo de caso

Página de portfólio que mostra, etapa por etapa, como fotos de inquérito e
um depoimento viraram um filme de reconstituição forense.

**No ar:** https://mjdanielsouza.github.io/portifolioia/

## O que tem na página

| Bloco | Conteúdo |
|---|---|
| O caso | Os fatos, sem nomes, com link para a reportagem |
| As cinco etapas | Stepper navegável — referência, cenário, personagens, frames, vídeos |
| Antes / depois | Slider arrastável: foto do inquérito ↔ cenário limpo por IA |
| Da foto ao personagem | Os três pares referência → character sheet |
| O filme | Os dois cortes finais, 16:9 e 9:16 |
| Comparativo | Contra reconstituição filmada |

Os **14 planos gerados** estão na etapa 05, cortados em ~3 s e em loop.

## Estrutura

```
index.html            página inteira (CSS e JS embutidos)
assets/img/    31     imagens das etapas
assets/vid/    16     14 takes + os 2 cortes do filme
assets/poster/ 16     primeiro quadro de cada vídeo
assets/fonts/   6     Montserrat e Roboto Mono, subconjunto latin
assets/og.jpg         imagem de compartilhamento
robots.txt            fora de buscadores
.nojekyll             desliga o Jekyll
```

Caminhos **relativos** em tudo — funciona tanto na raiz quanto em
`usuario.github.io/repositorio/`. Sem dependência externa: as fontes estão
no repositório, não vêm do Google Fonts.

## Publicar

Pages servindo de `main` / raiz. Depois de qualquer alteração:

```bash
git add -A && git commit -m "atualiza site" && git push
```

O deploy leva cerca de um minuto.

## Sobre o conteúdo

As imagens integram processo criminal com julgamento concluído em janeiro
de 2026 e reportagem pública. Uso restrito à demonstração do método.

A página traz `noindex` e o `robots.txt` bloqueia rastreadores — ela abre
por link, mas não aparece em busca. **Atenção:** isso vale para o site.
Os arquivos continuam visíveis em `github.com/MjDanielSouza/portifolioia`,
porque o repositório é público, e ficam no histórico do git mesmo se forem
removidos depois.

## Pendência

A linha **"Prazo"** do comparativo está em branco de propósito — é o único
número que dependia de dado real. Procure por `preencha com seu número` no
`index.html`.

---

Daniel Souza · [@7danielsouza](https://instagram.com/7danielsouza)
