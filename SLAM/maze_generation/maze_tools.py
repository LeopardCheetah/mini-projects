# copied, please ONLY use this when doing things
# returns a string given a m by m maze
def format_maze(m, border=True, double=True):

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