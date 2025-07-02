import random


# generate a n by n maze starting from top left to bottom right
# e.g.
# ......
# xx.xxx
# ...x..
# .xxx.x
# .x...x
# ...x..
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
    while _path_squares[-1] != (n, n):

        # choose a square from a list of squares you can go to
        # left/right/up/down
        _tent_sqs = [(_path_squares[-1][0] - 1, _path_squares[-1][1]), (_path_squares[-1][0] + 1, _path_squares[-1][1]), (_path_squares[-1][0], _path_squares[-1][1] - 1), (_path_squares[-1][0], _path_squares[-1][1] + 1)]

        # make checks to make sure squares are valid
        # while loop since for loop might get funky with list editing
        _c = 3
        while _c > -1:
            if _tent_sqs[_c] in _forbidden_path_squares:
                _tent_sqs.pop(_c)
                _c -= 1
                continue 

            # out of bounds
            if _tent_sqs[_c][0] > n or _tent_sqs[_c][0] < 1 or _tent_sqs[_c][1] > n or _tent_sqs[_c][1] < 1:
                _tent_sqs.pop(_c)
                _c -= 1
                continue 
            
            _c -= 1
            continue 

        if len(_tent_sqs) < 1: # aka 0
            print("grid path making failed :(")
            break
        

        _final_sq = random.choice(_tent_sqs)


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

print()
print(pr_grid(generate(20)))