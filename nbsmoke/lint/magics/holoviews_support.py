"""
Presumably I copied this in from holoviews and hacked til it worked,
as a proof of concept? But since holoviews is deprecating magics, no
attempt was ever made (or will ever be made...) to do it properly :)
"""

from itertools import groupby

from holoviews.util.parser import OptsSpec

def opts_handler(string_of_magic_args):
    """Given the arguments to an opts magic, return line of python
suitable for pyflakes.

    """
    return " ; ".join(OptsSpec.parse(string_of_magic_args)) + " # noqa: here to use names"


def _hvparse(cls, line, ns={}):
    """
    Parse an options specification, returning a dictionary with
    path keys and {'plot':<options>, 'style':<options>} values.
    """
    parses  = [p for p in cls.opts_spec.scanString(line)]
    if len(parses) != 1:
        raise SyntaxError("Invalid specification syntax.")
    else:
        e = parses[0][2]
        processed = line[:e]
        if (processed.strip() != line.strip()):
            raise SyntaxError("Failed to parse remainder of string: %r" % line[e:])

    grouped_paths = cls._group_paths_without_options(cls.opts_spec.parseString(line))
    things = []
    for pathspecs, group in grouped_paths:

#        normalization = cls.process_normalization(group)
#        if normalization is not None:
#            options['norm'] = normalization

        if 'plot_options' in group:
            plotopts =  group['plot_options'][0]
            opts = cls.todict(plotopts, 'brackets', ns=ns)
            things+=opts

        if 'style_options' in group:
            styleopts = group['style_options'][0]
            opts = cls.todict(styleopts, 'parens', ns=ns)
            things+=opts

    return things


def _hvtodict(cls, parseresult, mode='parens', ns={}):
    """
    Helper function to return dictionary given the parse results
    from a pyparsing.nestedExpr object (containing keywords).

    The ns is a dynamic namespace (typically the IPython Notebook
    namespace) used to update the class-level namespace.
    """
    grouped = []
    things = []
    tokens = cls.collect_tokens(parseresult, mode)
    # Group tokens without '=' and append to last token containing '='
    for group in groupby(tokens, lambda el: '=' in el):
        (val, items) = group
        if val is True:
            grouped += list(items)
        if val is False:
            elements =list(items)
            # Assume anything before ) or } can be joined with commas
            # (e.g tuples with spaces in them)
            joiner=',' if any(((')' in el) or ('}' in el))
                              for el in elements) else ''
            grouped[-1] += joiner + joiner.join(elements)

    for keyword in grouped:
        # Tuple ('a', 3) becomes (,'a',3) and '(,' is never valid
        # Same for some of the other joining errors corrected here
        for (fst,snd) in [('(,', '('), ('{,', '{'), ('=,','='),
                          (',:',':'), (':,', ':'), (',,', ','),
                          (',.', '.')]:
            keyword = keyword.replace(fst, snd)

        things.append('dict(%s)' % keyword)

    return things

OptsSpec.parse = classmethod(_hvparse)
OptsSpec.todict = classmethod(_hvtodict)
