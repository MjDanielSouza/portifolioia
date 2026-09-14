
import os as _os
# Caminhos relativos ao proprio script. Antes apontavam para a pasta
# temporaria da sessao, que nao sobrevive a uma conversa nova.
SP = _os.path.dirname(_os.path.abspath(__file__))   # .../SITE_GITHUB/build
G  = _os.path.dirname(SP)                           # .../SITE_GITHUB
# -*- coding: utf-8 -*-
"""Copy dos casos. Fica separado do manifesto porque manifesto e inventario
de arquivos; isto e texto, e texto se revisa a mao.

CASOS e a lista do que a pagina publica. O montar.py so monta o que estiver
aqui, entao tirar um caso do ar e mover o bloco dele para CASOS_FORA — o
prep_assets.py pode reler as pastas de origem sem ressuscitar o caso.
"""

CASOS = {
 "c1": {
   "num": "01",
   "titulo": "Dívida de R$ 400",
   "linha": "Homicídio e ocultação de cadáver",
   "local": "São José dos Pinhais · PR",
   "quando": "Maio de 2023 · júri em janeiro de 2026",
   "capa": "assets/c1/img/04_01.jpg",
   "resumo": """
     <p>Uma mulher de 35 anos desapareceu no fim de maio de 2023, numa área rural da
     Região Metropolitana de Curitiba. Em 1º de junho, um morador encontrou o corpo
     <strong>enterrado num terreno</strong> da localidade.</p>
     <p>A investigação apontou que ela foi morta dentro da casa de um vizinho, com quem
     tinha uma dívida de <strong>R$ 400</strong> referente a um celular. Com ajuda de um
     segundo homem, o corpo foi retirado do local e levado até o terreno em frente, onde
     foi enterrado. Em janeiro de 2026, o júri popular condenou o autor a
     <strong>oito anos e quatro meses</strong> por homicídio e ocultação de cadáver.</p>
     <p>A reconstituição foi montada a partir das fotos do inquérito e do relato do
     próprio acusado. <strong>Nenhuma pessoa foi filmada.</strong></p>
     <p class="fonte">Fonte pública do caso:
     <a href="https://www.bandab.com.br/seguranca/vizinho-condenado-matar-ocultar-corpo-mulher-grande-curitiba/" target="_blank" rel="noopener">Banda B — 21/01/2026</a>
     · Nomes omitidos por escolha editorial.</p>""",
   # pares antes/depois: so este caso tem chapa limpa
   "ba": [{"rot":"Garagem e escada", "a":"01_09", "b":"02_01"},
          {"rot":"Fundos da casa",   "a":"01_11", "b":"02_03"}],
   "deriv": [{"de":"01_01","para":"03_01","cap":"Foto do inquérito","cap2":"Personagem A · três vistas"},
             {"de":"01_06","para":"03_02","cap":"Foto do inquérito","cap2":"Personagem B · três vistas"},
             {"de":"01_07","para":"03_03","cap":"Foto de referência","cap2":"Personagem C · três vistas"}],
   "seq": {"arquivo":"assets/c1/vid/sequencia.mp4",
           "poster":"assets/c1/poster/sequencia.jpg",
           "texto":"Os 14 planos colados na ordem dos fatos, com cortes secos. "
                   "Não é a montagem final — é o material bruto em sequência, para "
                   "dar noção do percurso inteiro."},
 }
}

# Fora do ar desde 14/09/2026, a pedido do Daniel: a peca passou a mostrar
# so o caso 01. Para trazer de volta, mova o bloco para CASOS acima — o
# resto da pagina se ajusta sozinho, inclusive a barra de casos, que so
# aparece quando ha mais de um.
CASOS_FORA = {
 "c2": {
   "num": "02",
   "titulo": "Confusão na Ilha do Mel",
   "linha": "Importunação, desacato e termo circunstanciado",
   "local": "Ilha do Mel · litoral do PR",
   "quando": "Janeiro de 2026",
   "capa": "assets/c2/img/03_22.jpg",
   "resumo": """
     <p>Num comércio da Ilha do Mel, no litoral do Paraná, um influenciador digital de
     32 anos se aproximou de um cliente que estava com a esposa e
     <strong>passou a mão no peito do homem</strong>. O cliente reagiu com um tapa no
     rosto.</p>
     <p>Depois da reação, o influenciador passou a <strong>quebrar objetos do
     estabelecimento</strong>. A Polícia Militar foi acionada e conduziu os envolvidos
     à delegacia, onde ele acabou detido por desacato a um investigador — acusação que
     negou. Assinou termo circunstanciado e foi liberado.</p>
     <p>A reconstituição recria o percurso a partir das fotos do local, das imagens dos
     envolvidos e do relato. <strong>Nenhuma pessoa foi filmada.</strong></p>
     <p class="fonte">Fonte pública do caso:
     <a href="https://www.bandab.com.br/seguranca/influencer-confusao-ilha-do-mel-delegacia-parana/" target="_blank" rel="noopener">Banda B — 14/01/2026</a>
     · Nomes omitidos por escolha editorial.</p>""",
   "ba": [],
   "deriv": [{"de":"01_07","para":"02_01","cap":"Referência do envolvido","cap2":"Personagem A · três vistas"},
             {"de":"01_12","para":"02_02","cap":"Referência do cliente","cap2":"Personagem B · três vistas"},
             {"de":"01_13","para":"02_03","cap":"Referência da acompanhante","cap2":"Personagem C · três vistas"}],
   "seq": {"arquivo":"assets/c2/vid/sequencia.mp4",
           "poster":"assets/c2/poster/sequencia.jpg",
           "texto":"Os 11 planos colados na ordem dos fatos, com cortes secos. "
                   "Não é a montagem final — é o material gerado em sequência, para "
                   "dar noção do percurso inteiro."},
 },
}
