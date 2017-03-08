
"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))

def improved_score_with_distance_from_center_effect(game, player):
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    
    center_x=(game.width-1)/2.0
    center_y=(game.height-1)/2.0
    center_x_d=game.get_player_location(player)[0]-center_x
    center_y_d=game.get_player_location(player)[1]-center_y
    center_d=(center_x_d**2+center_y_d**2)
    max_distance=(((game.width-1)/2.0)**2+((game.height-1)/2.0)**2)
    distance_factor=1-center_d/(max_distance+1)
    
    #return float(own_moves - opp_moves)+distance_factor
    return float(own_moves)-opp_moves+distance_factor


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


    return improved_score_with_distance_from_center_effect(game, player)

def best_score_move(scores,maximizing_player):
    #find best score/move
    #yes there is probably a lambda thingy which makes the same thing in one line
    #but this I understand well, lambda thingies not so well
    best_score,best_move=scores[0]
    for score,m in scores:
        if maximizing_player:
            if score > best_score:
                best_score=score
                best_move=m
        else:
            if score < best_score:
                best_score=score
                best_move=m
                
    return best_score,best_move


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        if not legal_moves:
               return (-1, -1)
            #_, move = max([(self.score(game.forecast_move(m), self), m) for m in legal_moves])
            
        best_move=legal_moves[0]
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            
            

            search_depth=self.search_depth
            iterative=self.iterative
            
            #if it's iterative, we always start at search depth 0 and search indefinitely
            #untill timeout
            #if it's not iterative, we just search at the provided search depth
            current_search_depth=0
            while True:

                if not iterative:
                    current_search_depth=search_depth
                
                scores=[]            
                for m in legal_moves:
                    
                    
    
                    #Maximizing set to false because as we have already 
                    #forcasted our move, so in game.forecast_move(m),
                    #it's the opponent turn to play
                    if self.method=="alphabeta":
                        score,move=self.alphabeta(game.forecast_move(m), current_search_depth,0,game.width*game.height, False)
                    else:
                        score,move=self.minimax(game.forecast_move(m), current_search_depth, False)
                    
                    scores.append([score,m])
                    
                #find the maximum score and corresponding move
                best_score,best_move=best_score_move(scores,True)
                        
                #will go on deeper indefinitely if it's iterative search
                #else we will stop because we searched at the specified search_depth
                if iterative:
                    current_search_depth=current_search_depth+1
                else:
                    return best_move
    
            
            

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move
            pass

        # Return the best move from the last completed search iteration





    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()
            
        #if depth is 0, it is a leaf in the tree, and we just return the score of our player
        #note that I also return the location of the player that made the last move
        #which can be the location of our player or the opponent depending on who has played last
        if (depth == 0):
            score=self.score(game,self)
            m=game.get_player_location(game.inactive_player)
            return score,m
 

        legal_moves=game.get_legal_moves()      
        
        #if there is no moves possible, return our score and -1,-1 as location   
        if not legal_moves:
            return self.score(game,self),(-1,-1)
       
        scores=[]
        for m in legal_moves:
            #we alternate maximizing and minimizing levels, that's why maximizing is negated
            child_score,child_move=self.minimax(game.forecast_move(m), depth-1, not maximizing_player)
            scores.append([child_score,m])
            
        #find the best score and corresponding move
        best_score,best_move=best_score_move(scores,maximizing_player)

        return best_score,best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        #if depth is 0, it is a leaf in the tree, and we just return the score of our player
        #note that I also return the location of the player that made the last move
        #which can be the location of our player or the opponent depending on who has played last
        if (depth == 0):
            score=self.score(game,self)
            m=game.get_player_location(game.inactive_player)
            return score,m
 

        legal_moves=game.get_legal_moves()       
        
        #if there is no moves possible, return our score and -1,-1 as location        
        if not legal_moves:
            return self.score(game,self),(-1,-1)
        
        scores=[]         
        for m in legal_moves:
            #we alternate maximizing and minimizing levels, that's why maximizing is negated
            child_score,child_move=self.alphabeta(game.forecast_move(m), depth-1,alpha,beta, not maximizing_player)
            scores.append([child_score,m])
            
            if maximizing_player:
                
                if child_score<beta:
                    #just not the best move possible.
                    #continue to search to see is there is a better one in this branch
                    pass
                if child_score==beta:
                    #that's the bests possible score, we can stop here
                    break
                if child_score>beta:
                    #now that I write a comment here, I'm not sure why this happens
                    #and why I should break here.
                    #probably because the node above is a minimizing node and this is 
                    #the opponent turn, so we don't really want his score to be so high?
                    #Yes. That's must be it. Another branch has a lower score for us.
                    #So the opponent will chose this other branch, not this one.
                    #So no need to continue searching.
                    break
                                     
                if child_score>alpha:
                    #we're maximizing, so this is a new lower bound
                    alpha=child_score
                if child_score<alpha:
                    #now that I write a comment here, I wonder if something special
                    #should happen here...
                    #unit tests fails if we break
                    pass                    
                if child_score==alpha:
                    #worst move possible, but it happens... Nothing special to do
                    #units tests fails if we break
                    pass
                
            #if minimizing level
            if not maximizing_player:
                
                if child_score<beta:
                    #we're minimizing, so this is a new upper bound
                    beta=child_score
                if child_score>beta:
                    #now that I write a comment here, I'm not sure why this happens
                    #and maybe something special should happen here...
                    ###! unit tests doesnt fail if we break
                    pass
                if child_score==beta:
                    #just not a good move from our player point of view
                    #unit tests fails if we break
                    pass
                
                if child_score==alpha:
                    #ok, that's a bad score, no need to search the other branches, even if
                    #another have a better score, this is the one the opponent will chose
                    break
                if child_score>alpha:
                    #just not the worst move, lets see the other nodes...
                    pass
                if child_score<alpha:
                    #this move is so bad, that it's even lower than another branch we already search
                    break
                    
        best_score,best_move=best_score_move(scores,maximizing_player)

        return best_score,best_move