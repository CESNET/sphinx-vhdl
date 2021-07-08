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
``vhdl:enum``                      Enumeration-defined type. :rst:dir:`Example <vhdl:enum>`
``vhdl:portsignal``                A port of an entity. :rst:dir:`Example <vhdl:portsignal>`
================================== ==================================


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   directives_detailed.rst
   config.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Sphinx: https://http://www.sphinx-doc.org
