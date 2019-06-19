"""
Copied out of pyflakes to allow additions (denoted by "nbsmoke
addition"). Additions:

 * return more info for use by caller

 * support "noqa" in ipynb (of questionable value...)
"""

import sys
import re
import pyflakes.reporter, pyflakes.checker
import _ast

### nbsmoke addition ######################################################
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
###########################################################################

### nbsmoke addition ######################################################
import collections
FakeMessage = collections.namedtuple("FakeMessage", "lineno col message message_args")
###########################################################################


def flake_check(codeString, filename, reporter=None):
    if reporter is None:
        reporter = pyflakes.reporter._makeDefaultReporter()
    # First, compile into an AST and handle syntax errors.
    try:
        tree = compile(codeString, filename, "exec", _ast.PyCF_ONLY_AST)
    except SyntaxError:
        value = sys.exc_info()[1]
        msg = value.args[0]

        (lineno, offset, text) = value.lineno, value.offset, value.text

        if pyflakes.checker.PYPY:
            if text is None:
                lines = codeString.splitlines()
                if len(lines) >= lineno:
                    text = lines[lineno - 1]
                    if sys.version_info >= (3, ) and isinstance(text, bytes):
                        try:
                            text = text.decode('ascii')
                        except UnicodeDecodeError:
                            text = None
            offset -= 1

        # If there's an encoding problem with the file, the text is None.
        if text is None:
            # Avoid using msg, since for the only known case, it contains a
            # bogus message that claims the encoding the file declared was
            # unknown.
            reporter.unexpectedError(filename, 'problem decoding source')
        else:
            reporter.syntaxError(filename, msg, lineno, offset, text)
### nbsmoke addition ######################################################
# be able to report the syntax error details if "onlywarn"
# (the error case doesn't include the msgs because otherwise they'd
# appear twice, once now and once on stderr)
        syntax_error_details = StringIO()
        r = pyflakes.reporter.Reporter(syntax_error_details, syntax_error_details)
        r.syntaxError(filename, msg, lineno, offset, text)
# return more info
        return {'message_for_onlywarn': syntax_error_details.getvalue(),
                'messages':["Error - see captured stderr, below."]}
###########################################################################
    except Exception:
        reporter.unexpectedError(filename, 'problem decoding source')
### nbsmoke addition ######################################################
# return more info
        return {'message_for_onlywarn': 'problem decoding source',                
                'messages':["Error - see captured stderr, below."]}
###########################################################################
    # Okay, it's syntactically valid.  Now check it.
    w = pyflakes.checker.Checker(tree, filename)

### nbsmoke addition ######################################################
# hack to support '# noqa' in ipynb
    NOQA = re.compile('# noqa', re.IGNORECASE)
    noqa_lines = [i+1 for i,l in enumerate(codeString.splitlines()) if NOQA.search(l)]
    # (I assume there was a reason for updating list in place?)
    w.messages[:] = [m for m in w.messages if m.lineno not in noqa_lines]
###########################################################################

### nbsmoke addition ######################################################
# hack to support ' # nbsmoke-blacklisted: <magic>'
    blacklist = re.compile('.* # nbsmoke-blacklisted: (.*)', re.IGNORECASE)
    blacklist_messages = []
    for i,l in enumerate(codeString.splitlines()):
        m = blacklist.match(l)
        if m:
            blacklist_messages.append(
                FakeMessage(lineno=i+1, col=m.start(1), message="nbsmoke blacklisted magic: %s", message_args=(m.group(1),)))
    w.messages[:] = w.messages + blacklist_messages
###########################################################################

    w.messages.sort(key=lambda m: m.lineno)

### nbsmoke addition ######################################################
# return more info
    return {'messages':[("line %s col %s: "%(msg.lineno,msg.col))+msg.message%msg.message_args for msg in w.messages]}
###########################################################################
