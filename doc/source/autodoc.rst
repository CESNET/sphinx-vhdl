.. _autodoc_usage:

Autodoc Usage
=============

Before the automatic documentation feature of the Sphinx-VHDL plugin may be
used, the plugin must be set up with the path to a directory where the project
with the sources for automatic documentation reside. Please refer to
:py:attr:`vhdl_autodoc_source_path` for this.

The Sphinx-VHDL automatic documentation generation depends on being able to
extract documentation comments from the source code. Extraction of
documentation is only attempted from files with the ``.vhd`` or ``.vhdl``
suffix, and requires those source files to be mostly syntactically valid.
Documentation is only extracted from continuous line comment blocks; and allows
the full range of reStructuredText syntax on the inside; however, a mandatory
space symbol is expected just after each ``--``, and blank documentation lines
must also contain at least ``--`` at the beginning (there the space may be
omitted).

All documentation comments to be extracted must immediately precede the object
they are documenting; if a comment is not meant to be a documentation comment
and thus should not be extracted; it should be separated by at least a blank
line, or placed after the object definition.