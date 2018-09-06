from flloat.parser.ltlf import LTLfParser
from ltlf2dfa.DotHandler import DotHandler
from ltlf2dfa.Translator import Translator
import timeit
from timeit import Timer, repeat

import gc

#memory profiler
from memory_profiler import memory_usage

# set back-end for matplotlib on OSX
import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import numpy as np

flloat_formulas = ('!(a&b)|c',
                     'Fa->Fb',
                     'F(a->Fb)',
                     'Fa<->Fb',
                     'G(a->Fb)',
                     '(!bUa)|G(!b)',
                     'G(a->X(!aUb))',
                     'G(a->Xb)',
                     'G(Xb->a)',
                     'G(a<->Xb)',
                     '!(Fa&Fb)',
                     'G(a->!(Fb))',
                     'G(a->X(!b))'
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

def plot_results_memory(flloat_y_memories, ltlf2dfa_y_memories):

    x = np.arange(65)
    plt.plot(x, flloat_y_memories, color='r')
    plt.plot(x, ltlf2dfa_y_memories, color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Memory (MB)')
    plt.title('Plot of memory')



    # y = np.row_stack((flloat_y_memories, ltlf2dfa_y_memories))
    #
    # x = np.arange(65)
    # y_stack = np.cumsum(y, axis=0)
    #
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    #
    # ax1.plot(x, y_stack[0, :], label=1)
    # ax1.plot(x, y_stack[1, :], label=2)
    # ax1.legend(loc=2)
    #
    # colormap = plt.cm.gist_ncar
    # colors = [colormap(i) for i in np.linspace(0, 1, len(ax1.lines))]
    # for i, j in enumerate(ax1.lines):
    #     j.set_color(colors[i])

    plt.show()

if __name__ == '__main__':
    flloat_times = []
    flloat_memories = []
    ltlf2dfa_times = []
    ltlf2dfa_memories = []
    for formula in flloat_formulas:
        stmt = '{}(formula)'.format(functions[0])
        setp = 'from __main__ import formula, {}'.format(functions[0])
        # flloat_times.append(timeit.timeit(stmt, setp, number=1000))
        # flloat_times.append(min(repeat(stmt, setp, repeat=3, number=100)))
        flloat_memories += memory_usage(transform_to_dot_flloat(formula), interval=.2, timeout=1)
    gc.collect()
    for formula in ltlf2dfa_formulas:
        stmt = '{}(formula)'.format(functions[1])
        setp = 'from __main__ import formula, {}'.format(functions[1])
        # ltlf2dfa_times.append(timeit.timeit(stmt, setp, number=1000))
        # ltlf2dfa_times.append(timeit.Timer(stmt, setp).timeit(number=100) )
        # ltlf2dfa_times.append(min(repeat(stmt, setp, repeat=3, number=100)))
        ltlf2dfa_memories += memory_usage(transform_to_dot_ltlf2dfa(formula), interval=.2, timeout=1)

    # plot_results_time(flloat_formulas, flloat_times, ltlf2dfa_times)
    plot_results_memory(flloat_memories, ltlf2dfa_memories)
    # print(len(ltlf2dfa_memories))




