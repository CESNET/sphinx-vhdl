# autodoc.py: A basic VHDL parser and documentation extractor
# Copyright (C) 2021 CESNET z.s.p.o.
# Author(s): Jindrich Dite <xditej01@stud.fit.vutbr.cz>
#
# SPDX-License-Identifier: BSD-3-Clause

import glob
from collections import defaultdict
import os
from typing import Optional, List
from enum import Enum, auto

import logging

LOG = logging.getLogger('sphinxvhdl-autodoc')

entities = {}
portsignals = defaultdict(dict)
groups_desc = {}
constants = defaultdict(dict)
generics = defaultdict(dict)
packages = {}
records = {}
record_elements = defaultdict(dict)
enums = {}
enumvals = defaultdict(dict)
types = {}
functions = {}

# Function for parsing line comments
def parse_inline_doc_or_raise(line: str, current_doc: List[str]):
    if '-- ' in line:
        if len(current_doc) > 0:
            raise ValueError(
                'Documented entity has both a pre- and inline documentation; only one is allowed. Offending line:\n' +
                line)
        else:
            current_doc.append(line.split('-- ', 1)[1])


def parse_inline_doc_or_print_error(current_doc, filename, line, lineno):
    try:
        parse_inline_doc_or_raise(line, current_doc)
    except ValueError as ex:
        LOG.warning(f'Error parsing file {filename} at line {lineno}:')
        LOG.warning(ex.args)


class ParseState(Enum):
    ENTITY_DECL = auto()
    ARCH_DECL = auto()
    PORT = auto()
    CONST = auto()
    GROUPS = auto()
    GENERIC = auto()
    PACKAGE = auto()
    RECORD = auto()
    ENUM = auto()


def init(path: str) -> None:
    for filename in (
            glob.glob(os.path.join(path, "**", "*.vhd"), recursive=True) + glob.glob(os.path.join(path, "**", "*.vhdl"),
                                                                                     recursive=True)):
        with open(filename, 'r') as source_file:
            source_code = source_file.readlines()

        current_doc = []
        current_entity = '' # Name of the enetity
        current_constant = '' # Name of the constant
        current_group = '' # Name of the group
        group_definition = '' # Description of group of ports or generics
        current_package = ''
        current_type_name = ''  # record or enum
        state: Optional[ParseState] = None
        group_state: Optional[ParseState] = None
        open_parentheses = 0
        lineno = 0
        for line in source_code:
            lineno += 1
            line = line.strip()
            # Group parsing logic
            if state == ParseState.PORT and group_state == ParseState.GENERIC:
                current_group = ""

            # Line comments logic
            if line.startswith('-- '):
                # Logic for sampling names of groups of ports and generics
                if (state == ParseState.PORT or state == ParseState.GENERIC) and '====' in line:
                    group_state = state
                    state = ParseState.GROUPS
                    current_group = ""
                    current_doc = []
                elif state == ParseState.GROUPS and current_group != '' and '====' not in line:
                    current_doc.append(line[3:])
                elif state == ParseState.GROUPS and '====' not in line:
                    current_group = current_entity + " " + line[3:].strip()
                    current_doc = []
                elif state == ParseState.GROUPS and '====' in line:
                    group_definition = current_doc
                    groups_desc[current_group] = group_definition
                    state = group_state
                    current_doc = []
                else:
                    current_doc.append(line[3:])

            # If line start with keyword architecture then save name of architecture
            elif line.lower().startswith('architecture'):
                state = ParseState.ARCH_DECL
                current_constant = line.split()[3]

            # If line contains keyword constant and state is not generice then start to collecting constants
            elif state == ParseState.ARCH_DECL and 'constant' in line:
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                definition = line.split('--')[0].split(';')[0]
                if ':=' not in definition:
                    definition += ':= UNDEFINED'
                definition = definition[8:].strip()
                constants[current_constant.lower()][definition] = current_doc
                current_doc = []

            # If there is -- without gap, then ignore
            elif line == '--':
                current_doc.append('')

            # If there is word entity then try parse, save entity name and add description of entity to associative array
            # ID of ass. array is name of entity. At the end clear current description and change state to entity declaration
            elif line.lower().startswith('entity ') and ' is' in line:
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                current_entity = line.split()[1]
                entities[current_entity.lower()] = current_doc
                current_doc = []
                state = ParseState.ENTITY_DECL

            # Check if there is any port declaration
            elif state == ParseState.ENTITY_DECL and line.lower().startswith('port'):
                state = ParseState.PORT
                current_doc = []

            # Check if there is any generic declaration
            elif state == ParseState.ENTITY_DECL and line.lower().startswith('generic'):
                state = ParseState.GENERIC
                current_doc = []

            # If there is line which contains ":" then it's one of ports, parse it and save his definition
            elif state == ParseState.PORT and ':' in line:
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                definition = line.split('--')[0].split(';')[0].split(':=')[0].strip()
                if definition.lower().startswith('signal'):
                    definition = definition[6:].strip()
                if current_group == "":
                    definition = definition
                else:
                    definition = current_group + "}" + definition

                portsignals[current_entity.lower()][definition] = current_doc
                current_doc = []

            # If there is line which contains ":" then it's one of generic, parse it and save his definition
            elif state == ParseState.GENERIC and ':' in line:
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                definition = line.split('--')[0].split(';')[0].strip()
                if ':=' not in definition:
                    definition += ':= UNDEFINED'
                if definition.lower().startswith('constant'):
                    definition = definition[8:].strip()
                if current_group == "":
                    definition = definition
                else:
                    definition = current_group + "}" + definition

                generics[current_entity.lower()][definition] = current_doc
                current_doc = []

            # End of the entity was found
            elif state == ParseState.ENTITY_DECL and line.lower().startswith('end'):
                state = None
                group_state = None
                current_doc = []

            # If there is magic word package then parse package and save his definition
            elif (state is None or state is ParseState.PACKAGE) and line.lower().startswith('package'):
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                state = ParseState.PACKAGE
                current_package = ('' if current_package == '' else (current_package + '.')) + line.split()[1]
                packages[current_package.lower()] = current_doc
                current_doc = []

            # Signalization of end of the package
            elif state is ParseState.PACKAGE and line.lower().startswith('end package'):
                current_package = '.'.join(current_package.split('.')[:-1])
                state = None if current_package == '' else ParseState.PACKAGE
                current_doc = []

            # Package contains type, parse it
            elif (state is None or state is ParseState.PACKAGE) and line.lower().startswith('type'):
                if ' record' in line.split('--')[0].lower().split(maxsplit=2)[-1]:
                    parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                    records[line.split()[1]] = current_doc
                    current_doc = []
                    state = ParseState.RECORD
                    current_type_name = line.split()[1]
                elif ' '.join(line.split()[2:])[2:].strip().startswith('('):
                    parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                    enums[line.split()[1]] = current_doc
                    current_doc = []
                    state = ParseState.ENUM
                    current_type_name = line.split()[1]
                else:
                    parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                    types[line.split()[1]] = ' '.join(line.split()[3:]), current_doc
                    current_doc = []

            # Signalization of the end of record
            elif state is ParseState.RECORD and line.lower().startswith('end record'):
                if current_package != '':
                    state = ParseState.PACKAGE
                else:
                    state = None
                current_doc = []

            # Signalization of the start of record
            elif state is ParseState.RECORD and ':' in line:
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                element_name, element_type = tuple([x.strip() for x in line.split(';')[0].split(':', 1)])
                record_elements[current_type_name][f'{element_name} : {element_type}'] = current_doc
                current_doc = []

            # Enumarate parsing
            elif state is ParseState.ENUM:
                if not line.startswith(')'):
                    parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                    enumvals[current_type_name][line.split(',')[0]] = current_doc
                    current_doc = []

            # Function parsing
            elif line.lower().startswith('function') and line.split('--')[0].strip().endswith(';'):
                parse_inline_doc_or_print_error(current_doc, filename, line, lineno)
                return_type = '' if 'return' not in line else (line.split('return')[1].strip()[:-1] + '.')
                functions[return_type + line.lower().split()[1]] = current_doc
                current_doc = []

            # Ignore others
            else:
                current_doc = []

            # Connection between ports, generics and entity
            if state in (ParseState.PORT, ParseState.GENERIC):
                open_parentheses += line.split('--')[0].count('(')
                open_parentheses -= line.split('--')[0].count(')')
                if open_parentheses == 0:
                    state = ParseState.ENTITY_DECL

            # Connection between Enumerate and current package
            if state == ParseState.ENUM:
                open_parentheses += line.split('--')[0].count('(')
                open_parentheses -= line.split('--')[0].count(')')
                if open_parentheses == 0:
                    if current_package != '':
                        state = ParseState.PACKAGE
                    else:
                        state = None

