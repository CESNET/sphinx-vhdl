# SPHINX-VHDL

[![PyPI](https://img.shields.io/pypi/v/sphinx-vhdl)](https://pypi.org/project/sphinx-vhdl/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/CESNET/sphinx-vhdl/.github/workflows/doc.yml)](https://cesnet.github.io/sphinx-vhdl/)

> A [sphinx](https://www.sphinx-doc.org/) domain for semi-automatically documenting VHDL

This extension for Sphinx allows you to keep your documentation in code and automatically draw it out into your main documentation using just few simple directives.

You can see the detailed documentation at https://cesnet.github.io/sphinx-vhdl/, or build it yourself (running `make` while in the `doc` directory and having `sphinx` + `sphinx_rtd_theme` installed should be sufficient)

## Usage

The python package must be installed with
```shell
pip3 install sphinx-vhdl
```

This extension requires Python >= 3.8 and Sphinx >= 6.0.0.

*Note that your documentation may use multiple sphinx extensions or an alternative theme (such as `sphinx_rtd_theme`), which you must also have installed.*

## Configuration

In your sphinx `conf.py` file add

```python
extensions = ['sphinxvhdl.vhdl']
vhdl_autodoc_source_path = 'path/to/your/vhdl/sources/root'
```

## Where is the SPHINX-VHDL extension used?

- [Open FPGA Modules (OFM) by CESNET](https://github.com/CESNET/ofm/)
- [NDK Minimal Application by CESNET](https://github.com/CESNET/ndk-app-minimal)
- *Do you use SPHINX-VHDL in your public VHDL repository? Please add a link to this list!*

## Repository maintainer

- Jakub Cabal, cabal@cesnet.cz
- Vladislav Válek, valekv@cesnet.cz
