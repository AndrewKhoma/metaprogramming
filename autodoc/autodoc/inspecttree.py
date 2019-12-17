# -*- coding: utf-8 -*-


import os
import sys

from .clang import cindex
from xml.sax.saxutils import escape


def inspect_print_row(a, b, output_file, link=None):
    b = escape(str(b))

    if link:
        b = "<a href='#" + escape(link) + "'>" + b + "</a>"

    output_file.write("<tr><td>%s</td><td>%s</td></tr>" % (escape(str(a)), b))


def inspect_print_subtype(name, tp, subtype, output_file, indent=1):
    if not subtype or tp == subtype or subtype.kind == cindex.TypeKind.INVALID:
        return

    inspect_print_row('  ' * indent + '→ .' + name + '.kind', subtype.kind, output_file)
    inspect_print_row('  ' * indent + '→ .' + name + '.spelling', subtype.kind.spelling, output_file)
    inspect_print_row('  ' * indent + '→ .' + name + '.is_const_qualified', subtype.is_const_qualified(), output_file)

    if subtype.kind == cindex.TypeKind.CONSTANTARRAY:
        etype = subtype.get_array_element_type()
        num = subtype.get_array_size()

        inspect_print_subtype('array_type', subtype, etype, output_file, indent + 1)
        inspect_print_row('  ' * (indent + 1) + '→ .size', str(num), output_file)

    decl = subtype.get_declaration()

    if decl:
        inspect_print_row('  ' * indent + '→ .' + name + '.declaration', decl.displayname, output_file, decl.get_usr())

    inspect_print_subtype('get_canonical', subtype, subtype.get_canonical(), output_file, indent + 1)
    inspect_print_subtype('get_pointee', subtype, subtype.get_pointee(), output_file, indent + 1)
    inspect_print_subtype('get_result', subtype, subtype.get_result(), output_file, indent + 1)


def inspect_cursor(tree, cursor, output_file, indent):
    from xml.sax.saxutils import escape

    if not cursor.location.file:
        return

    if not str(cursor.location.file) in tree.files:
        return

    output_file.write(
        "<table id='" + escape(cursor.get_usr()) + "' class='cursor' style='margin-left: " + str(indent * 20) + "px;'>")

    inspect_print_row('kind', cursor.kind, output_file)
    inspect_print_row('  → .is_declaration', cursor.kind.is_declaration(), output_file)
    inspect_print_row('  → .is_reference', cursor.kind.is_reference(), output_file)
    inspect_print_row('  → .is_expression', cursor.kind.is_expression(), output_file)
    inspect_print_row('  → .is_statement', cursor.kind.is_statement(), output_file)
    inspect_print_row('  → .is_attribute', cursor.kind.is_attribute(), output_file)
    inspect_print_row('  → .is_invalid', cursor.kind.is_invalid(), output_file)
    inspect_print_row('  → .is_preprocessing', cursor.kind.is_preprocessing(), output_file)

    inspect_print_subtype('type', None, cursor.type, output_file, 0)

    inspect_print_row('usr', cursor.get_usr(), output_file)
    inspect_print_row('spelling', cursor.spelling, output_file)
    inspect_print_row('displayname', cursor.displayname, output_file)
    inspect_print_row('location', "%s (%d:%d - %d:%d)" % (
        os.path.basename(str(cursor.location.file)), cursor.extent.start.line, cursor.extent.start.column,
        cursor.extent.end.line, cursor.extent.end.column), output_file)
    inspect_print_row('is_definition', cursor.is_definition(), output_file)
    inspect_print_row('is_virtual_method', cursor.is_virtual_method(), output_file)
    inspect_print_row('is_static_method', cursor.is_static_method(), output_file)

    spec = cursor.access_specifier

    if not spec is None:
        inspect_print_row('access_specifier', spec, output_file)

    defi = cursor.get_definition()

    if defi and defi != cursor:
        inspect_print_row('definition', defi.displayname, output_file, link=defi.get_usr())

    if cursor.kind == cindex.CursorKind.CXX_METHOD:
        for t in cursor.type.argument_types():
            inspect_print_subtype('argument', None, t, output_file)

    output_file.write("</table>")


def inspect_cursors(tree, cursors, output_file, indent=0):
    for cursor in cursors:
        inspect_cursor(tree, cursor, output_file, indent)

        if (not cursor.location.file) or str(cursor.location.file) in tree.files:
            inspect_cursors(tree, cursor.get_children(), output_file, indent + 1)


def inspect_tokens(tree, filename, tu, output_file):
    it = tu.get_tokens(extent=tu.get_extent(filename, (0, os.stat(filename).st_size)))

    output_file.write("<table class='tokens'>")

    for token in it:
        output_file.write("<tr>")
        output_file.write("<td>%s</td>" % (token.kind,))
        output_file.write("<td>" + token.spelling + "</td>")
        output_file.write("<td>%s</td>" % (token.cursor.kind,))
        output_file.write("<td>%d:%d</td>" % (token.extent.start.line, token.extent.start.column,))
        output_file.write("</tr>")

    output_file.write("</table>")


def inspect(tree, output_dir):
    index = cindex.Index.create()

    filename = os.path.join(output_dir, "index.html")

    with open(filename, 'w') as file:
        file.write("""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style type='text/css'>
div.filename {
padding: 3px;
background-color: #eee;
}

table.cursor {
border-collapse: collapse;
margin-bottom: 10px;
}

a {
color: #3791db;
}

table.cursor tr td:first-child {
font-weight: bold;
padding-right: 10px;
color: #666;
vertical-align: top;
}
</style>
</head>
<body>""")

        for f in tree.files:
            tu = index.parse(f, tree.flags)

            for d in tu.diagnostics:
                sys.stderr.write(d.format())
                sys.stderr.write("\n")

            if not tu:
                sys.stderr.write("Could not parse file {0}...\n".format(f))

            file.write("<div class='file'><div class='filename'>" + f + "</div>")

            inspect_tokens(tree, f, tu, file)

            # Recursively inspect cursors
            # inspect_cursors(tree, tu.cursor.get_children(), file)

            file.write("</div>")

        file.write("</body>\n</html>")
