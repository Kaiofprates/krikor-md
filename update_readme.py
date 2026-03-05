import chess
import json
import os

STATE_FILE = "game_state.json"
README_FILE = "README.md"
BOARD_FILE = "board.svg"

# Replace with your actual GitHub repo info
repo_full_name = os.environ.get("GITHUB_REPOSITORY", "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME")
USER, REPO = repo_full_name.split("/", 1) if "/" in repo_full_name else ("USER", "REPO")

def load_state():
    if not os.path.exists(STATE_FILE):
        return chess.Board()
    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        return chess.Board(data["fen"])

def generate_readme():
    board = load_state()
    
    # Identify who's turn it is
    turn = "Brancas" if board.turn == chess.WHITE else "Pretas"
    
    # Start building the README content
    content = f"""# ♟️ Jogo de Xadrez no GitHub Actions

Este é um jogo de xadrez que você joga abrindo Issues!

## Tabuleiro Atual
Vez das: **{turn}**

![Tabuleiro]({BOARD_FILE})

## Como Jogar
Clique em um dos links abaixo para fazer sua jogada. Isso abrirá uma Issue pré-preenchida. Basta clicar em **"Submit new issue"** para confirmar o movimento.

### Movimentos Legais
"""
    
    # List legal moves as links
    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        san = board.san(move)
        issue_url = f"https://github.com/{USER}/{REPO}/issues/new?title=Chess+Move:+{san}"
        content += f"- [{san}]({issue_url})\n"

    content += f"""
---
Partida em andamento. Última atualização: {board.fen()}
"""

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_readme()
