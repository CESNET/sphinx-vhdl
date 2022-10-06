# Sphinx-vhdl

[![PyPI](https://img.shields.io/pypi/v/sphinx-vhdl)](https://pypi.org/project/sphinx-vhdl/)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/CESNET/sphinx-vhdl/documentation?label=documentation)](https://cesnet.github.io/sphinx-vhdl/)

> A [sphinx](https://www.sphinx-doc.org/) domain for semi-automatically documenting VHDL

This extension for Sphinx allows you to keep your documentation in code and automatically draw it out into your main documentation using just few simple directives.

You can see the detailed documentation at https://cesnet.github.io/sphinx-vhdl/, or build it yourself (running `make html` while in the `doc` directory and having `sphinx` installed should be sufficient)

## Usage

The python package must be installed with
```shell
pip3 install sphinx-vhdl
```

The usage of this extension requires Python >= 3.6 and Sphinx >= 4.0.0.

## Configuration

In your sphinx `conf.py` file add

```python
extensions = ['sphinxvhdl.vhdl']
vhdl_autodoc_source_path = 'path/to/your/vhdl/sources/root'
```

## Repository maintainer

- Original: Jindřich Dítě, 230810@vut.cz
- Backup: Jakub Cabal, cabal@cesnet.cz
- Backup: Daniel Kříž, danielkriz@cesnet.cz
