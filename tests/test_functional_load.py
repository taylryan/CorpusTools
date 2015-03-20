
import sys
import os

from corpustools.funcload.functional_load import (minpair_fl, deltah_fl,
                                                minpair_fl_wordtokens,deltah_fl_wordtokens)
from corpustools.corpus.classes import Segment


#class NeutralizeTest(unittest.TestCase):
#    pass


def test_minimal_pairs(unspecified_test_corpus):
    calls = [({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':0,
                    'relative_count':True},0.125),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':0,
                    'relative_count':False},1),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':0,
                    'relative_count':True},0.11111),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':0,
                    'relative_count':False},1),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':True},0),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':False},0),

            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':3,
                    'relative_count':True},0.14286),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':3,
                    'relative_count':False},1),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':3,
                    'relative_count':True},0),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':3,
                    'relative_count':False},0),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':True},0),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':False},0),

            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':True},0.14286),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':False},2),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':True},0.09091),
            ({'corpus': unspecified_test_corpus,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':False},1)]

    for c,v in calls:
        assert(abs(minpair_fl(**c)-v) < 0.0001)

def test_deltah(unspecified_test_corpus):
    calls = [({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':0,
                'type_or_token':'type'},0.13333),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':0,
                'type_or_token':'token'},0.24794),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':0,
                'type_or_token':'type'},0.13333),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':0,
                'type_or_token':'token'},0.00691),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'type'},0),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'token'},0),

            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':3,
                'type_or_token':'type'},0.16667),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':3,
                'type_or_token':'token'},0.25053),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':3,
                'type_or_token':'type'},0),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':3,
                'type_or_token':'token'},0),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'type'},0),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'token'},0),

            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'type'},0.26667),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'token'},0.25485),

            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'type'},0.16667),
            ({'corpus': unspecified_test_corpus,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'token'},0.25053),]

    for c,v in calls:
        assert(abs(deltah_fl(**c)-v) < 0.0001)


def test_minimal_pair_wordtokens(unspecified_discourse_corpus):
    c = unspecified_discourse_corpus.lexicon
    calls = [({'corpus': c,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':0,
                    'relative_count':True},0.125),
            ({'corpus': c,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':0,
                    'relative_count':False},1),
            ({'corpus': c,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':0,
                    'relative_count':True},0.11111),
            ({'corpus': c,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':0,
                    'relative_count':False},1),
            ({'corpus': c,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':True},0),
            ({'corpus': c,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':False},0),

            ({'corpus': c,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':3,
                    'relative_count':True},0.14286),
            ({'corpus': c,
                    'segment_pairs':[('s','ʃ')],
                    'frequency_cutoff':3,
                    'relative_count':False},1),
            ({'corpus': c,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':3,
                    'relative_count':True},0),
            ({'corpus': c,
                    'segment_pairs':[('m','n')],
                    'frequency_cutoff':3,
                    'relative_count':False},0),
            ({'corpus': c,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':True},0),
            ({'corpus': c,
                    'segment_pairs':[('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':False},0),

            ({'corpus': c,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':True},0.14286),
            ({'corpus': c,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':0,
                    'relative_count':False},2),
            ({'corpus': c,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':True},0.09091),
            ({'corpus': c,
                    'segment_pairs':[('s','ʃ'),
                                    ('m','n'),
                                    ('e','o')],
                    'frequency_cutoff':3,
                    'relative_count':False},1)]

    for c,v in calls:
        assert(abs(minpair_fl_wordtokens(**c)-v) < 0.0001)

def test_deltah_wordtokens(unspecified_discourse_corpus):
    c = unspecified_discourse_corpus.lexicon
    calls = [({'corpus': c,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':0,
                'type_or_token':'most_frequent_type'},0.13333),
            ({'corpus': c,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':0,
                'type_or_token':'most_frequent_token'},0.24794),
            ({'corpus': c,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':0,
                'type_or_token':'relative_type'},0.13333),
            ({'corpus': c,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':0,
                'type_or_token':'count_token'},0.00691),
            ({'corpus': c,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'most_frequent_type'},0),
            ({'corpus': c,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'most_frequent_token'},0),

            ({'corpus': c,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':3,
                'type_or_token':'relative_type'},0.16667),
            ({'corpus': c,
                'segment_pairs':[('s','ʃ')],
                'frequency_cutoff':3,
                'type_or_token':'count_token'},0.25053),
            ({'corpus': c,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':3,
                'type_or_token':'most_frequent_type'},0),
            ({'corpus': c,
                'segment_pairs':[('m','n')],
                'frequency_cutoff':3,
                'type_or_token':'most_frequent_token'},0),
            ({'corpus': c,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'relative_type'},0),
            ({'corpus': c,
                'segment_pairs':[('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'count_token'},0),

            ({'corpus': c,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'most_frequent_type'},0.26667),
            ({'corpus': c,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':0,
                'type_or_token':'most_frequent_token'},0.25485),

            ({'corpus': c,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'relative_type'},0.16667),
            ({'corpus': c,
                'segment_pairs':[('s','ʃ'),
                                ('m','n'),
                                ('e','o')],
                'frequency_cutoff':3,
                'type_or_token':'count_token'},0.25053),]

    for c,v in calls:
        assert(abs(deltah_fl_wordtokens(**c)-v) < 0.0001)


