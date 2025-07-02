import random
import time

# generate a n by n maze starting from top left to bottom right
# e.g.
# ......
# xx.xxx
# ...x..
# .xxx.x
# .x...x
# ...x..

RED = '\033[0;31m'
WHITE = '\033[0;37m'

# n: size of grid
# forbidden: squares forbidden to go to
# start: pair for start square
# end: end destination goal
def trapped(n, forbidden, start, end=None):
    # i could use slam here but i'll use field flow
    # fun fact i've never coded field flow
    _end = (n, n) if end is None else end
    _flow_blocks = [start]
    _new_flow = []
    _covered = [] + forbidden
    
    k = 0

    while len(_flow_blocks) > 0:
        k += 1
        time.sleep(0.1)
        # progress forward one tick in time and 'flow'
        # update places flowed to
        _flow_blocks = list(set(_flow_blocks))
        _new_flow = list(set(_new_flow))
        _covered = list(set(_covered))
        for _k in _flow_blocks:
            _covered.append(_k)
            # flow!
            _new_flow.append((_k[0] - 1, _k[1]))
            _new_flow.append((_k[0] + 1, _k[1]))
            _new_flow.append((_k[0], _k[1] - 1))
            _new_flow.append((_k[0], _k[1] + 1))
            continue 

        _c = len(_new_flow) - 1
        while _c > -1:
            if _new_flow[_c] in _covered:
                _new_flow.pop(_c)
                _c -= 1
                continue 
            
            if _new_flow[_c][0] > n or _new_flow[_c][0] < 1 or _new_flow[_c][1] > n or _new_flow[_c][1] < 1:
                _new_flow.pop(_c)
                _c -= 1
                continue 

            _c -= 1
            continue 


        _flow_blocks = _new_flow
        _new_flow = []
        if _end in _covered or _end in _new_flow:
            return False
        
        continue 
    
    if _end in _covered:
        return False # not trapped
    
    return True
            

    
def erase_prev_line():
    print('\033[1A\033[0K', end='') # erase previous line 
    return



def generate(n):
    if n < 5:
        return 'Grid size too small :('
    
    grid = [['.' for __ in range(n)] for _ in range(n)]

    # find path to navigate towards
    _path_squares = [(1, 1)]
    _forbidden_path_squares = [] # don't go here
    # ...
    # ..x <-- this is at (3, 2)
    # ...

    print('path length: 0')
    while _path_squares[-1] != (n, n):

        if _path_squares[-1] == (n - 1, n) or _path_squares[-1] == (n, n - 1):
            # end immediately else program may crash
            _path_squares.append((n, n))
            continue


        # interactive so people don't get bored
        erase_prev_line()
        print(f'path length: {len(_path_squares)}/{int(2.7*n)} (expected)') # 2.5 is arbitrary but makes it seem definite

        # choose a square from a list of squares you can go to
        # left/right/up/down
        _tent_sqs = [(_path_squares[-1][0] - 1, _path_squares[-1][1]), (_path_squares[-1][0] + 1, _path_squares[-1][1]), (_path_squares[-1][0], _path_squares[-1][1] - 1), (_path_squares[-1][0], _path_squares[-1][1] + 1)]

        # make checks to make sure squares are valid
        # while loop since for loop might get funky with list editing

        _c = 4 - 1
        _new_tent_sqs = []
        while _c > -1:
            if _tent_sqs[_c] in _forbidden_path_squares:
                _c -= 1
                continue 
            
            # out of bounds
            if _tent_sqs[_c][0] > n or _tent_sqs[_c][0] < 1 or _tent_sqs[_c][1] > n or _tent_sqs[_c][1] < 1:
                _tent_sqs.pop(_c) # pop so the forbidden squares list is accurate
                _c -= 1
                continue 

            # mock and see if it's possible
            # second check to expedite since maze shouldn't be able to get stuck anyways
            if len(_path_squares) < 8 or (not trapped(n, _forbidden_path_squares + _tent_sqs + [_path_squares[-1]], _tent_sqs[_c])): 
                # we are good to go
                _new_tent_sqs.append(_tent_sqs[_c])
                _c -= 1
                continue 

            # got trapped; don't add to new list
            _c -= 1
            continue 

        if len(_new_tent_sqs) < 1:
            # print('grid making fucked up')
            # if it fails, fail spectacularly.
            print('ERROR!!!')
            print('path_squares:', _path_squares)
            print('forbidden squares:', _forbidden_path_squares)
            print('tentative squares:', _tent_sqs)
            print(pr_grid(grid))
            print()
            return "grid path making failed :("
        
        _final_sq = random.choice(_new_tent_sqs)


        # update forbidden squares
        _forbidden_path_squares.append(_path_squares[-1])
        for _sq in _tent_sqs:
            _forbidden_path_squares.append(_sq)

        _path_squares.append(_final_sq)
        continue 


    # plot path on grid
    for _pair in _path_squares:
        grid[_pair[0] - 1][_pair[1] - 1] = 'o'
        continue         

    for _pair in _forbidden_path_squares:
        if _pair in _path_squares:
            continue 
        grid[_pair[0] - 1][_pair[1] - 1] = RED + 'x' + WHITE
        continue 

    return grid


# print grid
def pr_grid(ls):
    if isinstance(ls, str):
        return ls # some error message
    
    s = ''
    _n = len(ls)
    for _i in range(_n):
        for _j in range(_n):
            s += ls[_i][_j] + ' '
        
        s += '\n'
    
    return s

def get_length(ls):
    if isinstance(ls, str):
        return 'N/A'
    
    _c = 0
    for _i in range(len(ls)):
        for _j in range(len(ls)):
            if ls[_i][_j] == 'o':
                _c += 1
    
    return _c

print(WHITE)
gr = generate(9)
erase_prev_line()
print(f'Final path length: {get_length(gr)}')
print()
print(pr_grid(gr))