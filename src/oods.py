from base_player import BasePlayer
import networkx as nx
import math
import random

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

    def calc_new_perimeter_nodes(self,new_node):
        temp = self.board.nodes[new_node]['owner']
        self.board.nodes[new_node]['owner'] = self.player_num
        results = []
        my_nodes = list(self.nodes.keys())
        my_nodes.append(new_node)
        for node in my_nodes:
            if self.is_perimeter(node):
                results.append(node)
        self.board.nodes[new_node]['owner'] = temp
        return results


    def set_target(self):
        #TODO: Don't break when we frickin wreck everybody else
        perim_nodes = self.perimeter_nodes.keys()
        perim_neighbors = []
        for pn in perim_nodes:
            perim_neighbors += self.board.neighbors(pn)
        not_mine_perim_neighbors = self.not_me(perim_neighbors)
        random.shuffle(not_mine_perim_neighbors)
        self.target_node = min(not_mine_perim_neighbors,key=lambda x:len(self.calc_new_perimeter_nodes(x)))

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
        self.set_perimeter_nodes()
        self.set_target()
        self.set_attack_node()

        recruit_diffs, sorted_nodes = self.get_perimeter_priority()

        nodes_to_fill = list(filter(lambda x: recruit_diffs[x] >= 0,
                                    sorted_nodes))

        for node in nodes_to_fill:
            if recruit_diffs[node] > self.max_units:
                self.place_unit(node, recruit_diffs[node])
            else:
                self.place_unit(node, self.max_units)
                break

        if self.max_units > 0:
            #Fill up our attack node
            self.place_unit(self.attack_node, self.max_units)

        """
        Insert player logic here to determine where to place your units
        """

        return self.dict_moves #Returns moves built up over the phase. Do not modify!

    def make_attacks(self, attack_node, target_node):
        our_units = self.board.nodes[attack_node]['old_units']
        their_units = self.board.nodes[target_node]['old_units']

        if (our_units > their_units + 1):
            self.board.nodes[target_node]['owner'] = self.player_num
            target_is_perimeter = self.is_perimeter(target_node)
            attack_is_perimeter = self.is_perimeter(attack_node)
            self.board.nodes[target_node]['owner'] = None


            if not target_is_perimeter:
                self.move_unit(attack_node, target_node,
                          their_units + 1)

            elif not attack_is_perimeter:
                self.move_unit(attack_node, target_node,
                          our_units - 1)

            else:
                target_enemies = self.get_enemy_neighbor_sum(target_node)
                attack_enemies = self.get_enemy_neighbor_sum(attack_node)
                total_enemies = target_enemies + attack_enemies

                leftover_units = our_units - their_units - 2
                if (total_enemies != 0):
                    fraction_to_give = target_enemies / total_enemies
                else:
                    fraction_to_give = 0.5

                number_to_give = math.floor(fraction_to_give
                                            * leftover_units)
                number_to_move = their_units + 1 + number_to_give

                self.move_unit(attack_node, target_node,
                          number_to_move)

    """
    Called during the move phase to request player moves
    """
    def player_move_units(self):
        """
        Insert player logic here to determine where to move your units
        """

        #if self.board.nodes[self.target_node]['owner'] is None:

        self.make_attacks(self.attack_node, self.target_node)
        for node in self.perimeter_nodes:
            for neighbor in self.board.neighbors(node):
                if self.board.nodes[neighbor]['owner'] != self.player_num:
                    self.make_attacks(node, neighbor)

        return self.dict_moves #Returns moves built up over the phase. Do not modify!
