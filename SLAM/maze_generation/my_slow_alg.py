# this file is too slow

import random
import time


# color constants
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



# generate a n by n path starting from top left to bottom right
# e.g.
# ......
# xx.xxx
# ...x..
# .xxx.x
# .x...x
# ...x..
def generate_path(n, suppress=False):
    if n < 5:
        return 'Grid size too small :('
    
    if n > 20:
        return "This will take too long :c"
    
    grid = [['.' for __ in range(n)] for _ in range(n)]

    # find path to navigate towards
    _path_squares = [(1, 1)]
    _forbidden_path_squares = [] # don't go here
    # ...
    # ..x <-- this is at (3, 2)
    # ...

    if not suppress:
        print('path length: 0')
        pass 

    while _path_squares[-1] != (n, n):

        if _path_squares[-1] == (n - 1, n) or _path_squares[-1] == (n, n - 1):
            # end immediately else program may crash
            _path_squares.append((n, n))
            continue


        # interactive so people don't get bored
        if not suppress:
            erase_prev_line()
            print(f'path length: {len(_path_squares)}/{int(4.2*n)} (expected)')
            # 7/14 update -- i benchmarked my code for sizes 5-15 (n=2) and idfk this shit is downwards for a quadratic?
            # updated 3.6 -> 4.2 cuz i guess that fits better for limited sample size

        # long tangent:
        # https://math.stackexchange.com/questions/103142/expected-value-of-random-walk
        # -> l ~ sqrt(N)*gamma(1.5) ~ 0.886227*sqrt(N)
        # -> so N = (l/0.886227)^2
        # oops nvm
        # ill just keep arbitrary 3.6


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
            print(pr_path(grid))
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
        grid[_pair[0] - 1][_pair[1] - 1] = 'x'
        continue 

    return grid

# n by n maze
# t is a temp (0, 1) --> 1 meaning all 'squares' are open, 0 meaning all closed

def generate_maze(n, temp):
    _gr = generate_path(n)
    # turn all "xs" back into dots

    # percolation time
    # TODO -- make this actually near temp instead of just quasi-random
    # TODO -- fix maze generation software to generate quickly
    r = 0.00
    for _i in range(n):
        for _j in range(n):
            if _gr[_i][_j] == 'o':
                _gr[_i][_j] == '.'
                continue 

            r = random.random()
            if r > temp:
                _gr[_i][_j] = 'x'
            else:
                _gr[_i][_j] = '.'
    
    return _gr
    




# print path (SPECIFICALLY PATH)
def pr_path(ls):
    if isinstance(ls, str):
        return ls # some error message
    
    s = ''
    _n = len(ls)
    for _i in range(_n):
        for _j in range(_n):
            if ls[_i][_j] == 'x':
                s += RED + 'x' + WHITE + ' '
                continue 

            s += ls[_i][_j] + ' '
        
        s += '\n'
    
    return s


def pr_maze(ls):
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

# print(WHITE)
# gr = generate_path(15)
# erase_prev_line()
# print(f'Final path length: {get_length(gr)}')
# print()
# print(pr_path(gr))


'''
# strictly for benchmarking
# NOTE: this takes a while
end_time = -1.0
current_time = -1.0
maze_gen_times = []
start_time = last_time = time.perf_counter()

for _ in range(5, 16): # 5, 6, ..., 15
    print()
    gr = generate_maze(_, 0.6)
    current_time = time.perf_counter()
    print(f'Time taken to generate first {_}x{_} grid: {round(current_time - last_time, 3)}s')
    print(f'Cumulative time taken: {round(current_time - start_time, 3)}s')
    print()
    maze_gen_times.append(current_time - last_time)
    last_time = current_time

    gr2 = generate_maze(_, 0.6)
    current_time = time.perf_counter()
    print(f'Time taken to generate second {_}x{_} grid: {round(current_time - last_time, 3)}s')
    print(f'Cumulative time taken: {round(current_time - start_time, 3)}s')
    print()
    maze_gen_times.append(current_time - last_time)
    last_time = current_time

end_time = time.perf_counter()
print()
print(f'TOTAL TIME TAKEN: {round(end_time - start_time, 3)}s or {(end_time - start_time) // 60}m {round((end_time - start_time) - ((end_time-start_time)//60)*60, 3)}s')

print()
print('-----------------')
print('Times taken to generate first maze/second maze/average time:')
for i in range(5, 16):
    # 5 -> (0, 1)
    # 6 -> (2, 3)
    print(f'{round(maze_gen_times[2*(i - 5)], 3)}s {round(maze_gen_times[2*(i - 5) + 1], 3)}s {round((maze_gen_times[2*(i - 5)] + maze_gen_times[2*(i - 5) + 1])/2, 3)}s')


print('benchmarking complete!')
'''