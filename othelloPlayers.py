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

# Some globals
timesCalled = 0
curVal = 0
def alexaHeuristic(board):
    global timesCalled
    timesCalled += 1
    if timesCalled % 5 == 0:
        global curVal
        curVal += 1
    return curVal
    
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

        Returns the heuristic value of the greatest move we can expect to achieve on <board>.
        '''
        # Calculate all possible moves from this point
        moves = []
        for i in xrange(1,othelloBoard.size-1):
            for j in xrange(1,othelloBoard.size-1):
                move = board.makeMove(i,j,color)
                if move:
                    moves.append( (i,j) )

        # if len(moves) < 1:
        #     print "no moves available...."
        #     board.display()

        # depth == 0 is the leaf condition
        if depth == 0:
            print "reached a leaf"
            return self.heuristic(board)

        # Opponent's ply
        if color != self.color:
            print "Max player"
            greatestValue = float('-inf')
            for move in moves:
                # Max heuristic value through recursion
                lookahead = self._alphaBeta(board.makeMove(move[0],move[1],color),
                                            depth-1,
                                            color*-1,
                                            alpha,
                                            beta)
                print "move %s gives value %f"%(str(move),lookahead)
                # Compare heuristic value from the recursive call we
                # just made to the greatest one we've found so far
                if lookahead > greatestValue:
                    greatestValue = lookahead
                # Prune if our greatest value exceeds beta value
                if greatestValue >= beta:
                    print "** MAX is PRUNING ** ... greatestValue=%f, beta=%f"%(greatestValue,beta)
                    return greatestValue
                alpha = max(alpha, greatestValue)
            return greatestValue

        # Our ply
        print "Min player"
        leastValue = float('inf')
        for move in moves:
            # Min heuristic value through recursion
            lookahead = self._alphaBeta(board.makeMove(move[0],move[1],color),
                                        depth-1,
                                        color*-1,
                                        alpha,
                                        beta)
            print "move %s gives value %f"%(str(move),lookahead)
            if lookahead < leastValue:
                leastValue = lookahead
            if leastValue <= alpha:
                print "** MIN is PRUNING ** ... leastValue=%f, alpha=%f"%(leastValue,alpha)
                return leastValue
            beta = min(beta, leastValue)
        return leastValue
                
    def chooseMove(self,board):
        '''Choose a move based on heuristic values supplied by _alphaBeta'''
        # Choose the move that returns the greatest heuristic value through alpha beta
        ourMove = None
        minUtility = float('inf')
        ourAlpha = float('-inf')
        ourBeta = float('inf')
        for i in xrange(1,othelloBoard.size-1):
            for j in xrange(1,othelloBoard.size-1):
                move = board.makeMove(i,j,self.color)
                if move:
                    print "Min player... trying position %s"%str((i,j))
                    value = self._alphaBeta(move, self.plies-1, self.color*-1, ourAlpha, ourBeta)
                    minUtility = min(value, minUtility)
                    if minUtility <= ourAlpha:
                        return (i,j)
                    if minUtility < ourBeta:
                        ourBeta = minUtility
                        ourMove = (i,j)

        print "heuristic was called %d times"%timesCalled
        return ourMove
