from .ctype import Type
from .node import Node
from ..clang import cindex
from ..cmp import cmp


class TemplateTypeParameter(Node):
    kind = cindex.CursorKind.TEMPLATE_TYPE_PARAMETER

    def __init__(self, cursor, comment):
        Node.__init__(self, cursor, comment)

        self._default_type = None

        for child in self.cursor.get_children():
            if child.kind == cindex.CursorKind.TYPE_REF:
                self._default_type = Type(child.type, cursor=child)
                break

    @property
    def name(self):
        return self.cursor.spelling

    @property
    def default_type(self):
        return self._default_type

    @property
    def access(self):
        return cindex.AccessSpecifier.PUBLIC

    @access.setter
    def access(self, val):
        pass

    def compare_same(self, other):
        return cmp(self.sort_index, other.sort_index)


class TemplateNonTypeParameter(Node):
    kind = cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER

    def __init__(self, cursor, comment):
        super(TemplateNonTypeParameter, self).__init__(cursor, comment)

        self._type = Type(self.cursor.type, cursor=self.cursor)
        self._default_value = None

        for child in self.cursor.get_children():
            if child.kind == cindex.CursorKind.TYPE_REF:
                continue

            self._default_value = ''.join([t.spelling for t in child.get_tokens()][:-1])
            break

    @property
    def name(self):
        return self.cursor.spelling

    @property
    def access(self):
        return cindex.AccessSpecifier.PUBLIC

    @access.setter
    def access(self, val):
        pass

    @property
    def props(self):
        ret = Node.props.fget(self)
        ret['default'] = self._default_value

        return ret

    @property
    def type(self):
        return self._type

    @property
    def default_value(self):
        return self._default_value

    def compare_same(self, other):
        return cmp(self.sort_index, other.sort_index)
