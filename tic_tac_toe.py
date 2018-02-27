import getopt
import sys
import time
import random


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


def play(board, actual, round):
    index = -1
    choices = []
    neutral = 0

    if actual == 'X':
        next = 'O'
    else:
        next = 'X'

    for position in board:
        index += 1
        if position == '_':
            board[index] = actual
            value = minmax(board, next, round)
            board[index] = '_'

            if value > neutral:
                #print("Good Choise: "+str(index))
                choices = [index]
            elif value == neutral:
                choices.append(index)

    #if len(choices)>0:
        #print("Choises:")
        #for choice in choices:
          #print(choices[choices.index(choice)])

    if len(choices) > 0:
        return random.choice(choices)
    else:
        randIndex = random.randint(0, 8)
        while board[randIndex] != '_':
            randIndex = random.randint(0, 8)
        else:
            return randIndex



# Play the next round until someone win the game
def minmax(board, actual, round):

    if actual == 'X':
        next = 'O'
    else:
        next = 'X'

    winner = checkGameOver(board, round)

    if winner == first:
        return 1
    elif winner == second:
        return -1
    elif winner == 'D':
        return 0

    if actual == first:
        best = -1
        index = -1
        for position in board:
            index += 1
            if position == '_':
                board[index] = actual
                value = minmax(board, next, round)
                board[index] = '_'
                best = max(best,value)
        return best

    if actual == second:
        best = 1
        index = -1
        for position in board:
            index += 1
            if position == '_':
                board[index] = actual
                value = minmax(board, next, round)
                board[index] = '_'
                best = min(best,value)
        return best


def make_move(board, position, player):
        board[position] = player

# Check if someone has won the game
def checkGameOver(board, round):

    # For a unk reason PythonAnywhere have a problem with comma-separated prints... So, we need to concat with '+'
    if board[0] == board[1] == board[2] != '_':
        #print("Player " + board[0] + " won the game in round " + str(round) + " scoring at the first horizontal line")
        return board[0]

    elif board[3] == board[4] == board[5] != '_':
        #print("Player " + board[3] + " won the game in round " + str(round) + " scoring at the second horizontal line")
        return board[3]
    elif board[6] == board[7] == board[8] != '_':
        #print("Player " + board[6] + " won the game in round " + str(round) + " scoring at the third horizontal line")
        return board[6]

    elif board[0] == board[3] == board[6] != '_':
        #print("Player " + board[0] + " won the game in round " + str(round) + " scoring at the first vertical line")
        return board[0]

    elif board[1] == board[4] == board[7] != '_':
        #print("Player " + board[1] + " won the game in round " + str(round) + " scoring at the second vertical line")
        return board[1]

    elif board[2] == board[5] == board[8] != '_':
        #print("Player " + board[2] + " won the game in round " + str(round) + " scoring at the third vertical line")
        return board[2]

    elif board[0] == board[4] == board[8] != '_':
        #print("Player " + board[0] + " won the game in round " + str(round) + " scoring at the primary diagonal")
        return board[0]

    elif board[2] == board[4] == board[6] != '_':
        #print("Player " + board[2] + " won the game in round " + str(round) + " scoring at the secondary diagonal")
        return board[2]
    else:
        for element in board:
            if element == '_':
                #print("Play Again")
                return 'P'  #Play Again

        #print("Draw")
        return 'D'  #Draw


def main():
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hf:b:v", ["first=", "board=", "verbose="])
        global first
        global second
        global verbose
        board = list("_________")
        verbose = False


        for opt, arg in opts:
            if opt == '-h':
                print("%s -f x -b ____x____" % (__file__))
                sys.exit()
            elif opt in ("-v", "--verbose"):
                verbose = True
            elif opt in ("-b", "--board"):
                if len(arg) == 9:
                    board = list(arg)
                    for item in board:
                        board[board.index(
                            item)] = item.upper()  # Used to compare x and X in checkGameOver in a better 'friendly view'.  ( PythonAnywhere have a problem with it )
                else:
                    print("You've defined a wrong-sized board, try again!")
                    print("Remember, your board need to have 9 positions, like: ____x____")
                    sys.exit(2)
            elif opt in ("-f", "--first"):
                first = str(arg).upper()

        if board == list("_________"):
            print("You need to define a board first, try:")
            print("%s -f x -b ____x____" % (__file__))

        for position in board:
            if position != '_' and position.upper() != 'X' and position.upper() != 'O':
                print("You have defined a wrong board, you cant use " + position)
                sys.exit(2)

        # We'll set the second player now
        if first == 'X':
            second = 'O'
        else:  # first = O
            second = 'X'

        # Ok, now we can print our board and start the next round
        if verbose:
            print("The game has been started!\n")
            print_board(board)

        round = 1
        actual = first
        movePlayer = []
        movePC = []

        indexMove = play(board, first, round)
        print("Move: "+ str(indexMove) +" Player: "+first)
        make_move(board, indexMove, actual)

        winner = checkGameOver(board, round)
        actual = second
        while (winner != 'D' and winner != first and winner != second):

            round += 1

            indexMove = play(board, actual, round)
            print("Move: " + str(indexMove) + " Player: " + actual)
            make_move(board, indexMove, actual)
            winner = checkGameOver(board, round)

            if actual == first:
                actual = second
                movePlayer.append(indexMove)
            else:
                actual = first
                movePC.append(indexMove)

        else:
            print("\n\n\n")
            if winner == first:
                print("Player won!")
            elif winner == second:
                print("PC won!")
            elif winner == 'D':
                print("Draw!")
            print("Player Moves:",end=" ")
            for item in movePlayer:
                print(item,end=" ")
            print(" ")
            print("PC Moves:",end=" ")
            for item in movePC:
                print(item,end=" ")
            print(" ")
            print("Final Round: "+ str(round))

    except getopt.GetoptError:
        print(
            "You have used a wrong parameter. Valid parameters: -f (first), -v (verbose), -b (initial board), -h (help)")
        print("Example of use:")
        print("%s -f x -b ____x____" % (__file__))
        sys.exit(2)

if __name__ == "__main__":
    first = 'X'
    second = 'O'
    verbose = True
    main()


