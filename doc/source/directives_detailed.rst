.. _vhdl_enum_directive:

vhdl:enum
=========
Used for documenting enumeration defined types. Individual enum values can be defined using :ref:`vhdl:enumVal <vhdl_enumVal_directive>`.

.. code-block:: rst

  .. vhdl:enum:: YourTypeName

    Your type fulltext description.

.. _vhdl_enumVal_directive:

vhdl:enumVal
============
TODO

.. _vhdl_portsignal_directive:

vhdl:portsignal
===============
Used for documenting individual ports of an entity.

Options:
--------

========== ============
Option     Description
========== ============
``:type:`` Describes the type of the port, mandatory.
``:init:`` Describes the initial value of the port, optional.
========== ============

Example
-------

.. code-block:: rst

  .. vhdl:portsignal:: YourPortName
    :type: std_logic
    :init: '0'

    Your port fulltext description