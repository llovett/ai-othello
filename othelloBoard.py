import copy
import othelloPlayers

# Constant values used throughout the code
white = 1
black = -1
empty = 0
size = 10

class OthelloBoard:
    '''An Othello board, with a variety of methods for managing a game.'''
    
    def __init__(self,array=None):
        '''If the parameter 'board' is left out, then the game board
        is initialized to its typical starting postion. Alternatively,
        a two-dimensional list with a pre-existing starting position
        can be supplied as well. Note that the size of the board is
        10x10, instead of 8x8; this is because leaving a blank ring
        around the edge of the board makes the rest of the code much
        simpler.'''
        if array:
            self.array = array
        else:
            self.array = [[empty]*size for i in range(size)]
            self.array[4][4] = white
            self.array[5][5] = white
            self.array[4][5] = black
            self.array[5][4] = black

    def display(self):
        '''Displays the current board to the terminal window, with
        headers across the left and top. While some might accuse this
        text output as being "old school," having a scrollable game
        history actually makes debugging much easier.'''
        print '  ',
        for i in range(1,9):
            print i,
        print
        print
        for i in range(1,size-1):
            print i, '',
            for j in range(1,size-1):
                if self.array[i][j] == white:
                    print 'W',
                elif self.array[i][j] == black:
                    print 'B',
                else:
                    print '-',
            print

    def makeMove(self,row,col,piece):
        ''' Returns None if move is not legal. Otherwise returns an
        updated OthelloBoard, which is a copy of the original.'''

        # A move cannot be made if a piece is already there.
        if self.array[row][col] != empty:
             return None

        # A move cannot be made if the piece "value" is not black or white.
        if piece != black and piece != white:
            return None

        # Make a copy of the board (not just the pointer!)
        bcopy = copy.deepcopy(self.array)
        bcopy[row][col] = piece

        # Ranges for use below
        rowup = range(row+1,size)
        rowdown = range(row-1,-1,-1)
        rowfixed = [row for i in range(size)]
        colup = range(col+1,size)
        coldown = range(col-1,-1,-1)
        colfixed = [col for i in range(size)]

        # Set up ranges of tuples representing all eight directions.
        vectors = [zip(rowup,coldown),zip(rowup,colfixed), \
                zip(rowup,colup), zip(rowdown,coldown), \
                zip(rowdown, colfixed), zip(rowdown,colup), \
                zip(rowfixed,coldown), zip(rowfixed,colup)]

        # Try to make a move in each direction. Record if at least one
        # of them succeeds.
        flipped = False
        for vector in vectors:

            # Determine how far you can go in this direction. If you
            # see the opponent's piece, that's a candidate for
            # flipping: count and keep moving. If you see your own
            # piece, that's the end of the range and you're done. If
            # you see a blank space, you must not have had one of your
            # own pieces on the other end of the range.
            count = 0
            for (r,c) in vector:
                if bcopy[r][c] == -1*piece:
                    count += 1
                elif bcopy[r][c] == piece:
                    break
                else:
                    count = 0
                    break

            # If range is nontrivial, then it's a successful move.
            if count > 0:
                flipped = True

            # Actually record the flips.
            for i in range(count):
                (r,c) = vector[i]
                bcopy[r][c] = piece

        if flipped:
            return OthelloBoard(bcopy)
        else:
            return None
             
                         
    def _legalMoves(self,color):
        '''To be a legal move, the space must be blank, and you must take at
        least one piece. Note that this method works by attempting to
        move at each possible square, and recording which moves
        succeed. Therefore, using this method in order to try to limit
        which spaces you actually use in makeMoves is futile.'''
        moves = []
        for i in range(1,size-1):
            for j in range(1,size-1):
                bcopy = self.makeMove(i,j,color)
                if bcopy != None:
                    moves.append((i,j))
        return moves

    def scores(self):
        '''Returns a list of black and white scores for the current board.'''
        score = [0,0]
        for i in range(1,size-1):
            for j in range(1,size-1):
                if self.array[i][j] == black:
                    score[0] += 1
                elif self.array[i][j] == white:
                    score[1] += 1
        return score


    def playGame(self):
        '''Manages playing an actual game of Othello.'''
        
        print 'Black goes first.'
        # Two player objects: [black, white]
        players=[None,None]
        colorNames = ('black','white')
        colorValues = (black,white)
        invalidPasses = [0,0]
        illegalMoves = [0,0]

        # Determine whether each player is human or computer, and
        # instantiate accordingly
        for i in range(2):
            response = raw_input('Should ' + colorNames[i] + \
                             ' be (h)uman or (c)omputer? ')
            if response.lower() == 'h':
                name = raw_input("What is the player's name? ")
                players[i] = othelloPlayers.HumanPlayer(name,colorValues[i])
            else:
                plies = int(raw_input("How many plies ahead " + \
                                  "should the computer look? "))
                players[i] = othelloPlayers.ComputerPlayer(
                               'compy' + colorNames[i],colorValues[i],
                               othelloPlayers.alexaHeuristic,plies)

        # Number of times a "pass" move has been made, in a row
        passes = 0

        done = False
        curBoard = self
        while not done:

            # Black goes, then white
            for i in range(2):

                # Display board and statistics
                curBoard.display()
                scores = curBoard.scores()
                print 'Statistics: score / invalid passes / illegal moves'
                for j in range(2):
                    print colorNames[j] + ':',scores[j], '/', \
                          invalidPasses[j], '/',illegalMoves[j]
                print
                print 'Turn:',colorNames[i]

                # Obtain move that player makes
                move = players[i].chooseMove(curBoard)

                if move==None:
                    # If no move is made, that is considered a
                    # pass. Verify that there were in fact no legal
                    # moves available. If there were, allow the pass
                    # anyway (this is easier to code), but record that
                    # an invalid pass was taken.

                    passes += 1
                    print colorNames[i] + ' passes.'
                    legalMoves=curBoard._legalMoves(colorValues[i])
                    if legalMoves != []:
                        print colorNames[i] + \
                              ' passed, but there was a legal move.'
                        print 'Legal moves: ' + str(legalMoves)
                        invalidPasses[i] += 1
                else:
                    # If a move is made, make the move on the
                    # board. makeMove returns None if the move is
                    # illegal. Record as an illegal move, and forfeit
                    # the player's turn. This is easier to code than
                    # offering another turn.

                    passes = 0
                    print colorNames[i] + ' chooses ' + str(move) + '.'
                    bcopy = curBoard.makeMove(move[0],move[1],colorValues[i])
                    if bcopy==None:
                        print 'That move is illegal, turn is forfeited.'
                        illegalMoves[i] += 1
                    else:
                        curBoard = bcopy
                print

                # To keep code simple, never test for win or loss; if
                # one player has won, lost, or tied, two passes must
                # occur in a row.
                if passes == 2:
                    print 'Both players passed, game is over.'
                    done = True
                    break

        # Display final outcome
        scores = curBoard.scores()
        if scores[0] > scores[1]:
            print 'Black wins!'
        elif scores[1] > scores[0]:
            print 'White wins!'
        else:
            print 'Tie game!'

if __name__=='__main__':
    OthelloBoard().playGame()
