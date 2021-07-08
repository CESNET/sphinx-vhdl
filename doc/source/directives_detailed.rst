Directives
==========

.. rst:directive:: vhdl:enum

    Used for documenting enumeration defined types. Individual enum values can
    be defined using :rst:dir:`vhdl:enumVal <vhdl:enumVal>`.

    .. code-block:: rst

        .. vhdl:enum:: YourTypeName

            Your type fulltext description.

.. rst:directive:: vhdl:enumVal

    TODO

.. rst:directive:: vhdl:portsignal

    Used for documenting individual ports of an entity.

    .. rst:directive:option:: type: Describes the type of the port, mandatory.

        Unless :py:attr:`vhdl_autolink_type_disable` is set, a link to the
        documentation of the type will be created if found.

    .. rst:directive:option:: init: Describes the initial value of the port, optional.

    .. code-block:: rst

      .. vhdl:portsignal:: YourPortName
        :type: std_logic
        :init: '0'

        Your port fulltext description