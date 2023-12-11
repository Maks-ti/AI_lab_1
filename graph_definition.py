
class GraphNode:
    def __init__(self, name: str, children: list = None):
        self.name: str = name
        self.children: list[GraphNode] = children if children is not None else []

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.name == other.name
        return super(GraphNode, self).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, GraphNode):
            return self.name < other.name
        raise TypeError(f'type {type(GraphNode)} can not be compare with type {type(other)}')

    def __le__(self, other):
        if isinstance(other, GraphNode):
            return self.name <= other.name
        raise TypeError(f'type {type(GraphNode)} can not be compare with type {type(other)}')

    def __gt__(self, other):
        if isinstance(other, GraphNode):
            return self.name > other.name
        raise TypeError(f'type {type(GraphNode)} can not be compare with type {type(other)}')

    def __ge__(self, other):
        if isinstance(other, GraphNode):
            return self.name >= other.name
        raise TypeError(f'type {type(GraphNode)} can not be compare with type {type(other)}')
