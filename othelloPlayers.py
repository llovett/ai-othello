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

        # depth == 1 is the leaf condition
        if depth == 1:
            if len(moves) < 1:
                # Pass if no moves available
                return self.heuristic(board), (0,0)
            return reduce(greatest if color == self.color else least, moves)

        # If it's our ply
        if color == self.color:
            greatestValue = float('-inf')
            greatestMove = None
            bestMove = None
            for move in moves:
                lookahead = _alphaBeta(move,depth-1,color*-1,alpha,beta)[0]
                if lookahead[0] > greatestValue:
                    greatestValue = lookahead[0]
                    greatestMove = lookahead[1]
                if greatestValue >= beta:
                    return greatestValue
                alpha = max(alpha, greatestValue)
            return greatestValue, greatestMove

        # The opponent's ply
        leastValue = float('inf')
        leastMove = None
        for move in moves:
            lookahead = _alphaBeta(move,depth-1,color*-1,alpha,beta)
            if lookahead[0] < leastValue:
                leastValue = lookahead[0]
                leastMove = lookahead[1]
            if leastValue <= alpha:
                return leastValue
            beta = min(beta, leastValue)
        return leastValue, leastMove
                
    def chooseMove(self,board):
        '''Choose a move based on heuristic values supplied by _alphaBeta'''
        return self._alphaBeta(board,self.plies,self.color,float('-inf'),float('inf'))[1]
