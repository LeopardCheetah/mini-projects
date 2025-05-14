# See the Zine Paged Out #4 page 8,
# Generating Identicons from SHA-256 hashes

# idea: make a hexagon comb identificor sha thing

# 3-4-5-4-3 = 19 total combs (18 values -- middle will be filled)
# outside ring + inside ring + center = 3 colors = 9 bytes

# -> 27 bytes (sha 256 is 32 bytes)


#--------------------------------------------------------------

import hashlib
import os 
import random

hasher = hashlib.sha3_256()
name = input("Enter a username:\n> ")
salt = random.random()
new_name = name + str(salt)[2:7]
hasher.update(new_name.encode('utf-8'))
hash = hasher.hexdigest()



def generate_hexagonal_svg(ls):
    # ls, needs to have length 19 
    # -1 if there should be no coloring, hex color string (lowercase) if it does exist

    # ordering: go from outside in
    #  2  3
    # 7  1 4
    #  6  5, etc.


    # Create SVG string - more examples here https://www.w3schools.com/graphics/svg_intro.asp
    # apparently we need this xmlns clause so we'll keep it for now
    svg_s = ''
    svg_s += '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="500">\n'
    svg_s += '<rect width="500" height="500" style="fill:rgb(240, 240, 240)" />\n'


    # border
    # idk maybe finish this later cuz the border is hard
    # svg_s += '<polygon points="###" style="fill:rgb(240, 240, 240);stroke:black;stroke-width:2" />'



    """
    <polygon points="225,33.5 275,33.5 300,76.8 275,120.1, 225,120.1 200,76.8" style="fill:#000000" /
    </svg>
    """
    _xoff = 50
    _yoff = 33.5
    _xstep = 75 # center
    _ystep = 43.3

    # relative to the center (x,y) the points are (x-25, y-43.3), (x+25, y-43.3), (x+50, y), (x+25, y+43.3), (x-25, y+43.3), (x-50,y)
    _centers = [(2, 5)] + [(1, 4), (2, 3), (3, 4), (3, 6), (2, 7), (1, 6)] + [(0, 3), (1, 2), (2, 1), (3, 2), (4, 3), (4, 5), (4, 7), (3, 8), (2, 9), (1, 8), (0, 7), (0, 5)]

    _c = 0
    for _xy in _centers:
        _x = _xy[0]*_xstep + _xoff + 50 # another offset
        _y = _xy[1]*_ystep + _yoff 

        if not(ls[_c] == -1 or ls[_c] == '-1'):
            svg_s += f'<polygon points="{_x - 25},{_y - 43.3} {_x + 25},{_y - 43.3} {_x + 50},{_y} {_x + 25},{_y + 43.3} {_x - 25},{_y + 43.3} {_x - 50},{_y}" style="fill:#{ls[_c]}" />\n'
    
        _c += 1

    return svg_s




center_color = hash[-6:] # 3 bytes
l1_color = hash[-12:-6]
l2_color = hash[-18:-12]


hash_list = [center_color]
for _i in range(18):
    # 25 bytes, check odd/even
    if hash[_i*2] in ['0', '2', '4', '6', '8', 'a', 'c', 'e']:
        hash_list.append(-1)
        continue 


    if _i < 6:
        hash_list.append(l1_color)
        continue

    hash_list.append(l2_color) 


folder = r'.\hexagonal_svgs' 
if not os.path.exists(folder):
    os.makedirs(folder)

with open('.\\hexagonal_svgs\\' + f'{name}.svg', 'w') as f:
    f.write(generate_hexagonal_svg(hash_list))
    pass

print('done!')
    