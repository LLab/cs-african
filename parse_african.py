#!/usr/bin/python
'''
parses data from africa
'''

__author__ = 'as1986'

import logging


def parse_line(line, init=u'english', tokenize=False):
    import re

    stack = [init]
    bracketRec = re.compile(ur'(<([^>]*)>)')

    to_return = []
    proper_line = [x.strip() for x in bracketRec.sub(ur' \1 ', line).split()]

    if tokenize:
        import util

        # workaround for angle bracket chars
        to_join = []
        for w in proper_line:
            if bracketRec.match(w):
                to_join.append(w.replace(u'<',u'__begin__').replace(u'>',u'__end__'))
            else:
                to_join.append(w)
        to_tok = [u' '.join(to_join)]
        tokenized = util.tokenize(to_tok)[0].split()
        proper_line = []
        for t in tokenized:
            proper_line.append(t.replace(u'__begin__',u'<').replace(u'__end__',u'>'))

    for w in proper_line:
        m = bracketRec.match(w)
        if m is not None:
            lang_string = m.groups()[1]
            if lang_string == stack[-1]:
                logging.warn(u'language {} already appeared on stack'.format(lang_string))
            if lang_string.startswith('/'):
                stack.pop()
                if len(stack) == 0:
                    logging.warn(u'stack empty after popping {}'.format(lang_string))
                    stack.append(init)
            else:
                stack.append(lang_string)
            continue
        else:
            to_return.append((w, stack[-1]))
    return to_return


def main():
    import argparse

    import csv

    parser = argparse.ArgumentParser()

    parser.add_argument('csv')
    parser.add_argument('--tokenize', action='store_true')

    args = parser.parse_args()

    with open(args.csv, 'rU') as fh:
        print 'here'
        r = csv.reader(fh)
        lines = [x for x in r]
        print len(lines)
        for l in lines[1:]:
             if len(l[4]) == 0:
                 continue
             s = parse_line(l[4].decode('utf-8'), tokenize=args.tokenize)
             print s


if __name__ == '__main__':
    main()
