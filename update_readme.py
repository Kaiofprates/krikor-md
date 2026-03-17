import chess
import hashlib
import json
import os
import subprocess

STATE_FILE = "game_state.json"
README_FILE = "README.md"
BOARD_FILE = "board.svg"

# Replace with your actual GitHub repo info
repo_full_name = os.environ.get("GITHUB_REPOSITORY", "")

if not repo_full_name:
    try:
        remote_url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], stderr=subprocess.DEVNULL
        ).decode().strip()
        # Handle both https and ssh URLs
        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]
        if "github.com/" in remote_url:
            repo_full_name = remote_url.split("github.com/")[-1]
        elif "github.com:" in remote_url:
            repo_full_name = remote_url.split("github.com:")[-1]
    except Exception:
        repo_full_name = "YOUR_GITHUB_USERNAME/YOUR_REPO_NAME"

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
    content = f"""# ♟️ Krikor Chess Actions

Um jogo de xadrez colaborativo direto no GitHub — jogue abrindo Issues!

## Tabuleiro Atual
Vez das: **{turn}**

![Tabuleiro]({BOARD_FILE}?v={hashlib.md5(board.fen().encode()).hexdigest()[:8]})

## Como Jogar
Clique em um dos links abaixo para fazer sua jogada. Isso abrirá uma Issue pré-preenchida. Basta clicar em **"Submit new issue"** para confirmar o movimento.

### Movimentos Legais
"""

    # Group legal moves by piece type
    piece_groups = {
        "♚ Rei": [],
        "♛ Dama": [],
        "♜ Torre": [],
        "♝ Bispo": [],
        "♞ Cavalo": [],
        "♟ Peão": [],
    }

    piece_map = {
        "K": "♚ Rei",
        "Q": "♛ Dama",
        "R": "♜ Torre",
        "B": "♝ Bispo",
        "N": "♞ Cavalo",
    }

    legal_moves = list(board.legal_moves)
    for move in legal_moves:
        san = board.san(move)
        # First char uppercase = piece move, otherwise pawn
        if san[0].isupper():
            group = piece_map.get(san[0], "♟ Peão")
        else:
            group = "♟ Peão"
        issue_url = f"https://github.com/{USER}/{REPO}/issues/new?title=Chess+Move:+{san}"
        piece_groups[group].append(f"[`{san}`]({issue_url})")

    for group_name, moves in piece_groups.items():
        if moves:
            content += f"\n**{group_name}** · {' '.join(moves)}\n"

    move_number = board.fullmove_number
    reset_url = f"https://github.com/{USER}/{REPO}/issues/new?title=Chess+Reset&body=Clique+em+Submit+para+reiniciar+a+partida"
    content += f"""
---
♟️ Partida em andamento · Jogada #{move_number} · [🔄 Reiniciar Partida]({reset_url})
"""

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_readme()
