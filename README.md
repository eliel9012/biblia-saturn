# Bíblia para Sega Saturn

## English

Playable Portuguese Bible build for the Sega Saturn, with source, release images, and screenshots kept together in the repository.

### Status

- final build available in `saturn_app/game.iso` and `saturn_app/game.cue`
- clean 320x240 screenshots available in `saturn_app/1.png`, `saturn_app/2.png`, `saturn_app/3.png`, and `saturn_app/4.png`
- readable 320x240 verse bitmap preview available in `saturn_app/versiculo.png`
- repository organized for publication and optional rebuilds

### Final ROM Images

- `saturn_app/game.cue`
- `saturn_app/game.iso`

These are the official release files tracked in the project.

### Project Structure

- `saturn_app/`: Saturn app source and build artifacts
- `saturn_app/cd/`: CD-side data files such as text, fonts, and assets
- `tools/`: helper scripts for asset generation
- `tools/gen_readable_bitmap_preview.py`: generates the high-contrast 320x240 verse bitmap preview
- `docs/saturn-bitmap-legibility-prompt.md`: prompt and checklist for readable Saturn bitmap art
- `acf_clean.json`: Bible source text used during generation

### Optional Rebuild

Requirements:

- Linux
- Python 3
- Jo Engine installed locally

Build:

```bash
cd saturn_app
./compile.sh
```

This regenerates the assets and rebuilds `game.iso` and `game.cue`.

### Quick Test

Open `saturn_app/game.cue` in a Sega Saturn emulator such as Yabause, Kronos, or Mednafen, or use the image on real hardware.

## Português

Build jogável da Bíblia em português para Sega Saturn, com código-fonte, imagens finais e screenshots mantidos no mesmo repositório.

### Status

- build final disponível em `saturn_app/game.iso` e `saturn_app/game.cue`
- screenshots limpos 320x240 disponíveis em `saturn_app/1.png`, `saturn_app/2.png`, `saturn_app/3.png` e `saturn_app/4.png`
- preview legível 320x240 de versículo disponível em `saturn_app/versiculo.png`
- repositório organizado para publicação e recompilação opcional

### Imagens Finais da ROM

- `saturn_app/game.cue`
- `saturn_app/game.iso`

Esses são os arquivos oficiais de release do projeto.

### Estrutura do Projeto

- `saturn_app/`: código-fonte da aplicação Saturn e artefatos de build
- `saturn_app/cd/`: arquivos de dados do CD, como texto, fontes e assets
- `tools/`: scripts auxiliares para geração de assets
- `tools/gen_readable_bitmap_preview.py`: gera o preview de versículo 320x240 com alto contraste
- `docs/saturn-bitmap-legibility-prompt.md`: prompt e checklist para arte bitmap legível no Saturn
- `acf_clean.json`: texto-base da Bíblia usado na geração

### Recompilação Opcional

Requisitos:

- Linux
- Python 3
- Jo Engine instalado localmente

Build:

```bash
cd saturn_app
./compile.sh
```

Isso regenera os assets e recompila `game.iso` e `game.cue`.

### Teste Rápido

Abra `saturn_app/game.cue` em um emulador de Sega Saturn como Yabause, Kronos ou Mednafen, ou use a imagem em hardware real.
