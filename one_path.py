
import math
import heapq
from graph_definition import GraphNode


'''
Классический алгоритм Дейкстры, адаптированный для поиска пути с максимальной суммой весов, 
работает следующим образом:

    1. Инициализация: 
        Устанавливаем начальное максимальное расстояние для стартовой вершины равным 0, 
        а для всех остальных вершин — минус бесконечность.

    2. Обработка вершин:
        На каждом шаге выбираем из непосещённых вершин ту, у которой наибольшее расстояние от начальной точки.
        Для каждой соседней вершины этой вершины проверяем, увеличивает ли добавление текущего ребра общую сумму пути. 
        Если да, то обновляем расстояние для этой соседней вершины.

    3. Завершение: 
        Процесс продолжается, пока не будут обработаны все вершины 
        или пока не будет найден путь до конечной вершины. 
        В результате получаем максимальное расстояние от начальной до конечной вершины.

Основное отличие от стандартного алгоритма Дейкстры состоит в том, 
что мы максимизируем сумму весов, а не минимизируем их, 
и используем -бесконечность вместо бесконечности для инициализации расстояний.
'''


def dijkstra_max_product_path(node_pool: dict[str, GraphNode], start_node: GraphNode, end_node: GraphNode,
                              quotes: dict[str, float]) -> tuple[float, list[GraphNode]]:

    # функция логарифмирования веса (преобразуем умножение в сложение)
    def log_weight(edge_weight):
        return math.log(edge_weight)

    # инициализация
    distances: dict[str, float] = {node_name: float('-inf') for node_name in node_pool}  # расстояния
    distances[start_node.name] = 0  # 0 для начального
    predecessors: dict[GraphNode, GraphNode] = {node: None for node in node_pool.values()}  # предыдущие вершины
    priority_queue: list[tuple[int | float, GraphNode]] = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        current_distance = -current_distance

        for child in node_pool[current_node.name].children:
            edge_key: str = f'{current_node.name}{child.name}'
            weight: float = quotes[edge_key]
            distance: float = current_distance + log_weight(weight)
            if distance > distances[child.name]:
                distances[child.name] = distance
                predecessors[child] = current_node
                heapq.heappush(priority_queue, (-distance, child))

    # Восстановление пути
    path: list[GraphNode] = []
    current_vertex: GraphNode = end_node
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = predecessors[current_vertex]
    path.reverse()  # Переворачиваем путь, чтобы начать с начальной вершины

    return math.exp(distances[end_node.name]), path


def test_dijkstra_max_product_path():
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
    node4.children = [node8, node3]  # node 3 for debug
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
        '444333': 10,  # for test

        '555666': 2,
        '555777': 0.1,

        '666888': 1.5,

        '777888': 4
    }

    weight, path = dijkstra_max_product_path(node_pool, node1, node8, quotes)
    print("Максимальное произведение весов:", weight)
    print("Путь:", path)

    return node_pool, path, quotes


if __name__ == '__main__':
    test_dijkstra_max_product_path()


'''
тут алгорит Дейкстры для поиска пути с максимальным произведением весов
тестовый вариант для проверки самого алгоритма

import math
import heapq


def dijkstra_max_product_path(graph, start, end):
    def log_weight(edge_weight):
        return math.log(edge_weight)

    distances = {vertex: float('-inf') for vertex in graph}
    distances[start] = 0
    predecessors = {vertex: None for vertex in graph}
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        current_distance = -current_distance

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + log_weight(weight)
            if distance > distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (-distance, neighbor))

    # Восстановление пути
    path = []
    current_vertex = end
    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = predecessors[current_vertex]
    path.reverse()  # Переворачиваем путь, чтобы начать с начальной вершины

    return math.exp(distances[end]), path



# Пример графа
graph_2 = {
    '111': {'222': 1, '444': 2, '888': 3.5, '666': 3, '555': 2},
    '222': {'333': 1, '444': 1},
    '333': {'444': 1, '777': 1},
    '444': {'888': 2},
    '555': {'666': 2, '777': 0.1},
    '666': {'888': 1.5},
    '777': {'888': 4},
    '888': {}
}

# Вызов функции
max_product, path = dijkstra_max_product_path(graph_2, '111', '888')
print("Максимальное произведение весов:", max_product)
print("Путь:", path)


'''








