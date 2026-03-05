import chess
import chess.svg
import json
import os
import sys

STATE_FILE = "game_state.json"
BOARD_FILE = "board.svg"

def init_game():
    board = chess.Board()
    save_state(board)
    render_board(board)

def save_state(board):
    with open(STATE_FILE, "w") as f:
        json.dump({"fen": board.fen()}, f)

def load_state():
    if not os.path.exists(STATE_FILE):
        return chess.Board()
    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        return chess.Board(data["fen"])

def render_board(board):
    svg_data = chess.svg.board(board=board, size=400)
    with open(BOARD_FILE, "w") as f:
        f.write(svg_data)

def make_move(move_san):
    board = load_state()
    try:
        move = board.parse_san(move_san)
        if move in board.legal_moves:
            board.push(move)
            save_state(board)
            render_board(board)
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
