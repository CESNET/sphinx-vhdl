.. sphinx-vhdl documentation master file, created by
   sphinx-quickstart on Wed Jul  7 10:06:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sphinx-vhdl
===========
**sphinx-vhdl** is a `Sphinx`_ extension to generate documentation for the VHDL language. It can be used both to manually write your documentation, describing different language constructs used, and to automatically pull your documentation from source code comments.

Usage
=====
To setup sphinx-vhdl for your project, please edit your sphinx ``conf.py`` file to include the following - an include of the actual module, and (optionally) a configuration of path to use for the autodoc feature
``doc/conf.py``

.. code-block:: python

  extensions = ['sphinxvhdl.vhdl']
  vhdl_autodoc_source_path = 'path/to/your/vhdl/sources/root'

In case VHDL source files reside in two different directories, You can specify a list 
in :py:attr:`vhdl_autodoc_source_path`

.. code-block:: python

  extensions = ['sphinxvhdl.vhdl']
  vhdl_autodoc_source_path = ['path/to/your/vhdl/sources1', 'path/to/your/vhdl/sources1']

See :ref:`configuration` for more information.

Recognized directives
=====================

================================== =============================================
Directive                          Description
================================== =============================================
:rst:dir:`vhdl:autoentity`         Automatic documentation of entity.
:rst:dir:`vhdl:autoenum`           Automatic documentation of enumeration types.
:rst:dir:`vhdl:autofunction`       Automatic documentation of functions.
:rst:dir:`vhdl:autogenerics`       Automatic documentation of generics.
:rst:dir:`vhdl:autoconstants`      Automatic documentation of constants.
:rst:dir:`vhdl:autopackage`        Automatic documentation of package.
:rst:dir:`vhdl:autoports`          Automatic documentation of ports.
:rst:dir:`vhdl:autorecord`         Automatic documentation of record types.
:rst:dir:`vhdl:autotype`           Automatic documentation of general types.
:rst:dir:`vhdl:entity`             A single entity.
:rst:dir:`vhdl:enum`               Enumeration-defined type.
:rst:dir:`vhdl:enumval`            A single value in :rst:dir:`vhdl:enum`.
:rst:dir:`vhdl:function`           A pure function.
:rst:dir:`vhdl:generics`           Generics of an :rst:dir:`vhdl:entity`.
:rst:dir:`vhdl:constants`          Constants of an VHDL architecture.
:rst:dir:`vhdl:package`            A whole single package.
:rst:dir:`vhdl:parameters`         A parameter list to a subprogram.
:rst:dir:`vhdl:ports`              Ports of an :rst:dir:`vhdl:entity`.
:rst:dir:`vhdl:record`             Record-defined type.
:rst:dir:`vhdl:recordelem`         A single field in :rst:dir:`vhdl:record`
:rst:dir:`vhdl:type`               A type other than a record or enumeration.
================================== =============================================

See :ref:`directives` for more information.

Recognized roles
================

================================== ============================================================
Role                               Description
================================== ============================================================
:rst:role:`vhdl:entity`            References :rst:dir:`vhdl:entity`.
:rst:role:`vhdl:genconstant`       References individual constants in :rst:dir:`vhdl:generics`.
:rst:role:`vhdl:portsignal`        References individual ports in :rst:dir:`vhdl:ports`.
:rst:role:`vhdl:type`              References :rst:dir:`vhdl:enum`.
================================== ============================================================

See :ref:`roles` for more information.

Example of VHDL code written for auto documentation
===================================================

.. code-block:: vhdl

    library ieee;
    use ieee.numeric_std.all;

    -- This package provides basic mathematic functions utilised all through
    -- the design
    package math_pack is
        -- This function calculates the base 2 logarithm of a number.
        --
        -- .. vhdl:parameters:: log2
        --
        --     a : in unsigned
        --         The number of which to calculate the logarithm
        function log2 parameter (a : unsigned) return integer;
    end package math_pack;

    library ieee;
    use work.math_pack.all;
    use ieee.std_logic_1164.all;

    -- This is a simple counter entity that counts the amount of passed input
    -- clock cycles up to :vhdl:genconstant:`max_value <counter.max_value>`.
    entity counter is
    generic (
        -- Determines how many clock cycles must pass before the buffer
        -- overflowing.
        constant max_value : integer := 16
    );
    port (
        IN_EN  : in std_logic;                                       -- The input clock
        OUT_EN : out std_logic_vector(log2(max_value) - 1 downto 0)  -- The output signal
    );
    end entity counter;

To use the automatically extracted comments in your documentation, you then
have to place one of the ``auto…`` directives above on the relevant place in
your documentation files. See :ref:`example_doc` for how this code will look
when built.

.. code-block:: rst

  .. _example_doc:

   Example Documentation
   =====================

   .. vhdl:autopackage:: math_pack

     .. vhdl:autofunction:: log2

   .. vhdl:autoentity:: counter

See :ref:`autodoc_usage` for more information.

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

.. toctree::
   :maxdepth: 1
   :hidden:

   directives_detailed.rst
   roles_detailed.rst
   config.rst
   autodoc.rst
   example_built.rst
   group_example_built.rst

.. _Sphinx: https://www.sphinx-doc.org
