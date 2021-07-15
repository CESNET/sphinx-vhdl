# SPDX-License-Identifier: BSD-3-Clause

import glob
from collections import defaultdict
import os
from typing import Optional
from enum import Enum, auto

import logging

LOG = logging.getLogger('sphinxvhdl-autodoc')

entities = {}
portsignals = defaultdict(dict)
generics = defaultdict(dict)
packages = {}
objects = {
    'entities': entities,
    'portsignals': portsignals,
    'generics': generics
}


def parse_inline_doc_or_raise(line: str, current_doc: list[str]):
    if '-- ' in line:
        if len(current_doc) > 0:
            raise ValueError(
                'Documented entity has both a pre- and inline documentation; only one is allowed. Offending line:\n' +
                line)
        else:
            current_doc.append(line.split('-- ', 1)[1])


class ParseState(Enum):
    ENTITY_DECL = auto()
    PORT = auto()
    GENERIC = auto()
    PACKAGE = auto()


def init(path: str) -> None:
    for filename in (
            glob.glob(os.path.join(path, "**", "*.vhd"), recursive=True) + glob.glob(os.path.join(path, "**", "*.vhdl"),
                                                                                     recursive=True)):
        with open(filename, 'r') as source_file:
            source_code = source_file.readlines()

        current_doc = []
        current_entity = ''
        current_package = ''
        state: Optional[ParseState] = None
        open_parentheses = 0
        lineno = 0
        for line in source_code:
            lineno += 1
            line = line.strip()
            if line.startswith('-- '):
                current_doc.append(line[3:])
            elif line == '--':
                current_doc.append('')
            elif line.lower().startswith('entity ') and ' is' in line:
                try:
                    parse_inline_doc_or_raise(line, current_doc)
                except ValueError as ex:
                    LOG.warning(f'Error parsing file {filename} at line {lineno}:')
                    LOG.warning(ex.args[0])
                current_entity = line.split()[1]
                entities[current_entity.lower()] = current_doc
                current_doc = []
                state = ParseState.ENTITY_DECL
            elif state == ParseState.ENTITY_DECL and line.lower().startswith('port'):
                state = ParseState.PORT
                current_doc = []
            elif state == ParseState.ENTITY_DECL and line.lower().startswith('generic'):
                state = ParseState.GENERIC
                current_doc = []
            elif state == ParseState.PORT and ':' in line:
                try:
                    parse_inline_doc_or_raise(line, current_doc)
                except ValueError as ex:
                    LOG.warning(f'Error parsing file {filename} at line {lineno}:')
                    LOG.warning(ex.args[0])
                definition = line.split(';')[0].split(':=')[0].strip()
                if definition.lower().startswith('signal'):
                    definition = definition[6:].strip()
                portsignals[current_entity.lower()][definition] = current_doc
                current_doc = []
            elif state == ParseState.GENERIC and ':' in line:
                try:
                    parse_inline_doc_or_raise(line, current_doc)
                except ValueError as ex:
                    LOG.warning(f'Error parsing file {filename} at line {lineno}:')
                    LOG.warning(ex.args[0])
                definition = line.split(';')[0].strip()
                if ':=' not in definition:
                    definition += ':= UNDEFINED'
                if definition.lower().startswith('constant'):
                    definition = definition[8:].strip()
                generics[current_entity.lower()][definition] = current_doc
                current_doc = []
            elif state == ParseState.ENTITY_DECL and line.lower().startswith('end'):
                state = None
                current_doc = []
            elif state is None and line.lower().startswith('package'):
                state = ParseState.PACKAGE
                current_package = line.split()[1]
                packages[current_package.lower()] = current_doc
                current_doc = []
            elif state is ParseState.PACKAGE and line.lower().startswith('end package'):
                state = None
                current_doc = []
            else:
                current_doc = []
            if state in (ParseState.PORT, ParseState.GENERIC):
                open_parentheses += line.count('(')
                open_parentheses -= line.count(')')
                if open_parentheses == 0:
                    state = ParseState.ENTITY_DECL
