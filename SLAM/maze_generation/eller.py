# eller's algorithm
# https://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm
# this is implemented with sets so i guess ill use sets

import random

# generate eller maze
# gonna have to coerce n to be odd
def generate_eller_maze(n, path_symbol=" ", wall_symbol="x"):
    # generate maze
    
    if not isinstance(n, int):
        return f"Sidelength {n} not an integer :("
    
    if n < 1:
        return f"Sidelength {n} must not be less than 1."
    
    if n == 1:
        return [[path_symbol]]
    
    _n = ((n >> 1) << 1) + 1 # sneaky bitshift aah operations

    # generate .#.
    #          ###
    #          .#. (etc.)

    _maze = [[path_symbol if _x % 2 == _y % 2 == 0 else wall_symbol for _x in range(_n)] for _y in range(_n)]

    _q = _n // 2 + 1 # side length of inner maze

    # keep track of who's with who
    # for simplicity we'll just use the integers 0 -> n - 1 to do that
    _line_state = [{_v} for _v in range(_q)] 
    _set_state = [_v for _v in range(_q)] # which set is things in?

    # if the maze is 1-1-1 | 2-2 then set_state should be [0, 0, 0, 1, 1] and line_state should be [{0, 1, 2}, {3, 4}]

    # this apparently O(n) algorithm im gonna turn into O(n^2)

    # higher value = more likely to join
    # 1 = just a grid atp
    _join_temp = 0.6 
    _down_temp = 0.5

    for _row in range(_q - 1):
        # use eller's to generate a maze and write to the actual _maze object
        # randomly merge adjacent cells

        for _cell_ind in range(_q - 1):
            # conditionally merge _cell_ind with _cell_ind + 1
            if _set_state[_cell_ind] == _set_state[_cell_ind + 1]:
                continue 

            if random.random() > _join_temp:
                continue # rip rng

            # join sets
            # print(_line_state, _cell_ind, _set_state[_cell_ind], _set_state[_cell_ind + 1]) -- DEBUG
            _line_state[_set_state[_cell_ind]] = _line_state[_set_state[_cell_ind]].union(_line_state[_set_state[_cell_ind + 1]]) # merge!
            _line_state[_set_state[_cell_ind + 1]] = {}
            _c = _set_state[_cell_ind + 1]

            # write to main maze
            _maze[2*_row][2*_cell_ind + 1] = path_symbol


            for _ind in range(_q):
                # yes yes bad programming but i also needa mutate values its whatever
                if _set_state[_ind] == _c:
                    _set_state[_ind] = _set_state[_cell_ind]
                    continue 

        # print(f'clean up time: {_set_state}, {_line_state}') -- DEBUG

        # clean up + reformat everything
        _sub_list = [0]
        for _set in _line_state:
            if _set == {} or _set == set():
                _sub_list.append(_sub_list[-1] + 1)
                continue 

            _sub_list.append(_sub_list[-1])

        _sub_list.pop(0)
        
        # print(f'sub_list: {_sub_list}') -- DEBUG

        # formally pop everything, update other list
        # go from back to front
        for _i in range(len(_sub_list) - 1, 0, -1):
            if _sub_list[_i] != _sub_list[_i - 1]:
                _line_state.pop(_i)

        if _line_state[0] == set() or _line_state[0] == {}:
            _line_state.pop(0)

        # update final set list
        for _i, _v in enumerate(_set_state):
            _set_state[_i] -= _sub_list[_v]

        # print(f'set state: {_set_state}\nline state: {_line_state}') -- DEBUG

        _sets_columned = []
        _prev_down = False
        for _cell_ind, _v in enumerate(_set_state): # decide if we move down or not
            _down = False
            if _v not in _sets_columned and _v not in _set_state[_cell_ind + 1:]:
                _down = True 

            # just do a random coin flip sorta to decide this going down thing
            # do the _v check AFTER in case index 0
            # well technically index -1 exists but yeah thats bad
            if ((not _prev_down) or (_v != _set_state[_cell_ind - 1])) and (random.random() < _down_temp):
                _down = True

            if _down:
                # go down
                # remove wall, make sure values are part of the right sets
                _maze[2*_row + 1][2*_cell_ind] = path_symbol
                # print(f'wall removed at ({2*_row + 1}, {2*_cell_ind})') -- DEBUG
                continue 

            # don't go down
            _line_state[_v] = _line_state[_v].difference({_cell_ind}) # essentially pop from set
            _line_state.append({_cell_ind})
            _set_state[_cell_ind] = len(_line_state) - 1

            continue

        continue 

    # manually work with last row to merge everything not merged
    for _cind in range(_q - 1):
        if _set_state[_cind] == _set_state[_cind + 1]:
            continue 

        _line_state[_set_state[_cind + 1]] = {}
        _c = _set_state[_cind + 1]

        # write to main maze
        _maze[2*(_q - 1)][2*_cind + 1] = path_symbol


        for _ind in range(_q):
            # yes yes bad programming but i also needa mutate values its whatever
            if _set_state[_ind] == _c:
                _set_state[_ind] = _set_state[_cind]
                continue 



    return _maze



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
# print(make_maze_str(generate_eller_maze(21), double=True))