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

    Used for documenting the generic constants of an entity. Has one required
    argument; the name of the entity being documented, and uses a custom syntax
    for description of the individual constants.

    Individual constant are described in the content of the directive; where
    lines aligned to the left offset define the constants and lines offset from
    those are detailed descriptions of the constants above, supporting all the
    standard REStructured Text formatting and directives. Constant definitions
    then take on the form ``constantName : constantType := defaultValue``,
    where all the fields are mandatory and whitespace may be arbitrary.

    Individual constants will automatically cross-reference the definitions of
    their types if found, unless disabled by
    :py:attr:`vhdl_autolink_type_disable`

    Example

    .. code-block:: rst

        .. vhdl:generics:: UART_RX

            WORD_SIZE:natural:=8
                The machine word here is 8 bits.


                It just is.
            DWORD_SIZE   : integer := 16


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
    the form ``portName : mode type``, where whitespace can be arbitrary.

    Individual ports will automatically cross-reference the definitions of
    their types if found, unless disabled by
    :py:attr:`vhdl_autolink_type_disable`

    Example

    .. code-block:: rst

        .. vhdl:ports:: UART_RX

            CLK:in std_logic
                Receiver clock at 8 times the frequency of the input signal
            RST      :  in std_logic
                Reset signal

                Pull to high for at least one clock cycle before using this
                entity
            DIN      : in std_logic
                Data input line

            DOUT     : out std_logic_vector(7 downto 0)
                The received data will be written here
            DOUT_VLD : out std_logic
                When high, denotes the DOUT being valid
