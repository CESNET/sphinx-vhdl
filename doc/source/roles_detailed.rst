.. _roles:

Roles
=====

.. rst:role:: vhdl:entity

    This role allows referencing entities defined by an :rst:dir:`vhdl:entity`
    directive or :rst:dir:`vhdl:autoentity` directive.

.. rst:role:: vhdl:gengeneric

    This role allows referencing individual constants inside a
    :rst:dir:`vhdl:generics` or :rst:dir:`vhdl:autogenerics` directive.

.. rst:role:: vhdl:genconstant

    This role allows referencing individual constants inside a
    :rst:dir:`vhdl:constants` or :rst:dir:`vhdl:autoconstants` directive.

.. rst:role:: vhdl:portsignal

    This role allows referencing individual ports inside a
    :rst:dir:`vhdl:ports` or :rst:dir:`vhdl:autoports` directive.

.. rst:role:: vhdl:type

    This role allows referencing types defined by :rst:dir:`vhdl:enum` .


.. _name_resolution:

Name resolution
---------------

All identifiers can be referred to in a variety of names. Taking for example
ports, they can be specified with either just a short name of the port, in
which case it may however end up referring to identically named port on another
entity, or it may be prepended with arbitrarily large path specifier
delimitered by dots, e.g. ``ENTITYNAME.PORTNAME``, in which case it will try to
resolve to the closest matching identifier.

The resolution always exactly matches the last part of both identifiers, and
then filters more on it by checking how many __parts__ are identical between
the source and target identifier; the identifier with the most matches is
selected.