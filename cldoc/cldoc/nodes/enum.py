from .node import Node

from ..clang import cindex


class Enum(Node):
    kind = cindex.CursorKind.ENUM_DECL

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self.typedef = None
        self.process_children = True
        self.isclass = False

        if hasattr(self.cursor, 'get_tokens'):
            try:
                tokens = self.cursor.get_tokens()
                next(tokens)

                tt = next(tokens)

                if tt.kind == cindex.TokenKind.KEYWORD and tt.spelling == 'class':
                    self.isclass = True
            except StopIteration:
                pass

    @property
    def is_anonymous(self):
        return not self.isclass

    @property
    def comment(self):
        ret = Node.comment.fget(self)

        if not ret and self.typedef:
            ret = self.typedef.comment

        return ret

    @property
    def name(self):
        if not self.typedef is None:
            # The name is really the one of the typedef
            return self.typedef.name
        else:
            return Node.name.fget(self)

    def sorted_children(self):
        return list(self.children)
