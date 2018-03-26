#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ep.py
#  author: Srinath
#  Elance Profile: https://www.elance.com/s/fantasticcoder/, https://www.elance.com/s/nighthawkcoder/
#  skype: americakart
#  Email: americakart@gmail.com
#  Copyright 2015 Srinath R <americakart@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import networkx as nx
from heapq import heappush, heappop
import copy
import sys
from collections import defaultdict
import time
import logging

try:
    import matplotlib.pyplot as plt
except:
    raise
logging.basicConfig(filename='eppstein.log', level=logging.DEBUG)
total_edges_counter = 0


def draw_graph(G):
    pos = nx.circular_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='b', style='dashed')
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.axis('off')
    plt.savefig('rendered_graph.png')
    plt.show()


class EppsteinShortestPathAlgorithm(object):
    def __init__(self, graph, source='s', destination='t'):
        self._G = graph
        self.path_tree = []
        self.source = source
        self.destination = destination
        self.sidetrack_edges = []
        self.shortest_path_distance = None
        self.counter = 0

    def _get_path_from_predecessors(self, pred={}, destination=None):
        if not destination:
            destination = self.destination
        path = list()
        while (True):
            value = pred.get(destination, None)
            if not value:
                break
            path.append((value, destination))
            destination = value
        path = list(reversed(path))  # reverse the path
        return path

    def _all_shortest_paths(self):

        """ Find all shortest paths from every node to destination """
        # make a reversed graph (reversing all the edges), so we can find single destination shortest paths problem

        _reverse_graph = self._G.reverse(copy=True)
        _reverse_pred, _dist = nx.bellman_ford(_reverse_graph, 't')
        print (time.ctime(), "reverse_pred, & dist by using bellman ford ")
        _pred = defaultdict(dict)
        for node, neighbor in _reverse_pred.items():
            _pred[neighbor] = node
        for counter, node in enumerate(self._G.nodes()):
            try:
                self._G.node[node]['target_distance'] = _dist[node]
            except KeyError:
                self._G.node[node]['target_distance'] = float('inf')
            _path = self._get_path_from_predecessors((_reverse_pred), destination=node)
            path = list(reversed([(value, key) for key, value in _path]))
            self._G.node[node]['path'] = path

        self.shortest_path_distance = self._G.node[self.source]['target_distance']
        # print "DISTANCE",self._G.node[self.source]['target_distance']

    def __get_sidetrack_edges(self, G):
        sp_edges = set([i for i in (path for node in G.nodes() for path in G.node[node]['path'])])
        all_edges = set([edge for edge in G.edges()])
        sidetrack_edges = all_edges - sp_edges
        return sidetrack_edges

    def _init_path_tree(self):
        sp = self._G.node[self.source]['path']
        sp_distance = self._G.node[self.source]['target_distance']
        node_info = {}
        node_info['sigma_e'] = 0
        node_info['path'] = sp
        node_info['distance'] = sp_distance
        node_info['visited_edges'] = set()
        node_info['source'] = None

        heappush(self.path_tree, (node_info['sigma_e'], node_info))

    def _head_tail(self, edge):
        return edge[1], edge[0]

    def _is_tree(self, G):
        if nx.number_of_nodes(G) != nx.number_of_edges(G) + 1:
            return False
        return nx.is_connected(G)

    def _build_graph(self, adj_dict={}, Directed=True):
        """
        Build Graph from supplied adjacency list or adj dict
        """
        if Directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        for node in adj_dict.keys(): G.add_node(node)
        for node, neighbor_list in adj_dict.items():
            for neighbor in neighbor_list:
                G.add_edge(node, neighbor)
        return G

    def _has_path(self, source='s', destination='t', edges=[]):
        """
        from the list of given edges determine whether a path exists in betweeen source and destination
        """
        adj_dict = self._adj_dict(edges)

        G = self._build_graph(adj_dict)
        return nx.has_path(G, source, destination)

    def _adj_dict(self, edges):
        """
        returns adjacency dict for given set of edges
        """
        adj_dict = defaultdict(list)
        for i, j in edges:
            adj_dict[i].append(j)
        return adj_dict

    def __is_valid_sidetrack_edge(self, path, edge, ):
        # Check whether the given edge can become a side track edge for given path
        if not path: return False
        if edge in path:
            # logging.debug('Edge is in path' + str(path) +", Edge:"+str(edge))
            return False
        adj_dict = self._adj_dict(path)
        head, tail = self._head_tail(edge)

        if adj_dict[tail]:
            return True
        return False

    def __get_sidetrack_path(self, path, sidetrack_edge):
        head, tail = self._head_tail(sidetrack_edge)
        to_remove = []
        for counter, pe in enumerate(path):
            ph, pt = self._head_tail(pe)
            if pt == tail:
                to_remove.append(counter)
        assert (len(to_remove) == 1)  # make sure that we are dealing with a path
        remaining_edges = [pe for counter, pe in enumerate(path) if counter not in to_remove]
        remaining_edges.insert(to_remove[0], sidetrack_edge)
        remaining_edges.extend(list(self._G.node[head]['path']))
        return self._get_path_from_edges(remaining_edges)

    def _get_path_from_edges(self, edges, destination='t'):
        if self._has_path(edges=edges, destination=destination):
            adj_dict = self._adj_dict(edges)
            G = self._build_graph(adj_dict=adj_dict)
            pred, dist = nx.bellman_ford(G, self.source, destination)
            return self._get_path_from_predecessors(pred, destination)

    def __get_sidetrack_edge_info(self, edge=None, prev_sigma_e=None, path=None, source=None):
        info = {}
        head, tail = self._head_tail(edge)
        info['sigma_e'] = self._G.node[head]['target_distance'] - self._G.node[tail]['target_distance'] + \
                          self._G.edge[tail][head]['weight'] + prev_sigma_e
        info['edge'] = edge
        info['source'] = source
        info['path'] = self.__get_sidetrack_path(path, edge)
        return info

    def _draw_edge(self, root, children=None, node_info=None):
        """
        draw an edge in between root and the given node
        """
        graph = self.path_tree
        graph.add_node(children, index=children, node_info=node_info)
        graph.add_edge(root, children)

    def _build_path_tree(self, source='s', path=[], sidetrack_edges=set(), prev_sigma_e=0, current_vertex=0,
                         visited_edges=set()):
        for edge in sidetrack_edges:
            if self.__is_valid_sidetrack_edge(path=path, edge=edge, ):
                info = self.__get_sidetrack_edge_info(edge=edge, source=source, prev_sigma_e=prev_sigma_e, path=path)
                node_info = {}
                node_info['prev_sigma_e'] = prev_sigma_e
                node_info['sigma_e'] = info['sigma_e']
                node_info['path'] = info['path']
                node_info['distance'] = self.shortest_path_distance + node_info['sigma_e']
                seen_edges = copy.deepcopy(visited_edges)
                seen_edges.add(edge)
                node_info['visited_edges'] = visited_edges
                node_info['source'] = info['edge']
                flag = True
                for ancestor_edge in visited_edges:
                    if ancestor_edge not in info['path']:
                        flag = False
                if flag:
                    heappush(self.path_tree, (node_info['sigma_e'], node_info))

    def _pre_process(self):
        """
            Finall all shortest path from each node to destination.
            Retrieve side track edges
            build side_track
        """
        import time
        print (time.ctime(), "started")
        print ("total_nodes", len(self._G.nodes()), "total_edges", len(self._G.edges()))
        self._all_shortest_paths()
        print (time.ctime(), "all shortest paths completed")
        sidetrack_edges = self.__get_sidetrack_edges(self._G)
        self.sidetrack_edges = sidetrack_edges
        self._init_path_tree()
        print (time.ctime(), "Initialization has been done")

    def retrieve_k_best(self):
        while (self.path_tree):
            el_info = heappop(self.path_tree)
            visited_edges = el_info[1]['visited_edges']
            seen_edges = copy.deepcopy(visited_edges)
            seen_edges.add(el_info[1]['source'])

            sigma_e = el_info[1]['sigma_e']
            distance = el_info[1]['distance']
            path = el_info[1]['path']
            yield distance, path
            source = el_info[1]['source']
            if el_info[0] == 0:
                self._build_path_tree(sidetrack_edges=self.sidetrack_edges, path=path)
            else:
                self._build_path_tree(source=source, path=path, sidetrack_edges=self.sidetrack_edges,
                                      prev_sigma_e=sigma_e, visited_edges=seen_edges)

    def get_successive_shortest_paths(self):
        for weight, path in self.retrieve_k_best():
            # logging.info(str(weight)+":"+str(path))
            yield weight, path


def create_pos_weighted_graph():
    graph = nx.DiGraph()  # Directed Graph
    graph.add_node('s', name="source", index='s')
    graph.add_node('t', name="destination", index='t')
    for i in range(3):
        for j in range(4):
            graph.add_node((i, j), index=(i, j), name=(i, j))
    edges = []
    edges.append(('s', (0, 0), 0))
    edges.append(((2, 3), 't', 0))

    edges.append(((0, 0), (0, 1), 2))
    edges.append(((0, 0), (1, 0), 13))

    edges.append(((0, 1), (0, 2), 20))
    edges.append(((0, 1), (1, 1), 27))

    edges.append(((0, 2), (0, 3), 14))
    edges.append(((0, 2), (1, 2), 14))

    edges.append(((0, 3), (1, 3), 15))

    edges.append(((1, 0), (1, 1), 9))
    edges.append(((1, 0), (2, 0), 15))

    edges.append(((1, 1), (1, 2), 10))
    edges.append(((1, 1), (2, 1), 20))

    edges.append(((1, 2), (1, 3), 25))
    edges.append(((1, 2), (2, 2), 12))

    edges.append(((1, 3), (2, 3), 7))
    edges.append(((2, 0), (2, 1), 18))
    edges.append(((2, 1), (2, 2), 8))
    edges.append(((2, 2), (2, 3), 11))

    graph.add_weighted_edges_from(edges)
    return graph


def create_neg_weighted_graph():
    graph = nx.DiGraph()  # Directed Graph
    graph.add_node('s', name="source", index='s')
    graph.add_node('t', name="destination", index='t')
    for i in range(3):
        for j in range(4):
            graph.add_node((i, j), index=(i, j), name=(i, j))
    edges = []
    edges.append(('s', (0, 0), 0))
    edges.append(((2, 3), 't', 0))

    edges.append(((0, 0), (0, 1), -2))
    edges.append(((0, 0), (1, 0), -13))

    edges.append(((0, 1), (0, 2), -20))
    edges.append(((0, 1), (1, 1), -27))

    edges.append(((0, 2), (0, 3), -14))
    edges.append(((0, 2), (1, 2), -14))

    edges.append(((0, 3), (1, 3), -15))

    edges.append(((1, 0), (1, 1), -9))
    edges.append(((1, 0), (2, 0), -15))

    edges.append(((1, 1), (1, 2), -10))
    edges.append(((1, 1), (2, 1), -20))

    edges.append(((1, 2), (1, 3), -25))
    edges.append(((1, 2), (2, 2), -12))

    edges.append(((1, 3), (2, 3), -7))
    edges.append(((2, 0), (2, 1), -18))
    edges.append(((2, 1), (2, 2), -8))
    edges.append(((2, 2), (2, 3), -11))

    graph.add_weighted_edges_from(edges)
    return graph

#add a dict
# dict_origin = {'a': {'w': 14, 'x': 7, 'y': 9},
#             'b': {'w': 9, 'z': 6},
#             'w': {'a': 14, 'b': 9, 'y': 2},
#             'x': {'a': 7, 'y': 10, 'z': 15},
#             'y': {'a': 9, 'w': 2, 'x': 10, 'z': 11},
#             'z': {'b': 6, 'x': 15, 'y': 11}}

dict_origin = \
    {'七里庙': {'五里墩': 1123, '十里铺': 1204},
     '三眼桥': {'唐家墩': 1478, '香港路': 1281},
     '三角湖': {'体育中心': 1454, '汉阳客运站': 1563},
     '三阳路': {'大智路': 1010, '黄浦路': 1155},
     '东亭站': {'岳家嘴': 928, '青鱼嘴': 1048},
     '东吴大道': {'五环大道': 1652},
     '东风公司': {'体育中心': 842, '沌阳大道': 1448, '车城东路': 2390},
     '中南路': {'宝通寺': 1417, '梅苑小区': 1095, '洪山广场': 966},
     '中山公园': {'循礼门': 1542, '青年路': 946},
     '丹水池': {'徐州新村': 1525, '新荣': 1437},
     '二七小路': {'兴业路': 1253, '罗家庄': 758},
     '二七路': {'头道街': 915, '徐州新村': 795},
     '云飞路': {'武汉商务区': 1227, '范湖': 884},
     '五环大道': {'东吴大道': 1652, '额头湾': 1655},
     '五里墩': {'七里庙': 1123, '汉阳火车站': 1012},
     '仁和路': {'园林路': 1332, '工业四路': 1634},
     '体育中心': {'三角湖': 1454, '东风公司': 842},
     '光谷广场': {'杨家湾': 1317},
     '六渡桥': {'汉正街': 850, '江汉路': 976},
     '兴业路': {'二七小路': 1253, '后湖大道': 1180},
     '利济北路': {'友谊路': 888, '崇仁路': 880},
     '前进村': {'国博中心北': 843, '建港': 1476},
     '十里铺': {'七里庙': 1204, '王家湾': 950},
     '友谊路': {'利济北路': 888, '循礼门': 986},
     '双墩': {'宗关': 982, '武汉商务区': 1824},
     '古田一路': {'古田二路': 1518, '舵落口': 1435},
     '古田三路': {'古田二路': 907, '古田四路': 795},
     '古田二路': {'古田一路': 1518, '古田三路': 907},
     '古田四路': {'古田三路': 795, '汉西一路': 820},
     '后湖大道': {'兴业路': 1180, '市民之家': 1667},
     '唐家墩': {'三眼桥': 1478, '石桥': 953},
     '四新大道': {'汉阳客运站': 928, '陶家岭': 1358},
     '园博园北': {'轻工大学': 2804, '金银湖': 2279},
     '园林路': {'仁和路': 1332, '罗家港': 1035},
     '国博中心北': {'前进村': 843, '国博中心南': 2110},
     '国博中心南': {'国博中心北': 2110, '老关村': 960},
     '堤角': {'新荣': 1165, '滕子岗': 1025},
     '复兴路': {'拦江路': 3277, '首义路': 718},
     '大智路': {'三阳路': 1010, '循礼门': 1082, '江汉路': 762, '苗栗路': 1856},
     '天河机场': {'航空总部': 6004},
     '太平洋': {'宗关': 1580, '硚口路': 1045},
     '头道街': {'二七路': 915, '黄浦路': 1202},
     '孟家铺': {'永安堂': 1478, '黄金口': 2761},
     '宋家岗': {'巨龙大道': 2039, '航空总部': 1426},
     '宏图大道': {'市民之家': 2422, '常青城': 2886, '盘龙城': 3945},
     '宗关': {'双墩': 982, '太平洋': 1580, '汉西一路': 920, '王家湾': 2531},
     '宝通寺': {'中南路': 1417, '街道口': 1238},
     '小龟山': {'洪山广场': 1168, '螃蟹岬': 929},
     '岳家嘴': {'东亭站': 928, '铁机路': 1032},
     '崇仁路': {'利济北路': 880, '硚口路': 1142},
     '工业四路': {'仁和路': 1634, '杨春湖': 1173},
     '巨龙大道': {'宋家岗': 2039, '盘龙城': 1643},
     '市民之家': {'后湖大道': 1667, '宏图大道': 2422},
     '常青城': {'宏图大道': 2886, '金银潭': 2012},
     '常青花园': {'杨汊湖': 756, '轻工大学': 1825, '金银潭': 1092, '长港路': 1725},
     '广埠屯': {'虎泉': 1612, '街道口': 951},
     '建港': {'前进村': 1476, '马鹦路': 953},
     '徐州新村': {'丹水池': 1525, '二七路': 795},
     '循礼门': {'中山公园': 1542, '友谊路': 986, '大智路': 1082, '江汉路': 896},
     '惠济二路': {'赵家条': 896, '香港路': 934},
     '拦江路': {'复兴路': 3277, '钟家村': 833},
     '新荣': {'丹水池': 1437, '堤角': 1165},
     '杨家湾': {'光谷广场': 1317, '虎泉': 1442},
     '杨春湖': {'工业四路': 1173, '武汉火车站': 809},
     '杨汊湖': {'常青花园': 756, '石桥': 1524},
     '梅苑小区': {'中南路': 1095, '武昌火车站': 900},
     '楚河汉街': {'洪山广场': 1077, '青鱼嘴': 1225},
     '武昌火车站': {'梅苑小区': 900, '首义路': 896},
     '武汉商务区': {'云飞路': 1227, '双墩': 1824},
     '武汉火车站': {'杨春湖': 809},
     '武胜路': {'汉正街': 1552, '琴台': 804},
     '永安堂': {'孟家铺': 1478, '玉龙路': 1243},
     '汉口北': {'滠口新城': 3410},
     '汉口火车站': {'范湖': 1216, '长港路': 1406},
     '汉正街': {'六渡桥': 850, '武胜路': 1552},
     '汉西一路': {'古田四路': 820, '宗关': 920},
     '汉阳客运站': {'三角湖': 1563, '四新大道': 928},
     '汉阳火车站': {'五里墩': 1012, '钟家村': 1573},
     '江城大道': {'老关村': 1201, '车城东路': 1748},
     '江汉路': {'六渡桥': 976, '大智路': 762, '循礼门': 896, '积玉桥': 3291},
     '沌阳大道': {'东风公司': 1448},
     '洪山广场': {'中南路': 966, '小龟山': 1168, '楚河汉街': 1077},
     '滕子岗': {'堤角': 1025, '滠口新城': 1120},
     '滠口新城': {'汉口北': 3410, '滕子岗': 1120},
     '玉龙路': {'永安堂': 1243, '王家湾': 900},
     '王家墩东': {'范湖': 1409, '青年路': 1002},
     '王家湾': {'十里铺': 950, '宗关': 2531, '玉龙路': 900, '龙阳村': 1107},
     '琴台': {'武胜路': 804, '钟家村': 864},
     '盘龙城': {'宏图大道': 3945, '巨龙大道': 1643},
     '石桥': {'唐家墩': 953, '杨汊湖': 1524},
     '硚口路': {'太平洋': 1045, '崇仁路': 1142},
     '积玉桥': {'江汉路': 3291, '螃蟹岬': 1579},
     '竹叶海': {'舵落口': 806, '额头湾': 943},
     '罗家庄': {'二七小路': 758, '赵家条': 882},
     '罗家港': {'园林路': 1035, '铁机路': 1170},
     '老关村': {'国博中心南': 960, '江城大道': 1201},
     '航空总部': {'天河机场': 6004, '宋家岗': 1426},
     '舵落口': {'古田一路': 1435, '竹叶海': 806},
     '苗栗路': {'大智路': 1856, '香港路': 932},
     '范湖': {'云飞路': 884, '汉口火车站': 1216, '王家墩东': 1409, '菱角湖': 1676},
     '菱角湖': {'范湖': 1676, '香港路': 931},
     '虎泉': {'广埠屯': 1612, '杨家湾': 1442},
     '螃蟹岬': {'小龟山': 929, '积玉桥': 1579},
     '街道口': {'宝通寺': 1238, '广埠屯': 951},
     '赵家条': {'惠济二路': 896, '罗家庄': 882},
     '车城东路': {'东风公司': 2390, '江城大道': 1748},
     '轻工大学': {'园博园北': 2804, '常青花园': 1825},
     '金银湖': {'园博园北': 2279, '金银湖公园': 1296},
     '金银湖公园': {'金银湖': 1296},
     '金银潭': {'常青城': 2012, '常青花园': 1092},
     '钟家村': {'拦江路': 833, '汉阳火车站': 1573, '琴台': 864, '马鹦路': 1024},
     '铁机路': {'岳家嘴': 1032, '罗家港': 1170},
     '长港路': {'常青花园': 1725, '汉口火车站': 1406},
     '陶家岭': {'四新大道': 1358, '龙阳村': 905},
     '青年路': {'中山公园': 946, '王家墩东': 1002},
     '青鱼嘴': {'东亭站': 1048, '楚河汉街': 1225},
     '额头湾': {'五环大道': 1655, '竹叶海': 943},
     '首义路': {'复兴路': 718, '武昌火车站': 896},
     '香港路': {'三眼桥': 1281, '惠济二路': 934, '苗栗路': 932, '菱角湖': 931},
     '马鹦路': {'建港': 953, '钟家村': 1024},
     '黄浦路': {'三阳路': 1155, '头道街': 1202},
     '黄金口': {'孟家铺': 2761},
     '龙阳村': {'王家湾': 1107, '陶家岭': 905}}

def create_simple_graph():
    graph = nx.DiGraph()  # Directed Graph
    graph.add_node('s', name="source", index='s')
    graph.add_node('t', name="destination", index='t')

    #add graph key from added dictionary
    for key in dict_origin.keys():
        graph.add_node(key, index=key, name=key)

    #add edges,
    # beginning with start and end
    start = '汉口火车站'
    end = '唐家墩'
    #
    edges = []
    edges.append(('s', start, 0))
    edges.append((end, 't', 0))

    #add edges for nodes in dictionary
    for key in dict_origin.keys():
        [edges.append((key, k, v)) for k, v in dict_origin[key].items() if v >0]

    #finish and return graph
    graph.add_weighted_edges_from(edges)
    # graph.add_edges_from(edges)

    return graph


def main():
    graph = create_simple_graph()
    # graph = create_pos_weighted_graph()
    e = EppsteinShortestPathAlgorithm(graph)
    e._pre_process()
    counter = 0
    for cost, sol in e.get_successive_shortest_paths():
        counter += 1
        if counter == 4:
            break
        print (cost, sol)
        # draw_graph(graph)
#

if __name__ == "__main__":
    main()




# e = EppsteinShortestPathAlgorithm(graph)
# e._pre_process()
# counter = 0
# for cost, sol in e.get_successive_shortest_paths():
#     counter += 1
#     if counter == 100:
#         break
#     print cost, sol
#     # draw_graph(graph)