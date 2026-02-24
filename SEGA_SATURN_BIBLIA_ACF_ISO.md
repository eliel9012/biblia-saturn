# Sugestão de ISO Sega Saturn — Bíblia ACF

## Visão geral
Uma ISO para Sega Saturn focada na leitura da Bíblia Almeida Corrigida Fiel (ACF), com navegação rápida, interface simples e conteúdos extras opcionais (mapas, imagens e pequenos vídeos em resolução compatível com o Saturn). O objetivo é manter tudo leve, responsivo e fiel ao estilo 32-bit da época.

---

## Especificação técnica (proposta)

### Plataforma e mídia
- **Mídia**: CD-ROM (ISO 9660 + arquivos de dados)
- **Console**: Sega Saturn (VCD/CRAM, VDP1/VDP2)
- **Língua**: Português (pt-BR)
- **Entrada**: Controle padrão (D-Pad, A/B/C, X/Y/Z, L/R, Start)

### Resoluções e vídeo
- **Resolução principal**: 320x240 (NTSC) ou 320x256 (PAL) 16-bit
- **Modo de texto**: 320x240 com fonte bitmap 8x8 ou 8x12
- **Vídeos (opcional)**:
  - **Codec**: Cinepak (comum em Saturn) ou MJPEG simples
  - **Resolução**: 320x240
  - **FPS**: 15–20 fps (estável)
  - **Áudio**: PCM 22050 Hz mono ou stereo leve

### Resolução Saturn (referência rápida)
- **NTSC**: 320x240
- **PAL**: 320x256
- **Cor**: 15-bit (5:5:5), dither suave para gradientes
- **Formato de arte**: PNG sem compressão pesada, depois converter para tiles/sprites conforme o pipeline

### Áudio
- **BGM**: Redbook (CD-DA) ou PCM ADPCM
- **Efeitos**: PCM simples para navegação

### Armazenamento e desempenho
- **Texto**: compactado por livros (ex: LZ ou RLE leve)
- **Índice**: tabelas de referências (livro, capítulo, versículo)
- **Cache**: pré-carregar capítulo atual + próximos 1–2

---

## Estrutura de conteúdo

### Bíblia ACF
- **Livros**: 66 livros
- **Navegação**:
  - Livro > Capítulo > Versículo
  - Busca rápida (por palavra)
  - Favoritos e marcadores

### Conteúdos adicionais
- **Introduções**: breve resumo por livro
- **Mapas**: mapas bíblicos em baixa resolução (320x240)
- **Imagens**: gravuras temáticas (armazenadas como sprites/tiles)
- **Timeline**: linha do tempo bíblica com eventos principais
- **Vídeos curtos** (opcional):
  - Abertura (logo + tema)
  - Introdução histórica (30–60s)

---

## Interface e menus

### Tela inicial
- Logo “Bíblia ACF Saturn”
- Menu principal:
  1. Ler Bíblia
  2. Buscar
  3. Favoritos
  4. Mapas e imagens
  5. Linha do tempo
  6. Configurações

### Navegação
- **D-Pad**: mover seleção
- **A**: confirmar
- **B**: voltar
- **L/R**: trocar capítulo
- **Start**: menu rápido

### Menu rápido (durante leitura)
- Ir para capítulo
- Buscar palavra
- Adicionar favorito
- Modo noturno (fundo escuro + texto claro)

---

## Plano de fundos e visual

### Estilo geral
- **Tema**: clássico 32-bit, tons pergaminho e azul escuro
- **VDP2**: planos de fundo com gradiente suave + padrão sutil
- **VDP1**: sprites para ícones e frames

### Planos de fundo sugeridos
- **Menu principal**: pergaminho com ornamentos
- **Leitura**: fundo neutro (bege ou cinza claro)
- **Mapas**: textura de mapa antigo

---

## Tipografia e legibilidade
- **Fonte principal**: bitmap 8x12, alta legibilidade
- **Destaques**: palavras de Cristo em vermelho (opcional)
- **Ajustes**: tamanho de fonte (pequeno/médio/grande)

---

## Conteúdos visuais

### Imagens
- Gravuras bíblicas em baixa resolução
- Ícones temáticos (arca, cruz, pergaminho)

### Mapas
- Israel antigo
- Rotas de Paulo
- Jerusalém e arredores

### Vídeos (opcional)
- **Intro**: 20–30s com logotipo e versículo temático
- **Mini-documento**: 60–90s sobre contexto histórico

---

## Exemplos de telas

### Leitura
- Cabeçalho: livro + capítulo
- Corpo: texto alinhado em colunas simples
- Rodapé: número do versículo + dicas de controle

### Busca
- Campo de busca com teclado na tela
- Lista de resultados com rolagem

---

## Observações finais
- O foco é manter o desempenho fluido e a leitura confortável.
- Vídeos e imagens devem ser opcionais para reduzir tamanho da ISO.
- A navegação deve ser simples, com poucos passos por ação.

---

## Geração de imagens (Nano Banana) — prompts + resolução Saturn

### Regras de produção (para ficar perfeito no Saturn)
- **Saída final**: 320x240 (NTSC) ou 320x256 (PAL)
- **No Nano Banana**: **Aspect ratio 4:3** + **Resolução 1K** (2K se precisar de detalhe)
- **Fluxo sugerido**: gerar em 1K/2K, **reduzir** para 320x240/256 com dither leve
- **Paleta**: reduzir para 15-bit (5:5:5), evitar gradientes longos sem dither
- **Estilo**: “32-bit era”, leve granulado, bordas limpas, contraste moderado

### Resolução no Nano Banana (referência)
- **1K / 2K / 4K** (o tamanho exato em pixels varia com o aspect ratio)

### Prompts prontos (texto -> imagem)
Use o modelo Nano Banana com **aspect ratio 4:3** e gere em **1K**. Depois reduza para **320x240** (ou 320x256 no PAL).

1) **Tela inicial (pergaminho + logo)**
Prompt:
"old parchment background with subtle golden ornaments, dark navy border frame, empty center area for logo, 1990s 32-bit console UI vibe, soft grain, warm light, no text"
Saída Saturn: 320x240
com **aspect ratio 4:3** e gere em **1K**

2) **Leitura (fundo neutro)**
Prompt:
"clean parchment paper texture, very subtle fiber, low contrast, warm beige, minimal pattern, calm and readable, 32-bit console aesthetic, no text"
Saída Saturn: 320x240

3) **Menu principal (tema clássico)**
Prompt:
"classic 32-bit UI background, deep navy to teal gradient, faint geometric pattern, gold accents in the corners, soft vignette, no text, 4:3"
Saída Saturn: 320x240

4) **Mapa antigo (base para overlays)**
Prompt:
"ancient map parchment texture, faint contour lines, sepia ink, soft stains, hand-drawn feel, no labels, no text, 4:3"
Saída Saturn: 320x240

5) **Linha do tempo (base)**
Prompt:
"aged parchment with horizontal timeline guide lines, subtle sepia ink strokes, empty space for event markers, 32-bit console style, no text, 4:3"
Saída Saturn: 320x240

6) **Tela de busca (teclado virtual)**
Prompt:
"clean UI panel background, light stone texture, subtle shadowed panels, 1990s console UI, soft highlights, no text"
Saída Saturn: 320x240

7) **Gravuras temáticas (pack)**
Prompt:
"biblical engraving style illustration, monochrome sepia, high contrast ink lines, 19th century etching vibe, 4:3, no text"
Saída Saturn: 320x240

8) **Ícones (lote 1: arca, cruz, pergaminho)**
Prompt:
"icon set, ark of the covenant, simple cross, rolled parchment, clean silhouette, 32-bit console sprite style, flat colors, no text, transparent background"
Saída Saturn: 320x240 (depois recortar sprites individuais)

9) **Abertura (frame base)**
Prompt:
"dramatic light rays over parchment, subtle gold glow, cinematic 32-bit intro frame, empty center for logo, no text, 4:3"
Saída Saturn: 320x240

### Background por livro (menu de capítulos ou menu do livro)
Gerar **2 imagens por livro**, usando o mesmo tema e estilos diferentes:

**Estilo A (gravura/pergaminho) — prompt base**
"biblical book background, {TEMA}, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"

**Estilo B (pintura suave) — prompt base**
"biblical book background, {TEMA}, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

Lista de temas por livro (uma linha por livro; use o mesmo {TEMA} nos dois estilos):
- **Gênesis**: luz da criação, oceano, estrelas, jardim
- **Êxodo**: jornada no deserto, mar Vermelho, coluna de fogo
- **Levítico**: altar, incenso, símbolos sagrados
- **Números**: acampamento no deserto, tendas, céu noturno
- **Deuteronômio**: tábuas da lei, aliança
- **Josué**: travessia do Jordão, cidade fortificada
- **Juízes**: colinas rústicas, oliveiras, era dos juízes
- **Rute**: campos de trigo, colheita, paz rural
- **1 Samuel**: unção com óleo, início do reino
- **2 Samuel**: cidade real, silhueta do palácio
- **1 Reis**: templo majestoso, pilares de cedro
- **2 Reis**: reino dividido, glória em declínio
- **1 Crônicas**: genealogias, planos do templo
- **2 Crônicas**: adoração, átrios do templo
- **Esdras**: pergaminhos, reconstrução dos muros
- **Neemias**: muros da cidade, restauração
- **Ester**: palácio real, elegância sutil
- **Jó**: céu tempestuoso, cinzas, paciência
- **Salmos**: harpa, montanhas, amanhecer
- **Provérbios**: lâmpada, pergaminho aberto, sabedoria
- **Eclesiastes**: relógio de sol, crepúsculo silencioso
- **Cantares**: lírios, vinhedo, romance suave
- **Isaías**: visão do trono, brasa acesa
- **Jeremias**: profeta em pranto, jarro quebrado
- **Lamentações**: ruínas, luto, entardecer
- **Ezequiel**: rodas de fogo, rio
- **Daniel**: cova dos leões, estrelas da noite
- **Oséias**: corrente quebrada, campo restaurado
- **Joel**: sombra de gafanhotos, trombeta de alerta
- **Amós**: prumo, campos rurais
- **Obadias**: penhascos rochosos, lugares altos
- **Jonas**: ondas do mar, silhueta do grande peixe
- **Miquéias**: colinas de pastores, caminho de Belém
- **Naum**: tempestade, muros da cidade tremendo
- **Habacuque**: torre de vigia, espera
- **Sofonias**: chamada de trombeta, céu solene
- **Ageu**: reconstrução do templo, blocos de pedra
- **Zacarias**: oliveiras, candelabro dourado
- **Malaquias**: fogo do refinador, altar
- **Mateus**: estrela sobre Belém, linhagem real
- **Marcos**: caminho no deserto, servo-rei
- **Lucas**: luz de cura, amanhecer suave
- **João**: luz e água, cruz simples
- **Atos**: jornada de navio, estrada aberta
- **Romanos**: selo real, balança da justiça
- **1 Coríntios**: colunas da igreja, unidade
- **2 Coríntios**: cidade restaurada, consolo
- **Gálatas**: portão aberto, liberdade
- **Efésios**: armadura, batalha espiritual
- **Filipenses**: amanhecer alegre, correntes
- **Colossenses**: trono, supremacia
- **1 Tessalonicenses**: trombeta, esperança
- **2 Tessalonicenses**: chama constante, paciência
- **1 Timóteo**: cajado de pastor, orientação
- **2 Timóteo**: tocha passando, perseverança
- **Tito**: casa ordenada, integridade
- **Filemom**: aperto de mãos, reconciliação
- **Hebreus**: véu do sumo sacerdote, templo celestial
- **Tiago**: ramo de oliveira, sabedoria prática
- **1 Pedro**: fogo de prova, rocha firme
- **2 Pedro**: farol, advertência
- **1 João**: luz do coração, comunhão
- **2 João**: portal, verdade
- **3 João**: estrada de viajantes, hospitalidade
- **Judas**: vigia alerta, guardando
- **Apocalipse**: trono e arco-íris, nova cidade


### Prompts finais por livro (copiar e colar)
Para cada livro, gere **Estilo A** e **Estilo B** com os prompts abaixo.

**Gênesis — Estilo A**
Prompt: "biblical book background, luz da criação, oceano, estrelas, jardim, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Gênesis — Estilo B**
Prompt: "biblical book background, luz da criação, oceano, estrelas, jardim, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Êxodo — Estilo A**
Prompt: "biblical book background, jornada no deserto, mar Vermelho, coluna de fogo, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Êxodo — Estilo B**
Prompt: "biblical book background, jornada no deserto, mar Vermelho, coluna de fogo, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Levítico — Estilo A**
Prompt: "biblical book background, altar, incenso, símbolos sagrados, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Levítico — Estilo B**
Prompt: "biblical book background, altar, incenso, símbolos sagrados, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Números — Estilo A**
Prompt: "biblical book background, acampamento no deserto, tendas, céu noturno, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Números — Estilo B**
Prompt: "biblical book background, acampamento no deserto, tendas, céu noturno, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Deuteronômio — Estilo A**
Prompt: "biblical book background, tábuas da lei, aliança, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Deuteronômio — Estilo B**
Prompt: "biblical book background, tábuas da lei, aliança, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Josué — Estilo A**
Prompt: "biblical book background, travessia do Jordão, cidade fortificada, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Josué — Estilo B**
Prompt: "biblical book background, travessia do Jordão, cidade fortificada, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Juízes — Estilo A**
Prompt: "biblical book background, colinas rústicas, oliveiras, era dos juízes, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Juízes — Estilo B**
Prompt: "biblical book background, colinas rústicas, oliveiras, era dos juízes, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Rute — Estilo A**
Prompt: "biblical book background, campos de trigo, colheita, paz rural, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Rute — Estilo B**
Prompt: "biblical book background, campos de trigo, colheita, paz rural, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Samuel — Estilo A**
Prompt: "biblical book background, unção com óleo, início do reino, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Samuel — Estilo B**
Prompt: "biblical book background, unção com óleo, início do reino, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Samuel — Estilo A**
Prompt: "biblical book background, cidade real, silhueta do palácio, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Samuel — Estilo B**
Prompt: "biblical book background, cidade real, silhueta do palácio, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Reis — Estilo A**
Prompt: "biblical book background, templo majestoso, pilares de cedro, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Reis — Estilo B**
Prompt: "biblical book background, templo majestoso, pilares de cedro, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Reis — Estilo A**
Prompt: "biblical book background, reino dividido, glória em declínio, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Reis — Estilo B**
Prompt: "biblical book background, reino dividido, glória em declínio, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Crônicas — Estilo A**
Prompt: "biblical book background, genealogias, planos do templo, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Crônicas — Estilo B**
Prompt: "biblical book background, genealogias, planos do templo, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Crônicas — Estilo A**
Prompt: "biblical book background, adoração, átrios do templo, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Crônicas — Estilo B**
Prompt: "biblical book background, adoração, átrios do templo, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Esdras — Estilo A**
Prompt: "biblical book background, pergaminhos, reconstrução dos muros, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Esdras — Estilo B**
Prompt: "biblical book background, pergaminhos, reconstrução dos muros, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Neemias — Estilo A**
Prompt: "biblical book background, muros da cidade, restauração, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Neemias — Estilo B**
Prompt: "biblical book background, muros da cidade, restauração, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Ester — Estilo A**
Prompt: "biblical book background, palácio real, elegância sutil, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Ester — Estilo B**
Prompt: "biblical book background, palácio real, elegância sutil, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Jó — Estilo A**
Prompt: "biblical book background, céu tempestuoso, cinzas, paciência, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Jó — Estilo B**
Prompt: "biblical book background, céu tempestuoso, cinzas, paciência, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Salmos — Estilo A**
Prompt: "biblical book background, harpa, montanhas, amanhecer, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Salmos — Estilo B**
Prompt: "biblical book background, harpa, montanhas, amanhecer, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Provérbios — Estilo A**
Prompt: "biblical book background, lâmpada, pergaminho aberto, sabedoria, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Provérbios — Estilo B**
Prompt: "biblical book background, lâmpada, pergaminho aberto, sabedoria, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Eclesiastes — Estilo A**
Prompt: "biblical book background, relógio de sol, crepúsculo silencioso, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Eclesiastes — Estilo B**
Prompt: "biblical book background, relógio de sol, crepúsculo silencioso, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Cantares — Estilo A**
Prompt: "biblical book background, lírios, vinhedo, romance suave, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Cantares — Estilo B**
Prompt: "biblical book background, lírios, vinhedo, romance suave, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Isaías — Estilo A**
Prompt: "biblical book background, visão do trono, brasa acesa, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Isaías — Estilo B**
Prompt: "biblical book background, visão do trono, brasa acesa, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Jeremias — Estilo A**
Prompt: "biblical book background, profeta em pranto, jarro quebrado, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Jeremias — Estilo B**
Prompt: "biblical book background, profeta em pranto, jarro quebrado, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Lamentações — Estilo A**
Prompt: "biblical book background, ruínas, luto, entardecer, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Lamentações — Estilo B**
Prompt: "biblical book background, ruínas, luto, entardecer, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Ezequiel — Estilo A**
Prompt: "biblical book background, rodas de fogo, rio, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Ezequiel — Estilo B**
Prompt: "biblical book background, rodas de fogo, rio, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Daniel — Estilo A**
Prompt: "biblical book background, cova dos leões, estrelas da noite, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Daniel — Estilo B**
Prompt: "biblical book background, cova dos leões, estrelas da noite, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Oséias — Estilo A**
Prompt: "biblical book background, corrente quebrada, campo restaurado, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Oséias — Estilo B**
Prompt: "biblical book background, corrente quebrada, campo restaurado, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Joel — Estilo A**
Prompt: "biblical book background, sombra de gafanhotos, trombeta de alerta, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Joel — Estilo B**
Prompt: "biblical book background, sombra de gafanhotos, trombeta de alerta, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Amós — Estilo A**
Prompt: "biblical book background, prumo, campos rurais, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Amós — Estilo B**
Prompt: "biblical book background, prumo, campos rurais, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Obadias — Estilo A**
Prompt: "biblical book background, penhascos rochosos, lugares altos, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Obadias — Estilo B**
Prompt: "biblical book background, penhascos rochosos, lugares altos, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Jonas — Estilo A**
Prompt: "biblical book background, ondas do mar, silhueta do grande peixe, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Jonas — Estilo B**
Prompt: "biblical book background, ondas do mar, silhueta do grande peixe, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Miquéias — Estilo A**
Prompt: "biblical book background, colinas de pastores, caminho de Belém, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Miquéias — Estilo B**
Prompt: "biblical book background, colinas de pastores, caminho de Belém, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Naum — Estilo A**
Prompt: "biblical book background, tempestade, muros da cidade tremendo, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Naum — Estilo B**
Prompt: "biblical book background, tempestade, muros da cidade tremendo, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Habacuque — Estilo A**
Prompt: "biblical book background, torre de vigia, espera, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Habacuque — Estilo B**
Prompt: "biblical book background, torre de vigia, espera, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Sofonias — Estilo A**
Prompt: "biblical book background, chamada de trombeta, céu solene, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Sofonias — Estilo B**
Prompt: "biblical book background, chamada de trombeta, céu solene, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Ageu — Estilo A**
Prompt: "biblical book background, reconstrução do templo, blocos de pedra, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Ageu — Estilo B**
Prompt: "biblical book background, reconstrução do templo, blocos de pedra, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Zacarias — Estilo A**
Prompt: "biblical book background, oliveiras, candelabro dourado, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Zacarias — Estilo B**
Prompt: "biblical book background, oliveiras, candelabro dourado, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Malaquias — Estilo A**
Prompt: "biblical book background, fogo do refinador, altar, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Malaquias — Estilo B**
Prompt: "biblical book background, fogo do refinador, altar, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Mateus — Estilo A**
Prompt: "biblical book background, estrela sobre Belém, linhagem real, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Mateus — Estilo B**
Prompt: "biblical book background, estrela sobre Belém, linhagem real, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Marcos — Estilo A**
Prompt: "biblical book background, caminho no deserto, servo-rei, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Marcos — Estilo B**
Prompt: "biblical book background, caminho no deserto, servo-rei, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Lucas — Estilo A**
Prompt: "biblical book background, luz de cura, amanhecer suave, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Lucas — Estilo B**
Prompt: "biblical book background, luz de cura, amanhecer suave, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**João — Estilo A**
Prompt: "biblical book background, luz e água, cruz simples, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**João — Estilo B**
Prompt: "biblical book background, luz e água, cruz simples, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Atos — Estilo A**
Prompt: "biblical book background, jornada de navio, estrada aberta, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Atos — Estilo B**
Prompt: "biblical book background, jornada de navio, estrada aberta, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Romanos — Estilo A**
Prompt: "biblical book background, selo real, balança da justiça, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Romanos — Estilo B**
Prompt: "biblical book background, selo real, balança da justiça, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Coríntios — Estilo A**
Prompt: "biblical book background, colunas da igreja, unidade, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Coríntios — Estilo B**
Prompt: "biblical book background, colunas da igreja, unidade, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Coríntios — Estilo A**
Prompt: "biblical book background, cidade restaurada, consolo, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Coríntios — Estilo B**
Prompt: "biblical book background, cidade restaurada, consolo, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Gálatas — Estilo A**
Prompt: "biblical book background, portão aberto, liberdade, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Gálatas — Estilo B**
Prompt: "biblical book background, portão aberto, liberdade, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Efésios — Estilo A**
Prompt: "biblical book background, armadura, batalha espiritual, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Efésios — Estilo B**
Prompt: "biblical book background, armadura, batalha espiritual, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Filipenses — Estilo A**
Prompt: "biblical book background, amanhecer alegre, correntes, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Filipenses — Estilo B**
Prompt: "biblical book background, amanhecer alegre, correntes, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Colossenses — Estilo A**
Prompt: "biblical book background, trono, supremacia, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Colossenses — Estilo B**
Prompt: "biblical book background, trono, supremacia, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Tessalonicenses — Estilo A**
Prompt: "biblical book background, trombeta, esperança, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Tessalonicenses — Estilo B**
Prompt: "biblical book background, trombeta, esperança, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Tessalonicenses — Estilo A**
Prompt: "biblical book background, chama constante, paciência, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Tessalonicenses — Estilo B**
Prompt: "biblical book background, chama constante, paciência, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Timóteo — Estilo A**
Prompt: "biblical book background, cajado de pastor, orientação, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Timóteo — Estilo B**
Prompt: "biblical book background, cajado de pastor, orientação, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Timóteo — Estilo A**
Prompt: "biblical book background, tocha passando, perseverança, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Timóteo — Estilo B**
Prompt: "biblical book background, tocha passando, perseverança, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Tito — Estilo A**
Prompt: "biblical book background, casa ordenada, integridade, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Tito — Estilo B**
Prompt: "biblical book background, casa ordenada, integridade, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Filemom — Estilo A**
Prompt: "biblical book background, aperto de mãos, reconciliação, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Filemom — Estilo B**
Prompt: "biblical book background, aperto de mãos, reconciliação, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Hebreus — Estilo A**
Prompt: "biblical book background, véu do sumo sacerdote, templo celestial, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Hebreus — Estilo B**
Prompt: "biblical book background, véu do sumo sacerdote, templo celestial, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Tiago — Estilo A**
Prompt: "biblical book background, ramo de oliveira, sabedoria prática, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Tiago — Estilo B**
Prompt: "biblical book background, ramo de oliveira, sabedoria prática, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 Pedro — Estilo A**
Prompt: "biblical book background, fogo de prova, rocha firme, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 Pedro — Estilo B**
Prompt: "biblical book background, fogo de prova, rocha firme, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 Pedro — Estilo A**
Prompt: "biblical book background, farol, advertência, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 Pedro — Estilo B**
Prompt: "biblical book background, farol, advertência, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**1 João — Estilo A**
Prompt: "biblical book background, luz do coração, comunhão, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**1 João — Estilo B**
Prompt: "biblical book background, luz do coração, comunhão, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**2 João — Estilo A**
Prompt: "biblical book background, portal, verdade, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**2 João — Estilo B**
Prompt: "biblical book background, portal, verdade, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**3 João — Estilo A**
Prompt: "biblical book background, estrada de viajantes, hospitalidade, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**3 João — Estilo B**
Prompt: "biblical book background, estrada de viajantes, hospitalidade, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Judas — Estilo A**
Prompt: "biblical book background, vigia alerta, guardando, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Judas — Estilo B**
Prompt: "biblical book background, vigia alerta, guardando, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

**Apocalipse — Estilo A**
Prompt: "biblical book background, trono e arco-íris, nova cidade, parchment texture, sepia ink, engraved look, soft vignette, 32-bit console style, no text, 4:3"
**Apocalipse — Estilo B**
Prompt: "biblical book background, trono e arco-íris, nova cidade, soft painted look, warm light, subtle grain, classic 32-bit console art, no text, 4:3"

### Observações de conversão
- **Downscale**: usar filtro Lanczos + dither leve para manter detalhes
- **Sprites**: depois de gerar, recortar em tiles 16x16 ou 32x32
- **Consistência**: manter a mesma paleta base para todas as telas
