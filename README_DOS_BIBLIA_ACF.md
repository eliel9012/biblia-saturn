# Biblia ACF (DOS-like)

Leitor em tela cheia (TUI) "estilo DOS" para o texto da Biblia ACF em `acf_clean.json`/`acf.json`.

## Rodar

No Linux (terminal):

```bash
cd ~/Downloads/SaturnBible
python3 dos_biblia_acf.py
```

Se quiser apontar outro arquivo:

```bash
python3 dos_biblia_acf.py --json /caminho/para/acf_clean.json
```

Teste rapido (sem curses):

```bash
python3 dos_biblia_acf.py --selftest
```

No Windows (PowerShell):

1. Instale o Python 3.
2. (Opcional) Se `curses` nao existir: `pip install windows-curses`
3. Rode `python dos_biblia_acf.py`

## Teclas

- `Enter`: selecionar
- `b` ou `ESC`: voltar
- `q`: sair
- `F1`: ajuda
- `Setas`: navegar
- `PgUp` / `PgDn`: rolar mais rapido
- `Left` / `Right`: capitulo anterior/proximo (no modo leitura)
- `g`: ir para verso (numero) (no modo leitura)
- `/`: buscar (global)

## Observacoes

- O programa tenta achar automaticamente `acf_clean.json`/`acf.json` no mesmo diretorio do script.
- O JSON precisa estar no formato "lista de livros", igual ao `acf_clean.json` deste projeto.

