
import json
from graphviz import Digraph

from graph_definition import GraphNode
from one_path import dijkstra_max_product_path
from all_pathes import find_all_pathes, calculate_pathes_value
from parser import Parser


def visualize_graph(node_pool: dict[str, GraphNode], path: list[GraphNode], quotes: dict[str, float]):
    def is_neighbours_in_path(node1: GraphNode, node2: GraphNode) -> bool:
        nonlocal path
        if node1 not in path or node2 not in path:
            return False
        idx1 = path.index(node1)
        idx2 = path.index(node2)
        if abs(idx1 - idx2) < 2:
            return True
        return False

    dot = Digraph(comment='Graph Visualization')

    # Добавляем все узлы
    for node_name, node in node_pool.items():
        if node in path:
            # Выделение узлов, которые есть в пути
            dot.node(node_name, node_name, color='red')
        else:
            dot.node(node_name, node_name)

        # Добавляем все рёбра
        for child in node.children:
            if is_neighbours_in_path(node, child):
                dot.edge(node_name, child.name, label=str(quotes[f'{node.name}{child.name}']), color='red')
            else:
                dot.edge(node_name, child.name)

    print("graph has built \nwaiting visualization...")
    # Визуализация и сохранение графа
    dot.render('graph_output', view=True, format='png')


class Main:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Main, cls).__new__(cls)
        return cls._instance

    def __init__(self, access_key: str):
        self.access_key: str = access_key
        self.parser: Parser = Parser(access_key)

        self.all_quotes: dict[str, float] = dict()
        self.node_pool: dict[str, GraphNode] = dict()
        self.currencies: dict[str, str] = {}

    def get_real_data(self):
        self.parser.get_all_quotes()

        self.all_quotes = self.parser.all_quotes
        self.node_pool = self.parser.node_pool
        self.currencies = self.parser.currencies

    def get_mock_data(self):
        node_pool: dict[str, GraphNode] = dict()
        node1 = GraphNode('111')
        node2 = GraphNode('222')
        node3 = GraphNode('333')
        node4 = GraphNode('444')
        node5 = GraphNode('555')
        node6 = GraphNode('666')
        node7 = GraphNode('777')
        node8 = GraphNode('888')

        node_pool[node1.name] = node1
        node_pool[node2.name] = node2
        node_pool[node3.name] = node3
        node_pool[node4.name] = node4
        node_pool[node5.name] = node5
        node_pool[node6.name] = node6
        node_pool[node7.name] = node7
        node_pool[node8.name] = node8

        node1.children = [node2, node4, node8, node6, node5]
        node2.children = [node3, node4]
        node3.children = [node4, node7]
        node4.children = [node8]
        node5.children = [node6, node7]
        node6.children = [node8]
        node7.children = [node8]
        node8.children = []

        quotes = {
            '111222': 1,
            '111444': 2,
            '111888': 3.5,
            '111666': 3,
            '111555': 2,

            '222333': 1,
            '222444': 1,

            '333444': 1,
            '333777': 1,

            '444888': 2,

            '555666': 2,
            '555777': 0.1,

            '666888': 1.5,

            '777888': 4
        }

        self.all_quotes = quotes
        self.node_pool = node_pool
        return

    def calculate_by_all_pathes(self, start_node_name: str, end_node_name: str):
        if start_node_name not in self.node_pool:
            raise KeyError(f'Node with name {start_node_name} does not exists')
        if end_node_name not in self.node_pool:
            raise KeyError(f'Node with name {end_node_name} does not exists')

        start_node = self.node_pool[start_node_name]
        end_node = self.node_pool[end_node_name]

        all_pathes: list[list[GraphNode]] = find_all_pathes(start_node, end_node)
        print('\nall pathes')
        for cur_path in all_pathes:
            print(cur_path)

        values: list[float] = calculate_pathes_value(all_pathes, self.all_quotes)
        print('\nvalues')
        print(values)

        max_value = max(values)
        print(f'\nmax value = {max_value}')

        idx = values.index(max_value)

        path = all_pathes[idx]

        print("Максимальное произведение весов:", max_value)
        print("Путь:", path)

        visualize_graph(self.node_pool, path, self.all_quotes)
        return

    def calculate_by_one_path(self, start_node_name: str, end_node_name: str):
        if start_node_name not in self.node_pool:
            raise KeyError(f'Node with name {start_node_name} does not exists')
        if end_node_name not in self.node_pool:
            raise KeyError(f'Node with name {end_node_name} does not exists')

        start_node = self.node_pool[start_node_name]
        end_node = self.node_pool[end_node_name]

        weight, path = dijkstra_max_product_path(self.node_pool, start_node, end_node, self.all_quotes)
        print("Максимальное произведение весов:", weight)
        print("Путь:", path)

        # Вызов функции с вашими данными
        visualize_graph(self.node_pool, path, self.all_quotes)
        return

    def main(self):
        while True:
            try:
                option = int(
                    input('1 - get real data\n'
                          '2 - get mock data\n'
                          '3 - calculate by alg 1 - all pathes\n'
                          '4 - calculate by alg 2 - one path\n'
                          '5 - print all quotes\n'
                          '6 - print all currencies\n'
                          '7 - exit\n'
                          '-> '))
                match option:
                    case 1:
                        self.get_real_data()
                    case 2:
                        self.get_mock_data()
                    case 3:
                        start_name = input('start name -> ')
                        end_name = input('end name -> ')
                        self.calculate_by_all_pathes(start_name, end_name)
                    case 4:
                        start_name = input('start name -> ')
                        end_name = input('end name -> ')
                        self.calculate_by_one_path(start_name, end_name)
                    case 5:
                        print(json.dumps(self.all_quotes, indent=4))
                    case 6:
                        print(json.dumps(self.currencies, indent=4))
                    case 7:
                        return
                    case _:
                        print('неверный номер команды')
            except Exception as ex:
                print(ex)


if __name__ == '__main__':
    main = Main('cbdaabe4b8f76243c6acc161a45cb9d3')
    main.main()
