from .ctype import Type
from .method import Method
from .node import Node
from ..clang import cindex


class Class(Node):
    kind = cindex.CursorKind.CLASS_DECL

    class Base:
        def __init__(self, cursor, access=cindex.AccessSpecifier.PUBLIC):
            self.cursor = cursor
            self.access = access
            self.type = Type(cursor.type, cursor=cursor)
            self.node = None

    def __init__(self, cursor, comment):
        super(Class, self).__init__(cursor, comment)

        self.process_children = True
        self.current_access = cindex.AccessSpecifier.PRIVATE
        self.bases = []
        self.implements = []
        self.implemented_by = []
        self.subclasses = []
        self.name_to_method = {}

    def _all_bases(self):
        for b in self.bases:
            yield b

        for b in self.implements:
            yield b

    def resolve_bases(self, mapping):
        for b in self.bases:
            tpname = b.type.typename

            if tpname in mapping:
                b.node = mapping[tpname]
                b.node.subclasses.append(self)

        for b in self.implements:
            tpname = b.type.typename

            if tpname in mapping:
                b.node = mapping[tpname]
                b.node.implemented_by.append(self)

    @property
    def resolve_nodes(self):
        for child in Node.resolve_nodes.fget(self):
            yield child

        for base in self._all_bases():
            if base.node and base.access != cindex.AccessSpecifier.PRIVATE:
                yield base.node

                for child in base.node.resolve_nodes:
                    yield child

    def append(self, child):
        super(Class, self).append(child)

        if isinstance(child, Method):
            self.name_to_method[child.name] = child

    @property
    def methods(self):
        for child in self.children:
            if isinstance(child, Method):
                yield child

    def visit(self, cursor, citer):
        if cursor.kind == cindex.CursorKind.CXX_ACCESS_SPEC_DECL:
            self.current_access = cursor.access_specifier
            return []
        elif cursor.kind == cindex.CursorKind.CXX_BASE_SPECIFIER:
            # Add base
            self.bases.append(Class.Base(cursor.type.get_declaration(), cursor.access_specifier))
            return []

        return Node.visit(self, cursor, citer)

    @property
    def force_page(self):
        return True
