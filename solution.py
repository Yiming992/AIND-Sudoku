assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        counter_dict = {}

        for box in unit:
            if(len(values[box])==2):
                counter_dict.setdefault(values[box], []).append(box)

        for k,v in counter_dict.items():
            if(len(v)==2):
                boxes_to_eliminate_twins = [b for b in unit if b not in v]
                for box in boxes_to_eliminate_twins:
                    for digit in k:
                        values[box] = values[box].replace(digit, '')
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    ## Method 1
    # values = []
    # all_digits = '123456789'
    # for c in grid:
    #     if c == '.':
    #         values.append(all_digits)
    #     elif c in all_digits:
    #         values.append(c)
    # assert len(values) == 81
    # return dict(zip(boxes, values))

    ## Method 2
    assert len(grid)==81, "Input grid must be a string of length 81 (9x9)"
    values = {}
    for box, c in zip(boxes, grid):
        if(c=="."):
            values[box]="123456789"
        else:
            values[box]=c
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    ## Method 1
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # for box in solved_values:
    #     digit = values[box]
    #     for peer in peers[box]:
    #         values[peer] = values[peer].replace(digit,'')
    # return values

    ## Method 2
    for k,v in values.items():
        if len(v)==1:
            for peer in peers[k]:
                values[peer] = values[peer].replace(v, '')
    return values
    

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    ## Method 1
    # new_values = values.copy()  # note: do not modify original values
    # for unit in unitlist:
    #     for digit in '123456789':
    #         dplaces = [box for box in unit if digit in values[box]]
    #         if len(dplaces) == 1:
    #             new_values[dplaces[0]] = digit
    # return new_values

    ## Method 2
    new_values = values.copy()
    for units in unitlist:
        for digit in "123456789":
            digit_locations = [box for box in units if digit in values[box]]
            if(len(digit_locations)==1):
                new_values[digit_locations[0]] = digit

    return new_values    

def reduce_puzzle(values):
    ## Method 1
    # solved_values = [box for box in values.keys() if len(values[box]) == 1]
    # stalled = False
    # while not stalled:
    #     # Check how many boxes have a determined value
    #     solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        
    #     # Use the Eliminate Strategy
    #     values = eliminate(values)
    #     # Use the Only Choice Strategy
    #     values = only_choice(values)
    #     # Use the Naked Twins Strategy
    #     values = naked_twins(values)

    #     # Check how many boxes have a determined value, to compare
    #     solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
    #     # If no new values were added, stop the loop.
    #     stalled = solved_values_before == solved_values_after
    #     # Sanity check, return False if there is a box with zero available values:
    #     if len([box for box in values.keys() if len(values[box]) == 0]):
    #         return False
    # return values

    ## Method 2
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        values_solved_before = len([box for box in values.keys() if len(values[box])==1])

        # eliminate, only choice, naked twins
        # values = naked_twins(only_choice(eliminate(values)))
        values = only_choice(eliminate(values))

        values_solved_after = len([box for box in values.keys() if len(values[box])==1])

        stalled = values_solved_before==values_solved_after

        if any(len(values[box])==0 for box in values.keys()):
            return False

    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
        
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


## set up environment
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[cross(row, col)[0] for row, col in zip(rows,cols)], [cross(row, col)[0] for row, col in zip(rows[::-1],cols)]]

unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


if __name__ == '__main__':
    ## solve sudoku
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
