.. _configuration:

Configuration options
=====================

.. py:attribute:: vhdl_autodoc_source_path
  :type: string
  :value: "."

  Determines the root of the directory structure where the VHDL source codes
  used for automatic documentation generation reside. Must be relative to from
  where the build command is run.

  In case project contains directories which You do not wish to parse, the 
  list of directories can be also provided. Parsing will be done for each one 
  in the order defined by the list. 