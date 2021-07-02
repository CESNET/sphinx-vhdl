from docutils import nodes
from docutils.nodes import Element

from docutils.parsers.rst import directives
from sphinx.addnodes import desc_signature
from sphinx.directives import ObjectDescription, T
from sphinx import addnodes
from sphinx.domains import Domain
from sphinx.application import Sphinx


class VHDLPortSignalDirective(ObjectDescription):
    has_content = True
    required_arguments = 1
    option_spec = {
        'type': directives.unchanged_required,
        'init': directives.unchanged
    }

    def handle_signature(self, sig: str, signode: desc_signature) -> T:
        signode += addnodes.desc_name(text=sig)

        if 'type' in self.options:
            signode += addnodes.desc_type(text=f" : {self.options.get('type')}")

        return sig


class VHDLDomain(Domain):
    name = 'vhdl'
    label = 'VHDL Language'
    directives = {
        'portsignal': VHDLPortSignalDirective,
    }

    def get_full_qualified_name(self, node: Element) -> str:
        if type(node) == VHDLPortSignalDirective:
            node: VHDLPortSignalDirective
            return f'vhdl.portsignal.{node.arguments[0]}'
        raise TypeError


def setup(app: Sphinx):
    app.add_domain(VHDLDomain)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,

    }
