class ChessGame:
    # game class has a board and other features

    game_board = None
    white_king_check = False # is white king in check?
    black_king_check = False 
    white_turn = True # is it white's move?
    move_number = 1

    last_pawn_move = 'z0' # used for en passant, z0 is a null value -- this is where the en passant square IS (e.g. c7 --> c5 would make this c6)
    

    # ok we lowkey not using these 4 since I gave up on castling
    white_kingside_castling = True # true if white can still castle kingside at any given moment
    white_queenside_castling = True
    black_kingside_castling = True
    black_queenside_castling = True 

    white_piece_locations = []
    black_piece_locations = []

    half_move_clock = 0 # yeah idk tinker with this later -- see https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation

    def __init__(self):
        import board
        self.game_board = board.Board()

        self.game_board.reset_board()
        self.white_turn = True
        self.white_piece_locations = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'] + ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
        self.black_piece_locations = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8'] + ['a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7']
    
    
    def is_white_king_in_check(self, white_piece_positions=None):
        white_piece_location_list = []
        if white_piece_positions is None:
            white_piece_location_list = self.white_piece_locations
        else:
            white_piece_location_list = white_piece_positions
        # check's if in current position, white king is in check
        # returns true/false

        
        # basically, from position, see if white king is in check
        # check all legal moves of all black pieces!

        white_king_location = ""
        

        for piece_location in white_piece_location_list:
            if self.game_board.get_piece_type_atsq(piece_location) == 'K':
                white_king_location = piece_location
                break
        
        white_king_file = white_king_location[0]
        white_king_rank = white_king_location[1]

        # check for 8 knights, then each direction infinitely
        # check for knights
        for pair in [(-1, 2), (-1, -2), (1, 2), (1, -2), (2, -1), (2, 1), (-2, 1), (-2, -1)]:

            try:
                black_kn_file = chr(ord(white_king_file) + pair[0]) 
                black_kn_rank = chr(ord(white_king_rank) + pair[1])
                if self.game_board.get_piece_type_atsq(black_kn_file + black_kn_rank) == 'N' and self.game_board.get_piece_color_atsq(black_kn_file + black_kn_rank) == 'b':
                    return True # yeah there's a knight
            except:
                pass # lmao don't worry about this -- if it errors then it's out of bounds and we're fine
            

        # check in the other 8 directions infinitely
        # since this is where the king can move, kings can potentially touch here so we have to check that
        
        # check king's top right diagonal

        num_rank = int(white_king_rank)
        num_file = 8 - (ord('h') - ord(white_king_file))

        king_top_right_count = min(8 - num_rank, 8 - num_file)

        for ind in range(1, king_top_right_count + 1):
            piece_color_at_sq = self.game_board.get_piece_color_atsq(chr(ord(white_king_file) + ind) + str(num_rank + ind))

            if piece_color_at_sq == 'w':
                break # king is safe -- for now.
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(chr(ord(white_king_file) + ind) + str(num_rank + ind))
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True # we out
                
                if (piece_type_at_sq == 'K' or piece_type_at_sq == 'P') and ind == 1:
                    return True
                
                break # we are far enough away from other pieces so everything is fine
            continue
                

        # check top left
        king_top_left_count = min(8 - num_rank, num_file - 1)

        for ind in range(1, king_top_left_count + 1):
            king_str = chr(ord(white_king_file) - ind) + str(num_rank + ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'w':
                break 
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True # we out
                
                if (piece_type_at_sq == 'K' or piece_type_at_sq == 'P') and ind == 1:
                    return True # pawns are menacing beings
                
                break

            continue


        # check bottom left
        king_bottom_left_count = min(num_rank - 1, num_file - 1)

        for ind in range(1, king_bottom_left_count + 1):
            king_str = chr(ord(white_king_file) - ind) + str(num_rank - ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'w':
                break 
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True 
                
                if piece_type_at_sq == 'K' and ind == 1:
                    return True 
                
                break
            continue


        # check bottom right
        king_bottom_right_count = min(num_rank - 1, 8 - num_file)

        for ind in range(1, king_bottom_right_count + 1):
            king_str = chr(ord(white_king_file) + ind) + str(num_rank - ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'w':
                break 
            
            if piece_color_at_sq == 'b':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True 
                
                if piece_type_at_sq == 'K' and ind == 1:
                    return True 
                
                break
            
            continue 


        
        # from rook code
        # if-statement to check the 4 bounds of the king -- upper, lower, left, right

        # check limits of the top squares
        for sq_rank in range(num_rank + 1, 8 + 1):
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'w':
                break # end immediately; break only breaks out of one loop so we're fine 
            
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'b':
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) in ['R', 'Q']:
                    return True
                
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) == 'K' and (sq_rank - num_rank) == 1:
                    return True
                
                break
            continue 
        

        # check bottom
        for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'w':
                break # end immediately; break only breaks out of one loop so we're fine 
            
            if self.game_board.get_piece_color_atsq(white_king_file + str(sq_rank)) == 'b':
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) in ['R', 'Q']:
                    return True
                
                if self.game_board.get_piece_type_atsq(white_king_file + str(sq_rank)) == 'K' and (num_rank - sq_rank) == 1:
                    return True
                
                break
            continue 
        

        # check right
        # rank stays constant
        for sq_file_ord in range(ord(white_king_file) + 1, ord('h') + 1):
            # use chr(x) whenever
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'w':
                break
            
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'b':
                enemy_piece_type = self.game_board.get_piece_type_atsq(chr(sq_file_ord) + white_king_rank)
                if enemy_piece_type == 'R' or enemy_piece_type == 'Q' or (enemy_piece_type == 'K' and sq_file_ord - ord(white_king_file) == 1):
                    return True
                
                break
            continue
        
        for sq_file_ord in range(ord(white_king_file) - 1, ord('a') - 1, -1):
            # use chr(x) whenever
        
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'w':
                break
            
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + white_king_rank) == 'b':
                enemy_piece_type = self.game_board.get_piece_type_atsq(chr(sq_file_ord) + white_king_rank)
                if enemy_piece_type == 'R' or enemy_piece_type == 'Q' or (enemy_piece_type == 'K' and ord(white_king_file) - sq_file_ord == 1):
                    return True
                
                break
            continue

        # end of checking if king is in check
        return False

    # done!
    def is_black_king_in_check(self, black_piece_positions=None):
        # basically the same as the method above
        # these 2 methods should really only be used by the chess game class


        # copied from white

        black_piece_location_list = []
        if black_piece_positions is None:
            black_piece_location_list = self.black_piece_locations
        else:
            black_piece_location_list = black_piece_positions
        # check's if in current position, black king is in check
        # returns true/false

        
        # basically, from position, see if black king is in check
        # check all legal moves of all black pieces!

        black_king_location = ""
        

        for piece_location in black_piece_location_list:
            if self.game_board.get_piece_type_atsq(piece_location) == 'K':
                black_king_location = piece_location
                break
        
        black_king_file = black_king_location[0]
        black_king_rank = black_king_location[1]

        # check for 8 knights, then each direction infinitely
        # check for knights
        for pair in [(-1, 2), (-1, -2), (1, 2), (1, -2), (2, -1), (2, 1), (-2, 1), (-2, -1)]:

            try:
                white_kn_file = chr(ord(black_king_file) + pair[0]) 
                white_kn_rank = chr(ord(black_king_rank) + pair[1])


                if ord(white_kn_file) > ord('h') or ord(white_kn_file) < ord('a') or ord(white_kn_rank) > ord('8') or ord(white_kn_rank) < ord('1'):
                    continue



                if (white_kn_file + white_kn_rank not in black_piece_location_list) and (self.game_board.get_piece_type_atsq(white_kn_file + white_kn_rank) == 'N' and self.game_board.get_piece_color_atsq(white_kn_file + white_kn_rank) == 'w'):
                    
                    return True # yeah there's a knight
            except:
                pass # lmao don't worry about this -- if it errors then it's out of bounds and we're fine
            

        # check in the other 8 directions infinitely
        # since this is where the king can move, kings can potentially touch here so we have to check that
        
        # check king's top right diagonal

        num_rank = int(black_king_rank)
        num_file = 8 - (ord('h') - ord(black_king_file))

        king_top_right_count = min(8 - num_rank, 8 - num_file)

        for ind in range(1, king_top_right_count + 1):
            piece_color_at_sq = self.game_board.get_piece_color_atsq(chr(ord(black_king_file) + ind) + str(num_rank + ind))

            if piece_color_at_sq == 'b':
                break # king is safe -- for now.
            
            if piece_color_at_sq == 'w':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(chr(ord(black_king_file) + ind) + str(num_rank + ind))
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':

                    return True # we out
                
                if (piece_type_at_sq == 'K') and ind == 1:
                    return True # removing pawn since if black king is on a1 and white pawn on b2, there is no check. should be at bottom left/bottom right squares
                
                break # we are far enough away from other pieces so everything is fine
            continue
                

        # check top left
        king_top_left_count = min(8 - num_rank, num_file - 1)

        for ind in range(1, king_top_left_count + 1):
            king_str = chr(ord(black_king_file) - ind) + str(num_rank + ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'b':
                break 
            
            if piece_color_at_sq == 'w':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True # we out
                
                if (piece_type_at_sq == 'K') and ind == 1:
                    return True
                
                break

            continue


        # check bottom left
        king_bottom_left_count = min(num_rank - 1, num_file - 1)

        for ind in range(1, king_bottom_left_count + 1):
            king_str = chr(ord(black_king_file) - ind) + str(num_rank - ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'b':
                break 
            
            if piece_color_at_sq == 'w':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True 
                
                if (piece_type_at_sq == 'K' or piece_type_at_sq == 'P') and ind == 1:
                    return True 
                
                break
            continue


        # check bottom right
        king_bottom_right_count = min(num_rank - 1, 8 - num_file)

        for ind in range(1, king_bottom_right_count + 1):
            king_str = chr(ord(black_king_file) + ind) + str(num_rank - ind)
            piece_color_at_sq = self.game_board.get_piece_color_atsq(king_str)

            if piece_color_at_sq == 'b':
                break 
            
            if piece_color_at_sq == 'w':
                piece_type_at_sq = self.game_board.get_piece_type_atsq(king_str)
                if piece_type_at_sq == 'B' or piece_type_at_sq == 'Q':
                    return True 
                
                if (piece_type_at_sq == 'K' or piece_type_at_sq == 'P') and ind == 1:
                    return True 
                
                break
            
            continue 


        
        # from rook code
        # if-statement to check the 4 bounds of the king -- upper, lower, left, right

        # check limits of the top squares
        for sq_rank in range(num_rank + 1, 8 + 1):
            if self.game_board.get_piece_color_atsq(black_king_file + str(sq_rank)) == 'b':
                break # end immediately; break only breaks out of one loop so we're fine 
            
            if self.game_board.get_piece_color_atsq(black_king_file + str(sq_rank)) == 'w':
                if self.game_board.get_piece_type_atsq(black_king_file + str(sq_rank)) in ['R', 'Q']:
                    return True
                
                if self.game_board.get_piece_type_atsq(black_king_file + str(sq_rank)) == 'K' and (sq_rank - num_rank) == 1:
                    return True
                
                break
            continue 
        

        # check bottom
        for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
            if self.game_board.get_piece_color_atsq(black_king_file + str(sq_rank)) == 'b':
                break # end immediately; break only breaks out of one loop so we're fine 
            
            if self.game_board.get_piece_color_atsq(black_king_file + str(sq_rank)) == 'w':
                if self.game_board.get_piece_type_atsq(black_king_file + str(sq_rank)) in ['R', 'Q']:
                    return True
                
                if self.game_board.get_piece_type_atsq(black_king_file + str(sq_rank)) == 'K' and (num_rank - sq_rank) == 1:
                    return True
                
                break
            continue 
        

        # check right
        # rank stays constant
        for sq_file_ord in range(ord(black_king_file) + 1, ord('h') + 1):
            # use chr(x) whenever
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + black_king_rank) == 'b':
                break
            
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + black_king_rank) == 'w':
                enemy_piece_type = self.game_board.get_piece_type_atsq(chr(sq_file_ord) + black_king_rank)
                if enemy_piece_type == 'R' or enemy_piece_type == 'Q' or (enemy_piece_type == 'K' and sq_file_ord - ord(black_king_file) == 1):
                    return True
                
                break
            continue
        
        for sq_file_ord in range(ord(black_king_file) - 1, ord('a') - 1, -1):
            # use chr(x) whenever
        
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + black_king_rank) == 'b':
                break
            
            if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + black_king_rank) == 'w':
                enemy_piece_type = self.game_board.get_piece_type_atsq(chr(sq_file_ord) + black_king_rank)
                if enemy_piece_type == 'R' or enemy_piece_type == 'Q' or (enemy_piece_type == 'K' and ord(black_king_file) - sq_file_ord == 1):
                    return True
                
                break
            continue

        # end of checking if king is in check
        return False

    



    def printboard(self): 
        # should only be used for debugging
        self.game_board.printboard()
        return

    def printboard_blackpov(self):
        self.game_board.printboard_blackpov()
        return 




    # now there is castling
    def generate_white_candidate_moves(self):

        # candidate_moves is a list of all possible candidate moves
        # candidate_moves is a list of pairs, (a, b, c) where a is the starting square and b is the ending square of a piece
        # and c is the type of piece to promote to (N, B, R, Q) upon promotion if it is a pawn. otherwise it does not exist.
        candidate_moves = [] 

        # generate all possible moves for each piece + start pruning
        # just query all the pieces at each of the white squares

        # nah we not castling

        for square in self.white_piece_locations:
            # square is now a 2-digit thing
            piece_type = self.game_board.get_piece_type_atsq(square)
            file = square[0]
            rank = square[1]


            num_file = 8 - (ord('h') - ord(file))
            num_rank = int(rank)


            if piece_type == 'P':
                # pawn is at (file, rank)
                
                if rank == '7':
                    # check regular moves + pawn promotion moves

                    # check forward mobility
                    if self.game_board.get_piece_color_atsq(file + '8') == -1:
                        candidate_moves.append((file + '7', file + '8', 'Q'))
                        candidate_moves.append((file + '7', file + '8', 'R'))
                        candidate_moves.append((file + '7', file + '8', 'B'))
                        candidate_moves.append((file + '7', file + '8', 'N'))
                    
                    # check capture mobility
                    # check top left square
                    if file != 'a' and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + '8') == 'b':
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'Q'))
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'R'))
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'B'))
                        candidate_moves.append((file + '7', chr(ord(file) - 1) + '8', 'N'))
                    
                    if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + '8') == 'b':
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'Q'))
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'R'))
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'B'))
                        candidate_moves.append((file + '7', chr(ord(file) + 1) + '8', 'N'))

                    continue

                # check if pawn can move up
                if self.game_board.get_piece_color_atsq(file + str(int(rank) + 1)) == -1:
                    # pawn is free to move up (technically -- if not pinned)
                    candidate_moves.append((file + rank, file + str(int(rank) + 1)))

                    if rank == '2' and self.game_board.get_piece_color_atsq(file + '4') == -1:
                        # we can move 2 squares yippee
                        candidate_moves.append((file + '2', file + '4')) # move from x2 --> x4 (e.g. e2 --> e4)

                
                # check top left + top right of pawn for captures
                # top left
                if file != 'a' and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) + 1)) == 'b':
                    # eat 
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1)))
                
                # top right
                if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) + 1)) == 'b':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1)))
                

                # check for en passant
                # en passant to the left
                if rank == '5' and self.last_pawn_move[0] == chr(ord(file) - 1):
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1)))
                
                # en passant to the right

                if rank == '5' and self.last_pawn_move[0] == chr(ord(file) + 1):
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1)))
                
                # :)
                continue


            if piece_type == 'N':
                # idea: square = numbers, then generate based on numbers
                # a --> 1, h --> 8
                # 1 --> 8
                new_file = 8 - (ord('h') - ord(file))
                new_rank = int(rank)

                # treat new_file, new_rank as a pair
                possible_knight_squares = [(new_file - 2, new_rank - 1), (new_file + 2, new_rank - 1)] + [(new_file - 2, new_rank + 1), (new_file + 2, new_rank + 1)]
                possible_knight_squares += [(new_file - 1, new_rank + 2), (new_file + 1, new_rank + 2)] + [(new_file - 1, new_rank - 2), (new_file + 1, new_rank - 2)]
        
                # now parse pairs
                more_possible_kn_moves = []
                for pair in possible_knight_squares:
                    if pair[0] < 1 or pair[0] > 8 or pair[1] < 1 or pair[1] > 8:
                        continue
                    
                    more_possible_kn_moves.append(pair)
                

                # now check if there's a piece at that location
                for pair in more_possible_kn_moves:
                    # convert back to normal coordinates
                    new_file = chr(ord('a') - 1 + pair[0]) # 1 --> a, 2 --> b, etc.
                    new_rank = pair[1]

                    if self.game_board.get_piece_color_atsq(new_file + str(new_rank)) == 'w':
                        continue
                    
                    candidate_moves.append((file + rank, new_file + str(new_rank))) # doesn't matter if it's a capture or not
                
                continue
                    


            if piece_type == 'B':
                # uhh check the 4 intersecting diagonal things

                # piece is at file, rank
                # check top right diagonal

                bish_top_right_count = min(8 - num_rank, 8 - num_file)

                for ind in range(1, bish_top_right_count + 1):
                    # move up and to the right 1 sq and check the piece there
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(chr(ord(file) + ind) + str(num_rank + ind))

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                        break

                    candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                    continue
                


                # check top left
                bish_top_left_count = min(8 - num_rank, num_file - 1)

                for ind in range(1, bish_top_left_count + 1):
                    bish_str = chr(ord(file) - ind) + str(num_rank + ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue


                # check bottom left
                bish_bottom_left_count = min(num_rank - 1, num_file - 1)

                for ind in range(1, bish_bottom_left_count + 1):
                    bish_str = chr(ord(file) - ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue


                # check bottom right
                bish_bottom_right_count = min(num_rank - 1, 8 - num_file)

                for ind in range(1, bish_bottom_right_count + 1):
                    bish_str = chr(ord(file) + ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue

                continue


            if piece_type == 'R':
                # if-statement to check the 4 bounds of the rook -- upper, lower, left, right

                # check limits of the top squares
                for sq_rank in range(num_rank + 1, 8 + 1):
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break # end immediately; break only breaks out of one loop so we're fine 
                    
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank))) # business as usual
                    continue 
                
                # check bottom
                for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break 

                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank)))
                    continue
                

                # check right
                # rank stays constant
                for sq_file_ord in range(ord(file) + 1, ord('h') + 1):
                    # use chr(x) whenever
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue
                
                for sq_file_ord in range(ord(file) - 1, ord('a') - 1, -1):
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue 

                # mk we done
                continue


            if piece_type == 'Q':
                # just copy over rook + queen code and combine it
                # 
                # 
                #
                #
                # from bishop code
                queen_top_right_count = min(8 - num_rank, 8 - num_file)

                for ind in range(1, queen_top_right_count + 1):
                    # move up and to the right 1 sq and check the piece there
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(chr(ord(file) + ind) + str(num_rank + ind))

                    if piece_type_at_sq == 'w':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                        break

                    candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                    continue
                


                # check top left
                queen_top_left_count = min(8 - num_rank, num_file - 1)

                for ind in range(1, queen_top_left_count + 1):
                    queen_str = chr(ord(file) - ind) + str(num_rank + ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'w':
                        break 
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue


                # check bottom left
                queen_bottom_left_count = min(num_rank - 1, num_file - 1)

                for ind in range(1, queen_bottom_left_count + 1):
                    queen_str = chr(ord(file) - ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'w':
                        break 
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue


                # check bottom right
                queen_bottom_right_count = min(num_rank - 1, 8 - num_file)

                for ind in range(1, queen_bottom_right_count + 1):
                    queen_str = chr(ord(file) + ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'w':
                        break 
                    
                    if piece_type_at_sq == 'b':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue
                #
                #
                #
                #
                #
                # from rook code
                # if-statement to check the 4 bounds of the queen -- upper, lower, left, right

                # check limits of the top squares
                for sq_rank in range(num_rank + 1, 8 + 1):
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break # end immediately; break only breaks out of one loop so we're fine 
                    
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank))) # business as usual
                    continue 
                
                # check bottom
                for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        break 

                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank)))
                    continue
                

                # check right
                # rank stays constant
                for sq_file_ord in range(ord(file) + 1, ord('h') + 1):
                    # use chr(x) whenever
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue
                
                for sq_file_ord in range(ord(file) - 1, ord('a') - 1, -1):
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue 

                # end of queen if-statement
                continue


            if piece_type == 'K':
                is_at_top = 0 if rank == '8' else 1 # inverted so i dont need to put nots
                is_at_bottom = 0 if rank == '1' else 1
                is_at_left = 0 if file == 'a' else 1
                is_at_right = 0 if file == 'h' else 1

                # check top left
                if is_at_top and is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) + 1)) != 'w':
                    # add possible square move
                    # we are not looking at putting the king in check yet
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1)))
                
                # check top
                if is_at_top and self.game_board.get_piece_color_atsq(file + str(int(rank) + 1)) != 'w':
                    candidate_moves.append((file + rank, file + str(int(rank) + 1)))
                
                # check top right
                if is_at_top and is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) + 1)) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1)))
                

                # check directly left
                if is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + rank) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + rank))
                
                # check directly right 
                if is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + rank) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + rank))
                

                # check bottom left
                if is_at_bottom and is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) - 1)) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) - 1)))
                
                # check bottom
                if is_at_bottom and self.game_board.get_piece_color_atsq(file + str(int(rank) - 1)) != 'w':
                    candidate_moves.append((file + rank, file + str(int(rank) - 1)))
                
                # check bttom right
                if is_at_bottom and is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) - 1)) != 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) - 1)))
                

                continue #! am done with king!
            



            # ehrm code should never reach here
            raise ValueError("Piece at location", square, "does not exist.")

        
        # check legality of all moves
        # check if anything is pinned + if king is in check

        # NOTE -- this works even if the king is already in check -- as it will automatically reject anything that leaves the king in check

        # idea: move piece to location, then check if white king is in check at that point in time
        actual_candidate_moves = []

        for pair in candidate_moves:
            # move piece to location then reset it
            final_square_piece_type = self.game_board.get_piece_type_atsq(pair[1])
            
            final_square_piece_color = self.game_board.get_piece_color_atsq(pair[1])

            # move piece to square and check if king is in check
            self.game_board.move_piece(pair[0], pair[1])


            # modify the list of pieces if anything's moved etc etc so everything makes more sense
            piece_list = self.white_piece_locations.copy() # do a deep copy
            piece_list.pop(self.white_piece_locations.index(pair[0]))
            piece_list.append(pair[1])
            


            if self.is_white_king_in_check(piece_list):
                # don't add the pair
                pass 
            else:
                actual_candidate_moves.append(pair)
            
            # reset position
            if final_square_piece_type != -1:
                # piece exists
                self.game_board.move_piece(pair[1], pair[0])
                self.game_board.set_piece_tosq(pair[1], final_square_piece_type, final_square_piece_color)
                continue
            else:
                self.game_board.move_piece(pair[1], pair[0])
            continue # end for loop


        # manually add castling
        # kingside castling -- ('e1', 'g1') -- to indicate kingside castling
        # queenside castling -- ('e1', 'c1') -- to indicate queenside castling
        if self.white_kingside_castling:
            # check that 
            # a. the king does not move through check
            # b. there are no pieces between e1, f1, g1, h1 (besides rook on h1)

            # check first there are no pieces on f1 and g1
            # for failsafe check that the king is on e1, and that there is a rook on h1

            if self.game_board.get_piece_type_atsq('f1') == -1 and self.game_board.get_piece_type_atsq('g1') == -1:
                # no pieces on g1 and f1
                if self.game_board.get_piece_type_atsq('e1') == 'K' and self.game_board.get_piece_color_atsq('e1') == 'w' and self.game_board.get_piece_type_atsq('h1') == 'R' and self.game_board.get_piece_color_atsq('h1') == 'w':
                    # ok failsafes are in place
                    # next check that the king is not in check (on e1) (on f1) (on g1)

                    if not self.is_white_king_in_check():
                        # king is not in check on e1
                        
                        self.game_board.move_piece('e1', 'f1')


                        piece_list = self.white_piece_locations.copy() # do a deep copy
                        piece_list.pop(self.white_piece_locations.index('e1'))
                        piece_list.append('f1')
                        


                        if not self.is_white_king_in_check(piece_list):
                            # f1 is also save
                            self.game_board.move_piece('f1', 'g1')
                            piece_list_two = piece_list.copy()
                            piece_list.pop(piece_list.index('f1'))
                            piece_list.append('g1')

                            if not self.is_white_king_in_check(piece_list):
                                # raaaaaaahhhhh ok add to list
                                actual_candidate_moves.append(('e1', 'g1')) # no c -- uci doesn't support it
                            

                            # unwrap
                            self.game_board.move_piece('g1', 'f1')
                        
                        # move back
                        self.game_board.move_piece('f1', 'e1')

            # end kingside castling if-statement


        # queenside castling
        if self.white_queenside_castling:
            if self.game_board.get_piece_type_atsq('b1') == -1 and self.game_board.get_piece_type_atsq('c1') == -1 and self.game_board.get_piece_type_atsq('d1') == -1:
                if self.game_board.get_piece_type_atsq('e1') == 'K' and self.game_board.get_piece_color_atsq('e1') == 'w' and self.game_board.get_piece_type_atsq('a1') == 'R' and self.game_board.get_piece_color_atsq('a1') == 'w':
                    if not self.is_white_king_in_check():     
                        self.game_board.move_piece('e1', 'd1')
                        piece_list = self.white_piece_locations.copy()
                        piece_list.pop(self.white_piece_locations.index('e1'))
                        piece_list.append('d1')
                        if not self.is_white_king_in_check(piece_list):
                            self.game_board.move_piece('d1', 'c1')
                            piece_list_two = piece_list.copy()
                            piece_list.pop(piece_list.index('d1'))
                            piece_list.append('c1')
                            if not self.is_white_king_in_check(piece_list):
                                actual_candidate_moves.append(('e1', 'c1')) 
                            self.game_board.move_piece('c1', 'd1') # unwrap
                        self.game_board.move_piece('d1', 'e1') # move back
            # end queenside castling if-statement

            
        return actual_candidate_moves       
        # end white_candidate_moves
        
    # there is also castling here
    def generate_black_candidate_moves(self):
        candidate_moves = [] 


        for square in self.black_piece_locations:
            piece_type = self.game_board.get_piece_type_atsq(square)
            file = square[0]
            rank = square[1]


            num_file = 8 - (ord('h') - ord(file))
            num_rank = int(rank)

            # forward mobility in this case is going down a rank
            if piece_type == 'P':
                if rank == '2':
                    
                    if self.game_board.get_piece_color_atsq(file + '1') == -1:
                        candidate_moves.append((file + '2', file + '1', 'Q'))
                        candidate_moves.append((file + '2', file + '1', 'R'))
                        candidate_moves.append((file + '2', file + '1', 'B'))
                        candidate_moves.append((file + '2', file + '1', 'N'))
                    
                    # check capture mobility
                    if file != 'a' and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + '1') == 'w':
                        candidate_moves.append((file + '2', chr(ord(file) - 1) + '1', 'Q'))
                        candidate_moves.append((file + '2', chr(ord(file) - 1) + '1', 'R'))
                        candidate_moves.append((file + '2', chr(ord(file) - 1) + '1', 'B'))
                        candidate_moves.append((file + '2', chr(ord(file) - 1) + '1', 'N'))
                    
                    if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + '1') == 'w':
                        candidate_moves.append((file + '2', chr(ord(file) + 1) + '1', 'Q'))
                        candidate_moves.append((file + '2', chr(ord(file) + 1) + '1', 'R'))
                        candidate_moves.append((file + '2', chr(ord(file) + 1) + '1', 'B'))
                        candidate_moves.append((file + '2', chr(ord(file) + 1) + '1', 'N'))

                    continue

                # check if pawn can move DOWN
                if self.game_board.get_piece_color_atsq(file + str(int(rank) - 1)) == -1:
                    candidate_moves.append((file + rank, file + str(int(rank) - 1)))

                    if rank == '7' and self.game_board.get_piece_color_atsq(file + '5') == -1:
                        # we can move 2 squares yippee
                        candidate_moves.append((file + '7', file + '5')) 

                
                # check bottom left + bottom right of pawn for captures
                if file != 'a' and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) - 1)) == 'w':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) - 1)))
                
                if file != 'h' and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) - 1)) == 'w':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) - 1)))
                

                # check for en passant # e.g. d5 --> d4, e2 --> e4, d4 --> e3 e.p.
                # en passant to the left

                if rank == '4' and self.last_pawn_move[0] == chr(ord(file) - 1):
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) - 1)))
                
                # en passant to the right

                if rank == '4' and self.last_pawn_move[0] == chr(ord(file) + 1):
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) - 1))) 
                
                # :)
                continue


            if piece_type == 'N':
                # idea: square = numbers, then generate based on numbers
                # a --> 1, h --> 8
                # 1 --> 8
                new_file = 8 - (ord('h') - ord(file))
                new_rank = int(rank)

                # treat new_file, new_rank as a pair
                possible_knight_squares = [(new_file - 2, new_rank - 1), (new_file + 2, new_rank - 1)] + [(new_file - 2, new_rank + 1), (new_file + 2, new_rank + 1)]
                possible_knight_squares += [(new_file - 1, new_rank + 2), (new_file + 1, new_rank + 2)] + [(new_file - 1, new_rank - 2), (new_file + 1, new_rank - 2)]
        
                # now parse pairs
                more_possible_kn_moves = []
                for pair in possible_knight_squares:
                    if pair[0] < 1 or pair[0] > 8 or pair[1] < 1 or pair[1] > 8:
                        continue
                    
                    more_possible_kn_moves.append(pair)
                

                for pair in more_possible_kn_moves:
                    # convert back to normal coordinates
                    new_file = chr(ord('a') - 1 + pair[0]) # 1 --> a, 2 --> b, etc.
                    new_rank = pair[1]

                    if self.game_board.get_piece_color_atsq(new_file + str(new_rank)) == 'b':
                        continue # can't capture your own piece
                    
                    candidate_moves.append((file + rank, new_file + str(new_rank))) 
                
                continue
                    


            if piece_type == 'B':
                # uhh check the 4 intersecting diagonal things

                # piece is at file, rank
                # check top right diagonal

                bish_top_right_count = min(8 - num_rank, 8 - num_file)

                for ind in range(1, bish_top_right_count + 1):
                    # move up and to the right 1 sq and check the piece there
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(chr(ord(file) + ind) + str(num_rank + ind))

                    if piece_type_at_sq == 'b':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                        break

                    candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                    continue
                


                # check top left
                bish_top_left_count = min(8 - num_rank, num_file - 1)

                for ind in range(1, bish_top_left_count + 1):
                    bish_str = chr(ord(file) - ind) + str(num_rank + ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'b':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue


                # check bottom left
                bish_bottom_left_count = min(num_rank - 1, num_file - 1)

                for ind in range(1, bish_bottom_left_count + 1):
                    bish_str = chr(ord(file) - ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'b':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue


                # check bottom right
                bish_bottom_right_count = min(num_rank - 1, 8 - num_file)

                for ind in range(1, bish_bottom_right_count + 1):
                    bish_str = chr(ord(file) + ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(bish_str)

                    if piece_type_at_sq == 'b':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, bish_str))
                        break

                    candidate_moves.append((file + rank, bish_str))
                    continue

                continue


            if piece_type == 'R':
                # if-statement to check the 4 bounds of the rook -- upper, lower, left, right

                # check limits of the top squares
                for sq_rank in range(num_rank + 1, 8 + 1):
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        break # end immediately; break only breaks out of one loop so we're fine 
                    
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank))) # business as usual
                    continue 
                
                # check bottom
                for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        break 

                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank)))
                    continue
                

                # check right
                # rank stays constant
                for sq_file_ord in range(ord(file) + 1, ord('h') + 1):
                    # use chr(x) whenever
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue
                
                for sq_file_ord in range(ord(file) - 1, ord('a') - 1, -1):
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue 

                # mk we done
                continue


            if piece_type == 'Q':
                # just copy over rook + queen code and combine it
                # 
                # 
                #
                #
                # from bishop code
                queen_top_right_count = min(8 - num_rank, 8 - num_file)

                for ind in range(1, queen_top_right_count + 1):
                    # move up and to the right 1 sq and check the piece there
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(chr(ord(file) + ind) + str(num_rank + ind))

                    if piece_type_at_sq == 'b':
                        break # bishop is hemmed in by own piece
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                        break

                    candidate_moves.append((file + rank, chr(ord(file) + ind) + str(num_rank + ind)))
                    continue
                


                # check top left
                queen_top_left_count = min(8 - num_rank, num_file - 1)

                for ind in range(1, queen_top_left_count + 1):
                    queen_str = chr(ord(file) - ind) + str(num_rank + ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'b':
                        break 
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue


                # check bottom left
                queen_bottom_left_count = min(num_rank - 1, num_file - 1)

                for ind in range(1, queen_bottom_left_count + 1):
                    queen_str = chr(ord(file) - ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'b':
                        break 
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue


                # check bottom right
                queen_bottom_right_count = min(num_rank - 1, 8 - num_file)

                for ind in range(1, queen_bottom_right_count + 1):
                    queen_str = chr(ord(file) + ind) + str(num_rank - ind)
                    piece_type_at_sq = self.game_board.get_piece_color_atsq(queen_str)

                    if piece_type_at_sq == 'b':
                        break 
                    
                    if piece_type_at_sq == 'w':
                        candidate_moves.append((file + rank, queen_str))
                        break

                    candidate_moves.append((file + rank, queen_str))
                    continue
                #
                #
                #
                #
                #
                # from rook code
                # if-statement to check the 4 bounds of the queen -- upper, lower, left, right

                # check limits of the top squares
                for sq_rank in range(num_rank + 1, 8 + 1):
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        break # end immediately; break only breaks out of one loop so we're fine 
                    
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank))) # business as usual
                    continue 
                
                # check bottom
                for sq_rank in range(num_rank - 1, 0, -1): # backwards loop
                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'b':
                        break 

                    if self.game_board.get_piece_color_atsq(file + str(sq_rank)) == 'w':
                        candidate_moves.append((file + rank, file + str(sq_rank)))
                        break

                    candidate_moves.append((file + rank, file + str(sq_rank)))
                    continue
                

                # check right
                # rank stays constant
                for sq_file_ord in range(ord(file) + 1, ord('h') + 1):
                    # use chr(x) whenever
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue
                
                for sq_file_ord in range(ord(file) - 1, ord('a') - 1, -1):
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'b':
                        break
                    
                    if self.game_board.get_piece_color_atsq(chr(sq_file_ord) + rank) == 'w':
                        candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                        break
                    
                    candidate_moves.append((file + rank, chr(sq_file_ord) + rank))
                    continue 

                # end of queen if-statement
                continue


            if piece_type == 'K':
                is_at_top = 0 if rank == '8' else 1 # inverted so i dont need to put nots
                is_at_bottom = 0 if rank == '1' else 1
                is_at_left = 0 if file == 'a' else 1
                is_at_right = 0 if file == 'h' else 1

                # check top left
                if is_at_top and is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) + 1)) != 'b':
                    # add possible square move
                    # we are not looking at putting the king in check yet
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) + 1)))
                
                # check top
                if is_at_top and self.game_board.get_piece_color_atsq(file + str(int(rank) + 1)) != 'b':
                    candidate_moves.append((file + rank, file + str(int(rank) + 1)))
                
                # check top right
                if is_at_top and is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) + 1)) != 'b':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) + 1)))
                

                # check directly left
                if is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + rank) != 'b':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + rank))
                
                # check directly right 
                if is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + rank) != 'b':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + rank))
                

                # check bottom left
                if is_at_bottom and is_at_left and self.game_board.get_piece_color_atsq(chr(ord(file) - 1) + str(int(rank) - 1)) != 'b':
                    candidate_moves.append((file + rank, chr(ord(file) - 1) + str(int(rank) - 1)))
                
                # check bottom
                if is_at_bottom and self.game_board.get_piece_color_atsq(file + str(int(rank) - 1)) != 'b':
                    candidate_moves.append((file + rank, file + str(int(rank) - 1)))
                
                # check bttom right
                if is_at_bottom and is_at_right and self.game_board.get_piece_color_atsq(chr(ord(file) + 1) + str(int(rank) - 1)) != 'b':
                    candidate_moves.append((file + rank, chr(ord(file) + 1) + str(int(rank) - 1)))
                

                continue #! am done with king!
            



            # ehrm code should never reach here
            raise ValueError("Piece at location", square, "does not exist.")

        
        # check legality of all moves
        # check if anything is pinned + if king is in check

        # NOTE -- this works even if the king is already in check -- as it will automatically reject anything that leaves the king in check

        # idea: move piece to location, then check if black king is in check at that point in time
        actual_candidate_moves = []

        for pair in candidate_moves:
            # move piece to location then reset it
            final_square_piece_type = self.game_board.get_piece_type_atsq(pair[1])
            
            final_square_piece_color = self.game_board.get_piece_color_atsq(pair[1])

            # move piece to square and check if king is in check
            self.game_board.move_piece(pair[0], pair[1])


            # modify the list of pieces if anything's moved etc etc so everything makes more sense
            piece_list = self.black_piece_locations.copy() # do a deep copy
            piece_list.pop(self.black_piece_locations.index(pair[0]))
            piece_list.append(pair[1])
            


            if self.is_black_king_in_check(piece_list):
                # don't add the pair
                pass 
            else:
                actual_candidate_moves.append(pair)
            
            # reset position
            if final_square_piece_type != -1:
                # piece exists
                self.game_board.move_piece(pair[1], pair[0])
                self.game_board.set_piece_tosq(pair[1], final_square_piece_type, final_square_piece_color)
                continue
            else:
                self.game_board.move_piece(pair[1], pair[0])
            continue # end for loop



        # manually add everything
        if self.black_kingside_castling:
            if self.game_board.get_piece_type_atsq('f8') == -1 and self.game_board.get_piece_type_atsq('g8') == -1:
                # no pieces on f8, g8
                if self.game_board.get_piece_type_atsq('e8') == 'K' and self.game_board.get_piece_color_atsq('e8') == 'b' and self.game_board.get_piece_type_atsq('h8') == 'R' and self.game_board.get_piece_color_atsq('h8') == 'b':
                    if not self.is_black_king_in_check():
                        
                        self.game_board.move_piece('e8', 'f8')

                        piece_list = self.black_piece_locations.copy() # do a deep copy
                        piece_list.pop(self.black_piece_locations.index('e8'))
                        piece_list.append('f8')
                        


                        if not self.is_black_king_in_check(piece_list):
                            # f8
                            self.game_board.move_piece('f8', 'g8')
                            piece_list_two = piece_list.copy()
                            piece_list.pop(piece_list.index('f8'))
                            piece_list.append('g8')

                            if not self.is_black_king_in_check(piece_list):
                                # raaaaaaahhhhh ok add to list
                                actual_candidate_moves.append(('e8', 'g8'))
                            

                            # unwrap
                            self.game_board.move_piece('g8', 'f8')
                        
                        # move back
                        self.game_board.move_piece('f8', 'e8')

            # end kingside castling if-statement


        # queenside castling
        if self.black_queenside_castling:
            if self.game_board.get_piece_type_atsq('b8') == -1 and self.game_board.get_piece_type_atsq('c8') == -1 and self.game_board.get_piece_type_atsq('d8') == -1:
                if self.game_board.get_piece_type_atsq('e8') == 'K' and self.game_board.get_piece_color_atsq('e8') == 'b' and self.game_board.get_piece_type_atsq('a8') == 'R' and self.game_board.get_piece_color_atsq('a8') == 'b':
                    if not self.is_black_king_in_check():     
                        self.game_board.move_piece('e8', 'd8')
                        piece_list = self.black_piece_locations.copy()
                        piece_list.pop(self.black_piece_locations.index('e8'))
                        piece_list.append('d8')
                        if not self.is_black_king_in_check(piece_list):
                            self.game_board.move_piece('d8', 'c8')
                            piece_list_two = piece_list.copy()
                            piece_list.pop(piece_list.index('d8'))
                            piece_list.append('c8')
                            if not self.is_black_king_in_check(piece_list):
                                actual_candidate_moves.append(('e8', 'c8'))
                            self.game_board.move_piece('c8', 'd8') # unwrap
                        self.game_board.move_piece('d8', 'e8') # move back
            # end queenside castling if-statement

        
        return actual_candidate_moves       
        # end black_candidate_moves
   




    # never tested
    def send_uci_move(self, uci):
        # yeah just do it
        
        # e.g. c2c4, g1f3, a7a8q 
        # castling is just e1g1 (king position change)

        # find if the start sq is a white or black piece
        if self.game_board.get_piece_color_atsq(uci[0] + uci[1]) == 'w':
            # send white uci move

            if len(uci) == 5:
                return self.send_white_move(uci[0] + uci[1], uci[2] + uci[3], uci[4])
            
            return self.send_white_move(uci[0] + uci[1], uci[2] + uci[3])

        if self.game_board.get_piece_color_atsq(uci[0] + uci[1]) == 'b':
            if len(uci) == 5:
                return self.send_black_move(uci[0] + uci[1], uci[2] + uci[3], uci[4])
            
            return self.send_black_move(uci[0] + uci[1], uci[2] + uci[3])

        return -1 # ehrm something broke
        
        



    def send_white_move(self, start_sq, end_sq, pawn_promotion=None):
        # check legality of move
        # pawn_promotion is a string like 'Q' or 'N' -- piece to promote to
        
        if pawn_promotion is None and (start_sq, end_sq) not in self.generate_white_candidate_moves():
            # ehrm move is bad
            return -1
        
        if pawn_promotion is not None and (start_sq, end_sq, pawn_promotion) not in self.generate_white_candidate_moves():
            # move is still bad
            return -1
        
        # ok move seems legit
        self.game_board.send_move(start_sq, end_sq)
        if end_sq in self.black_piece_locations:
            self.black_piece_locations.remove(end_sq) # piece is captured
        
        self.white_piece_locations.remove(start_sq)
        self.white_piece_locations.append(end_sq)
        
        self.white_turn = False
        
        # ok eval board
        if self.is_black_king_in_check():
            self.black_king_check = True


        # check if last move was en passant
        # e.g. last move was g5 --> f6 and square is f6
        if self.game_board.get_piece_type_atsq(end_sq) == 'P' and self.last_pawn_move == end_sq:
            # en_passant lmao
            print("en_passant lmao")
            
            self.black_piece_locations.remove(end_sq[0] + chr(ord(end_sq[1]) - 1))
            # update board
            self.game_board.change_square(end_sq[0] + chr(ord(end_sq[1]) - 1), ".")



        # update last_pawn_move (if pawn moved from e.g. c2 to c4)
        if self.game_board.get_piece_type_atsq(end_sq) == 'P' and start_sq[1] == '2' and start_sq[0] == end_sq[0]:
            # chat im pretty sure the pawn just moved two squares
            self.last_pawn_move = start_sq[0] + chr(ord(start_sq[1]) + 1) # yippee
        else:
            self.last_pawn_move = 'z0' # null value

        
        if pawn_promotion in ['N', 'B', 'R', 'Q']:
            # change piece type at final sq
            self.game_board.set_piece_tosq(end_sq, pawn_promotion, 'w')





        # check if it's king/queenside castling
        if start_sq == 'e1' and end_sq == 'g1' and self.game_board.get_piece_type_atsq('g1') == 'K' and self.game_board.get_piece_type_atsq('h1') == 'R':
            # extra failsafe with the rook check

            # ok sure this seems legit
            # king has been moved to g1
            # move rook
            self.game_board.move_piece('h1', 'f1') # move rook
            self.white_kingside_castling = False
            self.white_queenside_castling = False
            self.white_piece_locations.remove('h1') # move rook
            self.white_piece_locations.append('f1')
        
        if start_sq == 'e1' and end_sq == 'c1' and self.game_board.get_piece_type_atsq('c1') == 'K' and self.game_board.get_piece_type_atsq('a1') == 'R':
            self.white_queenside_castling = False
            self.white_kingside_castling = False # white can't castle both queenside and kingside
            self.game_board.move_piece('a1', 'd1')
            self.white_piece_locations.remove('a1') 
            self.white_piece_locations.append('d1')

        # what if the rook moved???
        if self.game_board.get_piece_type_atsq(end_sq) == 'R' and start_sq == 'h1':
            # revoke castling rights
            self.white_kingside_castling = False
        
        if self.game_board.get_piece_type_atsq(end_sq) == 'R' and start_sq == 'a1':
            self.white_queenside_castling = False

        # check if king has moved or not
        if self.game_board.get_piece_type_atsq(end_sq) == 'K':
            # yeah ur cooked no castling
            self.white_kingside_castling = False
            self.white_queenside_castling = False

        return 0 # good exit code
    


    def send_black_move(self, start_sq, end_sq, pawn_promotion=None):

        
        if pawn_promotion is None and (start_sq, end_sq) not in self.generate_black_candidate_moves():
            return -1
        
        if pawn_promotion is not None and (start_sq, end_sq, pawn_promotion) not in self.generate_black_candidate_moves():
            return -1
        
        # ok move seems legit
        self.game_board.send_move(start_sq, end_sq)
        if end_sq in self.white_piece_locations:
            self.white_piece_locations.remove(end_sq) # piece is captured
        
        self.black_piece_locations.remove(start_sq)
        self.black_piece_locations.append(end_sq)
        
        self.white_turn = True
        
        # ok eval board
        if self.is_white_king_in_check():
            self.white_king_check = True


        # update last_pawn_move (if pawn moved from e.g. c7 to c5)
        if self.game_board.get_piece_type_atsq(end_sq) == 'P' and start_sq[1] == '7' and start_sq[0] == end_sq[0]:
            # chat im pretty sure the pawn just moved two squares
            self.last_pawn_move = start_sq[0] + chr(ord(start_sq[1]) - 1) # yippee
            # last move was e.g. c7 --> c5. We need to change the c7 --> c6 (hence the -1)
        else:
            self.last_pawn_move = 'z0' # null value

        
        if pawn_promotion in ['N', 'B', 'R', 'Q']:
            # change piece type at final sq
            self.game_board.set_piece_tosq(end_sq, pawn_promotion, 'b')




        # check if it's king/queenside castling (but black)
        if start_sq == 'e8' and end_sq == 'g8' and self.game_board.get_piece_type_atsq('g8') == 'K' and self.game_board.get_piece_type_atsq('h8') == 'R':
            self.game_board.move_piece('h8', 'f8') # move rook
            self.black_kingside_castling = False
            self.black_queenside_castling = False
            self.black_piece_locations.remove('h8') # move rook
            self.black_piece_locations.append('f8')
        
        if start_sq == 'e8' and end_sq == 'c8' and self.game_board.get_piece_type_atsq('c8') == 'K' and self.game_board.get_piece_type_atsq('a8') == 'R':
            self.black_queenside_castling = False
            self.black_kingside_castling = False # white can't castle both queenside and kingside
            self.game_board.move_piece('a8', 'd8')
            self.black_piece_locations.remove('a8') 
            self.black_piece_locations.append('d8')

        # what if the rook moved???
        if self.game_board.get_piece_type_atsq(end_sq) == 'R' and start_sq == 'h8':
            # revoke castling rights
            self.black_kingside_castling = False
        
        if self.game_board.get_piece_type_atsq(end_sq) == 'R' and start_sq == 'a8':
            self.black_queenside_castling = False

        # check if king has moved or not
        if self.game_board.get_piece_type_atsq(end_sq) == 'K':
            self.black_kingside_castling = False
            self.black_queenside_castling = False 



        return 0 # good exit code




    # done!
    def load_pos_from_fen(self, fen):
        # fen is the string
        # idea: reset board, then add pieces and update everything else accordingly


        # reset everything
        self.game_board.clear_board() # back to dots
        self.white_piece_locations = []
        self.black_piece_locations = []

        self.white_kingside_castling = False
        self.white_queenside_castling = False
        self.black_kingside_castling = False
        self.black_queenside_castling = False 
        


        fen_components = fen.split() # is list of length 6
        # fen[0] -- the actual fen string
        # fen[1] -- turn? (w/b)
        # fen[2] -- castling priviledge? KQ -- white can kingside queenside, k -- black can kingside, can be '-' for none
        # fen[3] -- en passant target square -- e.g. c6 if c7 --> c5 last move
        # fen[4] -- halfmove clock
        # fen[5] -- move number


        # tackle fen string, fen[0]
        # starts from rank 8 and works downward to rank 1
        # uppercase --> black piece, lowercase --> white piece
        rank_pointer = 0
        file_pointer = 0 # pointers -- (0, 0) means a8, (2, 3) means d6 -- c3 = file/rank

        for char in fen_components[0]:
            if char == '/':
                # move on yippee
                rank_pointer += 1
                file_pointer = 0
                continue

            if ord(char) > 48 and ord(char) < 57:
                # char is a number between 1 and 8
                file_pointer += int(char)
                continue
            
            
            if char.lower() == char:
                # is a black piece
                
                # convert (rank_pointer, file_pointer) to actual square
                actual_rank = str(8 - rank_pointer)
                actual_col = chr(ord('a') + file_pointer)
                self.black_piece_locations.append(actual_col + actual_rank) # file, rank

                # put piece on board
                self.game_board.set_piece_tosq(actual_col + actual_rank, char.upper(), 'b')
                file_pointer += 1
                continue
            
            # piece is a white piece
            actual_rank = str(8 - rank_pointer)
            actual_col = chr(ord('a') + file_pointer)
            self.white_piece_locations.append(actual_col + actual_rank)

            self.game_board.set_piece_tosq(actual_col + actual_rank, char, 'w')
            file_pointer += 1
            continue
        

        # tackle fen[1] --> fen[5]
        # from above:
        # fen[1] -- turn? (w/b)
        # fen[2] -- castling priviledge? KQ -- white can kingside queenside, k -- black can kingside, can be '-' for none
        # fen[3] -- en passant target square -- e.g. c6 if c7 --> c5 last move
        # fen[4] -- halfmove clock
        # fen[5] -- move number


    
        self.white_turn = (fen[1] == 'w') # fen[1]
        

        # castling priviledges
        if fen[2].find('K') != -1:
            self.white_kingside_castling = True
            
        if fen[2].find('Q') != -1:
            self.white_queenside_castling = True

        if fen[2].find('k') != -1:
            self.black_kingside_castling = True

        if fen[2].find('q') != -1:
            self.black_queenside_castling = True


        # target square en passant -- fen[3]
        if fen[3] == '-':
            self.last_pawn_move = 'z0'
        else:
            self.last_pawn_move = fen[3] # :D
        
        
        # halfmove clock, fen[4]
        self.half_move_clock = fen[4]

        self.move_number = fen[5]
        return #! we done


        

        


    
    # end class!
