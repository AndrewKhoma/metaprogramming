from .cclass import Class

from ..clang import cindex


class Struct(Class):
    kind = cindex.CursorKind.STRUCT_DECL

    def __init__(self, cursor, comment):
        Class.__init__(self, cursor, comment)

        self.typedef = None
        self.current_access = cindex.AccessSpecifier.PUBLIC

    @property
    def is_anonymous(self):
        return self.anonymous_id > 0 and self.typedef is None

    @property
    def comment(self):
        ret = Class.comment.fget(self)

        if not ret and self.typedef:
            ret = self.typedef.comment

        return ret

    @property
    def name(self):
        if not self.typedef is None:
            # The name is really the one of the typedef
            return self.typedef.name
        else:
            return Class.name.fget(self)

    @property
    def force_page(self):
        return not self.is_anonymous