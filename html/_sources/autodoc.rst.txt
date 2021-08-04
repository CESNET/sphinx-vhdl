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
suffix, and requires those source files to be reasonably well formatted, even if not necessarily syntactically valid.
Documentation is only extracted from continuous line comment blocks; and allows
the full range of reStructuredText syntax on the inside; however, a mandatory
space symbol is expected just after each ``--``, and blank documentation lines
must also contain at least ``--`` at the beginning (there the space may be
omitted).

All documentation comments to be extracted must immediately precede the object
they are documenting; if a comment is not meant to be a documentation comment
and thus should not be extracted; it should be separated by at least a blank
line, or placed after the object definition. For a very short documentation
comments, the comment immediately following the declaration on the same line is
also acceptable.

Formatting
----------

For the automatic extraction to work, the code must be particularly formatted. Specifically:

- entity declaration must be on its own individual line

  .. code-block:: vhdl

    entity entityName is

- inside entity declarations, the ``port (`` and ``generic (`` keywords must be
  on their own individual lines
- every signal/constant defined must be on its own individual line
- linebreaks must not be inserted *inside* signal/constant declarations - the
  whole declaration must be on one line
- enumeration-defined types must have the opening parenthesis on the same line
  as the ``type`` keyword, and individual values must each have their own line
- record-defined types must have the ``record`` keyword on the same line as the
  ``type`` keyword, and each element of that record must be on its own line

Example
-------

.. code-block:: vhdl

    -- This is not a documentation comment

    -- This is also not a documentation comment
    --Because this comment has no space
    -- This is a documentation comment for the entity
    -- Here it continues
    --
    -- Above here is a blank line in the documentation.
    -- It is still a documentation comment
    entity entityName is
    -- This is just a random comment, not documentation
    begin
    port (
      -- This is a documentation for the port
      signal portName : inout std_logic bus := ‘1’;
      -- This is not a documentation comment due to the blank line

      portName2 : bit;
      portName3 : in bit    -- This is a documentation comment for portName3
    );
    end entity entityName;
