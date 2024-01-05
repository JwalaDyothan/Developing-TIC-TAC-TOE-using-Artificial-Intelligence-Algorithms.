

import numpy as np
import time
from random import choice
import copy

TIME_OUT = 3 # in seconds
TUNNING_CONST = 1.4 # tunning between exploration & exploitation
INF = 1000000 # to simulate infinite
WIN_REWARD = 1
DRAW_REWARD = 0
LOSS_REWARD = -1
SIM_NBR = 5000 # approximately 4000 to converge

class Board(object):
    
    def __init__(self):
        self.board = np.full((3,3), '-')
        self.current_player = '-'
        self.winner = ''
         
    def game_over(self,board):
        
        # Ligne checking
        
        if board[0,0] == board[0,1] == board[0,2]!= '-':
            return True, board[0,0]
        
        if board[1,0] == board[1,1] == board[1,2]!= '-':
            return True, board[1,0]
        
        if board[2,0] == board[2,1] == board[2,2]!= '-':
            return True, board[2,0]
        
        # column checking
        
        if board[0,0] == board[1,0] == board[2,0]!= '-':
            return True, board[0,0]
        
        if board[0,1] == board[1,1] == board[2,1]!= '-':
            return True, board[0,1]
        
        if board[0,2] == board[1,2] == board[2,2]!= '-':
            return True, board[2,2]
        
        # Diagnol checking
        
        if board[0,0] == board[1,1] == board[2,2] != '-':
            return True, board[0,0]
        
        if board[0,2] == board[1,1] == board[2,0]!= '-':
            return True, board[0,2]
        
        #TODO performance issue
        if np.size(board[board[:,:]=='-']) == 0:
            return True, '-'
        
        return False, '*'
        
    def get_current_player(self):
        return self.current_player
    
    
    def is_board_full(self):
        is_full_board = np.argwhere(self.board[:,:]=='-')
        np.reshape(is_full_board,(np.size(is_full_board),1))
        
        if np.size(is_full_board) != 0:
            return True
        else:
            return False

    def print_board(self):
        print(self.board[0,0] + ' ' +self.board[0,1] + ' ' +self.board[0,2])
        print(self.board[1,0] + ' ' +self.board[1,1] + ' ' +self.board[1,2])
        print(self.board[2,0] + ' ' +self.board[2,1] + ' ' +self.board[2,2])
        print('\n')
    
    def update_board(self,player):

        player_move = input()
        
        if self.board[int(player_move[0]), int(player_move[2])] == '-':
            self.board[int(player_move[0]), int(player_move[2])] = player
            return (player_move[0], player_move[2])
        else:
            print("Wrong MOVE !")
            return
    
    @staticmethod
    def update(move,current_move,board):

        if board[int(move[0]), int(move[1])] == '-':
            board[int(move[0]), int(move[1])] = current_move
            if current_move =='X':
                return 'O'
            else:
                return 'X'   
        else:1,
            print("Wrong MOVE !")
            return
    
    @staticmethod
    def get_actions(board):
        available_actions = np.argwhere(board[:,:]=='-')
        np.reshape(available_actions,(np.size(available_actions),1))
        return available_actions    
    
    @staticmethod
    def get_board(board,move,player):
        copy_board = copy.deepcopy(board)  
        copy_board[int(move[0]), int(move[1])] = player
        return copy_board
    
class Node():
    
    def __init__(self,value,visits,parent=None):
        
        self.player = '-'
        self.value = value
        self.visits = visits
        self.parent = parent
        self.childs = {}
        self.board_state = np.full((3,3),'-')
    
    # setters
    
    def set_board_state(self,board):
        self.board_state = np.copy(board)
  
    def set_childs(self,action,node):
        self.childs.update({action:node})
        
    def set_value(self,value):
        self.value = value
     
    def set_player(self,*root):
        if self.parent == None:
            self.player = root[0]
        elif self.parent.get_player() == 'X':
            self.player = 'O'
        else:
            self.player = 'X'
            
    
    def set_visits(self,visits):
        self.visits = visits
    
    def set_parent(self,parent):
        self.parent = parent
        
    def init_childs(self):
        self.childs = {}
        
    # Getters
        
    def get_childs(self):
        return self.childs
        
    def get_value(self):
        return self.value
    
    def get_visits(self):
        return self.visits
    
    def get_player(self):
        return self.player

    
    def get_parent(self):
        return self.parent
    
    def get_board_state(self):
        return self.board_state
    
    def back_propagate(self,result,player):
        
        self.set_visits(self.get_visits()+1)
        
        if result == '-':
            self.set_value(self.get_value()+DRAW_REWARD) 
            
        elif self.get_player() != result:
            self.set_value(self.get_value()+WIN_REWARD)
            
        elif self.get_player() == result:
            self.set_value(self.get_value()+LOSS_REWARD)
            
        if self.get_parent():
            self.parent.back_propagate(result,player)
        

class MonteCarlo():
    
    def __init__(self,board):
        
        #self.MCTS = []
        self.board = board
        self.root = Node(0,0)
        self.current_node = self.root
    
    def init_root(self,current_player):

        self.root.set_board_state(self.board.board)
        self.root.init_childs()
        self.root.set_player(current_player)
        self.root.value = 0
        self.root.visits = 0
    
    def expand(self,node):
        
        # get first actions for board_state
        actions = self.board.get_actions(node.board_state)
        for k in actions:
            node.set_childs((k[0],k[1]),'')
            
        # create node for each action
        childs = node.get_childs()
        for action in childs:
            child = Node(0,0)
            child.set_parent(node)
            child.set_player()
            child.set_board_state(self.board.get_board(
                                    node.get_board_state(),action,node.get_player()))
            node.set_childs(action,child)
            #self.MCTS.append(child)
    
    def select(self,node):
        
        # select the best child of the current node
        max_ucb1 = -INF
        
        for action,child in node.get_childs().items():
            if max_ucb1 < self.calculate_ucb1(child):
                max_ucb1 = self.calculate_ucb1(child)
                self.current_node = child
    
    def simulate(self,node):

        # get the board state to simulate
        board_state = np.copy(node.get_board_state())
        # set the current player for this board state
        player = node.get_player()
        # test if the state is already an end of game
        finished,result = self.board.game_over(board_state)
        print('result = ', result)
        if finished == False:
            while True:
                actions = self.board.get_actions(board_state)
                random_move = choice(actions)
                player = self.board.update(random_move,player,board_state)
                finished,result = self.board.game_over(board_state)
                if finished:
                    break
        print('result = ', result,'player : ', player)

        return result,player

    
    def update(self,node):
        result,player = self.simulate(node)
        # update visits for current node and all its parents
        node.back_propagate(result,player)
                            
        print('root value = ', self.root.get_value())
    
    def calculate_ucb1(self,node):
        try:
            ucb1 = node.get_value()/node.get_visits() + TUNNING_CONST*np.sqrt(np.log(node.parent.get_visits())/node.get_visits())
        except:
            ucb1 = INF
        return ucb1
   
    def play(self,previous_move,player):
        
        # check if state is already existing in MCTS
        
        #FIXME: OPTIMIZATION AXE use pre-calculated value of states 
        #TODO: OPTIMIZATION AXE MCTS[0] must contain last added node
        # use previous nodes in the next move
        # for node in self.MCTS:
        #     if node.get_board_state == self.board.board:
        #         self.root = node
        #         break
        
        # initialize root for each turn (new tree is created)
        self.init_root(self.board.get_current_player())
        # add all childs and get actions for the board state
        self.expand(self.root)
        self.current_node = self.root
               
        games=0
        # while games < SIM_NBR :
        start = time.time()
        while time.time()-start < TIME_OUT:
            
            #select the best child by maximizing UCB1 and store it in current_node(override it)
            #the variable current_node is used to navigate in the tree
            self.select(self.current_node)
            # test if current_node is a Leaf
            #TODO : look for best way to make this condition
            if np.size(list(self.current_node.get_childs().values())) == 0:
                over, r = self.board.game_over(self.current_node.get_board_state())
                print('over = ',over)
                if self.current_node.get_visits() == 0 or over == True:
                    #Simulate node and update values/visits of all parents
                    self.update(self.current_node)
                    games+=1
                else:
                    # print('current_node_state to expand :',self.current_node.get_board_state())
                    # Create and add all childs of current_node in the tree(MCTS)
                    self.expand(self.current_node)
                    # select the best child by maximizing UCB1
                    self.select(self.current_node)
                    # simulate current_node and update values/visits of all his parents
                    self.update(self.current_node)
                    games+=1
                # when we finish a simulation we go back again to the root of the tree
                self.current_node = self.root
        
        
        # Printing stats of nodes
        next_nodes = list(self.root.get_childs().values())
        k=0
        for n in next_nodes:
            k+=1
            print(k,'value =',n.get_value(),'visits =',n.get_visits())
        
        #  select the best move
        
        best_win_rate = -INF
        for action,next_node in self.root.get_childs().items():
            if best_win_rate <= next_node.get_value()/next_node.get_visits():
                best_win_rate = next_node.get_value()/next_node.get_visits()
                move = action

        print('root value : ',self.root.get_value(),'\nroot visits :',self.root.get_visits())
        print('games simulated : ', games)
        return move
                        

               
board = Board()   
agent = MonteCarlo(board)

turn_X = True

while True:

    if turn_X:
        board.current_player = 'X'
        turn_X = False
    else:  
        board.current_player = 'O'
        turn_X = True

    print('Turn : ', board.current_player + '\n')
    board.print_board()
    #TODO risk implementation
    if board.current_player == 'X':
        move_x = board.update_board(board.current_player)
    else:
        move = agent.play(move_x,board.current_player)
        print('Monty plays : ',move)
        board.board[move[0], move[1]] = 'O'

    over,result = board.game_over(board.board)

    if over != False:
        board.print_board()
        if result == '-':
            print('Draw !')
            break
        else:
            print(result + 'Won the game !')
            break
        break