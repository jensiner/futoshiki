import copy


def readfile(file):
    """

    reads from input file to develop 3 2D arrays. One is the board with cells that are empty and those that are assigned,
    another is a 6x5 (6 rows, 5 columns) containing the horizontal constraints, and the last one is a 5x6 (5 rows, 6 columns)
    containing the vertical constraints

    """
    input_file = open(file, "r")
    board = [[], [], [], [], [], []]
    horizontal_constraints = [[], [], [], [], [], []]
    vertical_constraints = [[], [], [], [], []]
    input_counter = 0
    b_current_row = 0
    h_current_row = 0
    v_current_row = 0
    for line in input_file:
        for word in line.split():
            if input_counter < 36:
                if input_counter == 0:
                    board[b_current_row].append(word)
                else:
                    if input_counter % 6 == 0:
                        # go to next row every time a row is done (6 items added to board)
                        b_current_row += 1
                        board[b_current_row].append(word)
                    else:
                        board[b_current_row].append(word)
                input_counter += 1
                # read in 6x6 grid from input
                # [[0, 0, 0, 0, 0, 0],
                # [3, 0, 0, 0, 0, 0],
                # [0, 3, 0, 0, 6, 4],
                # [0, 0, 0, 0, 4, 0],
                # [0, 0, 0, 0, 0, 0],
                # [0, 0, 0, 0, 1, 3]]
            elif (input_counter > 35) and (input_counter < 66):
                # read in horizontal constraints --> create array
                if input_counter % 5 == 0:
                    horizontal_constraints[h_current_row].append(word)
                    h_current_row += 1
                else:
                    horizontal_constraints[h_current_row].append(word)
                input_counter += 1
            else:
                # read in vertical constraints --> create array
                if input_counter == 66:
                    vertical_constraints[v_current_row].append(word)
                else:
                    if input_counter % 6 == 0:
                        v_current_row += 1
                        vertical_constraints[v_current_row].append(word)
                    else:
                        vertical_constraints[v_current_row].append(word)
                input_counter += 1

    return board, horizontal_constraints, vertical_constraints


def forward_checking(board, horizontal_constraints, vertical_constraints, i, j, val):
    """
    Decrease domain of cells in neighbors
    :param board: the board/grid having gone through setup function
    :param horizontal_constraints: 2D array of horizontal constraints
    :param vertical_constraints: 2D array of vertical constraints
    :param i: the row where the cell is
    :param j: the column where the cell is
    :param val: val assigned to cell
    :return: bool based on success, new board
    """
    board_copy = copy.deepcopy(board)
    # decrease domain in the cells of the row
    for row in range(6):
        for col in range(6):
            # if you are at the same row as the changed cell, and the cell in question is not assigned
            if row == i and isinstance(board[row][col], list):
                for num in range(len(board[row][col])):  # for the number of items in the domain
                    if board[row][col][num] == val:
                        board_copy[row][col].remove(board_copy[row][col][num])
                        # if size of list is 0 -> return False
                        if len(board_copy[row][col]) == 0:
                            return False, None
            if col == j and isinstance(board[row][col], list):  # decrease domain in the cells of the column
                for num in range(len(board[row][col])):
                    if board[row][col][num] == val:
                        board_copy[row][col].remove(board_copy[row][col][num])
                        if len(board_copy[row][col]) == 0:
                            return False, None
    # check constraints
    # horizontal constraints
    if j < 5:
        if horizontal_constraints[i][j] != '0':  # right side of cell
            if horizontal_constraints[i][j] == '>':
                # remove items from i,j+1 that is < item[i][j]
                if isinstance(board_copy[i][j + 1], list):
                    remove_items = []
                    for num in range(len(board_copy[i][j + 1])):
                        if board[i][j] < board_copy[i][j + 1][num]:
                            remove_items.append(board_copy[i][j + 1][num])
                    for item_no in range(len(remove_items)):
                        board_copy[i][j + 1].remove(remove_items[item_no])
                    # check if there is a constraint at [i][j+1] (if j+1 < 5)
                    if j + 1 < 5 and horizontal_constraints[i][j + 1] != '0' and isinstance(board_copy[i][j + 2], list):
                        # if there is -> remove item from [i][j+1] that would make domain of cell [i][j+2] have no
                        # domain
                        if horizontal_constraints[i][j + 1] == '>':
                            remove_items = []
                            for num in range(len(board_copy[i][j + 1])):
                                constraint = False
                                for num2 in range(len(board_copy[i][j + 2])):
                                    if board_copy[i][j + 1][num] > board_copy[i][j + 2][num2]:
                                        constraint = True
                                if not constraint:
                                    remove_items.append(board_copy[i][j + 1][num])
                            for item_no in range(len(remove_items)):
                                board_copy[i][j + 1].remove(remove_items[item_no])
                        elif horizontal_constraints[i][j + 1] == '<':
                            remove_items = []
                            for num in range(len(board_copy[i][j + 1])):
                                constraint = False
                                for num2 in range(len(board_copy[i][j + 2])):
                                    if board_copy[i][j + 1][num] < board_copy[i][j + 2][num2]:
                                        constraint = True
                                if not constraint:
                                    remove_items.append(board_copy[i][j + 1][num])
                            for item_no in range(len(remove_items)):
                                board_copy[i][j + 1].remove(remove_items[item_no])

            elif horizontal_constraints[i][j] == '<':
                if isinstance(board_copy[i][j + 1], list):
                    remove_items = []
                    for num in range(len(board_copy[i][j + 1])):  # remove items from i,j+1 that is > item[i][j]
                        if board[i][j] > board_copy[i][j + 1][num]:
                            remove_items.append(board_copy[i][j + 1][num])
                    for item_no in range(len(remove_items)):
                        board_copy[i][j + 1].remove(remove_items[item_no])
                    # check if there is a constraint at [i][j+1] (if j+1 < 5)
                    if j + 1 < 5 and horizontal_constraints[i][j + 1] != '0' and isinstance(board_copy[i][j + 2], list):
                        # if there is -> remove item from [i][j+1] that would make domain of cell [i][j+2] have no domain
                        if horizontal_constraints[i][j + 1] == '>':
                            remove_items = []
                            for num in range(len(board_copy[i][j + 1])):
                                constraint = False
                                for num2 in range(len(board_copy[i][j + 2])):
                                    if board_copy[i][j + 1][num] > board_copy[i][j + 2][num2]:
                                        constraint = True
                                if not constraint:
                                    remove_items.append(board_copy[i][j + 1][num])
                            for item_no in range(len(remove_items)):
                                board_copy[i][j + 1].remove(remove_items[item_no])
                        elif horizontal_constraints[i][j + 1] == '<':
                            remove_items = []
                            for num in range(len(board_copy[i][j + 1])):
                                constraint = False
                                for num2 in range(len(board_copy[i][j + 2])):
                                    if board_copy[i][j + 1][num] < board_copy[i][j + 2][num2]:
                                        constraint = True
                                if not constraint:
                                    remove_items.append(board_copy[i][j + 1][num])
                            for item_no in range(len(remove_items)):
                                board_copy[i][j + 1].remove(remove_items[item_no])
            if isinstance(board_copy[i][j+1], list) and len(board_copy[i][j + 1]) == 0:  # if len(domain) of cell [i][j+1] == 0, return False
                return False, None

    if j > 0:
        if horizontal_constraints[i][j - 1] != '0' and isinstance(board_copy[i][j - 1], list):  # left side of cell
            if horizontal_constraints[i][j - 1] == '>':
                remove_items = []  # remove items from i,j-1 that is < item[i][j]
                for num in range(len(board_copy[i][j - 1])):
                    if board_copy[i][j - 1][num] < board[i][j]:
                        remove_items.append(board_copy[i][j - 1][num])
                for item_no in range(len(remove_items)):
                    board_copy[i][j - 1].remove(remove_items[item_no])
                # check if there is a constraint at [i,j-2] (if j-2 > -1)
                if j - 2 > -1 and horizontal_constraints[i][j - 2] != '0' and isinstance(board_copy[i][j - 2], list):
                    # if there is -> remove items from [i][j-1] that would make domain of cell [i][j-2] have no domain
                    if horizontal_constraints[i][j - 2] == '>':
                        remove_items = []
                        for num in range(len(board_copy[i][j - 1])):
                            constraint = False
                            for num2 in range(len(board_copy[i][j - 2])):
                                if board_copy[i][j - 2][num2] > board_copy[i][j - 1][num]:
                                    constraint = True
                            if not constraint:
                                remove_items.append(board_copy[i][j - 1][num])
                        for item_no in range(len(remove_items)):
                            board_copy[i][j - 1].remove(remove_items[item_no])
                    elif horizontal_constraints[i][j - 2] == '<':
                        remove_items = []
                        for num in range(len(board_copy[i][j - 1])):
                            constraint = False
                            for num2 in range(len(board_copy[i][j - 2])):
                                if board_copy[i][j - 2][num2] < board_copy[i][j - 1][num]:
                                    constraint = True
                            if not constraint:
                                remove_items.append(board_copy[i][j - 1][num])
                        for item_no in range(len(remove_items)):
                            board_copy[i][j - 1].remove(remove_items[item_no])

            elif horizontal_constraints[i][j - 1] == '<':
                remove_items = []
                for num in range(len(board_copy[i][j - 1])):
                    if board_copy[i][j - 1][num] > board[i][j]:
                        remove_items.append(board_copy[i][j - 1][num])
                for item_no in range(len(remove_items)):
                    board_copy[i][j - 1].remove(remove_items[item_no])
                if j - 2 > -1 and horizontal_constraints[i][j - 2] != '0' and isinstance(board_copy[i][j - 2], list):
                    # if there is -> remove items from [i][j-1] that would make domain of cell [i][j-2] have no domain
                    if horizontal_constraints[i][j - 2] == '>':
                        remove_items = []
                        for num in range(len(board_copy[i][j - 1])):
                            constraint = False
                            for num2 in range(len(board_copy[i][j - 2])):
                                if board_copy[i][j - 2][num2] > board_copy[i][j - 1][num]:
                                    constraint = True
                            if not constraint:
                                remove_items.append(board_copy[i][j - 1][num])
                        for item_no in range(len(remove_items)):
                            board_copy[i][j - 1].remove(remove_items[item_no])
                    elif horizontal_constraints[i][j - 2] == '<':
                        remove_items = []
                        for num in range(len(board_copy[i][j - 1])):
                            constraint = False
                            for num2 in range(len(board_copy[i][j - 2])):
                                if board_copy[i][j - 2][num2] < board_copy[i][j - 1][num]:
                                    constraint = True
                            if not constraint:
                                remove_items.append(board_copy[i][j - 1][num])
                        for item_no in range(len(remove_items)):
                            board_copy[i][j - 1].remove(remove_items[item_no])
            if isinstance(board_copy[i][j-1], list) and len(board_copy[i][j - 1]) == 0:  # if len(domain) of cell [i][j-1] == 0, return False
                return False, None

    # vertical constraints
    # if i < 5 (bottom side) and vertical_constraints[i][j] exist and board_copy[i+1][j] is list
    if i < 5 and vertical_constraints[i][j] != '0' and isinstance(board_copy[i + 1][j], list):
        # ^ -  if a domain in board_copy[i+1][j] is < board[i][j], remove that domain
        if vertical_constraints[i][j] == '^':
            remove_items = []
            for num in range(len(board_copy[i + 1][j])):
                if board_copy[i + 1][j][num] < board[i][j]:
                    remove_items.append(board_copy[i + 1][j][num])
            for item_no in range(len(remove_items)):
                board_copy[i + 1][j].remove(remove_items[item_no])
            # check if there is a vertical_constraint[i+1][j] (i+1 < 5) and board_copy[i+2][j] is list
            if i + 1 < 5 and vertical_constraints[i + 1][j] != '0' and isinstance(board_copy[i + 2][j], list):
                # ^ for ea. domain in board_copy[i+1][j], if there exists one domain in which board_copy[i+1][j] <
                # board_copy[i+2][j] -> constraint = TRUE
                if vertical_constraints[i + 1][j] == '^':
                    remove_items = []
                    for num in range(len(board_copy[i + 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i + 2][j])):
                            if board_copy[i + 1][j][num] < board_copy[i + 2][j][num2]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i + 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i+1][j]
                        board_copy[i + 1][j].remove(remove_items[item_no])
                # v for ea. domain in board_copy[i+1][j], if there exists one domain in which board_copy[i+1][j] >
                # board_copy[i+2][j] -> constraint = TRUE
                elif vertical_constraints[i + 1][j] == 'v':
                    remove_items = []
                    for num in range(len(board_copy[i + 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i + 2][j])):
                            if board_copy[i + 1][j][num] > board_copy[i + 2][j][num2]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i + 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i+1][j]
                        board_copy[i + 1][j].remove(remove_items[item_no])
        # v - if a domain in board[i+1][j] is > board[i][j], remove from domain
        if vertical_constraints[i][j] == 'v':
            remove_items = []
            for num in range(len(board_copy[i + 1][j])):
                if board_copy[i + 1][j][num] > board[i][j]:
                    remove_items.append(board_copy[i + 1][j][num])
            for item_no in range(len(remove_items)):
                board_copy[i + 1][j].remove(remove_items[item_no])
            # check if there is a vertical_constraint[i+1][j] (i+1 < 5) and board_copy[i+2][j] is list
            if i + 1 < 5 and vertical_constraints[i + 1][j] != '0' and isinstance(board_copy[i + 2][j], list):
                # ^ for ea. domain in board_copy[i+1][j], if there exists one domain in which board_copy[i+1][j] <
                # board_copy[i+2][j] -> constraint = TRUE
                if vertical_constraints[i + 1][j] == '^':
                    remove_items = []
                    for num in range(len(board_copy[i + 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i + 2][j])):
                            if board_copy[i + 1][j][num] < board_copy[i + 2][j][num2]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i + 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i+1][j]
                        board_copy[i + 1][j].remove(remove_items[item_no])
                # v for ea. domain in board_copy[i+1][j], if there exists one domain in which board_copy[i+1][j] >
                # board_copy[i+2][j] -> constraint = TRUE
                elif vertical_constraints[i + 1][j] == 'v':
                    remove_items = []
                    for num in range(len(board_copy[i + 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i + 2][j])):
                            if board_copy[i + 1][j][num] > board_copy[i + 2][j][num2]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i + 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i+1][j]
                        board_copy[i + 1][j].remove(remove_items[item_no])
        # if len(board_copy[i+1][j]) == 0, return False
        if len(board_copy[i + 1][j]) == 0:
            return False, None

    # if i > 0 (top side) and vertical_constraints[i-1][j] exist and board_copy[i-1][j] is list
    if i > 0 and vertical_constraints[i - 1][j] != '0' and isinstance(board_copy[i - 1][j], list):
        if vertical_constraints[i - 1][j] == '^':
            remove_items = []  # if a domain in board[i-1][j] is > board[i][j], remove that from domain
            for num in range(len(board_copy[i - 1][j])):
                if board_copy[i - 1][j][num] > board[i][j]:
                    remove_items.append(board_copy[i - 1][j][num])
            for item_no in range(len(remove_items)):
                board_copy[i - 1][j].remove(remove_items[item_no])
            # check if there is a vertical constraint[[i-2][j] (i-2 > -1) and board_copy[i-2][j] is list
            if i - 2 > -1 and vertical_constraints[i - 2][j] != '0' and isinstance(board_copy[i - 2][j], list):
                # ^ for ea. domain in board_copy[i-1][j], if there exists one domain in which board_copy[i-2][j] <
                # board_copy[i-1][j] -> constraint = TRUE
                if vertical_constraints[i - 2][j] == '^':
                    remove_items = []
                    for num in range(len(board_copy[i - 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i - 2][j])):
                            if board_copy[i - 2][j][num2] < board_copy[i - 1][j][num]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i - 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i-1][j]
                        board_copy[i - 1][j].remove(remove_items[item_no])
                elif vertical_constraints[i - 2][j] == 'v':  # v for ea. domain in board_copy[i-1][j], if there exists
                    # one domain in which board_copy[i-2][j] > board_copy[i-1][j] -> constraint = TRUE
                    remove_items = []
                    for num in range(len(board_copy[i - 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i - 2][j])):
                            if board_copy[i - 2][j][num2] > board_copy[i - 1][j][num]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i - 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i-1][j]
                        board_copy[i - 1][j].remove(remove_items[item_no])
        elif vertical_constraints[i - 1][j] == 'v':
            remove_items = []  # if a domain in board[i-1][j] is < board[i][j], remove that from domain
            for num in range(len(board_copy[i - 1][j])):
                if board_copy[i - 1][j][num] < board[i][j]:
                    remove_items.append(board_copy[i - 1][j][num])
            for item_no in range(len(remove_items)):
                board_copy[i - 1][j].remove(remove_items[item_no])
            # check if there is a vertical_constraint[i-2][j] (i-2 > -1) and board_copy[i-2][j] is list
            if i - 2 > -1 and vertical_constraints[i - 2][j] != '0' and isinstance(board_copy[i - 2][j], list):
                if vertical_constraints[i - 2][j] == '^':
                    remove_items = []
                    for num in range(len(board_copy[i - 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i - 2][j])):
                            if board_copy[i - 2][j][num2] < board_copy[i - 1][j][num]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i - 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i-1][j]
                        board_copy[i - 1][j].remove(remove_items[item_no])
                elif vertical_constraints[i - 2][j] == 'v':  # v for ea. domain in board_copy[i-1][j], if there exists
                    # one domain in which board_copy[i-2][j] > board_copy[i-1][j] -> constraint = TRUE
                    remove_items = []
                    for num in range(len(board_copy[i - 1][j])):
                        constraint = False
                        for num2 in range(len(board_copy[i - 2][j])):
                            if board_copy[i - 2][j][num2] > board_copy[i - 1][j][num]:
                                constraint = True
                        if not constraint:
                            remove_items.append(board_copy[i - 1][j][num])
                    for item_no in range(
                            len(remove_items)):  # for all domain vals where its not true -> remove from domain of
                        # board_copy[i-1][j]
                        board_copy[i - 1][j].remove(remove_items[item_no])
        if len(board_copy[i - 1][j]) == 0:  # if len(board_copy[i-1][j]) == 0, return False
            return False, None

    return True, board_copy


def setup(board, horizontal_constraints, vertical_constraints):
    """
    Identifies the domain for cells not assigned, and make cells assigned into integers
    :param horizontal_constraints: 2D array of horizontal constraints
    :param vertical_constraints: 2D array of vertical constraints
    :param board: the board initialized from the file input (after having run through the readfile function)
    :return: board with domain for ea. cell that is not assigned and convert string to number for cells that are assigned
    """
    forward_check_list = []
    for i in range(6):
        for j in range(6):
            if board[i][j] == '0':
                board[i][j] = [1, 2, 3, 4, 5, 6]
            elif board[i][j] == '1':
                board[i][j] = 1
                val = 1
                forward_check_list.append((i, j, val))
            elif board[i][j] == '2':
                board[i][j] = 2
                val = 2
                forward_check_list.append((i, j, val))
            elif board[i][j] == '3':
                board[i][j] = 3
                val = 3
                forward_check_list.append((i, j, val))
            elif board[i][j] == '4':
                board[i][j] = 4
                val = 4
                forward_check_list.append((i, j, val))
            elif board[i][j] == '5':
                board[i][j] = 5
                val = 5
                forward_check_list.append((i, j, val))
            elif board[i][j] == '6':
                board[i][j] = 6
                val = 6
                forward_check_list.append((i, j, val))
    for index in range(len(forward_check_list)):
        success, new_board = forward_checking(board, horizontal_constraints, vertical_constraints,
                                              forward_check_list[index][0], forward_check_list[index][1], forward_check_list[index][2])
        if success:
            board = copy.deepcopy(new_board)
    return board


class Board:
    def __init__(self, grid, horizontal_constraints, vertical_constraints):
        self.grid = grid
        self.horizontal_constraints = horizontal_constraints
        self.vertical_constraints = vertical_constraints

    def get_constraints_no(self, i, j):
        """
        check # of unassigned neighbors (by looking at how many cells in the row and column are of list type) and check
        # of inequality constraints in row and column
        :param i:
        :param j:
        :return: # of constraints
        """
        constraints = 0

        for row in range(6):
            for col in range(6):
                if row == i and col == j:
                    continue
                if row == i and isinstance(self.grid[row][col], list):  # check row (using i)
                    constraints += 1
                if col == j and isinstance(self.grid[row][col], list):  # check column (using j)
                    constraints += 1

        for row in range(6):  # check horizontal constraints (using i)
            for col in range(5):
                if row == i and horizontal_constraints[row][col] != '0':
                    constraints += 1

        for row in range(5):  # check vertical constraints (using j)
            for col in range(6):
                if col == j and vertical_constraints[row][col] != '0':
                    constraints += 1

        return constraints

    def get_domain(self, i, j):
        """
        :param i:
        :param j:
        :return: # of domain
        """
        return self.grid[i][j]  # only works for cells not assigned

    def isConsistent(self):
        """
        checks that no cell that is of list type has a len of 0
        :return: True or False
        """
        for row in range(6):
            for col in range(6):
                if isinstance(self.grid[row][col], list) and len(self.grid[row][col]) == 0:
                    return False
        return True

    def isComplete(self):
        """

        :return: T if no cell is of list type
        """
        for row in range(6):
            for col in range(6):
                if isinstance(self.grid[row][col], list):
                    return False
        return True


def select_unassigned_variable(board, Board):
    """
    selects variable to assign using MRV (get_domain) and degree (get_constraints)
    chooses a random value if no single is identified
    :param board: the grid itself
    :param Board: the Board object
    :return: i, j the indexes of the selected unassigned variable
    """
    # MRV (cell with least # of domain left)

    least_domain = 0
    low_domain_counter = 0
    Least_Domains = []
    # for 6x6 grid:
    for row in range(6):
        for col in range(6):
            if isinstance(board[row][col], list) and least_domain == 0:  # if least_domain has not been set
                least_domain = len(board[row][col])
                low_domain_counter = 1
                cell = (row, col)

            elif isinstance(board[row][col], list) and len(board[row][col]) < least_domain:  # new low
                low_domain_counter = 1
                cell = (row, col)

            elif isinstance(board[row][col], list) and len(board[row][col]) == least_domain:  # equal
                low_domain_counter += 1

    if low_domain_counter > 1:
        for row in range(6):
            for col in range(6):
                if isinstance(board[row][col], list) and len(board[row][col]) == least_domain:
                    Least_Domains.append((row, col))  # collect all the unassigned variables that have the lowest
                    # legal values left
        # degree heuristic
        highest_constraint = 0
        highest_constraint_counter = 0
        # for ea. item in Least_Domains, check constraint
        for item in range(len(Least_Domains)):
            # if # of constraint > highest_constraint: highest_constraint = THIS, set cell to Least_Domain[item], set counter = 1
            if Board.get_constraints_no(Least_Domains[item][0], Least_Domains[item][1]) > highest_constraint:
                highest_constraint = Board.get_constraints_no(Least_Domains[item][0], Least_Domains[item][1])
                highest_constraint_counter = 1
                cell = (Least_Domains[item][0], Least_Domains[item][1])
            # if # of constraint == highest_constraint: counter+=1
            elif Board.get_constraints_no(Least_Domains[item][0], Least_Domains[item][1]) == highest_constraint:
                highest_constraint_counter += 1

        return cell

    else:
        return cell


def backtrack(Board):
    """
    - check if assignment is complete, if it is RETURN assignment
    - select a VAR using select_unassigned_variable
    - for ea. value in domain for that variable:
        - save domain
        - assign VAR to value
        - forward checking on var (return bool, proposed changes (if bool is TRUE))
        if forward checking is NOT failure,
            - save copy of the board
            - make the changes to the board (forward_checking)
            - RESULT = backtrack(board)
            if RESULT is NOT failure, return RESULT
            remove changes to the board (forward_checking) (revert back to previous copy)
        restore domain
    - return failure

    :param Board:
    :return: Board
    """
    if Board.isComplete():
        return Board
    var = select_unassigned_variable(Board.grid, Board)  # gets a tuple where var[0] == row and var[1] == col
    for item in range(len(Board.get_domain(var[0], var[1]))):
        prev_domain = Board.get_domain(var[0], var[1])
        Board.grid[var[0]][var[1]] = prev_domain[item]
        val = copy.deepcopy(prev_domain[item])

        success, new_board = forward_checking(Board.grid, Board.horizontal_constraints, Board.vertical_constraints, var[0], var[1], val)
        if success:
            prev_board = copy.deepcopy(Board.grid)
            Board.grid = copy.deepcopy(new_board)
            result = backtrack(Board)
            if result:
                return result
            Board.grid = prev_board
        Board.grid[var[0]][var[1]] = prev_domain
    return False


def writefile(solution, file):
    """

    :param solution: final solution grid
    :param file: file object that has been opened
    :return:
    """
    for item in range(len(solution)):
        for val in range(len(solution[item])):
            file.write(str(solution[item][val]) + ' ')
        file.write('\n')

    file.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # input 1
    board, horizontal_constraints, vertical_constraints = readfile("Input1.txt")
    board = setup(board, horizontal_constraints, vertical_constraints)
    Board1 = Board(board, horizontal_constraints, vertical_constraints)
    solution1 = backtrack(Board1)
    f = open("Output1.txt", "w")
    writefile(solution1.grid, f)

    # input 2
    board2, horizontal_constraints2, vertical_constraints2 = readfile("Input2.txt")
    board2 = setup(board2, horizontal_constraints2, vertical_constraints2)
    Board2 = Board(board2, horizontal_constraints2, vertical_constraints2)
    solution2 = backtrack(Board2)
    f2 = open("Output2.txt", "w")
    writefile(solution2.grid, f2)

    # input 3
    board3, horizontal_constraints3, vertical_constraints3 = readfile("Input3.txt")
    board3 = setup(board3, horizontal_constraints3, vertical_constraints3)
    Board3 = Board(board3, horizontal_constraints3, vertical_constraints3)
    solution3 = backtrack(Board3)
    f3 = open("Output3.txt", "w")
    writefile(solution3.grid, f3)


