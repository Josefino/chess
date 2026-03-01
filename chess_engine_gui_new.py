import chess
import chess.polyglot
import sys
import time
import random
import tkinter as tk
import threading
import tempfile
import os
import struct
import math
from typing import List, Tuple, Optional

# ============ SOUND (macOS afplay) ============
def _write_wav(filename, freqs, durations, volume=0.6, sample_rate=44100):
    """Zapíše WAV soubor se sekvencí tónů."""
    samples = []
    for freq, dur in zip(freqs, durations):
        n = int(sample_rate * dur)
        attack = min(int(sample_rate * 0.008), n)
        release = min(int(sample_rate * 0.025), n)
        for i in range(n):
            val = math.sin(2 * math.pi * freq * i / sample_rate)
            if i < attack:
                val *= i / attack
            elif i >= n - release:
                val *= (n - i) / release
            samples.append(int(val * volume * 32767))

    num_samples = len(samples)
    num_channels = 1
    bits_per_sample = 16
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = num_samples * block_align

    with open(filename, 'wb') as f:
        # RIFF header
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + data_size))
        f.write(b'WAVE')
        # fmt chunk
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))           # PCM
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', bits_per_sample))
        # data chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        for s in samples:
            f.write(struct.pack('<h', s))

import subprocess

def _play_wav(filename):
    try:
        subprocess.Popen(
            ["afplay", filename],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print("Sound error:", e)

# Připrav WAV soubory při startu
_TMP_DIR = os.path.join(os.path.expanduser("~"), ".chess_sounds")
os.makedirs(_TMP_DIR, exist_ok=True)
_WAV_MOVE      = os.path.join(_TMP_DIR, "move.wav")
_WAV_CHECK     = os.path.join(_TMP_DIR, "check.wav")
_WAV_CHECKMATE = os.path.join(_TMP_DIR, "checkmate.wav")
_WAV_DRAW      = os.path.join(_TMP_DIR, "draw.wav")
_WAV_MATE_WARN = os.path.join(_TMP_DIR, "mate_warn.wav")

def _init_sounds():
    _write_wav(_WAV_MOVE,      [520, 680],           [0.055, 0.075])
    _write_wav(_WAV_CHECK,     [900, 670],           [0.13,  0.20])
    _write_wav(_WAV_CHECKMATE, [523, 659, 784, 1047],[0.13, 0.13, 0.13, 0.38])
    _write_wav(_WAV_DRAW,      [440, 370, 311],      [0.16, 0.16, 0.38])
    _write_wav(_WAV_MATE_WARN, [880, 660, 880],      [0.10, 0.08, 0.18])  # warning pulse

def sound_move():
    _play_wav(_WAV_MOVE)

def sound_check():
    _play_wav(_WAV_CHECK)

def sound_game_over(is_checkmate: bool):
    _play_wav(_WAV_CHECKMATE if is_checkmate else _WAV_DRAW)

def sound_mate_warning():
    _play_wav(_WAV_MATE_WARN)





# ============ CONFIGURATION ============
MAX_DEPTH = 4
TIME_LIMIT_PER_MOVE = 5.0          # increased to 12 s to allow deeper search
MAX_BOOK_MOVES = 25                 # opening book used up to 25 moves

PIECE_VALUES_MVV = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000
}

# ============ STATISTICS ============
nodes_searched = 0
max_depth_reached = 0

# ============ TRANSPOSITION TABLE ============
# Each entry: { zobrist_hash: (depth, flag, score, best_move) }
# flag: 'exact' | 'lower' (alpha) | 'upper' (beta)
TT: dict = {}
TT_MAX_SIZE = 1_000_000  # max entries to avoid unbounded memory use

def tt_store(key: int, depth: int, flag: str, score: int, move):
    if len(TT) >= TT_MAX_SIZE:
        TT.clear()  # simple eviction: clear when full
    TT[key] = (depth, flag, score, move)

def tt_lookup(key: int, depth: int, alpha: int, beta: int):
    """Returns (score, move) if usable hit, else (None, None)."""
    entry = TT.get(key)
    if entry is None:
        return None, None
    e_depth, e_flag, e_score, e_move = entry
    if e_depth >= depth:
        if e_flag == 'exact':
            return e_score, e_move
        if e_flag == 'lower' and e_score >= beta:
            return e_score, e_move
        if e_flag == 'upper' and e_score <= alpha:
            return e_score, e_move
    # Entry exists but not usable for cutoff – still return move for ordering
    return None, e_move

# ============ BUILT-IN OPENING BOOK ============
OPENING_BOOK = {
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR": [
        ("e2e4", 40), ("d2d4", 35), ("c2c4", 10), ("g1f3", 10), ("b1c3", 5)
    ],
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR": [
        ("e7e5", 50), ("c7c5", 40), ("e7e6", 5), ("g8f6", 5)
    ],
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR": [
        ("g1f3", 70), ("b1c3", 15), ("d2d4", 10), ("f1c4", 5)
    ],
    "rnbqkb1r/pppp1ppp/5n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R": [
        ("d2d4", 60), ("b1c3", 20), ("c2c4", 10), ("f1b5", 10)
    ],
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR": [
        ("g1f3", 70), ("b1c3", 20), ("d2d4", 10)
    ],
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR": [
        ("d7d5", 50), ("g8f6", 30), ("c7c5", 20)
    ],
    "rnbqkbnr/pppppppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR": [
        ("c2c4", 80), ("g1f3", 15), ("b1c3", 5)
    ],
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR": [
        ("c2c4", 70), ("g1f3", 20), ("b1c3", 10)
    ],
    "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R": [
        ("a7a6", 60), ("g8f6", 30), ("f8b4", 10)
    ],
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R": [
        ("g8f6", 50), ("b8c6", 30), ("d7d6", 20)
    ],
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR": [
        ("d2d4", 80), ("b1c3", 20)
    ],
    "rnbqkbnr/pppp1ppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR": [
        ("d2d4", 70), ("g1f3", 20), ("b1c3", 10)
    ],
    "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR": [
        ("e7e5", 50), ("c7c5", 30), ("g8f6", 20)
    ],
    "rnbqk2r/ppppppbp/5np1/8/2PP4/6N1/PP1PPP1P/RNBQKB1R": [
        ("b8g8", 40), ("d7d6", 40), ("f8g7", 20)
    ],
    "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR": [
        ("g8f6", 50), ("d7d5", 30), ("g8h6", 10), ("f5f6", 5), ("c7c5", 5)
    ],
    "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR": [
        ("d7d5", 60), ("g7g6", 20), ("f8b4", 10), ("e7e6", 10)
    ],
    "rnbqkb1r/ppp1pppp/5n2/3p4/3P4/2N5/PPP1PPPP/R1BQKBNR": [
        ("c1g5", 30), ("g1f3", 25), ("c2c4", 20), ("e2e4", 15), ("b2b3", 10)
    ],
    "r1bqkb1r/pppn1ppp/5n2/3p4/3P2B1/2N1P3/PPP1P1PP/R2QKB1R": [
        ("h7h6", 50), ("c7c5", 25), ("e7e6", 15), ("g7g6", 5), ("b7b6", 5)
    ],
    "r1bqkb1r/pppn1pp1/5np1/3p4/3P2B1/2N1P3/PPP1P1PP/R2QKB1R": [
        ("g5f4", 40), ("g5h4", 30), ("c2c4", 20), ("e2e4", 10)
    ],
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR": [
        ("e7e5", 45), ("c7c5", 35), ("e7e6", 10), ("c7c6", 10)
    ],
}

# ============ POSITION EVALUATION ============
# Piece-Square Tables (hodnoty v centipawnech, z pohledu bílého)
PST = {
    chess.PAWN: [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10, 5,  5,
        0,  0,  0, 20, 20,  0, 0,  0,
        5, -5, -10,  0,  0, -10, -5, 5,
        5, 10, 10, -20, -20, 10, 10, 5,
        0,  0,  0,  0,  0,  0,  0,  0
    ],
    chess.KNIGHT: [
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,  0,  0,  0,  0, -20, -40,
        -30,  0, 10, 15, 15, 10,  0, -30,
        -30,  5, 15, 20, 20, 15,  5, -30,
        -30,  0, 15, 20, 20, 15,  0, -30,
        -30,  5, 10, 15, 15, 10,  5, -30,
        -40, -20,  0,  5,  5,  0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ],
    chess.BISHOP: [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,  5,  0,  0,  0,  0,  5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10,  0, 10, 10, 10, 10,  0, -10,
        -10,  5,  5, 10, 10,  5,  5, -10,
        -10,  0,  5, 10, 10,  5,  0, -10,
        -10,  0,  0,  0,  0,  0,  0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ],
    chess.ROOK: [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ],
    chess.QUEEN: [
        -20, -10, -10, -5, -5, -10, -10, -20,
        -10,  0,  0,  0,  0,  0,  0, -10,
        -10,  0,  5,  5,  5,  5,  0, -10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0, -10,
        -10,  0,  5,  0,  0,  0,  0, -10,
        -20, -10, -10, -5, -5, -10, -10, -20
    ],
    chess.KING: [
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]
}

def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -999999 if board.turn == chess.WHITE else 999999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    white_score = 0
    black_score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            pt = piece.piece_type
            value = PIECE_VALUES_MVV.get(pt, 0)
            if piece.color == chess.WHITE:
                pst = PST.get(pt, [0]*64)[square]
                white_score += value + pst
            else:
                pst = PST.get(pt, [0]*64)[chess.square_mirror(square)]
                black_score += value + pst

    score = white_score - black_score

    # Mobility: difference in legal moves for both sides (2 cp per move)
    original_turn = board.turn
    board.turn = chess.WHITE
    white_mobility = board.legal_moves.count()
    board.turn = chess.BLACK
    black_mobility = board.legal_moves.count()
    board.turn = original_turn  # always restore correctly
    score += (white_mobility - black_mobility) * 2

    if board.is_check():
        score -= 50 if board.turn == chess.WHITE else 50

    return score
# ============ MOVE ORDERING ============
def sort_moves(board: chess.Board, moves: List[chess.Move]) -> List[chess.Move]:
    def move_score(m: chess.Move) -> int:
        if not board.is_capture(m):
            return 0
        captured = board.piece_at(m.to_square)
        if captured is None and board.is_en_passant(m):
            ep_rank_offset = -1 if board.turn == chess.WHITE else 1
            ep_file = chess.square_file(m.to_square)
            ep_rank = chess.square_rank(m.to_square) + ep_rank_offset
            ep_square = chess.square(ep_file, ep_rank)
            captured = board.piece_at(ep_square)
        victim_value = PIECE_VALUES_MVV.get(captured.piece_type if captured else chess.PAWN, 0)
        attacker = board.piece_at(m.from_square)
        attacker_value = PIECE_VALUES_MVV.get(attacker.piece_type if attacker else chess.PAWN, 0)
        return victim_value * 10 - attacker_value

    return sorted(moves, key=move_score, reverse=True)

# ============ QUIESCENCE SEARCH ============
def quiescence(board: chess.Board, alpha: int, beta: int, maximizing: bool) -> int:
    global nodes_searched
    nodes_searched += 1

    stand_pat = evaluate_board(board)
    if maximizing:
        alpha = max(alpha, stand_pat)
        if stand_pat >= beta: return beta
    else:
        beta = min(beta, stand_pat)
        if stand_pat <= alpha: return alpha

    if stand_pat + 880 < alpha:  # 880 = max hodnota dámy
        return alpha  # delta pruning

    captures = [m for m in board.legal_moves if board.is_capture(m)]
    captures = sort_moves(board, captures)

    for move in captures:
        board.push(move)
        score = quiescence(board, alpha, beta, not maximizing)
        board.pop()
        if maximizing:
            alpha = max(alpha, score)
            if alpha >= beta: return beta
        else:
            beta = min(beta, score)
            if beta <= alpha: return alpha
    return alpha if maximizing else beta

# ============ SEARCH ============
# ============ SEARCH ============
def search(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[chess.Move]]:
    global nodes_searched, max_depth_reached

    nodes_searched += 1

    current_depth = MAX_DEPTH - depth
    if current_depth > max_depth_reached:
        max_depth_reached = current_depth

    # Transposition table lookup
    key = chess.polyglot.zobrist_hash(board)
    orig_alpha = alpha
    tt_score, tt_move = tt_lookup(key, depth, alpha, beta)
    if tt_score is not None:
        return tt_score, tt_move

    if board.is_game_over():
        return evaluate_board(board), None

    if depth == 0:
        return quiescence(board, alpha, beta, maximizing), None

    # Use TT move first for better move ordering
    moves = sort_moves(board, list(board.legal_moves))
    if tt_move and tt_move in moves:
        moves.remove(tt_move)
        moves.insert(0, tt_move)

    best_move = None

    if maximizing:
        max_eval = -9999999
        for move in moves:
            board.push(move)
            eval_score, _ = search(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # beta cutoff
        flag = 'exact' if orig_alpha < max_eval < beta else ('lower' if max_eval >= beta else 'upper')
        tt_store(key, depth, flag, max_eval, best_move)
        return max_eval, best_move
    else:
        min_eval = 9999999
        for move in moves:
            board.push(move)
            eval_score, _ = search(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # alpha cutoff
        flag = 'exact' if orig_alpha < min_eval < beta else ('lower' if min_eval >= beta else 'upper')
        tt_store(key, depth, flag, min_eval, best_move)
        return min_eval, best_move

# ============ ITERATIVE DEEPENING ============
def iterative_deepening(board: chess.Board, max_depth: int, time_limit: float) -> Optional[chess.Move]:
    global nodes_searched, max_depth_reached

    best_move = None
    start_time = time.time()

    for depth in range(1, max_depth + 1):
        if time.time() - start_time > time_limit:
            break

        alpha = -9999999
        beta = 9999999
        moves = sort_moves(board, list(board.legal_moves))

        if board.turn == chess.WHITE:
            current_best = -9999999
            current_move = None
            for move in moves:
                board.push(move)
                score, _ = search(board, depth - 1, alpha, beta, False)
                board.pop()
                if score > current_best:
                    current_best = score
                    current_move = move
                alpha = max(alpha, score)
                if beta <= alpha: break
            if current_move: best_move = current_move
        else:
            current_best = 9999999
            current_move = None
            for move in moves:
                board.push(move)
                score, _ = search(board, depth - 1, alpha, beta, True)
                board.pop()
                if score < current_best:
                    current_best = score
                    current_move = move
                beta = min(beta, score)
                if beta <= alpha: break
            if current_move: best_move = current_move

    return best_move

# ============ OPENING BOOK ============
def opening_book_move(board: chess.Board) -> Optional[chess.Move]:
    try:
        import chess.polyglot
        with chess.polyglot.open_reader("book.bin") as reader:
            entries = list(reader.find_all(board))
            if entries:
                best_entry = max(entries, key=lambda e: e.weight)
                return best_entry.move
    except (FileNotFoundError, ImportError, OSError):
        pass

    fen_key = board.fen().split()[0]
    if fen_key in OPENING_BOOK:
        ucis, weights = zip(*OPENING_BOOK[fen_key])
        uci = random.choices(ucis, weights=weights)[0]
        move = chess.Move.from_uci(uci)
        if move in board.legal_moves:
            return move
    return None

# ============ MATE IN N ============
def find_mate_in_n(board: chess.Board, max_moves: int = 8) -> Optional[int]:
    """
    Returns the number of moves to forced mate for the side to move.
    - None = no forced mate within max_moves
    - 1 = mate in 1 (immediate mate after current move)
    - 2 = mate in 2, etc.
    """
    if board.is_checkmate():
        return 0  # already mate (should not happen here)

    def recursive_search(depth: int, maximizing: bool) -> Optional[int]:
        if depth == 0:
            return None

        legal_moves = list(board.legal_moves)
        if not legal_moves:
            if board.is_check():
                return 0  # checkmate!
            return None  # stalemate, not mate

        if maximizing:
            # Trying to deliver mate (find shortest path)
            shortest = None
            for move in legal_moves:
                board.push(move)
                result = recursive_search(depth - 1, False)
                board.pop()

                if result is not None:
                    moves_to_mate = result + 1
                    if shortest is None or moves_to_mate < shortest:
                        shortest = moves_to_mate
            return shortest
        else:
            # Opponent trying to avoid mate
            all_lead_to_mate = True
            longest_delay = -999999
            for move in legal_moves:
                board.push(move)
                result = recursive_search(depth - 1, True)
                board.pop()

                if result is None:
                    all_lead_to_mate = False
                    break  # escape found → no forced mate
                longest_delay = max(longest_delay, result)

            if all_lead_to_mate:
                return longest_delay
            return None

    # Call from current player's perspective
    return recursive_search(max_moves, True)

# ============ AI MOVE (statistics printed here) ============
def ai_move(board: chess.Board) -> Optional[chess.Move]:
    global nodes_searched, max_depth_reached
    
    # reset statistics
    nodes_searched = 0
    max_depth_reached = 0
    
    # Opening book – ONLY push if LEGAL
    if len(board.move_stack) < MAX_BOOK_MOVES:
        book_move = opening_book_move(board)
        if book_move:
            if book_move in board.legal_moves:
                print(f"AI (book): {book_move.uci()} (0.0s)")
                
                return book_move
            else:
                print(f"WARNING: Book suggested ILLEGAL move {book_move.uci()} in FEN {board.fen()} – falling back to search")
    
    print("AI is thinking...")
    start = time.time()
    move = iterative_deepening(board, MAX_DEPTH, TIME_LIMIT_PER_MOVE)
    end = time.time()

        
    if move:
        # push the move to the board
        board.push(move)

        # check if the move gives check
        check_sign = "+" if board.is_check() else ""

        # evaluate the current position AFTER the move (since AI just moved)
        evaluation = evaluate_board(board)
        board.pop() #back board, push will be in mine()

        # MATE DETECTION – only when eval suggests strong advantage (> 3 pawns)
        if abs(evaluation) > 0:
            mate_in = find_mate_in_n(board, max_moves=6)
        else:
            mate_in = None

        # Convert centipawns to pawns (positive = White advantage)
        if evaluation > 0:
            eval_display = f"+{evaluation / 100:.2f}"
        elif evaluation < 0:
            eval_display = f"{evaluation / 100:.2f}"
        else:
            eval_display = "0.00"
        
        
       
        # Build output
        output = f"AI: {move.uci()}{check_sign} " \
                 f"(time: {end-start:.1f}s | " \
                 f"depth: {max_depth_reached} | " \
                 f"nodes: {nodes_searched/1_000_000:.2f}MN | " \
                 f"eval: {eval_display}"
       
        if mate_in is not None :
            if mate_in == 1:
                mate_text = "Mate in 1!"
            elif mate_in == 2:
                mate_text = "Mate in 2!"
            elif mate_in == 3:
                mate_text = "Mate in 3!"
            else:
                mate_text = f"Mate in {mate_in}!"
            output += f" | **{mate_text}**"
       
        output += ")"
        print(output)
       
        return move
    else:
        print("AI failed to find a move!")
        return None

# ============ BOARD DISPLAY ============
def print_nice_board(board: chess.Board):
    uni = board.unicode(empty_square="·")
    lines = uni.split("\n")
    print("\n  a b c d e f g h")
    for r in range(8):
        print(f"{8-r} {lines[r]} {8-r}")
    print("  a b c d e f g h\n")

    # ============================================================
# PROFESSIONAL GUI CONTROLLER
# ============================================================

class ChessApp:
    LIGHT     = "#F0D9B5"
    DARK      = "#B58863"
    HIGHLIGHT = "#F6F669"
    SELECTED  = "#7FC97F"

    PIECES = {
        'P': '♟', 'N': '♞', 'B': '♝', 'R': '♜', 'Q': '♛', 'K': '♚',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    }

    def __init__(self):
        self.last_tick = time.time()
        self.animating = False
        self.animation_speed = 12   # čím větší, tím rychlejší
        self.last_move = None
        self.auto_color = None
        self.board = chess.Board()
        # ===== CHESS CLOCK =====
        self.start_time_seconds = 1800  # 30 minut
        self.white_time = self.start_time_seconds
        self.black_time = self.start_time_seconds
        self.clock_running = False  # starts after first move
        self.auto_running = False
        self.ai_thread = None
        self.selected_square = None
        self.legal_targets = set()

        self.root = tk.Tk()
        self.root.title("Chess Engine")
        # self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        screen = min(sw, sh)
        self.cell = int(int(screen * 0.8) // 8)

        self.main = tk.Frame(self.root, bg="#1E1E1E")
        self.main.pack(fill="both", expand=True)

        # levá část (pro centrování)
        self.board_frame = tk.Frame(self.main, bg="#1E1E1E")
        self.board_frame.pack(side="left", fill="both", expand=True)

        # šachovnice bude uvnitř tohoto frame
        self.canvas = tk.Canvas(self.board_frame,
                                width=self.cell*8,
                                height=self.cell*8)
        self.canvas.pack(expand=True)  # TOTO JE KLÍČ

        # pravý panel
        self.side = tk.Frame(self.main, bg="#2A2A2A", width=240)
        self.side.pack(side="right", fill="y")
        self.side.pack_propagate(False)   # ← DŮLEŽITÉ

        # info panel height: 4 positions, each 10% of screen height
        self._sh = sh
        self._info_pos = 1  # 1..4
        info_lines = max(4, int(sh * 0.20 / 20))
        self.info = tk.Text(self.side,
                    bg="#2A2A2A",
                    fg="#E0E0E0",
                    font=("Segoe UI", 15),
                    bd=0,
                    highlightthickness=0,
                    height=info_lines)
        self.info.pack(fill="x")
        # ===== CLOCK LABEL =====
        # ── Last move label ──
        self.last_move_label = tk.Label(
            self.side,
            text="—",
            bg="#2A2A2A",
            fg="#FFFFFF",
            font=("Courier", 15, "bold"),
            justify="center"
        )
        self.last_move_label.pack(pady=(6, 0))

        self.clock_label = tk.Label(
            self.side,
            text="",
            bg="#2A2A2A",
            fg="white",
            font=("Segoe UI", 16, "bold")
        )
        self.clock_label.pack(pady=10)

        # ── AI stats label ──
        self.stats_label = tk.Label(
            self.side,
            text="depth: —|nodes: —\neval: —",
            bg="#2A2A2A",
            fg="#AAAAAA",
            font=("Courier", 13),
            justify="center"
        )
        self.stats_label.pack(pady=(4, 2))

        btn = tk.Frame(self.side, bg="black")
        btn.pack(pady=10)

        tk.Button(btn, text="AI Move", width=12,
                  command=self.ai_move_once,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="AUTO", width=12,
                  command=self.auto_on,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="STOP", width=12,
                  command=self.auto_off,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="UNDO", width=12,
                  command=self.undo,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="RESET", width=12,
                  command=self.reset,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="Best Move", width=12,
                  command=self.show_best_move,
                  activebackground="#B58863").pack(pady=3)

        self.panel_btn = tk.Button(btn, text="↕ Panel: 1", width=12,
                  command=self.cycle_panel,
                  activebackground="#B58863")
        self.panel_btn.pack(pady=3)

        # ── separator ──
        tk.Frame(btn, bg="#555555", height=1, width=160).pack(pady=6, fill="x")

        tk.Button(btn, text="History", width=12,
                  command=self.show_history,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="Copy FEN", width=12,
                  command=self.copy_fen,
                  activebackground="#B58863").pack(pady=3)

        tk.Button(btn, text="Import FEN", width=12,
                  command=self.put_fen,
                  activebackground="#B58863").pack(pady=3)

        # ── depth / time controls ──
        tk.Frame(btn, bg="#555555", height=1, width=160).pack(pady=6, fill="x")

        dep_row = tk.Frame(btn, bg="black")
        dep_row.pack(pady=2, anchor="center")
        tk.Label(dep_row, text="Depth:", bg="black", fg="white",
                 font=("Segoe UI", 14), width=7, anchor="e").pack(side="left")
        self.dep_var = tk.StringVar(value=str(MAX_DEPTH))
        dep_entry = tk.Entry(dep_row, textvariable=self.dep_var, width=4,
                             font=("Segoe UI", 14))
        dep_entry.pack(side="left", padx=4)
        tk.Button(dep_row, text="Set", command=self.set_depth, width=5,
                  activebackground="#B58863").pack(side="left")

        lim_row = tk.Frame(btn, bg="black")
        lim_row.pack(pady=2, anchor="center")
        tk.Label(lim_row, text="Time(s):", bg="black", fg="white",
                 font=("Segoe UI", 14), width=7, anchor="e").pack(side="left")
        self.lim_var = tk.StringVar(value=str(TIME_LIMIT_PER_MOVE))
        lim_entry = tk.Entry(lim_row, textvariable=self.lim_var, width=4,
                             font=("Segoe UI", 14))
        lim_entry.pack(side="left", padx=4)
        tk.Button(lim_row, text="Set", command=self.set_time_limit, width=5,
                  activebackground="#B58863").pack(side="left")

        clk_row = tk.Frame(btn, bg="black")
        clk_row.pack(pady=2, anchor="center")
        tk.Label(clk_row, text="Clock:", bg="black", fg="white",
                 font=("Segoe UI", 14), width=7, anchor="e").pack(side="left")
        self.clk_var = tk.StringVar(value=str(self.start_time_seconds // 60))
        clk_entry = tk.Entry(clk_row, textvariable=self.clk_var, width=4,
                             font=("Segoe UI", 14))
        clk_entry.pack(side="left", padx=4)
        
        tk.Button(clk_row, text="Set", command=self.set_clock, width=5,
                  activebackground="#B58863").pack(side="left")

        # ── Author signature ──
        tk.Label(self.side, text="Josef@2026",
                 bg="#2A2A2A", fg="#777777",
                 font=("Segoe UI", 11, "italic")).pack(side="bottom", pady=4)

        self.canvas.bind("<Button-1>", self.on_click)

        if not self.animating:
            self.draw()
        self.update_clock()

    def cycle_panel(self):
        """Cycle info panel height through 4 positions (each +10% screen height)."""
        prev_pos = self._info_pos
        self._info_pos = (self._info_pos % 4) + 1
        # Position 1=10%, 2=20%, 3=30%, 4=40% of screen height
        pct = self._info_pos * 0.10
        lines = max(2, int(self._sh * pct / 20))
        self.info.config(height=lines)
        arrow = "↓" if self._info_pos > prev_pos or (prev_pos == 4 and self._info_pos == 1) else "↑"
        self.panel_btn.config(text=f"{arrow} Panel: {self._info_pos}")

    def log(self, text):
        self.info.insert("end", text + "\n")
        self.info.see("end")

    def log_replace(self, text):
        """Overwrite the last line in the log."""
        self.info.delete("end-2l", "end-1l")
        self.info.insert("end-1l", text + "\n")
        self.info.see("end")
    # ===== FORMAT TIME =====
    def format_time(self, seconds):
        minutes = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{minutes:02}:{secs:02}"
    def draw_rounded_square(self, x1, y1, x2, y2, radius, color):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        self.canvas.create_polygon(points, smooth=True, fill=color, outline="")

    # ===== CLOCK UPDATE =====
    def update_clock(self):
        now = time.time()
        delta = now - self.last_tick
        self.last_tick = now

        if self.start_time_seconds == 0:
            # Unlimited time – hide clock
            self.clock_label.config(text="")
            self.root.after(200, self.update_clock)
            return

        if self.clock_running and not self.board.is_game_over():
            if self.board.turn == chess.WHITE:
                self.white_time -= delta
            else:
                self.black_time -= delta

            if self.white_time <= 0:
                self.white_time = 0
                self.clock_running = False
                self.log("Black wins on time!")

            if self.black_time <= 0:
                self.black_time = 0
                self.clock_running = False
                self.log("White wins on time!")

        self.clock_label.config(
            text=f"White: {self.format_time(self.white_time)}\n"
                 f"Black: {self.format_time(self.black_time)}"
        )

        self.root.after(200, self.update_clock)

    def draw(self):
        self.canvas.delete("all")
        c = self.cell

        for rank in range(8):
            for file in range(8):
                sq = chess.square(file, 7-rank)
                x0, y0 = file*c, rank*c
                x1, y1 = x0+c, y0+c

                color = self.LIGHT if (file+rank)%2==0 else self.DARK

                if sq == self.selected_square:
                    color = self.SELECTED
                elif sq in self.legal_targets:
                    color = self.HIGHLIGHT

                radius = int(self.cell * 0.05)
                self.draw_rounded_square(x0, y0, x1, y1, radius, color)

                piece = self.board.piece_at(sq)
                if piece:
                    cx, cy = x0+c//2, y0+c//2
                    sym = self.PIECES[piece.symbol()]
                    fsz = int(c*0.8)
                    fill = "#ffffff" if piece.color else "#000000"

                    shadow_offset = 1
                    shadow_color = "#888888" if piece.color else "#CCCCCC"

                    # stín
                    self.canvas.create_text(
                        cx+shadow_offset, cy+shadow_offset,
                        text=sym,
                        font=("Segoe UI Symbol", fsz, "bold"),
                        fill=shadow_color
                    )

                    # figurka
                    self.canvas.create_text(
                        cx, cy,
                        text=sym,
                        font=("Segoe UI Symbol", fsz, "bold"),
                        fill=fill
                    )
        # ===== BOARD COORDINATES =====
        for i in range(8):
            # písmena dole
            self.canvas.create_text(
                i*self.cell + self.cell//2,
                8*self.cell - 10,
                text=chr(ord('a') + i),
                fill="black",
                font=("Segoe UI", 15, "bold")
            )

            # čísla vlevo
            self.canvas.create_text(
                10,
                i*self.cell + self.cell//2,
                text=str(8 - i),
                fill="black",
                font=("Segoe UI", 15, "bold")
            )
    def animate_move(self, move, is_ai_move=False):
        if self.animating:
            return

        self.animating = True
        c = self.cell

        from_file = chess.square_file(move.from_square)
        from_rank = 7 - chess.square_rank(move.from_square)
        to_file = chess.square_file(move.to_square)
        to_rank = 7 - chess.square_rank(move.to_square)

        start_x = from_file * c + c // 2
        start_y = from_rank * c + c // 2
        end_x = to_file * c + c // 2
        end_y = to_rank * c + c // 2

        piece = self.board.piece_at(move.from_square)
        if not piece:
            self.animating = False
            return

        sym = self.PIECES[piece.symbol()]
        fsz = int(c * 0.9)
        fill = "#ffffff" if piece.color else "#000000"

        # 🔥 NEODSTRAŇUJ figurku z boardu
        # jen překreslíme desku bez původního pole

        self.draw()
        self.update_clock()

        # překreslíme původní pole bez figurky (vizuálně)
        x0 = from_file * c
        y0 = from_rank * c
        x1 = x0 + c
        y1 = y0 + c
        square_color = self.LIGHT if (from_file + from_rank) % 2 == 0 else self.DARK
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=square_color, outline="")

        text_id = self.canvas.create_text(
            start_x, start_y,
            text=sym,
            font=("Segoe UI Symbol", fsz, "bold"),
            fill=fill
        )

        steps = 35
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

        def step_animation(step=0):
            if step < steps:
                self.canvas.move(text_id, dx, dy)
                self.root.after(self.animation_speed, step_animation, step + 1)
            else:
                self.canvas.delete(text_id)
                self.board.push(move)
                self.clock_running = True
                self.animating = False
                sound_move()
                self.draw()

                # ===== LOG MOVE =====
                if not is_ai_move:
                    move_number = (len(self.board.move_stack) + 1) // 2
                    side = "W" if not self.board.turn else "B"
                    check_sign = "+" if self.board.is_check() else ""
                    self.last_move_label.config(text=f"{move_number}. [{side}] {move.uci()}{check_sign}")

                # ===== CHECK / CHECKMATE =====
                if self.board.is_checkmate():
                    sound_game_over(True)
                    winner = "White" if self.board.turn == chess.BLACK else "Black"
                    self.last_move_label.config(text=f"CHECKMATE! {winner} wins.")
                elif self.board.is_stalemate():
                    sound_game_over(False)
                    self.last_move_label.config(text="Draw by stalemate.")
                elif self.board.is_check():
                    sound_check()
                    self.last_move_label.config(
                        text=self.last_move_label.cget("text") + "  CHECK!"
                    )

                # ===== CAPTURED PIECES – after board.push so counts are correct =====
                start_counts = {
                    chess.PAWN: 8, chess.ROOK: 2, chess.KNIGHT: 2,
                    chess.BISHOP: 2, chess.QUEEN: 1, chess.KING: 1,
                }
                white_counts = {pt: 0 for pt in start_counts}
                black_counts = {pt: 0 for pt in start_counts}
                for square in chess.SQUARES:
                    p = self.board.piece_at(square)
                    if p:
                        if p.color == chess.WHITE:
                            white_counts[p.piece_type] += 1
                        else:
                            black_counts[p.piece_type] += 1
                white_lost = []
                black_lost = []
                for pt, s in start_counts.items():
                    white_lost += [pt] * max(0, s - white_counts[pt])
                    black_lost += [pt] * max(0, s - black_counts[pt])

                def sym(pt, color):
                    return self.PIECES[chess.Piece(pt, color).symbol()]

                white_str = "".join(sym(pt, chess.BLACK) for pt in white_lost)
                black_str = "".join(sym(pt, chess.WHITE) for pt in black_lost)

                self.info.delete("1.0", "end")
                self.info.tag_configure("title", font=("Helvetica", 18, "bold"), justify="center")
                self.info.tag_configure("label", font=("Helvetica", 16), justify="center")
                self.info.tag_configure("pieces", font=("Helvetica", 26), justify="center")
                self.info.insert("end", "Captured pieces\n\n", "title")
                self.info.insert("end", "White lost:\n", "label")
                self.info.insert("end", white_str + "\n\n", "pieces")
                self.info.insert("end", "Black lost:\n", "label")
                self.info.insert("end", black_str + "\n", "pieces")

                # Mate-in-N detection – only for human moves (AI handles it separately)
                if not is_ai_move:
                    def mate_check_worker():
                        board_copy = self.board.copy()
                        ev = evaluate_board(board_copy)
                        if abs(ev) > 0:
                            mate = find_mate_in_n(board_copy, max_moves=6)
                            if mate is not None and mate > 0:
                                self.root.after(0, lambda m=mate: self._show_mate(m))
                    threading.Thread(target=mate_check_worker, daemon=True).start()

        step_animation()

    def on_click(self, event):
        if self.animating:
            return

        # Reject clicks outside the board area (important when board < canvas)
        board_px = self.cell * 8
        if not (0 <= event.x < board_px and 0 <= event.y < board_px):
            return

        file = event.x // self.cell
        rank = 7 - event.y // self.cell
        if not (0 <= file <= 7 and 0 <= rank <= 7):
            return

        sq = chess.square(file, rank)

        if self.selected_square is None:
            piece = self.board.piece_at(sq)
            if piece and piece.color == self.board.turn:
                self.selected_square = sq
                self.legal_targets = {
                    m.to_square for m in self.board.legal_moves
                    if m.from_square == sq
                }
                self.draw()
        else:
            move = chess.Move(self.selected_square, sq)

            # ===== PROMOTION HANDLING =====
            piece = self.board.piece_at(self.selected_square)
            if piece and piece.piece_type == chess.PAWN:
                rank = chess.square_rank(sq)
                if (piece.color == chess.WHITE and rank == 7) or \
                   (piece.color == chess.BLACK and rank == 0):
                    move = chess.Move(self.selected_square, sq, promotion=chess.QUEEN)
            self.selected_square = None
            self.legal_targets = set()

            if move in self.board.legal_moves:
                self.animate_move(move)
            else:
                self.draw()

    def _show_mate(self, mate_in):
        """Display mate-in-N in last_move_label and stats label."""
        sound_mate_warning()
        self.last_move_label.config(text=f"► Mate in {mate_in}!")
        self.stats_label.config(
            text=self.stats_label.cget("text").split("\n")[0] + f"\n► Mate in {mate_in}!"
        )

    def ai_worker(self):
        move = ai_move(self.board)
        if move:
            # Use a copy to avoid mutating self.board (evaluate_board changes board.turn)
            board_copy = self.board.copy()
            board_copy.push(move)
            ev = evaluate_board(board_copy)
            mate = find_mate_in_n(board_copy, max_moves=6) if abs(ev) > 0 else None
            self.root.after(0, self.after_ai_move, move, ev, mate)

    def after_ai_move(self, move, evaluation=0, mate_in=None):
        if not self.animating:
            self.animate_move(move, is_ai_move=True)
            # Update stats display
            if evaluation > 0:
                eval_str = f"+{evaluation / 100:.2f}"
            elif evaluation < 0:
                eval_str = f"{evaluation / 100:.2f}"
            else:
                eval_str = "0.00"
            mate_str = f"  |  Mate in {mate_in}!" if (mate_in is not None and mate_in > 0) else ""
            self.stats_label.config(
                text=f"depth: {max_depth_reached}  |  nodes: {nodes_searched/1_000_000:.2f}MN\nTT: {len(TT):,}  |  eval: {eval_str}{mate_str}"
            )
            move_number = (len(self.board.move_stack) + 1) // 2
            ai_side = "B" if self.board.turn == chess.WHITE else "W"
            check_sign = "+" if self.board.is_check() else ""
            log_text = f"{move_number}. [{ai_side}] {move.uci()}{check_sign}"
            if mate_in is not None and mate_in > 0:
                sound_mate_warning()
                log_text += f"  ► MATE in {mate_in}"
            self.last_move_label.config(text=log_text)

    def ai_move_once(self):
        if self.ai_thread and self.ai_thread.is_alive():
            return
        self.last_move_label.config(text="AI thinking...")
        self.ai_thread = threading.Thread(target=self.ai_worker, daemon=True)
        self.ai_thread.start()

    def auto_loop(self):
        if not self.auto_running:
            return

        if self.board.is_game_over():
            self.auto_running = False
            return

        # spustí tah jen pokud:
        # - není animace
        # - neběží AI thread
        # - je správná barva
        if (not self.animating and
            not (self.ai_thread and self.ai_thread.is_alive()) and
            self.board.turn == self.auto_color):

            self.ai_move_once()

        self.root.after(200, self.auto_loop)
    def auto_on(self):
        self.auto_running = True
        self.auto_color = self.board.turn  # AI hraje za aktuální barvu
        self.log(f"AUTO ON for {'White' if self.auto_color else 'Black'}")
        self.auto_loop()

    def auto_off(self):
        self.auto_running = False
        self.auto_color = None
        self.log("AUTO OFF")

    def undo(self):
        if self.board.move_stack:
            self.board.pop()
            self.draw()

    def show_best_move(self):
        """Calculate and highlight best move without playing it."""
        if self.board.is_game_over():
            self.log("Game is over.")
            return
        if self.ai_thread and self.ai_thread.is_alive():
            self.log("AI is already thinking...")
            return
        self.log("Calculating best move...")
        def worker():
            move = iterative_deepening(self.board, MAX_DEPTH, TIME_LIMIT_PER_MOVE)
            self.root.after(0, self._highlight_best_move, move)
        self.ai_thread = threading.Thread(target=worker, daemon=True)
        self.ai_thread.start()

    def _highlight_best_move(self, move):
        if not move:
            self.log("No best move found.")
            return
        # Temporarily highlight from/to squares in the info panel
        self.log(f"Best move: {move.uci()}")
        # Flash highlight on board
        self.selected_square = move.from_square
        self.legal_targets = {move.to_square}
        self.draw()
        # Clear highlight after 2 seconds
        self.root.after(2000, self._clear_best_highlight)

    def _clear_best_highlight(self):
        self.selected_square = None
        self.legal_targets = set()
        self.draw()

    def show_history(self):
        """Display full move history in the info panel."""
        self.info.delete("1.0", "end")
        self.info.tag_configure("title", font=("Helvetica", 14, "bold"), justify="center")
        self.info.tag_configure("move", font=("Courier", 15))
        self.info.insert("end", "Move History\n\n", "title")
        if not self.board.move_stack:
            self.info.insert("end", "No moves yet.\n", "move")
            return
        temp = chess.Board()
        pairs = []
        moves = list(self.board.move_stack)
        for i, move in enumerate(moves):
            temp.push(move)
            sign = "+" if temp.is_check() else ""
            uci = move.uci() + sign
            if i % 2 == 0:
                pairs.append([f"{i//2 + 1}. {uci}", ""])
            else:
                pairs[-1][1] = uci
        for white, black in pairs:
            self.info.insert("end", f"{white:<14}{black}\n", "move")

    def copy_fen(self):
        """Copy current FEN to clipboard and show in info panel."""
        fen = self.board.fen()
        self.root.clipboard_clear()
        self.root.clipboard_append(fen)
        self.info.delete("1.0", "end")
        self.info.tag_configure("title", font=("Helvetica", 14, "bold"), justify="center")
        self.info.tag_configure("fen", font=("Courier", 15), wrap="word")
        self.info.insert("end", "FEN copied to clipboard!\n\n", "title")
        self.info.insert("end", fen, "fen")

    def put_fen(self):
        """Open a dialog to load a position from a FEN string."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Load FEN")
        dialog.resizable(False, False)
        dialog.configure(bg="#2A2A2A")
        dialog.grab_set()  # modal

        tk.Label(dialog, text="Enter FEN:", bg="#2A2A2A", fg="white",
                 font=("Segoe UI", 13)).pack(padx=20, pady=(16, 4))

        fen_var = tk.StringVar()
        entry = tk.Entry(dialog, textvariable=fen_var, width=55,
                         font=("Courier", 12))
        entry.pack(padx=20, pady=4)
        entry.focus_set()

        msg_var = tk.StringVar()
        msg_label = tk.Label(dialog, textvariable=msg_var, bg="#2A2A2A",
                             fg="#FF6666", font=("Segoe UI", 11))
        msg_label.pack(pady=2)

        def apply():
            fen = fen_var.get().strip()
            try:
                new_board = chess.Board(fen)
                self.board = new_board
                self.selected_square = None
                self.legal_targets = set()
                self.last_move = None
                self.auto_running = False
                self.white_time = self.start_time_seconds
                self.black_time = self.start_time_seconds
                self.clock_running = False
                self.info.delete("1.0", "end")
                self.log(f"Position loaded: {fen}")
                self.draw()
                dialog.destroy()
            except ValueError as e:
                msg_var.set(f"Invalid FEN: {e}")

        btn_frame = tk.Frame(dialog, bg="#2A2A2A")
        btn_frame.pack(pady=(4, 16))
        tk.Button(btn_frame, text="Load", width=10, command=apply,
                  activebackground="#B58863").pack(side="left", padx=8)
        tk.Button(btn_frame, text="Cancel", width=10, command=dialog.destroy,
                  activebackground="#B58863").pack(side="left", padx=8)

        # Allow pressing Enter to confirm
        dialog.bind("<Return>", lambda e: apply())
        dialog.bind("<Escape>", lambda e: dialog.destroy())

    def set_clock(self):
        """Set clock time in minutes. 0 = unlimited (clock hidden)."""
        try:
            val = int(self.clk_var.get())
            self.start_time_seconds = max(0, val) * 60
            self.white_time = self.start_time_seconds
            self.black_time = self.start_time_seconds
            self.clock_running = False
            self.clk_var.set(str(max(0, val)))
            if self.start_time_seconds == 0:
                self.clock_label.config(text="")
                self.log("Clock disabled (unlimited time)")
            else:
                self.log(f"Clock set to {val} min – restart game to apply")
        except ValueError:
            self.log("Invalid clock value.")

    def set_depth(self):
        """Apply depth setting from the entry field."""
        global MAX_DEPTH
        try:
            val = int(self.dep_var.get())
            MAX_DEPTH = max(1, min(val, 20))
            self.dep_var.set(str(MAX_DEPTH))
            self.log(f"Depth set to {MAX_DEPTH}")
        except ValueError:
            self.log("Invalid depth value.")

    def set_time_limit(self):
        """Apply time limit setting from the entry field."""
        global TIME_LIMIT_PER_MOVE
        try:
            val = float(self.lim_var.get())
            TIME_LIMIT_PER_MOVE = max(0.5, min(val, 300.0))
            self.lim_var.set(str(TIME_LIMIT_PER_MOVE))
            self.log(f"Time limit set to {TIME_LIMIT_PER_MOVE}s")
        except ValueError:
            self.log("Invalid time value.")

    def reset(self):
        global TT, nodes_searched, max_depth_reached
        self.board.reset()
        self.selected_square = None
        self.legal_targets = set()
        self.auto_running = False
        self.auto_color = None

        self.white_time = self.start_time_seconds
        self.black_time = self.start_time_seconds
        self.clock_running = False
        self.last_tick = time.time()

        # Reset search statistics and transposition table
        TT.clear()
        nodes_searched = 0
        max_depth_reached = 0
        self.last_move_label.config(text="—")
        self.stats_label.config(text="depth: —  |  nodes: —\neval: —")

        self.info.delete("1.0", "end")
        self.draw()
        self.draw()

def main():
    _init_sounds()
    app = ChessApp()
    app.root.mainloop()

if __name__ == "__main__":
    main()
