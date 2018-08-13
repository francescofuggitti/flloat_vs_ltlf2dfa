from flloat.parser.ltlf import LTLfParser
from ltlf2dfa.DotHandler import DotHandler
from ltlf2dfa.Translator import Translator
import timeit

#import matplotlib.pyplot as plt
import numpy as np

flloat_formulas = ('!(a&b)|c',
                     'Fa -> Fb',
                     'F(a -> Fb)',
                     'Fa <-> Fb',
                     'G(a -> Fb)',
                     #'(!bUa)|G(!b)',
                     #'G(a -> X(!aUb))',
                     'G(a -> Xb)',
                     'G(Xb -> a)',
                     'G(a <-> Xb)',
                     '!(Fa & Fb)',
                     'G(a -> !(Fb))',
                     'G(a -> X(!b))'
                     )
ltlf2dfa_formulas = ('~(a&b)|c',
                     'Ea -> Eb',
                     'E(a -> Eb)',
                     'Ea <-> Eb',
                     'G(a -> Eb)',
                     #'(~bUa)|G(~b)',
                     #'G(a -> X(~aUb))',
                     'G(a -> Xb)',
                     'G(Xb -> a)',
                     'G(a <-> Xb)',
                     '~(Ea & Eb)',
                     'G(a -> ~(Eb))',
                     'G(a -> X(~b))'
                     )

# flloat_formulas = ('G( ( a <-> bUc ) <-> ( !d -> (Fe & fUg) ))',)
# ltlf2dfa_formulas = ('G((a <-> bUc) <-> (~d -> (Ee & fUg)))',)

# bU(Xc)
def transform_to_dot_flloat(f):

    parser = LTLfParser()
    parsed_formula = parser(f)

    dfa = parsed_formula.to_automaton(determinize=True)
    dfa.minimize().trim().to_dot("./automaton.dot")

def transform_to_dot_ltlf2dfa(f):

    translator = Translator(f)
    translator.formula_parser()
    translator.translate()
    translator.createMonafile(False)  # it creates automa.mona file
    translator.invoke_mona("automa.mona")  # it returns an intermediate automa.dot file

    # dotHandler = DotHandler("inter-automa.dot")
    # dotHandler.modify_dot()
    # dotHandler.output_dot()

functions = (
    'transform_to_dot_flloat',
    'transform_to_dot_ltlf2dfa'
)

def plot_results(formulas, flloat_y_labels, ltlf2dfa_y_labels):

    N = len(formulas)
    ind = np.arange(N)
    width = 0.3
    fig, ax = plt.subplots()

    rects1 = ax.bar(ind, flloat_y_labels, width, color='r')
    rects2 = ax.bar(ind + width, ltlf2dfa_y_labels, width, color='y')

    ax.set_ylabel('Time (ms)')
    ax.set_title('Time comparison FLLOAT - LTLf2DFA')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(formulas)
    ax.legend((rects1[0], rects2[0]), ('FLLOAT', 'LTLf2DFA'))

    plt.show()

if __name__ == '__main__':
    temps = []
    for formula in ltlf2dfa_formulas:
        #for func in functions:
        stmt = '{}(formula)'.format(functions[1])
        setp = 'from __main__ import formula, {}'.format(functions[1])
        temps.append(timeit.timeit(stmt, setp, number=100))
    print(temps)