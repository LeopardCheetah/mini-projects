# binary tree mazes
# just go up and to the left apparently

# TODO -- needs some work in some trapped spaces 

import random

# n by n grid
# really n has to be odd but if it's even we'll give you a bigger grid :)
def generate_binary_tree_maze(n, path_symbol=" ", wall_symbol="x"):
    if not isinstance(n, int):
        return f"Cannot work with a non-integer value of n: {n}!"

    if n < 0:
        return f"Cannot generate a maze with {n} grid size!"
    
    if n < 1:
        return [[path_symbol]]
    
    _n = n # use this instead of n for everything
    if _n % 2 == 0:
        _n += 1

    # don't worry we get rid of this symbol later
    _empty_symbol = 'e' if path_symbol != 'e' and wall_symbol != 'e' else 'f' if path_symbol != 'f' and wall_symbol != 'f' else 'g'
    _maze = [[_empty_symbol for __ in range(_n)] for _ in range(_n)]

    # make main pathway
    for _i in range(_n):
        _maze[_i][0] = path_symbol
        _maze[0][_i] = path_symbol

    _c = 0 # tracks how many tiles we've covered and verified they're not 'e' or 'f' or 'g'
    # grid fill:
    # 8 7 6
    # 5 4 3
    # 2 1 0
    while _c < _n*_n:
        _check_tile = _maze[_n - 1 - (_c // n)][_n - 1 - (_c % n)]
        

        if _check_tile != _empty_symbol:
            _c += 1
            # cell is filled
            continue

        # assume everything to the bottom is filled
        # also wlog we don't start on one of the "bad" squares (e.g. 1/3/5/7 above) 

        _has_reached_another_path = False
        _move_up, _move_left = True, True 
        _on_bottom, _on_right = False, False 
        _y = _n - 1 - (_c // n)
        _x = _n - 1 - (_c % n) 

        _c += 1

        # make wall if we're on a bad square
        if (_y + _x) % 2:
            _maze[_y][_x] = wall_symbol
            continue 

        while not _has_reached_another_path:
            if _maze[_y][_x] == wall_symbol:
                return f"For some reason we are on a wall. See maze {_maze} at location {_y}, {_x}."
        
            if _maze[_y][_x] == path_symbol:
                _has_reached_another_path = True
                continue


            # check if moving up/to the right is allowed
            _move_up, _move_left = _maze[_y - 1][_x] != wall_symbol, _maze[_y][_x - 1] != wall_symbol
            _on_bottom, _on_right = _y == _n - 1, _x == _n - 1

            if not _move_left and not _move_up:
                # Houston we have a problem
                # TODO -- make sure this never happens aka when we get trapped
                # e.g.
                # +---------------------------+
                # |                           |
                # |  x  x x x x x x x x x x x |
                # |  x                        |             
                # |  x x x x x x x x x x x    |
                # |                  x e x    |
                # |  x x x x x x x   x x x    |
                # |              x       x    |
                # +---------------------------+

                # for now, just leave the whole empty for fun and move on
                # return f"Maze generation failed :( -- no path was found for maze {_maze} at point {_y}, {_x}"
                _maze[_y][_x] = path_symbol
                _has_reached_another_path = True
                continue 
            
            if _move_left and _move_up:
                _coinflip = random.randint(0, 1)

                # eliminate an option rq
                if _coinflip:
                    _move_left = False 
                else:
                    _move_up = False 


            if _move_up: # move up
                # block 3 squares to the immediate left, top left, top right
                # conditionally block either the bottom or the left depending on where we came from 
                _maze[_y][_x] = path_symbol
                _maze[_y - 1][_x] = path_symbol
                _maze[_y][_x - 1] = wall_symbol
                _maze[_y - 1][_x - 1] = wall_symbol
                if not _on_right:
                    _maze[_y - 1][_x + 1] = wall_symbol

                if not _on_bottom and _maze[_y + 1][_x] == path_symbol and not _on_right:
                    # came from bottom, block right
                    _maze[_y][_x + 1] = wall_symbol
                
                if not _on_right and _maze[_y][_x + 1] == path_symbol and not _on_bottom: # block bottom ROW
                    _maze[_y + 1][_x] = wall_symbol
                    _maze[_y + 1][_x - 1] = wall_symbol
                    _maze[_y + 1][_x + 1] = wall_symbol
                
                _y -= 2
                continue 

            # move left
            # block bottom left, top left, top, and conditionally bottom/right
            _maze[_y][_x] = path_symbol
            _maze[_y][_x - 1] = path_symbol
            _maze[_y - 1][_x] = wall_symbol
            _maze[_y - 1][_x - 1] = wall_symbol
            if not _on_bottom:
                _maze[_y + 1][_x - 1] = wall_symbol

            if not _on_bottom and _maze[_y + 1][_x] == path_symbol and not _on_right: # came from bottom, block right column
                _maze[_y][_x + 1] = wall_symbol
                _maze[_y - 1][_x + 1] = wall_symbol
                _maze[_y + 1][_x + 1] = wall_symbol
            
            if not _on_right and _maze[_y][_x + 1] == path_symbol and not _on_bottom: # came from right, block bottom
                _maze[_y + 1][_x] = wall_symbol
            
            _x -= 2
            continue # end while loop

        # idk i feel like the while loop did everything
        continue 

    return _maze








# m is maze object aka n by n list of 1 char strings
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

print()
print(make_maze_str(generate_binary_tree_maze(21, ' ', 'x')))