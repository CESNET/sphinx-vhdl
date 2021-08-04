# vhdl.py: A vhdl domain for the Sphinx documentation system
# Copyright (C) 2021 CESNET z.s.p.o.
# Author(s): Jindrich Dite <xditej01@stud.fit.vutbr.cz>
#
# SPDX-License-Identifier: BSD-3-Clause

from collections import defaultdict
from typing import Iterable, Tuple, List, Optional

from docutils import nodes
from docutils.statemachine import StringList
from docutils.parsers.rst import directives

from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription, T
from sphinx.domains import Domain, Index, IndexEntry
from sphinx.roles import XRefRole
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import make_refnode

from . import autodoc


def init_autodoc(domain: Domain):
    if not domain.data['autodoc_initialized']:
        domain.data['autodoc_initialized'] = True
        autodoc.init(domain.env.app.config.vhdl_autodoc_source_path)


class VHDLEnumTypeDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature):
        signode += addnodes.desc_sig_keyword(text='TYPE ')
        signode += addnodes.desc_name(text=sig)
        signode += addnodes.desc_sig_keyword(text=' IS')

        return sig

    def add_target_and_index(self, name: T, sig: str, signode: desc_signature) -> None:
        name = f'vhdl-enum-{sig.lower()}'
        signode['ids'].append(name)
        if 'noindex' not in self.options:
            self.env.domaindata['vhdl']['types'].append((name, sig, 'Enumeration', self.env.docname))
            self.env.domaindata['vhdl']['refs']['types'][sig.split('.')[-1].lower()].append(
                (sig.lower(), (self.env.docname, name)))


class VHDLRecordTypeDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature):
        signode += addnodes.desc_sig_keyword(text='TYPE ')
        signode += addnodes.desc_name(text=sig)
        signode += addnodes.desc_sig_keyword(text=' IS RECORD')

        return sig

    def add_target_and_index(self, name: T, sig: str, signode: desc_signature) -> None:
        name = f'vhdl-record-{sig.lower()}'
        signode['ids'].append(name)
        if 'noindex' not in self.options:
            self.env.domaindata['vhdl']['types'].append((name, sig, 'Record', self.env.docname))
            self.env.domaindata['vhdl']['refs']['types'][sig.split('.')[-1].lower()].append(
                (sig.lower(), (self.env.docname, name)))


class VHDLGeneralTypeDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_sig_keyword(text='TYPE ')
        signode += addnodes.desc_name(text=sig.split(':')[0].strip())
        signode += addnodes.desc_sig_keyword(text=' : ')
        tempnode = nodes.entry('')
        self.state.nested_parse(StringList([sig.split(':', 1)[-1].strip()]), 0, tempnode)
        type_name = addnodes.desc_name()
        signode += type_name
        type_name += tempnode[0][0]
        return sig

    def add_target_and_index(self, name: T, sig: str, signode: desc_signature) -> None:
        name = f'vhdl-type-{sig.lower()}'
        signode['ids'].append(name)
        if 'noindex' not in self.options:
            self.env.domaindata['vhdl']['types'].append((name, sig, 'Type', self.env.docname))
            self.env.domaindata['vhdl']['refs']['types'][sig.split('.')[-1].lower()].append(
                (sig.lower(), (self.env.docname, name)))

class VHDLEnumValDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_name(text=sig)
        return sig


class VHDLRecordElementDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_name(text=sig.split(':')[0].strip())
        signode += addnodes.desc_sig_keyword(text=' : ')
        tempnode = nodes.entry('')
        self.state.nested_parse(StringList([sig.split(':', 1)[-1].strip()]), 0, tempnode)
        type_name = addnodes.desc_name()
        signode += type_name
        type_name += tempnode[0][0]
        return sig


class VHDLFunctionDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_sig_keyword(text='FUNCTION ')
        signode += addnodes.desc_name(text=sig.split()[0])
        signode += addnodes.desc_sig_keyword(text=' RETURNS ')
        signode += addnodes.desc_name(text=sig.split()[1])
        return sig


class VHDLEntityDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_sig_keyword(text='ENTITY ')
        signode += addnodes.desc_name(text=sig)
        signode += addnodes.desc_sig_keyword(text=' IS')
        return sig

    def add_target_and_index(self, name: T, sig: str, signode: desc_signature) -> None:
        name = f'vhdl-entity-{sig.lower()}'
        signode['ids'].append(name)
        if 'noindex' not in self.options:
            self.env.domaindata['vhdl']['refs']['entity'][sig.split('.')[-1].lower()].append(
                (sig.lower(), (self.env.docname, name))
            )


class VHDLEntityIOGenericDirective(SphinxDirective):
    has_content = True
    required_arguments = 1
    table_headers: Tuple[str, str, str, str]
    title: str
    id_title: str

    def get_fields_from_definition(self, definition: str) -> Tuple[str, str, str]:
        raise NotImplementedError

    def run(self):
        table = nodes.table()
        group = nodes.tgroup()
        table += group

        head = nodes.thead()
        body = nodes.tbody()
        group += nodes.colspec(colwidth=10)
        group += nodes.colspec(colwidth=10)
        group += nodes.colspec(colwidth=10)
        group += nodes.colspec(colwidth=70)
        group += head
        group += body

        row: Optional[nodes.row]
        row = nodes.row()
        row += nodes.entry('', nodes.paragraph('', nodes.Text(self.table_headers[0])))
        row += nodes.entry('', nodes.paragraph('', nodes.Text(self.table_headers[1])))
        row += nodes.entry('', nodes.paragraph('', nodes.Text(self.table_headers[2])))
        row += nodes.entry('', nodes.paragraph('', nodes.Text(self.table_headers[3])))
        head += row
        row = None
        current_description_lines = StringList()
        index = 0
        description_entry = nodes.entry('')
        while len(self.content) > index:
            if len(self.content[index]) > 0 and not self.content[index][0].isspace():
                if row is not None:
                    body += row
                row = nodes.row()
                fields = self.get_fields_from_definition(self.content[index])
                row_id = f'vhdl-{self.id_title}-{self.arguments[0].lower()}-{fields[0].lower()}'
                self.env.domaindata['vhdl']['refs'][self.id_title][fields[0].lower()].append(
                    (self.arguments[0].lower(), (self.env.docname, row_id)))
                row['ids'].append(row_id)
                row += nodes.entry('', nodes.paragraph('', nodes.Text(fields[0])))

                refnode = pending_xref(refdomain='vhdl', reftype='type', reftarget=fields[1])
                refnode += nodes.Text(fields[1])
                type_node = nodes.entry('')
                self.state.nested_parse(StringList(initlist=[fields[1]]), 0, type_node)
                row += type_node

                row += nodes.entry('', nodes.paragraph('', nodes.Text(fields[2])))

                self.state.nested_parse(current_description_lines.get_indented()[0], 0, description_entry)
                description_entry = nodes.entry('')
                row += description_entry
                current_description_lines = StringList()
            else:
                current_description_lines.append(self.content[index], source=self.content.info(index))
            index += 1
        if row is not None:
            self.state.nested_parse(current_description_lines.get_indented()[0], 0, description_entry)
            body += row

        return [addnodes.desc_name(text=self.title), table]


class VHDLPortsDirective(VHDLEntityIOGenericDirective):
    id_title = 'portsignal'
    title = 'Ports'
    table_headers = 'Port', 'Type', 'Mode', 'Description'

    def get_fields_from_definition(self, definition: str) -> Tuple[str, str, str]:
        try:
            return (
                definition.split(":")[0].strip(),
                definition.split(":", 1)[1].strip().split(maxsplit=1)[1],
                definition.split(":", 1)[1].strip().split()[0]
            )
        except:
            raise ValueError(
                f'Malformed port definition, must be in the form `name : mode type`, got {definition}'
            )


class VHDLParametersDirective(VHDLEntityIOGenericDirective):
    id_title = 'parameters'
    title = 'Parameters'
    table_headers = 'Parameter', 'Type', 'Mode', 'Description'

    def get_fields_from_definition(self, definition: str) -> Tuple[str, str, str]:
        try:
            return (
                definition.split(":")[0].strip(),
                definition.split(":", 1)[1].strip().split(maxsplit=1)[1],
                definition.split(":", 1)[1].strip().split()[0]
            )
        except:
            raise ValueError(
                f'Malformed port definition, must be in the form `name : mode type`, got {definition}'
            )


class VHDLGenericsDirective(VHDLEntityIOGenericDirective):
    id_title = 'genconstant'
    title = 'Generics'
    table_headers = 'Generic', 'Type', 'Default', 'Description'

    def get_fields_from_definition(self, definition: str) -> Tuple[str, str, str]:
        try:
            return (
                definition.split(':')[0].strip(),
                definition.split(':', 1)[1].split(':=')[0].strip(),
                definition.split(':=')[1].strip()
            )
        except:
            raise ValueError(
                f"Malformed generic definition, must be in the form `name : type := defaultValue`, got {definition}"
            )


class VHDLPackagesDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_sig_keyword(text='PACKAGE ')
        signode += addnodes.desc_name(text=sig)
        signode += addnodes.desc_sig_keyword(text=' IS')
        return sig


class VHDLAutoEntityDirective(VHDLEntityDirective):
    option_spec = {
        'noautoports': directives.flag,
        'noautogenerics': directives.flag
    }

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        init_autodoc(self.env.domains['vhdl'])
        self.content = self.content + StringList(['', ''] + autodoc.entities[sig.lower()])
        if 'noautogenerics' not in self.options:
            self.content = self.content + StringList(['', f'.. vhdl:autogenerics:: {sig}', ''])
        if 'noautoports' not in self.options:
            self.content = self.content + StringList(['', f'.. vhdl:autoports:: {sig}', ''])
        return super().handle_signature(sig, signode)


class VHDLAutoRecordDirective(VHDLRecordTypeDirective):
    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        init_autodoc(self.env.domains['vhdl'])
        self.content = self.content + StringList(['', ''] + autodoc.records[sig])
        for key, value in autodoc.record_elements[sig].items():
            self.content = self.content + StringList(['', '', f'.. vhdl:recordelem:: {key}', ''] + ['  ' + x for x in value])

        return super().handle_signature(sig, signode)


class VHDLAutoFunctionDirective(VHDLFunctionDirective):
    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        init_autodoc(self.env.domains['vhdl'])
        identifier = get_closest_identifier(sig.lower(), list(autodoc.functions.items()))
        self.content = self.content + StringList(['', ''] + identifier[1])
        super().handle_signature(f'{identifier[0].split(".")[-1]} {identifier[0].split(".")[0]}', signode)
        return sig


class VHDLAutoEnumDirective(VHDLEnumTypeDirective):
    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        init_autodoc(self.env.domains['vhdl'])
        self.content = self.content + StringList(['', ''] + autodoc.enums[sig])
        for key, value in autodoc.enumvals[sig].items():
            self.content = self.content + StringList(['', '', f'.. vhdl:enumval:: {key}', ''] + ['  ' + x for x in value])
        return super().handle_signature(sig, signode)


class VHDLAutoPackageDirective(VHDLPackagesDirective):
    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        init_autodoc(self.env.domains['vhdl'])
        self.content = StringList(get_closest_identifier(sig, list(autodoc.packages.items()))[1] + ['', '']) + self.content
        return super().handle_signature(sig, signode)


class VHDLAutoPortsDirective(VHDLPortsDirective):
    has_content = False

    def run(self):
        init_autodoc(self.env.domains['vhdl'])
        self.content = StringList(
            [item for subitem in [[key, *[f'  {x}' for x in autodoc.portsignals[self.arguments[0].lower()][key]]]
                                  for key in autodoc.portsignals[self.arguments[0].lower()].keys()] for item in subitem]
        )
        return super().run()


class VHDLAutoGenericsDirective(VHDLGenericsDirective):
    has_content = False

    def run(self):
        init_autodoc(self.env.domains['vhdl'])
        self.content = StringList(
            [item for subitem in [[key, *[f'  {x}' for x in autodoc.generics[self.arguments[0].lower()][key]]]
                                  for key in autodoc.generics[self.arguments[0].lower()].keys()] for item in subitem]
        )
        return super().run()


class VHDLAutoTypeDirective(VHDLGeneralTypeDirective):

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        init_autodoc(self.env.domains['vhdl'])
        closest_identifier = get_closest_identifier(sig, autodoc.types.items())
        self.content = self.content + StringList(['', ''] + closest_identifier[1][1])
        return super().handle_signature(sig + " : " + closest_identifier[1][0], signode)


class VHDLTypeIndex(Index):
    name = 'typeindex'
    localname = "Type Index"
    shortname = 'Types'

    def __init__(self, *args, **kwargs):
        super(VHDLTypeIndex, self).__init__(*args, **kwargs)

    def generate(self, docnames: Iterable[str] = None) -> Tuple[List[Tuple[str, List[IndexEntry]]], bool]:
        if docnames is not None:
            type_list = sorted([x for x in self.domain.data['types'] if x[3] in docnames], key=lambda x: x[1])
        else:
            type_list = sorted(self.domain.data['types'], key=lambda x: x[1])

        result: List[Tuple[str, List[IndexEntry]]] = []
        for name, sig, kind, docname in type_list:
            result.append((sig[0], [IndexEntry(sig, 0, docname, name, f'{kind} Type', '', '')]))

        return result, True


def get_closest_identifier(target_identifier: str, search_through: List[Tuple[str, T]]) -> Tuple[str, T]:
    """
    Finds the item with the closes matching identifier to a target one in a list
    :param target_identifier: an identifier to match against
    :param search_through: List of pairs of an identifier and any other bound data
    :return: The tuple with closes match
    """
    identifier_part = target_identifier.split('.')
    option_list = []
    for x in search_through:
        a = 0
        for y in x[0].split('.'):
            if y in identifier_part:
                a += 1
        option_list.append((a, x))
    return max(option_list, key=lambda z: z[0])[1]


class VHDLDomain(Domain):
    name = 'vhdl'
    label = 'VHDL Language'
    directives = {
        'enum': VHDLEnumTypeDirective,
        'enumval': VHDLEnumValDirective,
        'entity': VHDLEntityDirective,
        'autoentity': VHDLAutoEntityDirective,
        'autoports': VHDLAutoPortsDirective,
        'autopackage': VHDLAutoPackageDirective,
        'autogenerics': VHDLAutoGenericsDirective,
        'autorecord': VHDLAutoRecordDirective,
        'autoenum': VHDLAutoEnumDirective,
        'autotype': VHDLAutoTypeDirective,
        'autofunction': VHDLAutoFunctionDirective,
        'function': VHDLFunctionDirective,
        'parameters': VHDLParametersDirective,
        'ports': VHDLPortsDirective,
        'generics': VHDLGenericsDirective,
        'package': VHDLPackagesDirective,
        'record': VHDLRecordTypeDirective,
        'recordelem': VHDLRecordElementDirective,
        'type': VHDLGeneralTypeDirective,
    }
    initial_data = {
        'types': [],
        'refs': {
            'types': defaultdict(list),
            'portsignal': defaultdict(list),
            'genconstant': defaultdict(list),
            'parameters': defaultdict(list),
            'entity': defaultdict(list),
        },
        'autodoc_initialized': False
    }
    indices = {
        VHDLTypeIndex
    }
    roles = {
        'portsignal': XRefRole(),
        'genconstant': XRefRole(),
        'type': XRefRole(),
        'entity': XRefRole(),
    }

    def resolve_xref(self, env: "BuildEnvironment", fromdocname: str, builder: "Builder", typ: str, target: str,
                     node: pending_xref, contnode: nodes.Element) -> Optional[nodes.Element]:
        if typ == 'type':
            index = self.data['refs']['types']
        elif typ == 'portsignal':
            index = self.data['refs']['portsignal']
        elif typ == 'genconstant':
            index = self.data['refs']['genconstant']
        elif typ == 'entity':
            index = self.data['refs']['entity']
        elif True:
            raise NotImplementedError
        simple_name = target.split('.')[-1].lower()
        if simple_name in index:
            target_address = get_closest_identifier(target, index[simple_name])
            result = make_refnode(builder, fromdocname,
                                  target_address[1][0],
                                  target_address[1][1],
                                  contnode)
            return result


def setup(app: Sphinx):
    app.add_domain(VHDLDomain)
    app.add_config_value('vhdl_autodoc_source_path', '.', 'env', [str])

    return {
        'version': '0.1'
    }
