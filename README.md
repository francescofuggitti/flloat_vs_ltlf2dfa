# FLLOAT vs LTL<sub>f</sub>2DFA

This repo contains a time execution benchmark between [FLLOAT](https://pypi.org/project/flloat/)
and [LTL<sub>f</sub>2DFA](https://pypi.org/project/ltlf2dfa/) packages over a
set of LTL<sub>f</sub> formulas.

## Requirements

The `main.py` module requires the following packages to be installed:

- [flloat](https://pypi.org/project/flloat/)
- [ltlf2dfa](https://pypi.org/project/ltlf2dfa/)
- [matplotlib](https://pypi.org/project/matplotlib/)
- [numpy](https://pypi.org/project/numpy/)

## Usage

Simply run the main module:

```python3 main.py```

wait some seconds and you will get the histogram reporting
the results.

### Example of result

Histogram reporting the minimum value of 100 executions for each formula,
repeated 3 times.

![](https://github.com/Francesco17/flloat_vs_ltlf2dfa/blob/master/time-comparison.png "Benchmark")
