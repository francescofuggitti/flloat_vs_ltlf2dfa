from flloat.parser.ltlf import LTLfParser
from ltlf2dfa.DotHandler import DotHandler
from ltlf2dfa.Translator import Translator
import timeit
from timeit import Timer, repeat

import gc
import time

# set back-end for matplotlib on OSX
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

flloat_formulas = ('true & !(a&b)|c',
                     'true & Fa->Fb',
                     'true & F(a->Fb)',
                     'true & Fa<->Fb',
                     'true & G(a->Fb)',
                     'true & (!bUa)|G(!b)',
                     'true & G(a->X(!aUb))',
                     'true & G(a->Xb)',
                     'true & G(Xb->a)',
                     'true & G(a<->Xb)',
                     'true & !(Fa&Fb)',
                     'true & G(a->!(Fb))',
                     'true & G(a->X(!b))'
                     )
ltlf2dfa_formulas = ('~(a&b)|c',
                     'Fa -> Fb',
                     'F(a -> Fb)',
                     'Fa <-> Fb',
                     'G(a -> Fb)',
                     '(~bUa)|G(~b)',
                     'G(a -> X(~aUb))',
                     'G(a -> Xb)',
                     'G(Xb -> a)',
                     'G(a <-> Xb)',
                     '~(Fa & Fb)',
                     'G(a -> ~(Fb))',
                     'G(a -> X(~b))'
                     )

def transform_to_dot_flloat(f):

    parser = LTLfParser()
    parsed_formula = parser(f)

    dfa = parsed_formula.to_automaton(determinize=True)
    dfa.minimize().trim().to_dot("./automaton.dot")

def transform_to_dot_ltlf2dfa(f):

    translator = Translator(f)
    translator.formula_parser()
    translator.translate()
    translator.createMonafile(False)
    translator.invoke_mona()

    dotHandler = DotHandler()
    dotHandler.modify_dot()
    dotHandler.output_dot()

functions = (
    'transform_to_dot_flloat',
    'transform_to_dot_ltlf2dfa'
)

def plot_results_time(formulas, flloat_y_labels, ltlf2dfa_y_labels):

    N = len(formulas)
    ind = np.arange(N)
    width = 0.3
    fig, ax = plt.subplots()

    rects1 = ax.bar(ind, flloat_y_labels, width, color='r')
    rects2 = ax.bar(ind + width, ltlf2dfa_y_labels, width, color='b')

    ax.set_ylabel('Time (s)')
    ax.set_title('Time comparison FLLOAT - LTLf2DFA')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(formulas, rotation = 45, ha="right")
    ax.legend((rects1[0], rects2[0]), ('FLLOAT', 'LTLf2DFA'))
    plt.show()

if __name__ == '__main__':
    flloat_times = []
    ltlf2dfa_times = []
    for formula in flloat_formulas:
        stmt = '{}(formula)'.format(functions[0])
        setp = 'from __main__ import formula, {}'.format(functions[0])
        flloat_times.append(min(repeat(stmt, setp, repeat=3, number=100)))
    gc.collect()
    for formula in ltlf2dfa_formulas:
        stmt = '{}(formula)'.format(functions[1])
        setp = 'from __main__ import formula, {}'.format(functions[1])
        ltlf2dfa_times.append(min(repeat(stmt, setp, repeat=3, number=100)))

    plot_results_time(ltlf2dfa_formulas, flloat_times, ltlf2dfa_times)
