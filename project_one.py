'''
Author: Maya Strommen
CSCI 1913 Fall 2025
'''
import random

def generate_board(an_int):
    """
    This function uses the user input an_int and creates a playing board corrensponsing with that
    value as the height and width of the board. In the board, the value at the top left 
    is 1, and then each other value in the board alternates from that.
    """
    # creates an empty playing board
    board = []
    # checks if the user imput is 0 or less than 0, if so, returns empty list
    if an_int <= 0:
        return board
    # creates a board of length and width depending on an_int and puts 1 and 2 
    # alternating in each row
    for i in range(an_int):
        row_inboard = []
        for j in range(an_int):
            if (i+j) % 2 == 0:
                row_inboard.append(1)
            else:
                row_inboard.append(2)
        board.append(row_inboard)
    return board

def get_board_as_string(board):
    """
    This function takes a board as a list of lists and creates a string version that can be 
    printed out to the user. It inclues a header, filler lines, indexes, and tokens or
    empty cells based on what number was originally in the board.
    """
    # creates the tokens and empty spaces
    black_token = '\u25CF'
    white_token = '\u25CB'
    empty_cell = ' '
    # creates the number of rows and columns needed
    rows = len(board)
    if rows > 0:
        columns = len(board[0])
    else:
        columns = 0
    # creates top row of board
    top_row = "   "
    for i in range(columns):
        if i >= 10:
            top_row += str(i % 10) + " "
        else:
            top_row += str(i) + " "
    top_row += "\n"
    # creates the filler rows that will go in board
    filler_row = "  "
    for i in range(columns):
        filler_row += "+-"
    filler_row += "+\n"
    # starts board by putting top row and then the indexes of each row
    result = top_row
    for r in range(rows):
        result += filler_row
        if r >= 10:
            result += str(r % 10) + " |"
        else:
            result += str(r) + " |"
        # adds the correct tokens for each row and column index based on
        # the number in that cell
        for c in range(columns):
            value = board[r][c]
            if value == 0:
                token = empty_cell
            elif value == 1:
                token = black_token
            elif value == 2:
                token = white_token
            result += token + "|"
        result += "\n"
    result += filler_row
    return result

def prep_board_human(board):
    """
    This function asks a user to choose two tokens to remove, and only removes them if they
    are different colors and not on the edge of the board. If not, reprompts user.
    """
    print(get_board_as_string(board))
    # gets first token place from user and checks validity, if on edge then reprompts
    row_one = int(input("Enter a row value: "))
    column_one = int(input("Enter a column value: "))
    if (row_one == 0) or (row_one == len(board)-1) or (column_one == 0) or (column_one == len(board[0])):
        print("Please choose a different stone")
        row_one = int(input("Enter a row value: "))
        column_one = int(input("Enter a column value: "))
    # gets second token from user and checks validity, if on edge or same color as first token, reprompts
    row_two = int(input("Enter a row value: "))
    column_two = int(input("Enter a column value: "))
    if (row_two == 0) or (row_two == len(board)-1) or (column_two == 0) or (column_two == len(board[0])) or (board[row_one][column_one] == board[row_two][column_two]):
        print("Please choose a different stone")
        row_two = int(input("Enter a row value: "))
        column_two = int(input("Enter a column value: "))
    # places a 0 in place of the tokens that are being removed by user
    board[row_one][column_one] = 0
    board[row_two][column_two] = 0
    print(get_board_as_string(board))
    return

def is_valid_move(board, move):
    """
    This function checks the move the user is trying to make and makes sure it is a valid move
    according to the rules of the game. If it is a valid move, this function just returns True,
    and if not then the function returns False.
    """
    # checks the color that player is moving, and declares the enemy color
    player_color = board[move[0][0]][move[0][1]]
    if player_color == 1:
        enemy_color = 2
    else:
        enemy_color = 1
    # checks if move is straight
    if move[0][0] == move[1][0]:
        direction_row = False
    elif move[0][1] == move[1][1]:
        direction_row = True
    else:
        return False
    # declares starting positions and finds direction and distance the token is moving
    start_row = move[0][0]
    end_row = move[1][0]
    start_column = move[0][1]
    end_column = move[1][1]
    if direction_row:
        column_move = 0
        if end_row > start_row:
            row_move = 1
        else:
            row_move = -1
        distance = abs(end_row - start_row)
    else:
        row_move = 0
        if end_column > start_column:
            column_move = 1
        else:
            column_move = -1
        distance = abs(end_column - start_column)
    # checks to make sure token is being moved more than one spot 
    if distance < 2:
        return False
    # checks that final position is blank space
    if board[move[1][0]][move[1][1]] != 0:
        return False
    # declares a starting point and iterates for all spaces in between start and end
    # if any spaces have a token of the players color or more than one blank space in a row, returns false
    curr_row = start_row + row_move
    curr_column = start_column + column_move
    blank_count = 0
    seen_opponent = False
    while (curr_row != end_row) or (curr_column != end_column):
        space = board[curr_row][curr_column]
        if space == player_color:
            return False
        elif space == enemy_color:
            seen_opponent = True
            blank_count = 0
        elif space == 0:
            blank_count += 1
            if blank_count > 1:
                return False
        curr_row += row_move
        curr_column += column_move
    # checks to make sure the position next to the ending one isn't a blank space as well
    if board[end_row][end_column] == board[end_row - row_move][end_column - column_move]:
        return False
    return seen_opponent
        
def get_valid_moves_for_stone(board, stone):
    """
    This function takes the board and a specific stone on the board and finds all valid moves that 
    stone could make. It returns a tuple of tuples of all valid moves.
    """
    valid_moves = []
    num_rows = len(board)
    num_columns = len(board[0])
    stone_row = stone[0]
    stone_column = stone[1]
    player_color = board[stone_row][stone_column]
    # checks that the row and column that the stone is on is in the board
    if not ((0<= stone_row < num_rows) and (0 <= stone_column < num_columns)):
        return valid_moves
    # checks to make sure it is not starting on a blank space, and identifies opponents color
    if player_color == 0:
        return valid_moves
    elif player_color == 1:
        opponent_color = 2
    else:
        opponent_color = 1
    # this checks for any valid moves upwards 
    row = stone_row - 1
    expecting = opponent_color
    while row >= 0:
        curr_place = board[row][stone_column]
        if curr_place == expecting:
            if expecting == opponent_color:
                expecting = 0
            else:
                expecting = opponent_color
            if curr_place == 0 and expecting == opponent_color:
                valid_moves.append(((stone_row, stone_column), (row, stone_column)))
        else:
            row = -1
        row -= 1
    # this checks for any valid moves downwards
    row = stone_row + 1
    expecting = opponent_color
    while row < num_rows:
        curr_place = board[row][stone_column]
        if curr_place == expecting:
            if expecting == opponent_color:
                expecting = 0
            else:
                expecting = opponent_color
            if curr_place == 0 and expecting == opponent_color:
                valid_moves.append(((stone_row, stone_column), (row, stone_column)))
        else:
            row = num_rows
        row +=1
    # checks for any valid moves in the left direction
    column = stone_column - 1
    expecting = opponent_color
    while column >= 0:
        curr_place = board[stone_row][column]
        if curr_place == expecting:
            if expecting == opponent_color:
                expecting = 0
            else:
                expecting = opponent_color
            if curr_place == 0 and expecting == opponent_color:
                valid_moves.append(((stone_row, stone_column), (stone_row, column)))
        else:
            column = -1
        column -= 1
    # checks for any valid moves in the right direction
    column = stone_column + 1
    expecting = opponent_color
    while column < num_columns:
        curr_place = board[stone_row][column]
        if curr_place == expecting:
            if expecting == opponent_color:
                expecting = 0
            else:
                expecting = opponent_color
            if curr_place == 0 and expecting == opponent_color:
                valid_moves.append(((stone_row, stone_column), (stone_row, column)))
        else:
            column = num_columns
        column += 1
    return valid_moves

def get_valid_moves(board, player):
    """
    This function takes the board and the players color(the stones they can move) and returns
    a tuple of tuples for all valid moves for each color stone of theirs on the board. Uses 
    the get_valid_moves_for_stone for each stone of their color to check for moves.
    """
    # declares an empty tuple of moves and the row and columns of the board
    valid_moves = []
    num_rows = len(board)
    num_columns = len(board[0])
    # this for loop iterates through each spot on board and if the stone is the
    # players color then it checks valid moves for the stone and adds them to the 
    # valid moves tuple if any.
    for row in range(num_rows):
        for column in range(num_columns):
            if board[row][column] == player:
                stone_moves = get_valid_moves_for_stone(board, (row, column))
                if stone_moves:
                    valid_moves.extend(stone_moves)
    return valid_moves

def human_player(board, player):
    """
    This function takes the board and the player(the color stone they can move). It prints the board and
    then prompts the user to choose a stone and place to move the stone(prompts them to make a move). It then 
    checks to see if the move they chose was valid by the get_valid_moves function and if not it reprompts
    them. If it is valid then it returns the move they chose
    """
    black_token = '\u25CF'
    white_token = '\u25CB'
    # gets valid moves, prints them if there are any, if not, returns empty tuple
    valid_moves = get_valid_moves(board, player)
    if valid_moves:
        print(get_board_as_string(board))
    else:
        return ()
    # asks user to input valid move, symbol based on what color they are 
    if player == 1:
        print("Enter a valid move for " + black_token + ": ")
    else:
        print("Enter a valid move for " + white_token + ": ")
    # while loop that gets suer input for start and end position and reprompts until valid
    user_move = False
    while not user_move:
        start_row = int(input("Enter Starting row: "))
        start_column = int(input("Enter Starting column: "))
        end_row = int(input("Enter Ending row: "))
        end_column = int(input("Enter Ending column: "))
        given_move = ((start_row, start_column), (end_row, end_column))
        if given_move in valid_moves:
            print(given_move)
            user_move = True
        else:
            print(str(given_move) + " is not a valid move, Try again.")
    return given_move

def random_player(board, player):
    """
    This function takes the current board and the player's token color and returns a random
    valid move that the player could take.
    """
    # puts all valid moves in a tuple, if any, and uses the random.choice function to randomly
    # choose one move from the tuple and returns it to the player, or an empty tuple
    valid_moves = get_valid_moves(board, player)
    if valid_moves:
        return random.choice(valid_moves)
    else:
        return ()

def ai_player(board, player):
    """
    This function takes the current board and a player and gets the valid moves the player can make,
    and then returns one valid move for that player.
    """
    # gets all valid move for player
    valid_moves = get_valid_moves(board, player)
    # returns an empty tuple if no move, or the first valid move if there are any
    if not valid_moves:
        return ()
    else:
        return valid_moves[0]

def play_game(board):
    """
    This function takes a board and plays a full game of Konane between two AI players.
    It goes until one player can not make another move, and returns the player that won.
    """
    # randomly chooses which color starts
    current_player = random.randint(1, 2)
    # while loop goes until a player is returned(wins) and updates the board after each move
    while True:
        # finds a random move and if no moves, the other player is returned
        move = ai_player(board, current_player)
        if not move:
            if current_player == 1:
                return 2
            else:
                return 1
        # declares starting and ending place of the token and updates
        start_row = move[0][0]
        start_column = move[0][1]
        end_row = move[1][0]
        end_column = move[1][1]
        board[start_row][start_column] = 0
        board[end_row][end_column] = current_player
        # finds the variables in between and updates board taking away opponent tokens
        captured_row = (start_row + end_row) // 2
        captured_column = (start_column + end_column) // 2
        board[captured_row][captured_column] = 0
        # switches the player after each move made by the other
        if current_player == 1:
            current_player = 2
        else:
            current_player = 1

