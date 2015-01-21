#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Scott
#
# Created:     12/01/2015
# Copyright:   (c) Scott 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from corpustools.corpus.classes import Corpus
from corpustools.corpus.io import load_binary
from corpustools.kl.kl import KullbackLeibler
import argparse
from math import log
from collections import defaultdict
import os
from codecs import open

def main():
    parser = argparse.ArgumentParser(description = 'Phonological CorpusTools: Kullback-Leibler CL interface')
    parser.add_argument('corpus_file_name', help='Path to corpus file. This can just be the file name if it\'s in the same directory as CorpusTools')
    parser.add_argument('seg1', help='First segment')
    parser.add_argument('seg2', help='Second segment')
    parser.add_argument('-o', '--outfile', help='Name of output file (optional)')
    args = parser.parse_args()
    corpus_path = args.corpus_file_name
    if not os.path.isfile(corpus_path):
        corpus_path = os.path.join(os.getcwd(), corpus_path)
    corpus = load_binary(corpus_path)
    outfile = args.outfile
    results = KullbackLeibler(corpus, args.seg1, args.seg2)
    if outfile is not None:
        if not os.path.isfile(outfile):
            outfile = os.path.join(os.getcwd(), outfile)
        if not outfile.endswith('.txt'):
            outfile += '.txt'

        with open(outfile, mode='w', encoding='utf-8') as f:
            print('Context, Context frequency, {} frequency in context, {} frequency in context\n\r'.format(seg1,seg2), file=f)
            for context,result in allC.items():
                cfrequency = freq_c[context]/totalC
                print('{},{},{},{}\n\r'.format(context,
                                cfrequency,
                                result.seg1/result.sum(),
                                result.seg2/result.sum()),
                        file=f)
        print('Done!')

    else:
        print(KL, seg1_entropy, seg2_entropy, ur, sr)

if __name__ == '__main__':
    main()