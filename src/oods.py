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
        self.set_perimeter_nodes()
        recruit_diffs, sorted_nodes = self.get_perimeter_priority()

        nodes_to_fill = list(filter(lambda x: recruit_diffs[x] >= 0,
                                    sorted_nodes))

        nodes_to_fill.append(self.attack_node)
        for node in nodes_to_fill:
            if recruit_diffs[node] > self.max_units:
                self.place_unit(node, recruit_diffs[node])
            else:
                self.place_unit(node, self.max_units)
                break

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

        if self.board.nodes[self.target_node]['owner'] is None:
            our_units = self.board.nodes[self.attack_node]['old_units']
            their_units = self.board.nodes[self.target_node]['old_units']

            if (our_units > their_units):
                self.board.nodes[self.target_node]['owner'] = self.player_num

                if not self.is_perimeter(self.target_node):
                    self.move(self.attack_node, self.target_node,
                              their_units + 1)

                elif not self.is_perimeter(self.attack_node):
                    self.move(self.attack_node, self.target_node,
                              our_units - 1)

                else:
                    self.move()


        return self.dict_moves #Returns moves built up over the phase. Do not modify!
