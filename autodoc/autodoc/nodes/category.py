from .node import Node


class Category(Node):
    def __init__(self, name):
        Node.__init__(self, None, None)

        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def is_unlabeled(self):
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
