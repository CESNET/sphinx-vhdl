.. _directives:

Directives
==========

.. rst:directive:: vhdl:entity

    Used for documenting individual entities. Individual ports and generics
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

.. rst:directive:: vhdl:function

    Describes a pure function. Has two required space-separated arguments - the
    name of the function and the return type.

    Parameters of the function should be documented using
    :rst:dir:`vhdl:parameters`

    Example:

    .. code-block:: rst

        .. vhdl:function:: log2 integer

            Calculates the base 2 logarithm of the parameter

            .. vhdl:parameters:: n : in integer/std_logic_vector(31 downto 0)

                The number to calculate the logarithm of

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

.. rst:directive:: vhdl:package

    Used for documenting packages.

.. rst:directive:: vhdl:parameters

    Used for documenting the parameters of a subprogram (
    :rst:dir:`vhdl:function` or :rst:dir:`vhdl:procedure` ). Has one required
    argument; the name of the subprogram being documented, and uses a custom
    syntax for descriptions of the individual parameters.

    Individual parameters are described in the content of the directive; where
    lines aligned to the left offset define the parameter names and lines
    offset from those are detailed descriptions of the parameters above,
    supporting all the standard reStructuredText formatting and directives.
    Parameter definitions then take on the form
    ``parameterName : mode type``, where whitespace can be arbitrary.

    The type and description may contain full ReST syntax.

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

            DOUT     : out std_logic_vector( :vhdl:genconstant:`WORD_SIZE <UART_RX.WORD_SIZE>` - 1 downto 0)
                The received data will be written here
            DOUT_VLD : out std_logic
                When high, denotes the :vhdl:portsignal:`UART_RX.DOUT` being valid

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

.. rst:directive:: vhdl:record

    Used for documenting record-defined types. Individual fields of the type
    can be documented using :rst:dir:`vhdl:recordelem`.

    .. code-block:: rst

        .. vhdl:record:: PACKET_DATA

            Describes the data associated with each packet

            .. vhdl:recordelem:: SOURCE_IP : :vhdl:type:`IP`

                The IP address of the packet sender

            .. vhdl:recordelem:: ARRIVED_AT : TIME

                The time when the packet was received.

.. rst:directive:: vhdl:recordelem

    Used for documenting individual fields of a :rst:dir:`vhdl:record`. The
    argument of this directive should take on the form of
    ``fieldName : fieldType``, where ``fieldType`` can contain arbitrary sphinx
    syntax.

.. rst:directive:: vhdl:type

    Used for documenting types other than record- and enumeration-defined ones.

    For enumeration-defined types, please use :rst:dir:`vhdl:enum`. For record
    defined types, please use :rst:dir:`vhdl:record`.

    The argument of this directive should take on the form
    ``typeName : type signature``; where ``type signature`` may contain
    arbitrary sphinx formatting.

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

.. rst:directive:: vhdl:autoenum

    Automatically generates a documentation for an enumeration defined type.
    Has one required argument, the name of the type. For the automatic
    generation to work, the :py:attr:`vhdl_autodoc_source_path` configuration
    option must be set to point to a valid directory containing VHDL sources
    describing this entity. See :ref:`autodoc_usage` for further instructions
    on how the source code must be set up.

.. rst:directive:: vhdl:autofunction

    Automatically generates a documentation for a pure function.
    Has one required argument, the name of the type. For the automatic
    generation to work, the :py:attr:`vhdl_autodoc_source_path` configuration
    option must be set to point to a valid directory containing VHDL sources
    describing this entity. See :ref:`autodoc_usage` for further instructions
    on how the source code must be set up.

.. rst:directive:: vhdl:autogenerics

    Automatically generates a documentation for an entity's generics. Has one
    required argument, the name of the entity whose generics to document. For
    the automatic generation to work, the :py:attr:`vhdl_autodoc_source_path`
    configuration option must be set to point to a valid directory containing
    VHDL sources describing the target entity.  See  :ref:`autodoc_usage` for
    further instruction on how the source must be set up.

.. rst:directive:: vhdl:autopackage

    Automatically generates a documentation for a package. Has one required
    argument, the name of the package to document. For the automatic generation
    to work, the :py:attr:`vhdl_autodoc_source_path` configuration option must
    be set to point to a valid directory containing VHDL sources defining the
    target package. See :ref:`autodoc_usage` for further instructions on how
    the source must be set up.

.. rst:directive:: vhdl:autoports

    Automatically generates a documentation for an entity's ports. Has one
    required argument, the name of the entity whose ports to document. For the
    automatic generation to work, the :py:attr:`vhdl_autodoc_source_path`
    configuration option must be set to point to a valid directory containing
    VHDL sources describing the target entity. See :ref:`autodoc_usage` for
    further instruction on how the source must be set up.

.. rst:directive:: vhdl:autorecord

    Automatically generates a documentation for a record-defined type. Has one
    required argument, the name of the type to document. For the automatic
    generation to work, the :py:attr:`vhdl_autodoc_source_path` configuration
    option must be set to point to a valid directory containing VHDL sources
    describing the type. See :ref:`autodoc_usage` for further instructions on
    how the source must be set up.

.. rst:directive:: vhdl:autotype

    Automatically generates a documentation for a type other than enumeration-
    record-defined one. Has one required argument, the name of the type to
    document. For the automatic generation to work, the
    :py:attr:`vhdl_autodoc_source_path` configuration option must be set to
    point to a valid directory containing VHDL sources describing the type. See
    :ref:`autodoc_usage` for further instructions on how the sources must be
    set up.