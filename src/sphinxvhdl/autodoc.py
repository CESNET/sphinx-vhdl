# CESNET, association of legal entities (hereinafter referred to as „the
# association“) owns all right, title and interest in and to the source code
# and you are not allowed to use it in any way without the permission of the
# association. In particular, you may not, without the permission of the
# association, use, execute, reproduce, display, distribute internally or
# externally, communicate to the public, modify, perform, transmit, adapt or
# alter the source code in any way (especially, prepare new versions or
# derivative works based upon the source code), use the source code in a
# collection or connection with any other work or elements, or incorporate
# the source code in a database or any other collection of works.

import glob
from collections import defaultdict
import os
from pyVHDLParser.Token.Parser import Tokenizer
from pyVHDLParser.Blocks import TokenToBlockParser, MetaBlock, CommentBlock
from pyVHDLParser.Blocks.Common import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Structural import Entity
from pyVHDLParser.Blocks.List import PortList, GenericList
from pyVHDLParser.Base import ParserException
import logging

LOG = logging.getLogger('sphinxvhdl-autodoc')

entities = {}
portsignals = defaultdict(dict)
generics = defaultdict(dict)
objects = {
    'entities': entities,
    'portsignals': portsignals,
    'generics': generics
}


def init(path: str) -> None:
    for block in MetaBlock.BLOCKS:
        try:
            block.__cls_init__()
        except AttributeError:
            pass
    for filename in (
            glob.glob(os.path.join(path, "**", "*.vhd"), recursive=True) + glob.glob(os.path.join(path, "**", "*.vhdl"),
                                                                                     recursive=True)):
        with open(filename, 'r') as source_file:
            source_code = source_file.read()
        token_stream = Tokenizer.GetVHDLTokenizer(source_code)
        block_stream = TokenToBlockParser.Transform(token_stream)
        current_doc = []
        current_entity = ''
        last_documented = -1, None, 'undefined'  # line of definition; dictionary with objects; key in dictionary
        try:
            for block in block_stream:
                if type(block) is IndentationBlock:
                    continue
                if type(block) is LinebreakBlock:
                    current_doc = []
                    continue
                if type(block) is CommentBlock:
                    if len(str(block).strip()) > 2:
                        if str(block).strip().startswith('-- '):
                            if block.StartToken.Start.Row == last_documented[0]:
                                if len(last_documented[1][last_documented[2]]) == 0:
                                    last_documented[1][last_documented[2]].append(str(block).strip()[3:])
                                else:
                                    raise ValueError('Got documentation comment immediately preceding and following a documented entity; only one is allowed')
                            else:
                                current_doc.append(str(block).strip()[3:])
                        else:
                            current_doc = []
                    else:
                        current_doc.append('')
                if type(block) is Entity.NameBlock:
                    current_entity = str(block).strip().split()[1]
                    entities[current_entity] = current_doc
                    current_doc = []
                    last_documented = block.StartToken.Start.Row, entities, current_entity
                if type(block) is PortList.PortListInterfaceSignalBlock:
                    if len(str(block).strip()) == 0:
                        current_doc = []
                        continue
                    pure_part = str(block).strip().split(':=')[0]
                    portsignals[current_entity.lower()][pure_part] = current_doc
                    current_doc = []
                    last_documented = block.StartToken.Start.Row, portsignals[current_entity.lower()], pure_part
                if type(block) is GenericList.GenericListInterfaceConstantBlock:
                    if len(str(block).strip()) == 0:
                        current_doc = []
                        continue
                    if ':=' not in str(block).strip():
                        pure_part = str(block).strip() + ":= UNDEFINED"
                        generics[current_entity.lower()][pure_part] = current_doc
                    else:
                        pure_part = str(block).strip() + str(next(block_stream, 'UNDEFINED')).strip()
                        generics[current_entity.lower()][pure_part] = current_doc
                    current_doc = []
                    last_documented = block.StartToken.Start.Row, generics[current_entity.lower()], pure_part
        except NotImplementedError:
            LOG.error(f'File {filename} constains unsupported syntax')
        except ParserException as ex:
            LOG.error(f'Error parsing file {filename}: {ex}')
