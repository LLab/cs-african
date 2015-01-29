#!/usr/bin/python
'''
parses data from africa
'''

__author__ = 'as1986'

import logging


def write_crf(lst_sentences, sd_fname, labels_fname):
    from io import open

    assert isinstance(lst_sentences, list)

    with open(sd_fname, 'w', encoding='utf-8') as sd_fh, open(labels_fname, 'w', encoding='utf-8') as labels_fh:
        for sentence in lst_sentences:
            assert isinstance(sentence, list)
            words = [x[0] for x in sentence]
            labels = [x[1] for x in sentence]

            sd_fh.write(u'{}\n'.format(u' '.join(words)))
            labels_fh.write(u'{}\n'.format(u' '.join(labels)))


def parse_line(line, init=u'english', tokenize=False):
    import re

    stack = [init]
    bracketRec = re.compile(ur'(<([^> ]+)\s*[^>]*>)')

    to_return = []
    proper_line = [x.strip() for x in bracketRec.sub(ur' <\2> ', line).split()]

    if tokenize:
        import util

        # workaround for angle bracket chars
        to_join = []
        for w in proper_line:
            if bracketRec.match(w):
                to_join.append(w.replace(u'<', u'__begin__').replace(u'>', u'__end__'))
            else:
                to_join.append(w)
        to_tok = [u' '.join(to_join)]
        tokenized = util.tokenize(to_tok)[0].split()
        proper_line = []
        for t in tokenized:
            proper_line.append(t.replace(u'__begin__', u'<').replace(u'__end__', u'>'))

    for w in proper_line:
        logging.info(u'current word: {}'.format(w))
        m = bracketRec.match(w)
        if m is not None:
            lang_string = m.groups()[1]
            if lang_string == stack[-1]:
                logging.warn(u'language {} already appeared on stack for word {} in line \n {}'.format(lang_string, w, line))
            if lang_string.startswith('/'):
                stack.pop()
                if len(stack) == 0:
                    logging.warn(u'stack empty after popping {}'.format(lang_string))
                    stack.append(init)
            else:
                stack.append(lang_string)
                logging.info(u'new language: {}'.format(lang_string))
            continue
        else:
            to_return.append((w, stack[-1]))
    return to_return


def main():
    import argparse

    import csv

    parser = argparse.ArgumentParser()

    parser.add_argument('csv')
    parser.add_argument('sd')
    parser.add_argument('labels')
    parser.add_argument('--tokenize', action='store_true')
    parser.add_argument('--log-to-file', action='store_true')

    args = parser.parse_args()

    if args.log_to_file:
       logging.basicConfig(filename='{}.log'.format(args.csv), filemode='w', level=logging.WARN)

    with open(args.csv, 'rU') as fh:
        sentences = []
        r = csv.reader(fh)
        lines = [x for x in r]
        print len(lines)
        for l in lines[1:]:
            if len(l[4]) == 0:
                continue
            sentences.append(parse_line(l[4].decode('utf-8'), tokenize=args.tokenize))

        write_crf(sentences, args.sd, args.labels)


if __name__ == '__main__':
    main()
