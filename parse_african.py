#!/usr/bin/python
'''
parses data from africa
'''

__author__ = 'as1986'

import logging


def parse_line(line, init='english', tokenize=False):
    import re

    stack = [init]
    bracketRec = re.compile(r'(<([^>]*)>)')

    to_return = []
    proper_line = [x.strip() for x in bracketRec.sub(r' \1 ', line).split()]

    if tokenize:
        import util

        to_tok = [' '.join(proper_line)]
        proper_line = util.tokenize(to_tok)[0].split()

    for w in proper_line:
        m = bracketRec.match(w)
        if m is not None:
            lang_string = m.groups()[1]
            if lang_string == stack[-1]:
                logging.warn('language {} already appeared on stack'.format(lang_string))
            if lang_string.startswith('/'):
                stack.pop()
                if len(stack) == 0:
                    logging.warn('stack empty after popping {}'.format(lang_string))
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
        r = csv.reader(fh)
        lines = [x for x in r]
        for l in lines[1:]:
            try:
                print parse_line(l[4], tokenize=args.tokenize)
            except Exception as e:
                raise e


if __name__ == '__main__':
    main()