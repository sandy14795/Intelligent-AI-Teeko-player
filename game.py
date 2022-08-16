import random
import copy 

class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.drop_phase = True
        self.piece_count = 0
    
    def succ(self, state, turn=0):
        
        states = []
        
        if self.drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        temp = copy.deepcopy(state)
                        temp[row][col] = self.pieces[turn]
                        child = [temp, (row,col), 0]
                        states.append(child)
                        del temp
                        del child
                    
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.pieces[turn]:
                        valid_slots = self.get_valid_adjacents(row,col,state)
                        for slots in valid_slots:
                            temp = copy.deepcopy(state)
                            temp[row][col] = ' '
                            temp[slots[0]][slots[1]] = self.pieces[turn]
                            child = [temp, (slots[0],slots[1]), (row,col)]
                            if child not in states:
                                states.append(child)
                            del temp
                            del child
        
        return states 
    
    def get_valid_adjacents(self,a,b,state):
        adjacentSlots = []
        directions = [
            [-1, -1], [-1, 0], [-1, +1],
            [0, -1],           [0, +1],
            [+1, -1], [+1, 0], [+1, +1],
        ]

        for i in directions:
            x = a + i[0]
            y = b + i[1]

            if( 0 <= x <= 4 and 0 <= y <= 4) and (state[x][y] == ' '):
                adjacentSlots.append([x,y])
        return adjacentSlots
    
    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        turn = self.pieces.index(self.my_piece)
        if not self.drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase
            
            succ_states = self.succ(state, turn)
#            random.shuffle(succ_states)
            max_score = float('-inf')
            for cand_state in succ_states:
                score = self.max_value(cand_state[0], depth = 1, turn = (turn+1)%2)

                if score > max_score:
                    max_score = score 
                    move = []
#                   cand = random.choice(succ_states)
                    move.append(cand_state[1])
                    move.append(cand_state[2])
            return move

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        else:
            succ_states = self.succ(state, turn)
#            random.shuffle(succ_states)
            max_score = float('-inf')
            for cand_state in succ_states:
                score = self.max_value(cand_state[0], depth = 1, turn = (turn+1)%2)

                if score > max_score:
                    max_score = score 
                    move = []
#                   cand = random.choice(succ_states)
                    move.insert(0,cand_state[1])
            # ensure the destination (row,col) tuple is at the beginning of the move list
#            (row,col) = random.choice(succ_states)[1]
#            move.insert(0, (row, col))
            
        self.piece_count += 2
        if self.piece_count < 8:
            self.drop_phase = True
        else:
            self.drop_phase = False
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
#        print(move)
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
    
    def heuristic_game_value(self, state, piece): # check largest number of pieces connected
        if piece == 'b':
            mine = 'b'
            oppo = 'r'

        elif piece == 'r':
            mine = 'r'
            oppo = 'b'

        # for horizontal
        mymax = 0
        oppmax = 0
        mycnt = 0
        oppcnt = 0

        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == mine:
                    mycnt += 1
            if mycnt > mymax:
                mymax = mycnt
            mycnt = 0
        i=0
        j=0
        for i in range(len(state)):
            for j in range(len(state)):
                if state[i][j] == oppo:
                    oppcnt += 1
            if oppcnt > oppmax:
                oppmax = oppcnt
            oppcnt = 0

        # for vertical
        for i in range(len(state)):
            for j in range(len(state)):
                if state[j][i] == mine:
                    mycnt += 1
            if mycnt > mymax:
                mymax = mycnt
            mycnt = 0
        i=0
        j=0
        for i in range(len(state)):
            for j in range(len(state)):
                if state[j][i] == oppo:
                    oppcnt += 1
            if oppcnt > oppmax:
                oppmax = oppcnt
            oppcnt = 0


        # for / diagonal
        mycnt = 0
        oppcnt = 0

        for row in range(3, 5):
            for i in range(2):
                if state[row][i] == mine:
                    mycnt += 1
                if state[row - 1][i + 1] == mine:
                    mycnt += 1
                if state[row - 2][i + 2] == mine:
                    mycnt += 1
                if state[row - 3][i + 3] == mine:
                    mycnt += 1

                if mycnt > mymax:
                    mymax = mycnt
                mycnt = 0

        row = 0
        i= 0

        for row in range(3, 5):
            for i in range(2):
                if state[row][i] == oppo:
                    oppcnt += 1
                if state[row - 1][i + 1] == oppo:
                    oppcnt += 1
                if state[row - 2][i + 2] == oppo:
                    oppcnt += 1
                if state[row - 3][i + 3] == oppo:
                    oppcnt += 1
                if oppcnt > oppmax:
                    oppmax = oppcnt
                oppcnt = 0

        # for \ diagonal
        mycnt = 0
        oppcnt = 0
        row = 0
        i = 0
        for row in range(2):
            for i in range(2):
                if state[row][i] == mine:
                    mycnt += 1
                if state[row + 1][i + 1] == mine:
                    mycnt += 1
                if state[row + 2][i + 2] == mine:
                    mycnt += 1
                if state[row + 3][i + 3] == mine:
                    mycnt += 1
                if mycnt > mymax:
                    mymax = mycnt
                mycnt = 0

        row = 0
        i = 0
        for row in range(2):
            for i in range(2):
                if state[row][i] == oppo:
                    oppcnt += 1
                if state[row + 1][i + 1] == oppo:
                    oppcnt += 1
                if state[row + 2][i + 2] == oppo:
                    oppcnt += 1
                if state[row + 3][i + 3] == oppo:
                    oppcnt += 1
                if oppcnt > oppmax:
                    oppmax = oppcnt
                oppcnt = 0

        # for diamond
        mycnt = 0
        oppcnt = 0
        row = 0
        i = 0
        for row in range(1,4):
            for i in range(1,4):
                if state[row][i] != ' ':
                    continue
                if state[row-1][i] == mine:
                    mycnt += 1
                if state[row][i + 1] == mine:
                    mycnt += 1
                if state[row + 1][i] == mine:
                    mycnt += 1
                if state[row][i - 1]== mine:
                    mycnt += 1
                if mycnt > mymax:
                    mymax = mycnt
                mycnt = 0

        row = 0
        i = 0
        for row in range(1,4):
            for i in range(1,4):
                if state[row][i] != ' ':
                    continue
                if state[row-1][i] == oppo:
                    oppcnt += 1
                if state[row][i + 1] == oppo:
                    oppcnt += 1
                if state[row + 1][i] == oppo:
                    oppcnt += 1
                if state[row][i - 1]== oppo:
                    oppcnt += 1
                if oppcnt > oppmax:
                    oppmax = oppcnt
                oppcnt = 0

        if mymax == oppmax:
            return 0
        if mymax >= oppmax:
            return mymax/6.0 # if mine is longer than opponent, return positive float

        return (-1) * oppmax/6.0 # if opponent is longer than mine, return negative float
    
    def max_value(self, state, depth, turn):
        s = self.game_value(state)
        if s != 0:
            return s
        elif depth == 0:
            return self.heuristic_game_value(state, self.my_piece)
        elif turn == self.pieces.index(self.my_piece):
            children = self.succ(state,turn)
            max_score = float('-inf')
            for y in children:
                score = self.max_value(y[0],depth-1, (turn+1)%2)
                max_score = max(score, max_score)
#            print(max_score)
            return max_score
        else:
            children = self.succ(state,turn)
            min_score = float('inf')
            for y in children:
                score = self.max_value(y[0],depth-1, (turn+1)%2)
                min_score = min(score, min_score)
#            print(min_score)
            return min_score
                
    
    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == self.my_piece else -1
                    
        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(4,2,-1):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row-3][col-3]:
                    return 1 if state[row][col] == self.my_piece else -1
                
        # TODO: check diamond wins
        for row in range(1,4):
            for col in range(1,4):
                if state[row][col] == ' ' and state[row-1][col] != ' ' and state[row-1][col] == state[row][col-1] == state[row][col+1] == state[row+1][col]:
                    return 1 if state[row][col] == self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = Teeko2Player()
    piece_count = 0
    turn = 0

    # drop phase
    ai.drop_phase = True
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            """
            User input Moves
            """
#            move_made = False
#            ai.print_board()
#            print(ai.opp+"'s turn")
#            while not move_made:
#                player_move = input("Move (e.g. B3): ")
#                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
#                    player_move = input("Move (e.g. B3): ")
#                try:
#                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
#                    move_made = True
#                except Exception as e:
#                    print(e)

            """
            Random Automatic Moves
            """                   
            move = []
            (row, col) = (random.randint(0,4), random.randint(0,4))
            while not ai.board[row][col] == ' ':
                (row, col) = (random.randint(0,4), random.randint(0,4))

            ai.opponent_move([(row, col)])

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2
    
    ai.drop_phase = False
    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            print(move)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            """
            User input Moves
            """
#            move_made = False
#            ai.print_board()
#            print(ai.opp+"'s turn")
#            while not move_made:
#                move_from = input("Move from (e.g. B3): ")
#                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
#                    move_from = input("Move from (e.g. B3): ")
#                move_to = input("Move to (e.g. B3): ")
#                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
#                    move_to = input("Move to (e.g. B3): ")
#                try:
#                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
#                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
#                    move_made = True
#                except Exception as e:
#                    print(e)
                
            """
            Random Automatic Moves
            """
            possible_moves = []
            for r in range(5):
                for c in range(5):
                    if ai.board[r][c] == ai.opp:
                        for i in [-1, 0, 1]:
                            for j in [-1, 0, 1]:
                                if r+i >= 0 and r+i < 5 and c+j >= 0 and c+j < 5 and ai.board[r+i][c+j] == ' ':
                                    possible_moves.append([(r+i, c+j), (r, c)])
            ai.opponent_move(random.choice(possible_moves))

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
