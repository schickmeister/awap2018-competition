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

    def is_perimeter(self, node):
        return not self.is_interior(node)

    def is_interior(self, node, search_tree = None):
        if search_tree is None:
            search_tree = nx.bfs_tree(self.board, node)

        for tree_node in search_tree.successors(node):
            owner = self.board.nodes[tree_node]['owner']
            if owner is None:
                if not self.is_interior(tree_node, search_tree): return False
            if owner is not self.player_num:
                return False

        return True

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