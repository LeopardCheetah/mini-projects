# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Iterative_randomized_Kruskal's_algorithm_(with_sets)

import random

# strat: generate trees and something

# switch all instances of target with replacement
def switch(ls, target, replacement):
    if not isinstance(ls, list):
        return "bruh"
    
    if not isinstance(ls[0], list):
        return "Operation 'switch' not supported on 1d lists."
    
    new_list = []
    
    # assume ls is a 2d list
    for _l in ls:
        _ls = []
        for _item in _l:
            if _item == target:
                _ls.append(replacement)
                continue 

            _ls.append(_item)
        
        new_list.append(_ls)
    
    return new_list



def generate_kruskal_maze(n, path_symbol=" ", wall_symbol="x"):
    # generate maze
    
    if not isinstance(n, int):
        return f"Sidelength {n} not an integer :("
    
    if n < 1:
        return f"Sidelength {n} must not be less than 1."
    
    if n == 1:
        return [[path_symbol]]
    
    if n > 1023:
        # average hardcoded constant behavior moment
        return f"Side lengths longer than 1023 ({n} > 1023) are not supported yet :/"
    
    
    _n = ((n >> 1) << 1) + 1 

    # generate .#.
    #          ###
    #          .#. (etc.)
    _maze = [[path_symbol if _x % 2 == _y % 2 == 0 else wall_symbol for _x in range(_n)] for _y in range(_n)]

    _walls = [] 
    _lookup_table = [[1024 for __ in range(_n)] for _ in range(_n)] 
    # who's connected to who?
    _c = 0


    for _y in range(_n):
        for _x in range(_n):
            if _y % 2 == 0 and _x % 2 == 0:
                _lookup_table[_y][_x] = _c
                _c += 1
                continue 
            
            if _y % 2 and _x % 2:
                continue # this is a 1,1 square and will always be a wall

            _walls.append((_y, _x))
            continue 
        
    random.shuffle(_walls)

    while len(_walls) > 0:
        _wp = _walls.pop() # wp = wall pair

        _xdir, _ydir = _wp[1] % 2, _wp[0] % 2
        
        # if _xdir, move in the x-direction
        # /#/
        # ?x?
        # /#/
        
        # print(_wp[0], _wp[1], _ydir, _xdir) -- DEBUG

        if _lookup_table[_wp[0] - _ydir][_wp[1] - _xdir] == _lookup_table[_wp[0] + _ydir][_wp[1] + _xdir]:
            # paths already joined, no need to make a loop
            continue 

        # remove wall, update lookup table
        _maze[_wp[0]][_wp[1]] = path_symbol

        _lookup_table = switch(_lookup_table, _lookup_table[_wp[0] - _ydir][_wp[1] - _xdir], _lookup_table[_wp[0] + _ydir][_wp[1] + _xdir])
        continue 

    # i guess we done


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

# print(make_maze_str(generate_kruskal_maze(21), double=True))