.. sphinx-vhdl documentation master file, created by
   sphinx-quickstart on Wed Jul  7 10:06:12 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

sphinx-vhdl
===========
**sphinx-vhdl** is a `Sphinx`_ extension to generate documentation for the
VHDL language


Usage
=====
``doc/conf.py``

.. code-block:: python

  extensions = ['sphinxvhdl.vhdl']

Recognized directives
=====================

================================== ==================================
Directive                          Description
================================== ==================================
:rst:dir:`vhdl:autoentity`         Automatic documentation of entity.
:rst:dir:`vhdl:autoenum`           Automatic documentation of enumeration types.
:rst:dir:`vhdl:autogenerics`       Automatic documentation of generics.
:rst:dir:`vhdl:autopackage`        Automatic documentation of package.
:rst:dir:`vhdl:autoports`          Automatic documentation of ports.
:rst:dir:`vhdl:autorecord`         Automatic documentation of record types.
:rst:dir:`vhdl:entity`             A single entity.
:rst:dir:`vhdl:enum`               Enumeration-defined type.
:rst:dir:`vhdl:enumval`            A single value in :rst:dir:`vhdl:enum`.
:rst:dir:`vhdl:generics`           Ports of an :rst:dir:`vhdl:entity`.
:rst:dir:`vhdl:package`            A whole single package.
:rst:dir:`vhdl:ports`              Generics of an :rst:dir:`vhdl:entity`.
:rst:dir:`vhdl:record`             Record-defined type.
:rst:dir:`vhdl:recordelem`         A single field in :rst:dir:`vhdl:record`
:rst:dir:`vhdl:type`               A type other than a record or enumeration.
================================== ==================================

Recognized roles
================

================================== ==================================
Role                               Description
================================== ==================================
:rst:role:`vhdl:entity`            References :rst:dir:`vhdl:entity`.
:rst:role:`vhdl:genconstant`       References individual constants in :rst:dir:`vhdl:generics`.
:rst:role:`vhdl:portsignal`        References individual ports in :rst:dir:`vhdl:ports`.
:rst:role:`vhdl:type`              References :rst:dir:`vhdl:enum`.
================================== ==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   directives_detailed.rst
   roles_detailed.rst
   config.rst
   autodoc.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Sphinx: https://http://www.sphinx-doc.org
