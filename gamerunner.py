import chess 
import numpy
import time
import robbysengine

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