import glob
from collections import defaultdict
import os
from pyVHDLParser.Token.Parser import Tokenizer
from pyVHDLParser.Blocks import TokenToBlockParser, MetaBlock, CommentBlock
from pyVHDLParser.Blocks.Common import LinebreakBlock, IndentationBlock
from pyVHDLParser.Blocks.Structural import Entity
from pyVHDLParser.Blocks.List import PortList
from pyVHDLParser.Base import ParserException
import logging

LOG = logging.getLogger('sphinxvhdl-autodoc')

entities = {}
portsignals = defaultdict(dict)

def init(path: str) -> None:
    for block in MetaBlock.BLOCKS:
        try:
            block.__cls_init__()
        except AttributeError:
            pass
    for filename in (glob.glob(os.path.join(path, "**", "*.vhd"), recursive=True) + glob.glob(os.path.join(path, "**", "*.vhdl"), recursive=True)):
        with open(filename, 'r') as source_file:
            source_code = source_file.read()
        token_stream = Tokenizer.GetVHDLTokenizer(source_code)
        block_stream = TokenToBlockParser.Transform(token_stream)
        current_doc = []
        current_entity = ''
        try:
            for block in block_stream:
                if type(block) is IndentationBlock:
                    continue
                if type(block) is LinebreakBlock:
                    current_doc = []
                    continue
                if type(block) is CommentBlock:
                    if len(str(block).strip()) > 2:
                        current_doc.append(str(block).strip()[3:])
                    else:
                        current_doc.append('')
                if type(block) is Entity.NameBlock:
                    current_entity = str(block).strip().split()[1]
                    entities[current_entity] = current_doc
                    current_doc = []
                if type(block) is PortList.PortListInterfaceSignalBlock:
                    if len(str(block).strip()) == 0:
                        current_doc = []
                        continue
                    pure_part = str(block).strip().split(':=')[0]
                    portsignals[current_entity.lower()][pure_part] = current_doc
                    current_doc = []
        except NotImplementedError:
            LOG.error(f'File {filename} constains unsupported syntax')
        except ParserException as ex:
            LOG.error(f'Error parsing file {filename}: {ex}')
