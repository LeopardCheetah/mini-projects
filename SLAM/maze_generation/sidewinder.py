# https://weblog.jamisbuck.org/2011/2/3/maze-generation-sidewinder-algorithm
# if eller's and binary trees combined

import random

def generate_sidewinder_maze(n, path_symbol=' ', wall_symbol='x'):
    if not isinstance(n, int):
        return f"Sidelength {n} not an integer :("
    
    if n < 1:
        return f"Sidelength {n} must not be less than 1."
    
    if n == 1:
        return [[path_symbol]]
    
    _n = (n // 2)*2 + 1
    _q = (n // 2) + 1

    _maze = []

    for _r in range(_n):
        if _r % 2:
            # fill with walls -- it's an odd row
            _maze.append([wall_symbol for _ in range(_n)])
            continue 

        if _r == 0:
            _maze.append([path_symbol for _ in range(_n)])
            continue 

        _rls = []
        _run = 0
        # higher temp = longer rows => more corridor-like structures
        _carve_temp = 0.6
        for _p in range(_q - 1):
            _rls.append(path_symbol)
            # roll a dice 
            # continue eastword; make corridor
            if random.random() < _carve_temp:
                _run += 1
                _rls.append(path_symbol)
                continue 
            
            _rls.append(wall_symbol)
            # else, look for a way to move up
            _rand = random.randint(0, _run)
            # burrow a path _r squares back

            _maze[-1][2*(_p - _rand)] = path_symbol

            _run = 0
            continue 

       
        # do 1 last roll iteration
        _rls.append(path_symbol)
        _maze.append(_rls)
        _rand = random.randint(0, _run)
        _maze[-2][2*(_q - 1 - _rand)] = path_symbol
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

print(make_maze_str(generate_sidewinder_maze(21), double=True))