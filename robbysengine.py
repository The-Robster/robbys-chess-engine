import chess 
import numpy
import time
import helpers

my_color = chess.WHITE
def opponent_color():
    return not my_color

in_opening = True
pieces_developed = False
opening_development_bias = 1

has_white_castled = False
has_black_castled = False
def has_color_castled(color):
    if(color == chess.WHITE) : return has_white_castled
    else: return has_black_castled

def determine_evaluation_opening(board):
    return mod_from_piece_development(board) + mod_from_space_controlled(board) + mod_from_material_imbalance(board)

def mod_from_piece_development(board):
    return mod_from_piece_development_color(board, chess.WHITE) - mod_from_piece_development_color(board, chess.BLACK)

def mod_from_piece_development_color(board, color):
    eval_mod_pawns = 0
    #let's say every piece developed from its starting position is worth half a pawn
    eval_mod_pawns += .5*helpers.num_pieces_developed(board, color)

    #Castling worth half a pawn
    if(has_color_castled(color)): eval_mod_pawns += .5

    #Losing castling rights without castling is worth -.75 pawns
    if(not has_color_castled(color)) and (not board.has_queenside_castling_rights(color) and (not board.has_kingside_castling_rights(color))): eval_mod_pawns -= .75

    #Central square control worth .25 pawns each
    eval_mod_pawns += .25*helpers.times_central_squares_controlled(board, color)

    return eval_mod_pawns

def determine_evaluation_middlegame(board, color):
    return 0

def mod_from_space_controlled(board):
    return mod_from_space_controlled_color(board, chess.WHITE) - mod_from_space_controlled_color(board, chess.BLACK)

def mod_from_space_controlled_color(board, color):
    return 0

def mod_from_material_imbalance(board):
    eval_mod_pawns = 0

    eval_mod_pawns += (len(board.pieces(chess.PAWN, chess.WHITE)) - len(board.pieces(chess.PAWN, chess.BLACK)))
    eval_mod_pawns += (len(board.pieces(chess.KNIGHT, chess.WHITE)) - len(board.pieces(chess.KNIGHT, chess.BLACK))) * 2.9
    eval_mod_pawns += (len(board.pieces(chess.BISHOP, chess.WHITE)) - len(board.pieces(chess.BISHOP, chess.BLACK))) * 3
    eval_mod_pawns += (len(board.pieces(chess.ROOK, chess.WHITE)) - len(board.pieces(chess.ROOK, chess.BLACK))) * 5
    eval_mod_pawns += (len(board.pieces(chess.QUEEN, chess.WHITE)) - len(board.pieces(chess.QUEEN, chess.BLACK))) * 9

    return eval_mod_pawns


def mod_from_king_safety(board):
    return mod_from_king_safety_color(board, chess.WHITE) - mod_from_king_safety_color(board, chess.BLACK)

def mod_from_king_safety_color(board, color):
    return 0

def evaluate_position(board):
    if(board.is_checkmate()):
        if(chess.turn == chess.WHITE):
            #negative if white, because if its whites turn and they're checkmated, black mated them
            return -1000000000
        else:
            return 1000000000


    if(in_opening): return determine_evaluation_opening(board)
    return determine_evaluation_middlegame(board)

def check_opening_completed(board):
    global in_opening
    global pieces_developed
    if not in_opening: return
    #check piece development
    if(not pieces_developed):
        if(helpers.num_pieces_developed(board, my_color) == 4):
            pieces_developed = True

    #check if castled (or castling not allowed)
    if(has_color_castled(my_color) and pieces_developed) : 
        print("~~ Opening Completed ~~")
        in_opening = False


def choose_move(legal_moves_with_evals, color):
    legal_moves_with_evals_random_mod = []

    #for each move add a random modifier to it, to give some variance (normally distributed random, so not too much variance)
    for move in legal_moves_with_evals:
        gaussean_mod = 0#numpy.random.normal(2, .25)
        gaussean_mod = max(gaussean_mod, 0)
        gaussean_mod = min(gaussean_mod, 4)
        legal_moves_with_evals_random_mod.append((move[0], move[1] + gaussean_mod))
    
    tentative_move = legal_moves_with_evals_random_mod[0]

    #now just choose max or min
    if(color == chess.WHITE):
        for move in legal_moves_with_evals_random_mod:
            if(move[1] > tentative_move[1]): tentative_move = move
    else:
       for move in legal_moves_with_evals_random_mod:
            if(move[1] < tentative_move[1]): tentative_move = move 
        
    print("Evaluation for chosen move: " + str(tentative_move[1]))
    return tentative_move[0]


def find_next_move(board):
    
    if(helpers.was_last_move_castle(board)): 
        if(my_color == chess.WHITE): has_black_castled = True
        else : has_white_castled = True

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
        castle_state = has_color_castled(my_color)
        #If we're checking castle we need to adjust for the fact that we've castled
        if(helpers.was_last_move_castle(board)):
            if(my_color == chess.WHITE): has_white_castled = True
            else : has_black_castled = True
        
        evaluation = (move, evaluate_position(board))
        #print(evaluation[0])
        #print(evaluation[1])
        legal_moves_with_evals.append(evaluation)
        board.pop()

        #forget that we just tested castling
        if(my_color == chess.WHITE): has_white_castled = castle_state
        else : has_black_castled = castle_state

    chosen_move = choose_move(legal_moves_with_evals, my_color)

    print(board.san(chosen_move))
    board.push(chosen_move)
    
    if(helpers.was_last_move_castle(board)): 
        if(my_color == chess.WHITE): has_white_castled = True
        else : has_black_castled = True

    if(board.is_checkmate()):
        print("you lose")
        print("good game")
        return None

    return chosen_move
