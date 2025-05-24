import chess

def num_pieces_developed(board, color):
    num_pieces_developed = 0

    rank = 1
    if(color == chess.BLACK): rank = 8

    #minor piece development
    num_pieces_developed += piece_developed(board, chess.Piece(chess.KNIGHT, color), chess.parse_square("b"+str(rank)))
    num_pieces_developed += piece_developed(board, chess.Piece(chess.KNIGHT, color), chess.parse_square("g"+str(rank)))
    num_pieces_developed += piece_developed(board, chess.Piece(chess.BISHOP, color), chess.parse_square("c"+str(rank)))
    num_pieces_developed += piece_developed(board, chess.Piece(chess.BISHOP, color), chess.parse_square("f"+str(rank)))

    return num_pieces_developed

        
def piece_developed(board, piece, square):
    if board.piece_at(square) == piece: return 0
    return 1

def was_last_move_castle(board):
    try:
        return (board.peek() == board.parse_san("O-O") or board.peek() == board.parse_san("O-O-O"))
    except:
        return False
    
def times_central_squares_controlled(board, color):
    attack_count = 0

    attack_count += len(board.attackers(color, chess.D4))
    attack_count += len(board.attackers(color, chess.E4))
    attack_count += len(board.attackers(color, chess.D5))
    attack_count += len(board.attackers(color, chess.E5))

    #print(attack_count)

    return attack_count