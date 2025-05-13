# See the Zine Paged Out #4 page 8,
# Generating Identicons from SHA-256 hashes
# this file will try to make some sort of clone on the github identificons
# --------------------------------------------------------------

import hashlib
import os 





hasher = hashlib.sha3_256()
name = input("Enter a username:\n> ")
salt = 'atgithub'
new_name = name + salt
hasher.update(new_name.encode('utf-8'))
hash = hasher.hexdigest()

# 32 bytes
# 25 bytes --> github identicon? (w/o replacement) --> real github replacement has some measure of symmetry and only really uses 15 "bytes" but whatever
# 3 bytes --> color
# 4 byte --> checker?/NA


rgb_color = hash[-14:-8] # 3 bytes

hash_list = []
for _i in range(25):
    # 25 bytes, check odd/even
    if hash[_i*2] in ['0', '2', '4', '6', '8', 'a', 'c', 'e']:
        hash_list.append(-1)
        continue 

    hash_list.append(rgb_color) 



def generate_svg_from_list(ls):
    # ls, needs to have length 25 
    # -1 if there should be no coloring
    # hex color string (lowercase) if it does exist

    # e.g.: ls = [-1, -1, '000000', -1, -1, '000000', -1, '000000', -1] would make:
    # [ ] [ ] [x]
    # [ ] [ ] [x]
    # [ ] [x] [ ] 
    # where [x] is a black square, [ ] is an empty square

        
    # schema:
    # github identicons are 5x5 with color + odd/even pixel counts
    # in a 600x600 rectangle, the inner 500x500 is for the 25 squares and theres a 50 pixel width as a border band


    svg_s = ''
    svg_s += '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600">\n'
    svg_s += '<rect width="600" height="600" style="fill:rgb(240, 240, 240)" />\n' 

    for _y in range(5):
        for _x in range(5):
            if ls[5*_y + _x] == -1 or ls[5*_y + _x] == '-1':
                continue # empty square

            svg_s += f'<rect width="100" height="100" x="{50 + _x*100}" y="{50 + _y*100}" style="fill:#{ls[5*_y + _x]}" />\n'


    return svg_s



folder = r'.\github_generated_svgs' 
if not os.path.exists(folder):
    os.makedirs(folder)

with open('.\\github_generated_svgs\\' + f'{name}.svg', 'w') as f:
    f.write(generate_svg_from_list(hash_list))
    pass

print('done!')
    