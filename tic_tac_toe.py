import getopt
import sys
import time
import random

# a
def print_board(board):
    board = ''.join(board)
    if len(board) == 9:
        print("           ")
        for line in range(3):
            line_str = ''
            line_bar = ['','|','|']
            for item in board[line*3: line*3+3]:
                if item.upper() == 'X':
                    line_str+=' X '+line_bar.pop()
                elif item.upper() == 'O':
                    line_str+=' O '+line_bar.pop()
                else:
                    line_str+= '   '+line_bar.pop()
            print(line_str)
            if line==2:
                print("           ")
            else:
                print("-----------")

# Play the next round until someone win the game
def play(board, player, round):

    randIndex = random.randint(0, 8)
    while board[randIndex] != '_':
        randIndex = random.randint(0, 8)
    else:
        board[randIndex] = player

    if player == 'X':
        player = 'O'
    else:
        player = 'X'

    # Get value from global var
    if verbose:
        print("Round %d:" % round)
        print_board(board)

    filleds = 0
    for position in board:
        if position != '_':
            filleds += 1

    if filleds >= 5:
        checkGameOver(board, round, filleds)

    round += 1

    play(board, player, round)

# Check if someone has won the game
def checkGameOver(board, round, filleds):

    # For a unk reason PythonAnywhere have a problem with comma-separated prints... So, we need to concat with '+'
    if board[0] == board[1] == board[2] != '_':
        print("Player " + board[0] + " won the game in round " + str(round) + " scoring at the first horizontal line")
    elif board[3] == board[4] == board[5] != '_':
        print("Player " + board[3] + " won the game in round " + str(round) + " scoring at the second horizontal line")
    elif board[6] == board[7] == board[8] != '_':
        print("Player " + board[6] + " won the game in round " + str(round) + " scoring at the third horizontal line")
    elif board[0] == board[3] == board[6] != '_':
        print("Player " + board[0] + " won the game in round " + str(round) + " scoring at the first vertical line")
    elif board[1] == board[4] == board[7] != '_':
        print("Player " + board[1] + " won the game in round " + str(round) + " scoring at the second vertical line")
    elif board[2] == board[5] == board[8] != '_':
        print("Player " + board[2] + " won the game in round " + str(round) + " scoring at the third vertical line")
    elif board[0] == board[4] == board[8] != '_':
        print("Player " + board[0] + " won the game in round " + str(round) + " scoring at the primary diagonal")
    elif board[2] == board[4] == board[6] != '_':
        print("Player " + board[2] + " won the game in round " + str(round) + " scoring at the secondary diagonal")
    else:
        if filleds == 9:
            print("The game ended in a draw. Better lucky next time :)")
        else:
            return
    sys.exit()

if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"hf:b:v",["first=","board=","verbose="])
        first = 'X'
        board = list("_________")
        verbose = False
        for opt, arg in opts:
            if opt == '-h':
                print("%s -f x -b ____x____"%(__file__))
                sys.exit()
            elif opt in ("-v", "--verbose"):
                verbose = True
            elif opt in ("-b", "--board"):
                if len(arg) == 9:
                    board = list(arg)
                    for item in board:
                        board[board.index(item)] = item.upper() # Used to compare x and X in checkGameOver in a better 'friendly view'.  ( PythonAnywhere have a problem with it )
                else:
                    print("You've defined a wrong-sized board, try again!")
                    print("Remember, your board need to have 9 positions, like: ____x____")
                    sys.exit(2)
            elif opt in ("-f", "--first"):
                first = str(arg).upper()

        if board == list("_________"):
            print("You need to define a board first, try:")
            print("%s -f x -b ____x____" % (__file__))

        # We'll set the second player now
        if first == 'X':
            second = 'O'
        else:  # first = O
            second = 'X'

        # Erros/Exceptions Handled atm:
        '''
         - Board with wrong size of position
         - Position with wrong value
         - More than one position filled in the initial board
         - Invalid Parameter
         - Missed board parameter
         - Missed first player parameter
         - Change 0 to O 
        '''

        # Ok, now we can print our board and start the next round
        if verbose:
            print("The game has been started!\n")
            print("Round 1:")
            print_board(board)

        play(board,second,2)


    except getopt.GetoptError:
        print ("You have used a wrong parameter. Valid parameters: -f (first), -v (verbose), -b (initial board), -h (help)")
        print ("Example of use:")
        print("%s -f x -b ____x____"%(__file__))
        sys.exit(2)

