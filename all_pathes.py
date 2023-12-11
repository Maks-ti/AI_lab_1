
from graph_definition import GraphNode


# метод получения всех уникальных путей из start_node в end_node
def find_all_pathes(start_node: GraphNode, end_node: GraphNode) -> list[list[GraphNode]]:
    all_pathes: list[list[GraphNode]] = []  # список всех уникальных путей
    visited: set[GraphNode] = set()  # множество посещённых узлов
    current_path: list[GraphNode] = []  # текущий путь

    def dfs(current_node: GraphNode):
        if current_node == end_node:
            all_pathes.append(list(current_path))  # копируем ссылки, но не сами объекты
            return
        # добавляем пометку, что мы заходили в текущую вершину (все предыдущие тоже тут), это позволяет исключить циклы
        visited.add(current_node)
        for child in current_node.children:
            if child not in visited:
                current_path.append(child)
                dfs(child)
                current_path.pop()  # возврат к предыдущей вершине
        visited.remove(current_node)  # убираем пометку, того что мы заходили в текущую вершину
        return

    # запускаем поиск
    current_path.append(start_node)
    dfs(start_node)
    return all_pathes


'''
данный алгоритм довольно неоптимален и сложен по времени
его имеет смысл использовать в системе, когда нам надо посмотреть все пути 
и посмотреть значение каждого их этих путей

плюсы данного алгоритма - если система работает постоянно 
его можно запустить один раз получить все пути и после этого
просто пересчитывать значения уже путей, не затрагивая информацию о графе

будем его использовать когда надо следить за конкретным путём преобразования
'''


# метод расчёта значения одного отдельного пути
def calculate_path_value(path: list[GraphNode], quotes: dict[str, float]) -> float:
    path_value: float = 1.
    for i in range(len(path) - 1):
        key = f"{path[i]}{path[i + 1]}"
        path_value = path_value * quotes[key]
    return path_value


def calculate_pathes_value(pathes: list[list[GraphNode]], quotes: dict[str, float]) -> list[float]:
    values: list[float] = []
    for path in pathes:
        value = calculate_path_value(path, quotes)
        values.append(value)
    return values


def test_find_all_pathes():
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

    all_pathes: list[list[GraphNode]] = find_all_pathes(node1, node8)
    print('\nall pathes')
    for cur_path in all_pathes:
        print(cur_path)

    values: list[float] = calculate_pathes_value(all_pathes, quotes)
    print('\nvalues')
    print(values)

    max_value = max(values)
    print(f'\nmax value = {max_value}')

    idx = values.index(max_value)

    path = all_pathes[idx]

    print("Максимальное произведение весов:", max_value)
    print("Путь:", path)

    return node_pool, path, quotes


if __name__ == '__main__':
    test_find_all_pathes()



