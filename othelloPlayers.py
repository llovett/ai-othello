import othelloBoard

'''You should modify the chooseMove code for the ComputerPlayer
class. You should also modify the heuristic function, which should
return a number indicating the value of that board position (the
bigger the better). We will use your heuristic function when running
the tournament between players.

Feel free to add additional methods or functions.'''

class HumanPlayer:
    '''Interactive player: prompts the user to make a move.'''
    def __init__(self,name,color):
        self.name = name
        self.color = color
        
    def chooseMove(self,board):
        while True:
            try:
                move = eval('(' + raw_input(self.name + \
                 ': enter row, column (or type "0,0" if no legal move): ') \
                 + ')')

                if len(move)==2 and type(move[0])==int and \
                   type(move[1])==int and (move[0] in range(1,9) and \
                   move[1] in range(1,9) or move==(0,0)):
                    break

                print 'Illegal entry, try again.'
            except Exception:
                print 'Illegal entry, try again.'

        if move==(0,0):
            return None
        else:
            return move

def heuristic(board):
    '''This very silly heuristic just adds up all the 1s, -1s, and 0s
    stored on the othello board.'''
    sum = 0
    for i in range(1,othelloBoard.size-1):
        for j in range(1,othelloBoard.size-1):
            sum += board.array[i][j]
    return sum
    

class ComputerPlayer:
    '''Computer player: chooseMove is where the action is.'''
    def __init__(self,name,color,heuristic,plies):
        self.name = name
        self.color = color
        self.heuristic = heuristic
        self.plies = plies

    def _alphaBeta(self,board,depth,color,alpha,beta):
        '''Runs alpha-beta pruning on <board>, probing at <depth>.
        <color>, <alpha>, and <beta> are all used in the recursion,
        and should be set to self.color, -inf, +inf respectively when
        calling this function for the first time.

        Returns a tuple (heuristic_value, move_row_and_column_pair)
        '''
        greatest = lambda x,y:x if x[0] > y[0] else y
        least = lambda x,y:x if x[0] < y[0] else y

        # Calculate all possible moves from this point
        moves = []
        for i in xrange(1,othelloBoard.size-1):
            for j in xrange(1,othelloBoard.size-1):
                move = board.makeMove(i,j,color)
                if move:
                    moves.append( (self.heuristic(move), (i,j)) )

        # Pass if no moves available
        if len(moves) < 1:
            return [(self.heuristic(board), (0,0))]

        # depth == 1 is the leaf condition
        if depth == 1:
            return [reduce(greatest if color == self.color else least, moves)]

        # If it's our ply
        if color == self.color:
            greatestValue = float('-inf')
            greatestMove = None
            # lookahead "looks ahead" in the recursion to find the best move
            lookahead = None
            for move in moves:
                lookahead = self._alphaBeta(board.makeMove(move[1][0],move[1][1],color),
                                            depth-1,
                                            color*-1,
                                            alpha,
                                            beta)
                # Compare heuristic value from the recursive call we
                # just made to the greatest one we've found so far
                h = lookahead[-1][0]
                if h > greatestValue:
                    greatestValue = h
                    greatestMove = lookahead[-1][1]
                # Prune if our greatest value exceeds beta value
                if greatestValue >= beta:
                    lookahead.append( (greatestValue, greatestMove) )
                    return lookahead
                alpha = max(alpha, greatestValue)
            lookahead.append( (greatestValue, greatestMove) )
            return lookahead

        # The opponent's ply
        leastValue = float('inf')
        leastMove = None
        lookahead = None
        for move in moves:
            lookahead = self._alphaBeta(board.makeMove(move[1][0],move[1][1],color),
                                        depth-1,
                                        color*-1,
                                        alpha,
                                        beta)
            h = lookahead[-1][0]
            if h < leastValue:
                leastValue = h
                leastMove = lookahead[-1][1]
            if leastValue <= alpha:
                lookahead.append( (leastValue, leastMove) )
                return lookahead
            beta = min(beta, leastValue)
        lookahead.append( (leastValue, leastMove) )
        return lookahead
                
    def chooseMove(self,board):
        '''Choose a move based on heuristic values supplied by _alphaBeta'''
        plySequence = self._alphaBeta(board,self.plies,self.color,float('-inf'),float('inf'))
        print "computers best move sequence is ",plySequence

        return plySequence[-1][1]
