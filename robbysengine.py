import chess 
import numpy
import time

is_white = 1 # -1 for black

in_opening = True
opening_development_bias = 3

def determine_evaluation_opening(board):
    return (mod_from_piece_development(board) * opening_development_bias) + mod_from_space_controlled(board) + mod_from_material_imbalance(board)

def mod_from_piece_development(board):
    return 0

def determine_evaluation_middlegame(board):
    return 0

def mod_from_space_controlled(board):
    return 0

def mod_from_material_imbalance(board):
    return 0

def mod_from_king_safety(baord):
    return 0

def evaluate_position(board):
    if(board.is_checkmate()):
        return 1000000000


    if(in_opening): return determine_evaluation_opening(board)
    return determine_evaluation_middlegame(board)

def check_opening_completed(board):
    if not in_opening: return
    #check piece development

    #check if castled (or castling not allowed)

def choose_move(legal_moves_with_evals):
    legal_moves_with_evals_random_mod = []

    #for each move add a random modifier to it, to give some variance (normally distributed random, so not too much variance)
    for move in legal_moves_with_evals:
        gaussean_mod = numpy.random.normal(2, .25)
        gaussean_mod = max(gaussean_mod, 0)
        gaussean_mod = min(gaussean_mod, 4)
        legal_moves_with_evals_random_mod.append((move[0], move[1] + gaussean_mod))
    
    tentative_move = legal_moves_with_evals_random_mod[0]
    #now just choose max
    for move in legal_moves_with_evals_random_mod:
        if(move[1] > tentative_move[1]): tentative_move = move
    
    return tentative_move[0]


def find_next_move(board):

    if(board.is_stalemate()):
        print("stalemate")
        return None
    
    if(board.is_checkmate()):
        print("I lose")
        time.sleep(3)
        print("coward")
        return None

    check_opening_completed(board)

    legal_moves = board.legal_moves

    #evaluate all possible moves
    legal_moves_with_evals = []
    for move in legal_moves:
        board.push(move)
        legal_moves_with_evals.append((move, evaluate_position(board)))
        board.pop()

    chosen_move = choose_move(legal_moves_with_evals)

    print(board.san(chosen_move))
    board.push(chosen_move)

    if(board.is_checkmate()):
        print("you lose")
        print("good game")
        return None

    return chosen_move

def await_user_move(board):
    move_san = input("Ok your move...")

    try: 
        return board.push_san(move_san)
    except:
        print("invalid move")
        return await_user_move(board)

def await_move(whites_move, board):
    move = None
    if(whites_move == is_white):
        move = find_next_move(board)
    else:
        move = await_user_move(board)

    print("")
    print(board)
    print("")
    return move

def execeute_turn(board):

    time.sleep(1)
    print("White's move:")
    time.sleep(1)
    if await_move(True, board) == None: return

    time.sleep(1)
    print("Black's move:")
    time.sleep(1)
    if await_move(False, board) == None: return

    execeute_turn(board)

is_white = False
if(is_white): print("I'll play White")
else: print("I'll play Black")

execeute_turn(chess.Board())