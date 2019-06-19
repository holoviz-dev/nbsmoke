from IPython.utils._process_common import arg_split
import argparse

cell_magic_handlers = {}
line_magic_handlers = {}

_capture_arg_parser = argparse.ArgumentParser()
_capture_arg_parser.add_argument('output', nargs='?', default=None)
def capture_handler(magic):
    string_of_magic_args = magic.python
    x,_ = _capture_arg_parser.parse_known_args(arg_split(string_of_magic_args))
    if x.output:
        return '%s = "dummy captured output"'%x.output
    else:
        return 'pass # was capture cell magic with no output arg'

cell_magic_handlers['capture'] = capture_handler

_script_arg_parser = argparse.ArgumentParser()
_script_arg_parser.add_argument("--out")

def script_handler(magic):
    string_of_magic_args = magic.python
    script_name, _, script_arg_s = string_of_magic_args.partition(' ')
    return _script_handler(magic, script_name, script_arg_s)

def specific_script_handler(magic):
    script_name = magic.name
    script_arg_s = magic.python
    return _script_handler(magic, script_name, script_arg_s)
    
def _script_handler(magic, script_name, script_arg_s):
    x,_ = _script_arg_parser.parse_known_args(arg_split(script_arg_s))
    # this is sneaky
    magic.additional_lines = ["pass # script content omitted"]
    if x.out:
        return '%s = "dummy output from %s script run in subprocess"'%(x.out, script_name)
    else:
        return 'pass # was %s script cell magic with no --out'%script_name

_SCRIPT_MAGICS = [
    'bash',
    'perl',
    'pypy',
    'python',
    'python2',
    'python3',
    'ruby',
    'sh'
]

cell_magic_handlers['script'] = script_handler
for _magic in _SCRIPT_MAGICS:
    cell_magic_handlers[_magic] = specific_script_handler
