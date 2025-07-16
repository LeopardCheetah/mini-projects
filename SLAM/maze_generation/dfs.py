# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Randomized_depth-first_search - recursive ver

import random

# binary search on list for target
# ls should be sorted
# ls in this case will all be integers
# if target not found then -1 will be returned
def bsearch(ls, target):
    if len(ls) == 0:
        return -1
    
    if ls[0] == target:
        return 0
    
    if ls[-1] == target:
        return len(ls) - 1
    
    _left = 0
    _right = len(ls) - 1
    _mid = 1

    while _left < _right:
        _mid = (_left + _right) // 2
        if ls[_mid] == target:
            return _mid 
        
        if ls[_mid] > target:
            # target is in lower half 
            # move right pointer
            _right = _mid - 1
            continue 

        # ls[_mid] < target
        # move left pointer up
        _left = _mid + 1
        continue 
    
    if ls[_left] == target:
        return _left 
    
    return -1


def generate_dfs_maze(n, path_symbol=" ", wall_symbol="x"):
    # basic checks
    if not isinstance(n, int):
        return f"Cannot use a non-integer {n} side length!"
    
    if n < 1:
        return f"Side length {n} cannot be shorter than 1!"
    
    if n == 1:
        return [[path_symbol]]
    
    if n > 100:
        return f"Mazes of size {n} > 100 are not supported."
    
    _n = ((n >> 1) << 1) + 1 # turn n odd

    # essentially turn grid into 
    # .x.x.
    # xxxxx
    # .x.x. etc. to do dfs on

    _maze = [[path_symbol if _x % 2 == _y % 2 == 0 else wall_symbol for _x in range(_n)] for _y in range(_n)]

    _qn = (_n // 2 + 1) # valuable quantity for side length of this smaller wall maze thing
    _not_visited = [i for i in range(_qn**2)] # just remove from this list as appropriate 
    _squares_backtracked = []
    # 0 1 2 3 4
    # 5 6 7 8 9
    # ......
    # 15
    # 20 21 22 23 24

    _y = random.randint(0, _qn - 1)
    _x = 0
    # _y*(_qn) + _x = square id

    # start alg!
    # choose path if path is available
    # else backtrack
    _not_visited.remove(_y*_qn + _x)
    _potential_sqs = [-1, -1, -1, -1]

    # last square wont be "backtrackable"
    while len(_squares_backtracked) < _qn**2 - 1:
        # generate potentail_list
        _potential_sqs = []

        if _x > 0: # not on very left edge
            if bsearch(_not_visited, _y*_qn + _x - 1) > -1:
                _potential_sqs.append((_y*_qn + _x - 1, 'w'))
        
        if _x < _qn - 1:
            if bsearch(_not_visited, _y*_qn + _x + 1) > -1:
                _potential_sqs.append((_y*_qn + _x + 1, 'e'))

        if _y > 0: # not on very top
            if bsearch(_not_visited, (_y - 1)*_qn + _x) > -1:
                _potential_sqs.append(((_y - 1)*_qn + _x, 'n'))
            
        if _y < _qn - 1:
            if bsearch(_not_visited, (_y + 1)*_qn + _x) > -1:
                _potential_sqs.append(((_y + 1)*_qn + _x, 's'))
    
        # yikes, backtrack
        if len(_potential_sqs) == 0:  
            # make sure there is a path to specified square AND square exists 

            _btrackable = [_y*_qn + _x - 1, (_y + 1)*_qn + _x, _y*_qn + _x + 1, (_y - 1)*_qn + _x] # W, S, E, N 

            # check n first, then e, then s, then w

            # north
            # if we are on the edge or if we've backtracked here before or if there's a wall between us then not a viable candidate
            if (_y < 1) or ((_y - 1)*_qn + _x in _squares_backtracked) or (_maze[2*_y - 1][2*_x] == wall_symbol): # rahhhhh why am i working with ids
                _btrackable.pop() # i can do this since 3 is the last element

            # east
            if (_x > _qn - 2) or (_y*_qn + _x + 1 in _squares_backtracked) or (_maze[2*_y][2*_x + 1] == wall_symbol):
                _btrackable.pop(2)

            # south
            if (_y > _qn - 2) or ((_y + 1)*_qn + _x in _squares_backtracked) or (_maze[2*_y + 1][2*_x] == wall_symbol):
                _btrackable.pop(1)
            
            # west
            if (_x < 1) or (_y*_qn + _x - 1 in _squares_backtracked) or (_maze[2*_y][2*_x - 1] == wall_symbol):
                _btrackable.pop(0)

            # lowkey idk why i did that much work
            if len(_btrackable) == 0:
                # assume we're done!?!?!?! 
                # this should never happen
                print("Not sure why but we're somehow out of the loop.")
                break

            if len(_btrackable) > 1:
                # what the algorithm just happened bro 
                print("Not sure why we're able to backtrack to more than more than one location.")
                print(f"Apparently we can backtrack to {_btrackable}.")
                raise Exception(f"Backtrack Error: More than 1 square available to backtrack to. See map {_maze} at square (x={2*_x}, y={2*_y}); Backtracked squares = {_squares_backtracked}.")
            
            # backtrack lmao
            _squares_backtracked.append(_y*_qn + _x)
            _y, _x = divmod(_btrackable[0], _qn)
            continue 

        # barge forward in search of more squares
        _new_sq = random.choice(_potential_sqs)
        # go towards the promised land
        _not_visited.remove(_new_sq[0])

        # remove wall
        if _new_sq[1] == 'n':
            _maze[2*_y - 1][2*_x] = path_symbol
        elif _new_sq[1] == 's':
            _maze[2*_y + 1][2*_x] = path_symbol
        elif _new_sq[1] == 'e':
            _maze[2*_y][2*_x + 1] = path_symbol
        elif _new_sq[1] == 'w':
            _maze[2*_y][2*_x - 1] = path_symbol

        _y, _x = divmod(_new_sq[0], _qn)
        continue 

    # we should be done
    return _maze


# <copied>
def make_maze_str(m, border=True, double=True):
    if not isinstance(m, list):
        return m # some error
    
    s = ''
    _d = 2 if double else 1
    if not border:
        for _i, _v in enumerate(m):
            for _j, _w in enumerate(_v):
                s += _w 

                if double:
                    s += 'x' if _w == 'x' else ' '
            
            s += '\n'

        return s 
    
    s += '+' + '-'*len(m)*_d + '+' + '\n'

    for _i, _v in enumerate(m):
        s += '|'

        for _j, _w in enumerate(_v):
            if _w == 'x': # wall
                s += _w*_d
                continue 
            
            s += _w + ' '*(_d - 1) 
        
        s += '|' + '\n'

    s += '+' + '-'*len(m)*_d + '+' + '\n' # end off
    return s

# print()
# print(make_maze_str(generate_dfs_maze(25), double=True))