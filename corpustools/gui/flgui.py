from collections import OrderedDict
import corpustools.funcload.functional_load as FL
from corpustools.funcload.io import save_minimal_pairs

from .imports import *
from .widgets import (SegmentPairSelectWidget, RadioSelectWidget, TierWidget,
                    ContextWidget, SaveFileWidget)
from .environments import EnvironmentSelectWidget
from .windows import FunctionWorker, FunctionDialog
from corpustools.exceptions import PCTError, PCTPythonError
from corpustools.contextmanagers import (CanonicalVariantContext,
                                        MostFrequentVariantContext,
                                        SeparatedTokensVariantContext,
                                        WeightedVariantContext)

class FLWorker(FunctionWorker):
    def run(self):
        kwargs = self.kwargs
        self.results = []
        context = kwargs.pop('context')
        if kwargs.pop('algorithm') == 'min_pairs':
            func = FL.minpair_fl
            rel_func = FL.relative_minpair_fl
        else:
            func = FL.deltah_fl
            rel_func = FL.relative_deltah_fl
        if context == ContextWidget.canonical_value:
            cm = CanonicalVariantContext
        elif context == ContextWidget.frequent_value:
            cm = MostFrequentVariantContext
        elif context == ContextWidget.separate_value:
            cm = SeparatedTokensVariantContext
        elif context == ContextWidget.relative_value:
            cm = WeightedVariantContext
        with cm(kwargs.pop('corpus'),
                kwargs.pop('sequence_type'),
                kwargs.pop('type_token'),
                frequency_threshold = kwargs.pop('frequency_cutoff')) as c:
            try:
                pairs = kwargs.pop('segment_pairs')
                output_filename = kwargs.pop('output_filename', None)
                if output_filename is not None:
                    to_output = []
                    outf = open(output_filename, mode='w', encoding='utf-8')
                    save_minimal_pairs(outf, [], write_header= True)
                else:
                    outf = None
                for pair in pairs:
                    if len(pair) == 1:
                        res = rel_func(c, pair[0],
                            output_filename = outf, **kwargs)
                    else:
                        if isinstance(pair[0], (list, tuple)):
                            in_list = list(zip(pair[0], pair[1]))
                        else:
                            in_list = [pair]
                        res = func(c, in_list, **kwargs)
                        if self.stopped:
                            break
                        if output_filename is not None:
                            to_output.append((pair, res[1]))
                    self.results.append(res)
                if output_filename is not None:
                    save_minimal_pairs(outf, to_output)
                    outf.close()
            except PCTError as e:
                self.errorEncountered.emit(e)
                return
            except Exception as e:
                e = PCTPythonError(e)
                self.errorEncountered.emit(e)
                return
        if self.stopped:
            self.finishedCancelling.emit()
            return
        self.dataReady.emit(self.results)



class FLDialog(FunctionDialog):
    header = ['Corpus',
                'First segment',
                'Second segment',
                'Algorithm',
                'Distinguished homophones',
                'Relative count',
                'Transcription tier',
                'Frequency type',
                'Pronunciation variants',
                'Minimum word frequency',
                'Environments',
                'Result']

    _about = [('This function calculates the functional load of the contrast'
                    ' between any two segments, based on either the number of minimal'
                    ' pairs or the change in entropy resulting from merging that contrast.'),
                    '',
                    'References: ',
                    ('Surendran, Dinoj & Partha Niyogi. 2003. Measuring'
                    ' the functional load of phonological contrasts.'
                    ' In Tech. Rep. No. TR-2003-12.'),
                    ('Wedel, Andrew, Abby Kaplan & Scott Jackson. 2013.'
                    ' High functional load inhibits phonological contrast'
                    ' loss: A corpus study. Cognition 128.179-86')]

    name = 'functional load'

    def __init__(self, parent, settings, corpus, inventory, showToolTips):
        FunctionDialog.__init__(self, parent, settings, FLWorker())

        self.corpus = corpus
        self.inventory = inventory
        self.showToolTips = showToolTips
        self.kwargs = dict()

        flFrame = QFrame()
        fllayout = QHBoxLayout()

        self.segPairWidget = SegmentPairSelectWidget(self.inventory, single_segment = True)

        fllayout.addWidget(self.segPairWidget)

        secondPane = QFrame()

        l = QVBoxLayout()

        self.algorithmWidget = RadioSelectWidget('Functional load algorithm',
                                            OrderedDict([('Minimal pairs','min_pairs'),
                                            ('Change in entropy','entropy')]),
                                            {'Minimal pairs': self.minPairsSelected,
                                            'Change in entropy': self.entropySelected})

        l.addWidget(self.algorithmWidget)

        secondPane.setLayout(l)

        fllayout.addWidget(secondPane)

        optionLayout = QVBoxLayout()

        self.tierWidget = TierWidget(corpus,include_spelling=False)

        optionLayout.addWidget(self.tierWidget)


        self.typeTokenWidget = RadioSelectWidget('Type or token frequencies',
                                                    OrderedDict([('Type','type'),
                                                    ('Token','token')]))
        actions = None
        self.variantsWidget = ContextWidget(self.corpus, actions)

        optionLayout.addWidget(self.variantsWidget)
        optionLayout.addWidget(self.typeTokenWidget)

        minFreqFrame = QGroupBox('Minimum frequency')
        box = QFormLayout()
        self.minFreqEdit = QLineEdit()
        box.addRow('Minimum word frequency:',self.minFreqEdit)

        minFreqFrame.setLayout(box)

        optionLayout.addWidget(minFreqFrame)

        minPairOptionFrame = QGroupBox('Minimal pair options')

        box = QVBoxLayout()

        self.relativeCountWidget = QCheckBox('Use counts relative to number of possible pairs')
        self.relativeCountWidget.setChecked(True)
        self.homophoneWidget = QCheckBox('Distinguish homophones')

        box.addWidget(self.relativeCountWidget)
        box.addWidget(self.homophoneWidget)

        fileFrame = QGroupBox('Output list of minimal pairs to a file')

        self.saveFileWidget = SaveFileWidget('Select file location','Text files (*.txt)')

        vbox = QHBoxLayout()
        vbox.addWidget(self.saveFileWidget)

        fileFrame.setLayout(vbox)

        box.addWidget(fileFrame)

        minPairOptionFrame.setLayout(box)

        l.addWidget(minPairOptionFrame)

        entropyOptionFrame = QGroupBox('Entropy options')

        box2 = QVBoxLayout()
        entropyOptionFrame.setLayout(box2)
        self.preventNormalizationWidget = QCheckBox('Do not normalize results')
        self.preventNormalizationWidget.setChecked(False)
        box2.addWidget(self.preventNormalizationWidget)

        l.addWidget(entropyOptionFrame)

        optionFrame = QGroupBox('Options')
        optionFrame.setLayout(optionLayout)
        fllayout.addWidget(optionFrame)

        self.envWidget = EnvironmentSelectWidget(self.inventory, middle = False)
        fllayout.addWidget(self.envWidget)

        flFrame.setLayout(fllayout)


        self.layout().insertWidget(0,flFrame)

        self.algorithmWidget.initialClick()
        if self.showToolTips:

            self.preventNormalizationWidget.setToolTip(('<FONT COLOR=black>'
            'When calculating change in entropy, this option prevents normalization of the entropy difference by '
                        'the pre-neutralization entropy. To replicate the Surendran and Niyogi metric, '
                        'turn this option OFF.'
            '</FONT>'))

            self.homophoneWidget.setToolTip(("<FONT COLOR=black>"
            'This setting will overcount alternative'
                            ' spellings of the same word, e.g. axel~actual and axle~actual,'
                            ' but will allow you to count e.g. sock~shock twice, once for each'
                            ' meaning of \'sock\' (footwear vs. punch)'
            "</FONT>"))

            self.relativeCountWidget.setToolTip(("<FONT COLOR=black>"
            'The raw count of minimal pairs will'
                            ' be divided by the number of words that include any of the target segments'
                            ' present in the list at the left.'
            "</FONT>"))
            self.tierWidget.setToolTip(("<FONT COLOR=black>"
                                    'Choose which tier functional load should'
                                    ' be calculated over (e.g., the whole transcription'
                                    ' vs. a tier containing only [+voc] segments).'
                                    ' New tiers can be created from the Corpus menu.'
                                    "</FONT>"))
            self.segPairWidget.setToolTip(("<FONT COLOR=black>"
            'Add pairs of sounds whose contrast to collapse.'
                                    ' For example, if you\'re interested in the functional load of the [s]'
                                    ' / [z] contrast, you only need to add that pair. If, though, you\'re'
                                    ' interested in the functional load of the voicing contrast among obstruents,'
                                    ' you may need to add (p, b), (t, d), and (k, g).'
            "</FONT>"))
            self.algorithmWidget.setToolTip(("<FONT COLOR=black>"
            'Calculate the functional load either using'
                            ' the contrast between two sets of segments as a count of minimal pairs'
                            ' or using the decrease in corpus'
                            ' entropy caused by a merger of paired segments in the set.'
            "</FONT>"))
            self.saveFileWidget.setToolTip(("<FONT COLOR=black>"
            'Note that whether "Distinguish homophones" is checked or not, this file will'
            ' include all minimal pairs with unique spellings.'
            "</FONT>"))

    def minPairsSelected(self):
        self.saveFileWidget.setEnabled(True)
        self.relativeCountWidget.setEnabled(True)
        self.homophoneWidget.setEnabled(True)
        self.preventNormalizationWidget.setEnabled(False)
        #self.typeTokenWidget.widgets[0].setChecked(True)
        self.typeTokenWidget.setEnabled(False)

    def entropySelected(self):
        self.saveFileWidget.setEnabled(False)
        self.relativeCountWidget.setEnabled(False)
        self.homophoneWidget.setEnabled(False)
        self.preventNormalizationWidget.setEnabled(True)
        self.typeTokenWidget.widgets[1].setChecked(True)
        self.typeTokenWidget.setEnabled(True)

    def generateKwargs(self):
        segPairs = self.segPairWidget.value()
        if len(segPairs) == 0:
            reply = QMessageBox.critical(self,
                    "Missing information", "Please specify at least one segment pair.")
            return None
        try:
            frequency_cutoff = float(self.minFreqEdit.text())
        except ValueError:
            frequency_cutoff = 0.0
        alg = self.algorithmWidget.value()
        self.kwargs = {'corpus':self.corpus,
                'segment_pairs':segPairs,
                'context': self.variantsWidget.value(),
                'sequence_type': self.tierWidget.value(),
                'frequency_cutoff':frequency_cutoff,
                'type_token':self.typeTokenWidget.value(),
                'algorithm': alg,
                'prevent_normalization': self.preventNormalizationWidget.isChecked(),
                'environment_filters': self.envWidget.value()}
        if alg == 'min_pairs':
            out_file = self.saveFileWidget.value()
            if out_file == '':
                out_file = None
            self.kwargs['relative_count'] = self.relativeCountWidget.isChecked()
            self.kwargs['distinguish_homophones'] = self.homophoneWidget.isChecked()
            self.kwargs['output_filename'] = out_file

        return self.kwargs

    def setResults(self, results):
        self.results = []
        seg_pairs = self.segPairWidget.value()
        try:
            frequency_cutoff = float(self.minFreqEdit.text())
        except ValueError:
            frequency_cutoff = 0.0
        for i, r in enumerate(results):
            if isinstance(r, tuple):
                r = r[0]
            seg_one = seg_pairs[i][0]
            try:
                seg_two = seg_pairs[i][1]
            except IndexError:
                seg_two = ''

            if not self.envWidget.displayValue():
                environments = 'None'
            else:
                environments = ' ; '.join([x for x in self.envWidget.displayValue()])
            self.results.append({'Corpus': self.corpus.name,
                                'First segment': seg_one,
                                'Second segment': seg_two,
                                'Algorithm': self.algorithmWidget.displayValue(),
                                'Distinguished homophones': self.homophoneWidget.isChecked(),
                                'Relative count': self.relativeCountWidget.isChecked(),
                                'Transcription tier': self.tierWidget.displayValue(),
                                'Frequency type': self.typeTokenWidget.value().title(),
                                'Pronunciation variants': self.variantsWidget.value().title(),
                                'Minimum word frequency': frequency_cutoff,
                                'Environments': environments,
                                'Result': r})