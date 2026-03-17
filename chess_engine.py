import chess
import chess.svg
import json
import os
import sys

STATE_FILE = "game_state.json"
BOARD_FILE = "board.svg"

def init_game():
    board = chess.Board()
    save_state(board, last_move=None)
    render_board(board, last_move=None)

def save_state(board, last_move=None):
    data = {"fen": board.fen()}
    if last_move:
        data["last_move"] = last_move.uci()
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return chess.Board(), None
    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        board = chess.Board(data["fen"])
        last_move = chess.Move.from_uci(data["last_move"]) if "last_move" in data else None
        return board, last_move

def render_board(board, last_move=None):
    svg_data = chess.svg.board(
        board=board,
        size=480,
        coordinates=True,
        colors={
            "square light": "#eeeed2",
            "square dark": "#769656",
            "square light lastmove": "#f6f669",
            "square dark lastmove": "#baca2b",
        },
        lastmove=last_move,
    )
    with open(BOARD_FILE, "w") as f:
        f.write(svg_data)

def make_move(move_san):
    board, _ = load_state()
    try:
        move = board.parse_san(move_san)
        if move in board.legal_moves:
            board.push(move)
            save_state(board, last_move=move)
            render_board(board, last_move=move)
            return True, f"Move {move_san} successful!"
        else:
            return False, f"Move {move_san} is illegal."
    except ValueError:
        return False, f"Invalid SAN notation: {move_san}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "init":
            init_game()
            print("Game initialized.")
        elif command == "move":
            move_san = sys.argv[2]
            success, msg = make_move(move_san)
            print(msg)
            if not success:
                sys.exit(1)
    else:
        print("Usage: python chess_engine.py [init|move <san>]")
