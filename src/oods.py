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
        # self.possible_attacks = dict()

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

        return neighbor_sum

    def set_perimeter_nodes(self):
        self.perimeter_nodes = dict() #Reset perimeter
        for node in self.nodes:
            if self.is_perimeter(node):
                self.perimeter_nodes[node] = 0


    def get_recruit_diffs(self):
        recruit_diffs = dict()
        for node in self.perimeter_nodes:
            current_units = self.board.nodes[node]['old_units']
            neighbor_sum = self.get_enemy_neighbor_sum(node)
            recruit_diffs[node] = neighbor_sum - current_units
        return recruit_diffs

    def get_perimeter_priority(self):
        recruit_diffs = self.get_recruit_diffs()
        sorted_nodes = sorted(recruit_diffs.keys(),
                              key=lambda x: -recruit_diffs[x])
        return (recruit_diffs, sorted_nodes)

    def not_me(self,nodes):
        return list(filter(lambda x:self.board.nodes[x]['owner'] != self.player_num,nodes))

    def are_me(self,nodes):
        return list(filter(lambda x:self.board.nodes[x]['owner'] == self.player_num,nodes))

    def set_target(self):
        perim_nodes = self.perimeter_nodes.keys()
        perim_neighbors = []
        for pn in perim_nodes:
            perim_neighbors += self.board.neighbors(pn)
        not_mine_perim_neighbors = self.not_me(perim_neighbors)
        self.target_node = min(not_mine_perim_neighbors,key=lambda x:len(self.not_me(self.board.neighbors(x))))

    def set_attack_node(self):
        target_neighbors = self.are_me(self.board.neighbors(self.target_node))
        mapped = map(lambda x: (x,self.board.nodes[x]['old_units']-self.get_enemy_neighbor_sum(x)),target_neighbors)
        a_node,a_node_diff = max(mapped,key=lambda x:x[1])
        self.attack_node = a_node

    """
    Called at the start of every placement phase and movement phase.
    """
    def init_turn(self, board, nodes, max_units):
        super().init_turn(board, nodes, max_units)       #Initializes turn-level state variables
        """
        Insert any player-specific turn initialization code here
        """

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
