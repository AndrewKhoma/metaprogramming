from .category import Category
from .node import Node


class Root(Node):
    def __init__(self):
        Node.__init__(self, None, None)

    @property
    def is_anonymous(self):
        return True

    def sorted_children(self):
        schildren = list(Node.sorted_children(self))

        # Keep categories in order though
        c = [x for x in self.children if isinstance(x, Category)]
        c.reverse()

        if len(c) == 0:
            return schildren

        for i in range(0, len(schildren)):
            if isinstance(schildren[i], Category):
                schildren[i] = c.pop()

        return schildren
