Directives
==========

.. rst:directive:: vhdl:entity

    Used for documenting individual entitites. Individual ports and generics
    should be specified under :rst:dir:`vhdl:ports` or
    :rst:dir:`vhdl:generics`, respectively.

    TODO example

.. rst:directive:: vhdl:enum

    Used for documenting enumeration defined types. Individual enum values can
    be defined using :rst:dir:`vhdl:enumVal <vhdl:enumval>`.

    .. code-block:: rst

        .. vhdl:enum:: YourTypeName

            Your type fulltext description.

            .. vhdl:enumval:: YourTypeFirstPossibleValue

                Your first possible value fulltext documentation

            .. vhdl:enumval:: YourTypeSecondPossibleValue

.. rst:directive:: vhdl:enumval

    Describes a single possible enumeration type value. Should only appear in
    :rst:dir:`vhdl:enum`

.. rst:directive:: vhdl:generics

    TODO

.. rst:directive:: vhdl:ports

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