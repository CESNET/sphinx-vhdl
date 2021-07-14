Directives
==========

.. rst:directive:: vhdl:entity

    Used for documenting individual entitites. Individual ports and generics
    should be specified under :rst:dir:`vhdl:ports` or
    :rst:dir:`vhdl:generics`, respectively.

    .. code-block:: rst

        .. vhdl:entity:: EntityName

            Entity description and full-text documentation

            .. vhdl:generics:: EntityName

                FREQ: natural := 5

            .. vhdl:ports:: EntityName

                CLK : in 1

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

    Used for documenting the generic constants of an entity. Has one required
    argument; the name of the entity being documented, and uses a custom syntax
    for description of the individual constants.

    Individual constant are described in the content of the directive; where
    lines aligned to the left offset define the constants and lines offset from
    those are detailed descriptions of the constants above, supporting all the
    standard REStructured Text formatting and directives. Constant definitions
    then take on the form ``constantName : constantType := defaultValue``,
    where all the fields are mandatory and whitespace may be arbitrary.

    The types and description may contain full ReST syntax.

    Example

    .. code-block:: rst

        .. vhdl:generics:: UART_RX

            WORD_SIZE:natural:=8
                The machine word here is 8 bits. Used for :vhdl:portsignal:`DOUT`.


                It just is.
            DWORD_SIZE   : :vhdl:type:`YourAwesomeType` := 16


            QWORD_SIZE : float     := 32.0
                Because why sink when you can float?

.. rst:directive:: vhdl:ports

    Used for documenting the ports of an entity. Has one required argument;
    the name of the entity being documented, and uses a custom syntax for
    descriptions of the individual ports.

    Individual ports are described in the content of the directive; where lines
    aligned to the left offset define the ports and lines offset from those are
    detailed descriptions of the ports above, supporting all the standard
    REStructured text formatting and directives. Port definitions then take on
    the form ``portName : mode sig_width``, where whitespace can be arbitrary.

    Data width signifies the width of the ``std_logic_vector`` on the port.

    The signal width and description may contain full ReST syntax.

    Example

    .. code-block:: rst

        .. vhdl:ports:: UART_RX

            CLK:in 1
                Receiver clock at 8 times the frequency of the input signal
            RST      :  in 1
                Reset signal

                Pull to high for at least one clock cycle before using this
                entity
            DIN      : in 1
                Data input line

            DOUT     : out :vhdl:genconstant:`WORD_SIZE <UART_RX.WORD_SIZE>`
                The received data will be written here
            DOUT_VLD : out 1
                When high, denotes the :vhdl:portsignal:`UART_RX.DOUT` being valid

Auto- Directives
----------------

.. rst:directive:: vhdl:autoentity

    Automatically generates a documentation for an entity. Has one required
    argument, the  name of the entity. For the automatic generation to work,
    the :py:attr:`vhdl_autodoc_source_path` configuration option must be set to
    point to a valid directory containing VHDL sources describing this entity.
    See :ref:`autodoc_usage` for further instructions on how the source code
    must be set up.

    .. rst:directive:option:: noautogenerics

        Do not generate a :rst:dir:`vhdl:autogenerics` directive as part of
        generating the automatic documentation for the entity.

    .. rst:directive:option:: noautoports

        Do not generate a :rst:dir:`vhdl:autoentity` directive as part of
        generating the automatic documentation for the entity.

.. rst:directive:: vhdl:autogenerics

    Automatically generates a documentation for an entity's generics. Has one
    required argument, the name of the entity whose generics to document. For
    the automatic generation to work, the :py:attr:`vhdl_autodoc_source_path`
    configuration option must be set to point to a valid directory containing
    VHDL sources describing the target entity.  See  :ref:`autodoc_usage` for
    further instruction on how the source must be set up

.. rst:directive:: vhdl:autoports

    Automatically generates a documentation for an entity's ports. Has one
    required argument, the name of the entity whose ports to document. For the
    automatic generation to work, the :py:attr:`vhdl_autodoc_source_path`
    configuration option must be set to point to a valid directory containing
    VHDL sources describing the target entity. See :ref:`autodoc_usage` for
    further instruction on how the source must be set up