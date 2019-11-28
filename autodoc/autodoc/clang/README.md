# libclang Python Bindings

This is an import of the python bindings for libclang taken from the
`bindings/python/clang` directory of the
[clang](https://github.com/llvm-mirror/clang) repository.

The files are taken from SVN commit 328949
with the modifications listed in
`autodoc/clang/cindex-updates.patch`.

To apply the autodoc changes, run:

	cp ${CLANG_DIR}/bindings/python/clang/cindex.py autodoc/clang/cindex.py
	patch -p1 < autodoc/clang/cindex-updates.patch

To revert the custom modifications, run:

	patch -R -p1 < autodoc/clang/cindex-updates.patch

To create a new patch (e.g. after applying the autodoc changes on top of
a new clang version), run:

	git add autodoc/clang/cindex.py
	cp ${CLANG_DIR}/bindings/python/clang/cindex.py autodoc/clang/cindex.py
	git diff -R autodoc/clang/cindex.py > autodoc/clang/cindex-updates.patch
