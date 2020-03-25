from .method import Method

from ..clang import cindex


class ConversionFunction(Method):
    kind = cindex.CursorKind.CONVERSION_FUNCTION

    def __init__(self, cursor, comment):
        Method.__init__(self, cursor, comment)
