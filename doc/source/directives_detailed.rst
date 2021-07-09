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

    Used for documenting the ports of an entity. Has one required argument;
    the name of the entity being documented, and uses a custom syntax for
    describing the individual ports.

    Individual ports are described in the content of the directive; where lines
    aligned to the left offset define the ports and lines offset from those are
    detailed descriptions of the ports above, with blank lines for paragraph
    ends. Port definitions then take on the form ``portName : mode type``,
    where whitespace can be arbitrary.

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
