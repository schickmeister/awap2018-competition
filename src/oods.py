from base_player import BasePlayer
import networkx as nx

class Player(BasePlayer):

    """
    You will implement this class for the competition.
    You can add any additional variables / methods in this file.
    Do not modify the class name or the base class and do not modify the lines marked below.
    """

    def __init__(self, p_id):
        super().__init__(p_id)  #Initializes the super class. Do not modify!

        self.perimeter_nodes = dict()

        """
        Insert player-specific initialization code here
        """
        return

    def is_perimeter(self,node):
        return self.search_enemy(node,nx.bfs_tree(self.board,node)) != None

    def search_enemy(self,node,search_tree):
        results = []
        for tnode in search_tree.successors(node):
            owner = self.board.nodes[tnode]['owner']
            if owner == self.player_num:
                continue
            elif owner == None:
                results.append(self.search_enemy(tnode,search_tree))
            else:
                return tnode
        L = list(filter(lambda x:x != None,results))
        if L != []:
            return L[0]
        else:
            return None

    def get_enemy_neighbor_sum(self, node):
        neighbor_sum = 0
        for neighbor in self.board.neighbors(node):
            own_node = self.board.nodes[neighbor]['owner'] == self.player_num
            blank_node = self.board.nodes[neighbor]['owner'] == None

            if not (own_node or blank_node):
                neighbor_sum += self.board.nodes[neighbor]['old_units']

        print("Node %d (%d)" % (node, neighbor_sum))

    def get_perimeter_nodes(self):
        self.perimeter_nodes = dict() #Reset perimeter
        for node in self.nodes:
            if self.is_perimeter(node):
                self.perimeter_nodes[node] = 0

    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        """
        Insert any player-specific turn initialization code here
        """

        self.get_perimeter_nodes()
        print(list(self.perimeter_nodes.keys()))
        return


    """
    Called during the placement phase to request player moves
    """
    def player_place_units(self):
        self.get_perimeter_nodes()
        """
        Insert player logic here to determine where to place your units
        """

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
