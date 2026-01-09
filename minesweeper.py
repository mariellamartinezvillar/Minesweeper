# Import modules
import random

# Declare constants
MINES = -1
INCREMENT = 1
FLAG = '\u2691'
UNKNOWN = '?'
rate_easy = (10/100)
rate_medium = (30/100)
rate_hard = (50/100)

# 1 Nested List Functions
# 1.1 init_board
def init_board(nb_rows, nb_cols, value):
    """
    (positive int, positive int, any immutable type) -> list[list]
    
    Constructs and returns a 2D list with nb_rows and nb_cols, where each
    value in the inner lists is the given immutable argument value.
    Each row is a distinct list.
    
    >>> init_board(2,2,'111')
    [['111', '111'], ['111', '111']]   
    >>> init_board(3,3,1)
    [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  
    >>> init_board(2,2,'101')
    [['101', '101'], ['101', '101']]      
    """
    board = []  # empty list to hold rows
    
    for cell in range((nb_rows)):
        element = []  # empty row
        
        for sublist in range((nb_cols)):
            element.append(value)  # add value to the row
            
        board.append(element)     # add the row to the board
        
    return board

# 1.2 count_total
def count_total(board, value):
    """
    (list[list], any type) -> int
    
    Returns an integer representing the number of times that value occurs
    in board. The function counts how many times value occurs in the inner
    lists.
    
    >>> count_total([[4, 5, 0], [6, 5, 6], [4, 5, 7, 5]], 5)
    4
    >>> count_total([[0, 1, 2], [3, 4, 6], [7, 8, 9]], 0)
    1
    >>> count_total([[5, 5, 5], [2, 2, 2], [6, 6, 7]], 2)
    3
    """
    occurrence_count = 0   # start count at 0
    for element in board:
        for sublist in element:
            if sublist == value:
                # increment (+1) count when value is found
                occurrence_count += INCREMENT
    return occurrence_count

# 1.3 is_valid_position
def is_valid_position(board, row, col):
    """
    (list[list], int, int) -> bool
    
    Returns True if (row, col) is a valid position in board, False otherwise.
    A position is invalid if row or col is negative, or if it falls outside
    the board's dimensions.
    
    >>> board = init_board(4, 4, 1)
    >>> is_valid_position(board, 3, 3)
    True
    >>> is_valid_position(board, 4, 4)
    False
    >>> is_valid_position(board, -1, -2)
    False
    """
    if row < 0 or col < 0:  # check for negative indices
        return False
    
    # validate if row and col is within number of rows and columns
    if row >= len(board) or col >= len(board[row]):
        return False
    
    return True

# 1.4 get_neighbour_positions
def get_neighbour_positions(board, row, col):
    """
    (list[list], int, int) -> list[list[int]]
    
    Given position (row, col), returns a list of positions of valid adjacent
    positions (row, col) in board. Each adjacent position is represented as
    [neighbour_row, neighbour_col].
    
    >>> board = init_board(4, 4, 1)
    >>> get_neighbour_positions(board, 2, 2)
    [[1, 1], [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [3, 3]]
    >>> get_neighbour_positions(board, 3, 1)
    [[2, 0], [2, 1], [2, 2], [3, 0], [3, 2]]
    >>> get_neighbour_positions(board, 2, 3)
    [[1, 2], [1, 3], [2, 2], [3, 2], [3, 3]]
    """
    neighbours = []
    for delta_row in [-1, 0, 1]:
        for delta_col in [-1, 0, 1]:
            
            # remove the original position
            if not (delta_row == 0 and delta_col == 0):  
                neighbour_row = row + delta_row
                neighbour_col = col + delta_col
                
                if is_valid_position(board, neighbour_row, neighbour_col):
                    neighbours.append([neighbour_row, neighbour_col])
                    
    return neighbours
                
# 1.5 count_neighbours
def count_neighbours(board, row, col, value):
    """
    (list[list], int, int, any type) -> int
    
    Counts how many neighbour positions around (row, col) are in board
    containing value, and returns the count.
    
    >>> count_neighbours([[1, 2, 3, 4], [5, 6, 7, 8], [9, 1, 0, 2],
        [3, 4, 5, 6]], 2, 3, 0)
    1
    >>> count_neighbours([[4, 5, 4, 5], [2, 3, 4, 5], [6, 7, 6, 7],
        [8, 8, 2, 2]], 2, 1, 8)
    2
    >>> count_neighbours([[5, 5, 5, 5], [3, 4, 3, 5], [6, 7, 8, 2],
        [7, 8, 9, 8]], 1, 2, 5)
    4
    """
    value_count = 0
    # get the adjacent positions
    neighbour_positions = get_neighbour_positions(board, row, col)
    for element in neighbour_positions:
        neighbour_row = element[0]
        neighbour_col = element[1]
        if board[neighbour_row][neighbour_col] == value:
            value_count += INCREMENT
                
    return value_count
            
# 2 The Helper Board
# 2.1 new_mine_position
def new_mine_position(board):
    """
    (list[list[int]]) -> (int, int)
    
    Generates a random valid position (row, col) in board that does not
    contain a mine (-1). The function keeps trying until a non-mine cell
    is found.
    
    >>> random.seed(202)
    >>> new_mine_position([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    (1, 2)
    >>> random.seed(202)
    >>> new_mine_position([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    (1, 2)
    >>> random.seed(202)
    >>> new_mine_position([[1, 0, 1], [0, 0, 1], [-1, 0, -1]])
    (1, 2)
    
    """
    nb_row = len(board)
    nb_col = len(board[0])
    while True:
        row = random.randint(0, nb_row - 1)
        col = random.randint(0, nb_col - 1)
        if board[row][col] != MINES:
            return row, col
        
# 2.2 new_mine
def new_mine(board):
    """
    (list[list[int]]) -> None
    
    Randomly generates new mine position, sets its value in board to -1, and
    increments the value of all adjacent non-mine cells by 1.
    
    >>> random.seed(202)
    >>> board = init_board(2, 2, 1)
    >>> board
    [[1, 1], [1, 1]]
    >>> new_mine(board)
    >>> board
    [[2, 2], [2, -1]]
    >>> new_mine(board)
    >>> board
    [[3, 3], [-1, -1]]
    """
    # randomly generated a new mine position
    row, col = new_mine_position(board)
    board[row][col] = MINES
    # adjacent positions
    neighbours = get_neighbour_positions(board, row, col)
    for adjacent in neighbours:
        adj_row = adjacent[0]
        adj_col = adjacent[1]
        if board[adj_row][adj_col] != MINES:
            board[adj_row][adj_col] += INCREMENT
            
    return
        
# 2.3 generate_helper_board
def generate_helper_board(nb_rows, nb_cols, nb_mines):
    """
    (positive int, positive int, nonnegative int) -> list[list[int]]
    
    Creates a board of nb_rows (rows) and nb_cols (columns) with no 
    mines, then generates a board with nb_mines (mines) and returns
    the updated board.
    
    >>> random.seed(202)
    >>> generate_helper_board(3, 3, 1)
    [[0, 1, 1], [0, 1, -1], [0, 1, 1]]
    >>> generate_helper_board(4, 4, 0)
    [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    >>> generate_helper_board(2, 2, 1)
    [[1, 1], [1, -1]]
    >>> generate_helper_board(5, 5, 0) == init_board(5, 5, 0)
    True
    """
    # initialize board with no mines
    board = init_board(nb_rows, nb_cols, 0)
    
    mine_present = 0
    while mine_present < nb_mines:
        new_mine(board)
        mine_present += INCREMENT # track number of mines placed
        
    return board

# 3 The Game Board
# 3.1 flag
def flag(board, row, col):
    """
    (list[list], int, int) -> None
    
    At the position (row, col) in board, if it holds '?', the function changes
    it to '\u2691' (FLAG). If it holds '\u2691', the function changes it to 
    '?'.
    
    >>> board = [['?', '?', '?', '1'], ['⚑', '⚑', '⚑', '?'], 
        ['1', '1', '0', '0']]
    >>> flag(board, 0, 1)
    >>> board
    [['?', '⚑', '?', '1'], ['⚑', '⚑', '⚑', '?'], ['1', '1', '0', '0']]
    >>> board = [['⚑', '⚑', '⚑', '?'], ['?', '⚑', '⚑', '?'], 
        ['1', '0', '1', '0']]
    >>> flag(board, 1, 1)
    >>> board
    [['⚑', '⚑', '⚑', '?'], ['?', '?', '⚑', '?'], ['1', '0', '1', '0']]
    >>> board = [['?', '?', '?', '0'], ['1', '0', '1', '0'], 
        ['⚑', '⚑', '⚑', '⚑']]
    >>> flag(board, 2, 2)
    >>> board
    [['?', '?', '?', '0'], ['1', '0', '1', '0'], ['⚑', '⚑', '?', '⚑']]
    """
    if board[row][col] == UNKNOWN:
        board[row][col] = FLAG
    elif board[row][col] == FLAG:
        board[row][col] = UNKNOWN
        
    return
    
# 3.2 reveal
def reveal(helper_board, game_board, row, col):
    """
    (list[list[int]], list[list], int, int) -> None
    
    Gets the value at position (row, col) in helper board. If it is -1, the
    function raises an AssertionError with the message 'BOOM! You lost.'.
    Otherwise, it updates game_board at that position (row, col) with the
    string representation of the integer found in helper board.
    
    >>> helper_board = [[1, 2, 3], [4, -1, -1], [1, 2, 3]]
    >>> game_board = init_board(3, 3, '?')
    >>> game_board
    [['?', '?', '?'], ['?', '?', '?'], ['?', '?', '?']]
    >>> reveal(helper_board, game_board, 2, 2)
    >>> game_board
    [['?', '?', '?'], ['?', '?', '?'], ['?', '?', '3']]
    >>> reveal(helper_board, game_board, 0, 2)
    >>> game_board
    [['?', '?', '3'], ['?', '?', '?'], ['?', '?', '3']]
    Traceback (most recent call last):
    AssertionError: BOOM! You lost.
    """
    value = helper_board[row][col]
    if value == MINES:
        raise AssertionError('BOOM! You lost.')
    else:
        game_board[row][col] = str(value)
    
    return

# 3.3 print_board
def print_board(board):
    """
    (list[list]) -> None
    
    Displays board such that the elements within a row are separated by a
    space and each row is separated by a new line.
    
    >>> board = [list('?'*5), list('001⚑?'), list('⚑⚑?01'), list('?'*5), 
        list('100?⚑')]
    >>> print_board(board)
    ? ? ? ? ?
    0 0 1 ⚑ ?
    ⚑ ⚑ ? 0 1
    ? ? ? ? ?
    1 0 0 ? ⚑
    >>> board = [list('001⚑⚑'), list('?'*5), list('?'*5), list('102⚑⚑'), 
        list('?⚑⚑??')]
    >>> print_board(board)
    0 0 1 ⚑ ⚑
    ? ? ? ? ?
    ? ? ? ? ?
    1 0 2 ⚑ ⚑
    ? ⚑ ⚑ ? ?
    >>> board = [list('?'*5), list('?'*5), list('?'*5), list('001⚑?'), 
        list('????⚑')]
    >>> print_board(board)
    ? ? ? ? ?
    ? ? ? ? ?
    ? ? ? ? ?
    0 0 1 ⚑ ?
    ? ? ? ? ⚑
    """
    for row in board:
        print(' '.join(row))

# 4 Playing the Game
# 4.1 play
# Step 1: Initializing the Boards
def play():
    """
    () -> None
    
    Runs an interactive game of Minesweeper in the console. Prompts users for
    board size (number of rows and columns) and difficulty level (easy,
    medium and hard). It initializes the helper and game boards, and enters
    a loop where the user reveals or flags cells. The game ends with either
    a loss (revealing a mine) or a win (all safe cells revealed), at which
    point the final board is displayed with remaining mines flagged.
    """
    # Step 1: Initializing the Boards
    # User inputs
    nb_row = int(input("Enter number of rows for the board: "))
    nb_col = int(input("Enter number of columns for the board: "))
    level = input("Choose a difficulty from [EASY, MEDIUM, HARD]: ")

    # Determine mine rate based on difficulty
    if level == 'EASY':
        rate = rate_easy
    elif level == 'MEDIUM':
        rate = rate_medium
    else:
        rate = rate_hard
        
    nb_mine = int(nb_row * nb_col * rate)


    helper_board = generate_helper_board(nb_row, nb_col, nb_mine)
    game_board = init_board(nb_row, nb_col, UNKNOWN)

    # Step 2: Gameplay Loop
    
    nb_non_mine = nb_row * nb_col - nb_mine
    revealed_count = 0

    # Loop until all non-mine cells are revealed
    while revealed_count < nb_non_mine:
        
        # Remaining mines
        nb_flag = count_total(game_board, FLAG)
        mine_remaining = nb_mine - nb_flag
        
        # Display Current Board and the number of mines remaining
        print("Current Board: (" + str(mine_remaining) + " mines remaining)")
        print_board(game_board)

        # Get user's decision and its position
        decision = input("Choose 0 to reveal or 1 to flag: ")
        row = int(input("Which row? "))
        col = int(input("Which column? "))
            
        # Execute decision
        if decision == '0':
            reveal(helper_board, game_board, row, col)
        else:
            flag(game_board, row, col)
        
        # Recount revealed cells
        revealed_count = 0
        for row in game_board:
            for cell in row:
                if cell != FLAG and cell != UNKNOWN:
                    revealed_count += INCREMENT

    # Step 3: Congratulating the User
    # Flag all unflagged mines
    for row in range(nb_row):
        for col in range(nb_col):
            if game_board[row][col] == UNKNOWN:
                game_board[row][col] = FLAG
                
    # Print Final Board
    print("Congratulations! You won!")
    print("Final Board:")
    print_board(game_board)

# 5 Making a Bot
# 5.1 solve_cell
def solve_cell(board, row, col, left_click, right_click):
    """
    (list[list], int, int, function, function) -> None
    
    If position (row, col) in board does not hold an integer (in string form),
    the function does nothing.
    If the number of adjacent flagged cells is equal to the number of adjacent
    mines, function calls left_click on all neighbours that are not yet
    revealed or flagged.
    If the number of revealed neighbours is equal to the number of adjacent
    non-mines, function calls right_click on all neighbours that are not yet
    revealed or flagged.
    If both or neither conditions apply, nothing is done.
    """
    cell = board[row][col]
    if cell == UNKNOWN or cell == FLAG:
        return
    
    nb_adj_mine = int(cell)
    neighbours = get_neighbour_positions(board, row, col)
    
    # Count flagged and unknown neighbours
    nb_flag = 0
    nb_unknown = 0
    for element in neighbours:
        neighbour_row = element[0]
        neighbour_col = element[1]
        if board[neighbour_row][neighbour_col] == FLAG:
            nb_flag += 1
        elif board[neighbour_row][neighbour_col] == UNKNOWN:
            nb_unknown += 1
                
    # Condition 1: All mines flagged → reveal all remaining unknown
    if nb_flag == nb_adj_mine:
        for adjacent in neighbours:
            adj_row = adjacent[0]
            adj_col = adjacent[1]
            if board[adj_row][adj_col] == UNKNOWN:
                left_click(adj_row, adj_col)
        return
                    
    # Condition 2: All non-mines revealed → flag remaining unknowns

    nb_revealed = len(neighbours) - nb_flag - nb_unknown
    nb_non_mine = len(neighbours) - nb_adj_mine
    if nb_revealed == nb_non_mine:
        for neighbour in neighbours:
            neighbour_row = neighbour[0]
            neighbour_col = neighbour[1]
            if board[neighbour_row][neighbour_col] == UNKNOWN:
                right_click(neighbour_row, neighbour_col)
                
        return

                    
# 5.2 solve
def solve (board, left_click, right_click):
    """
    (list[list], function, function) -> None
    
    While there is at least one cell left on the board that is neither
    revealed nor flagged (i.e. a '?'), the function calls solve_cell on
    every single position in the board.
    """
    while count_total(board, UNKNOWN) > 0:
        for row in range(len(board)):
            for col in range(len(board[0])):
                solve_cell(board, row, col, left_click, right_click)
    return
