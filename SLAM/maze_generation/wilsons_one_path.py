# me when the unbiased maze
# https://en.wikipedia.org/wiki/Maze_generation_algorithm#Wilson's_algorithm
# note: Wilson's is slow


# note: i somehow screwed up the algorithm to the point where only one path is generated
# im not sure how this happened but yeah since it did ill leave it here its cool
# essentially this is now a space filling curve

import random



def generate_wilsons_maze(n, path_symbol=" ", wall_symbol="x"):
    # generate maze
    
    if not isinstance(n, int):
        return f"Sidelength {n} not an integer :("
    
    if n < 1:
        return f"Sidelength {n} must not be less than 1."
    
    if n == 1:
        return [[path_symbol]]
    
    if n > 100:
        return f"Side lengths longer than 100 ({n} > 100) are most likely too slow for practical applications. Use another maze algorithm."
    
    
    _n = ((n >> 1) << 1) + 1 

    # generate .#.
    #          ###
    #          .#. (etc.)
    _maze = [[path_symbol if _x % 2 == _y % 2 == 0 else wall_symbol for _x in range(_n)] for _y in range(_n)]

    _q = _n // 2 + 1
    _been_visited = [0 for _ in range(_q**2)]


    # current square
    _cury = None
    _curx = None
    _last_dir = None

    # 0 --> not visited
    # 1 --> visited on this current randomized journey
    # 2 --> is engrained in the path
    _been_visited[random.randint(1, _q**2 - 1)] = 2

    while 0 in _been_visited:
        # just a choose a random direction from current spot 
        # that hasnt been visited and step there
        # if inevitably we hit a loop just backtrack until we're back to the same spot

        if _cury is None:
            # find first cell, set that as cury, keep moving
            _cury, _curx = divmod(_been_visited.index(0), _q)
            _been_visited[_cury*_q + _curx] = 1
            continue 


        _directions = []

        if _cury > 0 and _been_visited[_q*(_cury - 1) + _curx] != 1 and _last_dir != 's':
            _directions.append('n')

        if _cury < _q - 1 and _been_visited[_q*(_cury + 1) + _curx] != 1 and _last_dir != 'n':
            _directions.append('s')

        if _curx > 0 and _been_visited[_q*_cury + _curx - 1] != 1 and _last_dir != 'e':
            _directions.append('w')

        if _curx < _q - 1 and _been_visited[_q*_cury + _curx + 1] != 1 and _last_dir != 'w':
            _directions.append('e')

        if len(_directions) == 0:
            # backtrack and cut the loop out

            # this should NEVER happen
            if _last_dir is None:
                raise Exception("what the heck why can't i go anywhere")
            
            # we actually don't need last dir, we can just tell by the walls where the path was
            # whatever
            # find target
            if _cury > 0 and _last_dir != 's':
                _directions.append('n')
            
            if _cury < _q - 1 and _last_dir != 'n':
                _directions.append('s')
            
            if _curx > 0 and _last_dir != 'e':
                _directions.append('w')
            
            if _curx < _q - 1 and _last_dir != 'w':
                _directions.append('e')
            
            if len(_directions) == 0:
                # what the hell
                # why are we here
                raise Exception("this code has failed spectaculraly. please contact tech support")
            
            _target_dir = random.choice(_directions)
            _target = _cury*_q + _curx 
            if _target_dir == 'n':
                _target -= _q 
            elif _target_dir == 's':
                _target += _q
            elif _target_dir == 'w':
                _target -= 1
            elif _target_dir == 'e':
                _target += 1
            
            # validate 
            # print(_target, _directions)
            if _been_visited[_target] != 1:
                raise Exception("this code sucks")
            
            # FINALLY start backtracking omg
            while _target != _curx + _q*_cury:
                # essentially, flip bits and shit
                _been_visited[_curx + _q*_cury] = 0

                if _cury > 0 and _maze[2*_cury - 1][2*_curx] == path_symbol:
                    # backtrack north
                    _maze[2*_cury - 1][2*_curx] = wall_symbol
                    _cury -= 1
                    continue 

                if _cury < _q - 1 and _maze[2*_cury + 1][2*_curx] == path_symbol:
                    _maze[2*_cury + 1][2*_curx] = wall_symbol
                    _cury += 1
                    continue 

                if _curx > 0 and _maze[2*_cury][2*_curx - 1] == path_symbol:
                    _maze[2*_cury][2*_curx - 1] = wall_symbol
                    _curx -= 1
                    continue 

                if _q - 1 > _curx and _maze[2*_cury][2*_curx + 1] == path_symbol:
                    _maze[2*_cury][2*_curx + 1] = wall_symbol
                    _curx += 1
                    continue 
                
                # we should NEVER be here
                raise Exception("You shouldn't be here.")
            # restore last_dir state in case our code blows up because we don't
            
            if _cury > 0 and _maze[2*_cury - 1][2*_curx] == path_symbol:
                _last_dir = 's'
                continue 

            if _cury < _q - 1 and _maze[2*_cury + 1][2*_curx] == path_symbol:
                _last_dir = 'n'
                continue 

            if _curx > 0 and _maze[2*_cury][2*_curx - 1] == path_symbol:
                _last_dir = 'e'
                continue 

            if _q - 1 > _curx and _maze[2*_cury][2*_curx + 1] == path_symbol:
                _last_dir = 'w'
                continue 

            # too lazy to throw an exception 
            continue 


        # just choose a random direction, head that way, and keep on winning
        _dir = random.choice(_directions)
        _last_dir = _dir

        _dy = -1 if _dir == 'n' else 1 if _dir == 's' else 0
        _dx = -1 if _dir == 'w' else 1 if _dir == 'e' else 0

        _maze[2*_cury + _dy][2*_curx + _dx] = path_symbol
        _been_visited[_q*(_cury + _dy) + _curx + _dx] = 1
        _cury += _dy
        _curx += _dx
        
        if _been_visited[_q*_cury + _curx] != 2:
            continue 
        
        # we've made it back to the main path; solidify everything
        for _i, _v in enumerate(_been_visited):
            if _v == 1:
                _been_visited[_i] = 2
        
        _cury = None
        _curx = None
        _last_dir = None
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

# print(make_maze_str(generate_wilsons_maze(15), double=True))