# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Fractal_Tessellation_algorithm

import random

# this function has been tested and verified through monte carlo :)
# f: assuming x >= 1, find ceil(log_2(x))
def manual_log2(x):
    if x == 1:
        return 0
    
    # don't even need stupid bit shifts lol
    # since 64 -> 7 but 2^6 = 64, subtract 1
    return len(bin(x - 1)) - 2




# n by n grid of maze
# in reality if n != 2^k - 1 then i'll ignore it lmao
def generate_fractal_maze(n, path_symbol=".", wall_symbol='#'):
    if not isinstance(n, int):
        return f"Your maze length, {n}, is not an integer!"

    if n < 1:
        return f"Mazes with side lengths of {n} cannot exist!"
    
    if len(path_symbol) != 1 or len(wall_symbol) != 1:
        return f"Cannot make maze with symbol(s) '{path_symbol}'/'{wall_symbol}' as they are more than one character long."
    
    if n == 1:
        return [[path_symbol]]
    
    if n == 2:
        return random.choice([[[path_symbol, wall_symbol], [path_symbol, path_symbol]], [[path_symbol, path_symbol], [path_symbol, wall_symbol]]])
    
    if n > 1000:
        return f"We do not support mazes that are more than 1000x1000. Your maze is {n}x{n}."
    
    _iter_count = manual_log2(n)

    # maze generated is of size 2^k - 1 so if we need a 4x4 we give them 7x7 rather than 3x3
    if n == 1 << _iter_count:
        _iter_count += 1

    _maze = [[path_symbol for _ in range((1 << _iter_count) - 1)] for __ in range((1 << _iter_count) - 1)]
    
    for _i in range(1, _iter_count):
        # turn the 2**_i - 1 area into 2*2**_i - 1 via copying and stuff

        _q = (1 << _i) - 1 

        # add separator lines
        for _j in range(_q):
            _maze[_j][_q] = wall_symbol
            _maze[(2*_q) - _j][_q] = wall_symbol
            _maze[_q][_j] = wall_symbol
            _maze[_q][(2*_q) - _j] = wall_symbol
        
        # add middle :p
        _maze[_q][_q] = wall_symbol


        # copy top left to all corners of the board
        for _x in range (_q):
            for _y in range(_q):
                _maze[_q + 1 + _x][_y] = _maze[_x][_y] # top left to bottom left
                _maze[_x][_q + 1 + _y] = _maze[_x][_y]
                _maze[_q + 1 + _x][_q  + 1 + _y] = _maze[_x][_y]
                continue 
            continue 

        # randomly remove a wall (or three) (or not)
        _not_removable = random.randint(1, 4)
        
        _ns_c = 0
        for _ydx in range(_q):
            if _maze[_ydx][0] == path_symbol and _maze[_ydx][_q - 1] == path_symbol:
                _ns_c += 1
        
        _ew_c = 0
        for _xdx in range(_q):
            if _maze[0][_xdx] == path_symbol and _maze[_q - 1][_xdx] == path_symbol:
                _ew_c += 1


        if _not_removable != 1:
            # remove something from the north side
            # manually find index :/
            _idx = random.randint(1, _ns_c)
            for _ydx in range(_q):
                if _maze[_ydx][0] == path_symbol and _maze[_ydx][_q - 1] == path_symbol:
                    _idx -= 1
                
                if _idx == 0:
                    # remove specified block 
                    _maze[_ydx][_q] = path_symbol
                    break
        
        # ok do the same thing for the east side now
        if _not_removable != 2:
            # manually find index round 2
            _idx = random.randint(1, _ew_c)
            for _xdx in range(_q):
                if _maze[0][_xdx] == path_symbol and _maze[_q - 1][_xdx] == path_symbol:
                    _idx -= 1
                
                if _idx == 0:
                    # remove specified block 
                    _maze[_q][_q + 1 + _xdx] = path_symbol 
                    break

        # south
        if _not_removable != 3:
            _idx = random.randint(1, _ns_c)
            for _ydx in range(_q):
                if _maze[_ydx][0] == path_symbol and _maze[_ydx][_q - 1] == path_symbol:
                    _idx -= 1
                
                if _idx == 0:
                    _maze[_q + 1 + _ydx][_q] = path_symbol 
                    break
        
        # west
        if _not_removable != 4:
            _idx = random.randint(1, _ew_c)
            for _xdx in range(_q):
                if _maze[0][_xdx] == path_symbol and _maze[_q - 1][_xdx] == path_symbol:
                    _idx -= 1
                
                if _idx == 0:
                    _maze[_q][_xdx] = path_symbol 
                    break

        # end iter
        continue 

    return _maze 

# m is maze object aka n by n list of 1 char strings
def make_maze_str(m, border=True):
    s = ''
    if not border:
        for _i, _v in enumerate(m):
            for _j, _w in enumerate(_v):
                s += _w + ' '
            
            s += '\n'

        return s 
    
    s += '+' + '-'*len(m)*2 + '+' + '\n' # assuming square
    for _i, _v in enumerate(m):
        s += '|'

        for _j, _w in enumerate(_v):
            s += _w + ' '
        
        s += '|' + '\n'

    s += '+' + '-'*len(m)*2 + '+' + '\n' # end off
    return s

print()
print(make_maze_str(generate_fractal_maze(18, ' ', 'x')))