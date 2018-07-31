import unittest
import sys
# from link_grammar.inprocparser import parse_batch_ps_output, parse_file_with_lgp, parse_file_with_lgp0
from grammar_tester.optconst import *
from grammar_tester.lginprocparser import LGInprocParser

lg_post_output = """
echo set to 1
postscript set to 1
graphics set to 0
verbosity set to 0
tuna has fin .
[(LEFT-WALL)(tuna)(has)(fin)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C04)][3 4 0 (C04C03)]]
[0]

eagle isa bird .
[(LEFT-WALL)(eagle)(isa)(bird)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C06)][3 4 0 (C06C03)]]
[0]

fin isa extremity .
[(LEFT-WALL)(fin)(isa)(extremity)(.)]
[[0 1 0 (C05C04)][1 2 0 (C04C01)][2 3 0 (C01C06)][3 4 0 (C06C03)]]
[0]

tuna isa fish .
[(LEFT-WALL)(tuna)(isa)(fish)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C06)][3 4 0 (C06C03)]]
[0]

fin has scale .
[(LEFT-WALL)(fin)([has])(scale)(.)]
[[0 1 0 (C05C04)][1 3 0 (C04C04)][3 4 0 (C04C03)]]
[0]

eagle has wing .
[(LEFT-WALL)(eagle)(has)(wing)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C04)][3 4 0 (C04C03)]]
[0]

wing has feather .
[(LEFT-WALL)(wing)([has])(feather)(.)]
[[0 1 0 (C05C04)][1 3 0 (C04C04)][3 4 0 (C04C03)]]
[0]

wing isa extremity .
[(LEFT-WALL)(wing)(isa)(extremity)(.)]
[[0 1 0 (C05C04)][1 2 0 (C04C01)][2 3 0 (C01C06)][3 4 0 (C06C03)]]
[0]

herring isa fish .
[(LEFT-WALL)(herring)(isa)(fish)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C06)][3 4 0 (C06C03)]]
[0]

herring has fin .
[(LEFT-WALL)(herring)(has)(fin)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C04)][3 4 0 (C04C03)]]
[0]

parrot isa bird .
[(LEFT-WALL)(parrot)(isa)(bird)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C06)][3 4 0 (C06C03)]]
[0]

parrot has wing .
[(LEFT-WALL)(parrot)(has)(wing)(.)]
[[0 1 0 (C05C02)][1 2 0 (C02C01)][2 3 0 (C01C04)][3 4 0 (C04C03)]]
[0]

Bye.
"""

lg_post_explosion = \
"""
conclusions : icp-sf-ms is a reliable method of blood analysis for cd , mn and pb even for the evaluation on an individual basis.
by comparing eyebrow shape and position in both young and mature women , this study provides objective data with which to plan forehead rejuvenating procedures.
the odds of being overweight in adulthood was @number@ times greater ( @percent@ ci : @date@ @number@ ) in overweight compared with healthy weight youth.
holocaust survivors did not differ in the level of resilience from comparisons ( mean : @number@ ± @number@ vs. @number@ ± @number@ respectively ) .
[(LEFT-WALL)(holocaust.n)(survivors.n)(did.v-d)(not.e)(differ.v)(in.r)(the)(level.n)(of)
(resilience.n-u)(from)(comparisons.n)(()(mean.a)([:])(@number@[?].n)(±[?].n)(@number@[?].n)(vs.)
(@number@[?].n)(±[?].n)(@number@[?].n)([respectively])())(.)]
[[0 25 4 (Xp)][0 5 2 (WV)][0 2 1 (Wd)][1 2 0 (AN)][2 3 0 (Sp)][3 5 1 (I*d)][3 4 0 (N)]
[4 5 0 (En)][5 11 2 (MVp)][5 6 0 (MVp)][6 8 1 (Js)][7 8 0 (Ds**c)][8 9 0 (Mf)][9 10 0 (Jp)]
[10 11 0 (Mp)][11 12 0 (Jp)][12 18 3 (MXp)][13 18 2 (Xd)][14 18 1 (A)][17 18 0 (AN)][16 17 0 (AN)]
[18 24 3 (Xc)][18 19 0 (Mp)][19 22 2 (Jp)][20 22 1 (AN)][21 22 0 (AN)]]
[0]
"""


class LGInprocParserTestCase(unittest.TestCase):
    # @unittest.skip
    def test_parse_batch_ps_output(self):
        pr = LGInprocParser()
        num_sent = len(pr._parse_batch_ps_output(lg_post_output))
        self.assertEqual(num_sent, 12, "'parse_batch_ps_output()' returns '{}' instead of '{}'".format(num_sent, 12))

    # @unittest.skip
    def test_parse_batch_ps_output_explosion(self):
        pr = LGInprocParser()
        num_sent = len(pr._parse_batch_ps_output(lg_post_explosion, 0))
        self.assertEqual(num_sent, 4, "'parse_batch_ps_output()' returns '{}' instead of '{}'".format(num_sent, 4))


    @unittest.skip
    def test_parse_file_with_lgp(self):
        """ Test 'parse_file_with_lgp' with default dictionary """
        # print(__doc__, sys.stderr)

        # Testing over poc-turtle corpus... 100% success is expected.
        options = 0 | BIT_STRIP

        metrics = parse_file_with_lgp("test-data/dict/poc-turtle", "test-data/corpora/poc-turtle/poc-turtle.txt",
                             None, 1, options)

        self.assertEqual(1.0, metrics.completely_parsed_ratio)
        self.assertEqual(0.0, metrics.completely_unparsed_ratio)
        self.assertEqual(1.0, metrics.average_parsed_ratio)

    @unittest.skip
    def test_parse_file_with_lgp_cmp(self):
        """ Make sure 'parse_file_with_lgp' and 'parse_file_with_lgp0' produce the same results. """
        # print(__doc__, sys.stderr)

        pr = LGInprocParser()

        # Testing over poc-turtle corpus... 100% success is expected.
        options = 0 | BIT_STRIP

        # Test if two functions return the same results.
        tup_lgp = parse_file_with_lgp0("test-data/dict/poc-turtle", "test-data/corpora/poc-turtle/poc-turtle.txt",
                                      None, 1, options)

        metrics = pr.parse("test-data/dict/poc-turtle", "test-data/corpora/poc-turtle/poc-turtle.txt", None,
                                      None, options)

        print(tup_lgp, sys.stderr)
        print(metrics.text(metrics), sys.stderr)

        self.assertEqual(tup_lgp[0], metrics.completely_parsed_ratio)
        self.assertEqual(tup_lgp[1], metrics.completely_unparsed_ratio)
        self.assertEqual(tup_lgp[2], metrics.average_parsed_ratio)


if __name__ == '__main__':
    unittest.main()
