# goal: get the chess bot going

class color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    WARNING = '\033[93m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDCOLOR = '\033[0m'

    # these not used
    BOLD = '\033[1m'
    GRAY = '\033[2m'
    UNDERLINE = '\033[4m'


class Board:
    board = [["." for a in range(8)] for b in range(8)] # generic

    white_piece_color = color.BLUE # white's pieces are blue
    black_piece_color = color.FAIL # black's pieces are red


    def __init__(self):
        return 


    def convert_coord_to_index(self, square):
        # convert a chess coordinate (e.g. f4) into a list index (e.g. [4][5])
        # input: square (string) from a1 -- h8

        sq_rank = int(square[1])
        sq_file = square[0]

        return (8 - sq_rank), int(ord(sq_file) - ord('a'))

    

    def printboard(self):
        # print the chess board
        print()
        print('  +-----------------+')
        c = 8
        for row in self.board:
            print(c, '|', end=' ')
            c -= 1
            for item in row:
                print(item, end=' ')
            
            print('|')
        
        print('  +-----------------+')
        print('    a b c d e f g h')
        return



    def printboard_blackpov(self):
        # print from black's pov
        print()
        print('  +-----------------+')
        c = 1
        for row_ind in range(8):
            print(c, '|', end=' ')
            c += 1
            for col_ind in range(8):
                print(self.board[7 - row_ind][7 - col_ind], end=' ')
            
            print('|')
        
        print('  +-----------------+')
        print('    h g f e d c b a')
        return




    def reset_board(self):
        # reset board to starting position of normal chess

        # add pieces
        starting_ls = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        pointer = 'a'
        for piece in starting_ls:
            self.change_square(pointer+'1', f'{self.white_piece_color}' + piece + f'{color.ENDCOLOR}')
            self.change_square(pointer+'8', f'{self.black_piece_color}' + piece + f'{color.ENDCOLOR}')
            pointer = chr(ord(pointer) + 1) # increment pointer
        
        pointer = 'a'
        # add pawns
        for _ in range(8):
            self.change_square(pointer+'2', f'{self.white_piece_color}P{color.ENDCOLOR}')
            self.change_square(pointer+'7', f'{self.black_piece_color}P{color.ENDCOLOR}')
            pointer = chr(ord(pointer) + 1) # increment pointer
        
        return #!!


    def clear_board(self):
        self.board = [["." for a in range(8)] for b in range(8)] # back to dots and nothingness
        return 




    def move_piece(self, starting_sq, final_sq):
        # using chess notation, move a piece
        # physically swap a piece from starting square to final square
        
        start_row, start_col = self.convert_coord_to_index(starting_sq)
        end_row, end_col = self.convert_coord_to_index(final_sq)

        self.board[end_row][end_col], self.board[start_row][start_col] = self.board[start_row][start_col], "."
        return 

    
    def change_square(self, final_square, piece_after):
        # change square from what it is to piece_after
        # square is a square in chess notation (like c3)
        # (useful in pawn promotions or in crazyhouse or something)
        
        end_row, end_col = self.convert_coord_to_index(final_square)
        self.board[end_row][end_col] = piece_after
        return
    

    def set_piece_tosq(self, square, piece_type, piece_color):
        # square --> a1 or whatever
        # piece type -- N/B/R/Q/K/P?
        # piece color -- w/b

        # we assume all inputs are "good"

        color_code = self.white_piece_color if piece_color == 'w' else self.black_piece_color # blue -- white, green -- black

        self.change_square(square, f'{color_code}' + piece_type + f'{color.ENDCOLOR}')
        return 


    def send_move(self, start_sq, end_sq):
        # use this command to submit a move
        self.move_piece(start_sq, end_sq)
        return
    
    
    def get_board(self):
        return self.board


    def get_piece_color_atsq(self, square):
        # note if the piece at square x is black or white or none.
        row, col = self.convert_coord_to_index(square)
        if self.board[row][col] == ".":
            return -1
    

        return 'w' if self.board[row][col][3] == self.white_piece_color[3] else 'b' # some interesting string stuff going on here 
        # ehrm this needs to be fixed.
    

    def get_piece_type_atsq(self, square):
        row, col = self.convert_coord_to_index(square)
        if self.board[row][col] == ".":
            return -1
        
        return self.board[row][col][5]



    # sample text


# sample commands
# board = Board()
# board.send_move('e2', 'e4')
# board.send_move('c7', 'c5')
# board.send_move('g1', 'f3')