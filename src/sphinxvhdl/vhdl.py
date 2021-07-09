from collections import defaultdict
from typing import Iterable, Tuple, List, Optional

from docutils import nodes
from docutils.parsers.rst import directives, Directive
from docutils.statemachine import StringList

from sphinx import addnodes
from sphinx.addnodes import desc_signature, pending_xref
from sphinx.application import Sphinx
from sphinx.directives import ObjectDescription, T
from sphinx.domains import Domain, Index, IndexEntry
from sphinx.util.nodes import make_refnode
from .directives import mode


class VHDLPortSignalDirective(ObjectDescription):
    has_content = True
    required_arguments = 1
    option_spec = {
        'type': directives.unchanged_required,
        'init': directives.unchanged,
        'mode': mode,
    }

    def handle_signature(self, sig: str, signode: desc_signature):
        signode += addnodes.desc_sig_keyword(text='SIGNAL ')
        signode += addnodes.desc_name(text=sig)

        if 'type' in self.options and 'mode' in self.options:
            signode += addnodes.desc_sig_operator(text=' : ')
            signode += addnodes.desc_sig_keyword(text=self.options.get('mode'))
            signode += addnodes.desc_sig_operator(text=' ')
            refnode = pending_xref(refdomain='vhdl', reftype='type', reftarget=self.options.get('type'))
            refnode += addnodes.desc_type(text=self.options.get('type'))
            signode += refnode

        if 'init' in self.options:
            signode += addnodes.desc_sig_operator(text=' := ')
            signode += addnodes.desc_sig_literal_string(text=self.options.get('init'))

        return sig


class VHDLEnumTypeDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature):
        signode += addnodes.desc_sig_keyword(text='TYPE ')
        signode += addnodes.desc_name(text=sig)
        signode += addnodes.desc_sig_keyword(text=' IS')

        return sig

    def add_target_and_index(self, name: T, sig: str, signode: desc_signature) -> None:
        name = f'vhdl-enum-{sig}'
        signode['ids'].append(name)
        if 'noindex' not in self.options:
            self.env.domaindata['vhdl']['types'].append((name, sig, 'Enumeration', self.env.docname))
            self.env.domaindata['vhdl']['refs']['types'][sig.split('.')[-1]].append((sig, (self.env.docname, name)))


class VHDLEnumValDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_name(text=sig)
        return sig


class VHDLEntityDirective(ObjectDescription):
    has_content = True
    required_arguments = 1

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_sig_keyword(text='ENTITY ')
        signode += addnodes.desc_name(text=sig)
        signode += addnodes.desc_sig_keyword(text=' IS')
        return sig


class VHDLPortsDirective(Directive):
    has_content = True
    required_arguments = 1

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
        row += nodes.entry('', nodes.paragraph('', nodes.Text('Port')))
        row += nodes.entry('', nodes.paragraph('', nodes.Text('Mode')))
        row += nodes.entry('', nodes.paragraph('', nodes.Text('Type')))
        row += nodes.entry('', nodes.paragraph('', nodes.Text('Description')))
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
                row['ids'].append(
                    f'vhdl-portsignal-{self.arguments[0].lower()}-{self.content[index].split(":")[0].strip().lower()}')
                row += nodes.entry('', nodes.paragraph('', nodes.Text(self.content[index].split(":")[0].strip())))
                row += nodes.entry('', nodes.paragraph('', nodes.Text(
                    self.content[index].split(":", 1)[1].strip().split()[0])))
                row += nodes.entry('', nodes.paragraph('', nodes.Text(
                    self.content[index].split(":", 1)[1].strip().split(maxsplit=1)[1])))

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

        return [addnodes.desc_sig_keyword(text='Ports'), table]


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


def get_closest_identifier(target_identifier: str, search_through: list[tuple[str, T]]) -> tuple[str, T]:
    """
    Finds the item with the closes matching identifier to a target one in a list
    :param target_identifier: an identifier to match against
    :param search_through: List of pairs of an identifier and any other bound data
    :return: The tuple with closes match
    """
    # TODO implement
    for x in search_through:
        if target_identifier.split('.')[-1] in x[0]:
            return x
    raise ValueError


class VHDLDomain(Domain):
    name = 'vhdl'
    label = 'VHDL Language'
    directives = {
        'enum': VHDLEnumTypeDirective,
        'enumval': VHDLEnumValDirective,
        'entity': VHDLEntityDirective,
        'ports': VHDLPortsDirective,
    }
    initial_data = {
        'types': [],
        'refs': {'types': defaultdict(list)}
    }
    indices = {
        VHDLTypeIndex
    }

    def resolve_xref(self, env: "BuildEnvironment", fromdocname: str, builder: "Builder", typ: str, target: str,
                     node: pending_xref, contnode: nodes.Element) -> Optional[nodes.Element]:
        if typ == 'type':
            index = self.data['refs']['types']
        elif True:
            raise NotImplementedError
        simple_name = target.split('.')[-1]
        if simple_name in index and not env.app.config.vhdl_autolink_type_disable:
            target_address = get_closest_identifier(target, index[simple_name])
            result = make_refnode(builder, fromdocname,
                                  target_address[1][0],
                                  target_address[1][1],
                                  contnode)
            return result


def setup(app: Sphinx):
    app.add_config_value('vhdl_autolink_type_disable', False, 'html')
    app.add_domain(VHDLDomain)

    return {
        'version': '0.1'
    }
