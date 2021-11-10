from roulette import *
from unittest import TestCase


class TestWheel(TestCase):
    def test_wheel(self):
        w = Wheel()
        o1 = Outcome("Red", 1)
        o2 = Outcome("Black", 2)
        o3 = Outcome("Red", 4)
        o4 = Outcome("High", 1)
        o5 = Outcome("low", 12)
        b1 = Bin({o1, o2, o3})
        b2 = Bin({o4, o5, o3})

        for o in b1:
            w.addOutcome(1, o)
        for o in b2:
            w.addOutcome(2, o)
        self.assertEqual(print(w.get(1)), print(b1))
        self.assertEqual(print(w.get(2)), print(b2))

    def test_wheel_sequence(self):
        wheel = Wheel()
        wheel.addOutcome(8, Outcome("test", 1))
        wheel.addOutcome(36, Outcome("test", 2))
        wheel.rng.seed(1)
        self.assertIn(Outcome("test", 1), wheel.choose().outcomes)
        self.assertIn(Outcome("test", 2), wheel.choose().outcomes)

    def test_wheel_bins(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        self.assertIn(Outcome("0", 35), wheel.get(0).outcomes)
        self.assertIn(Outcome("1-2-4-5", 8), wheel.get(5).outcomes)


class TestBinBuilder(TestCase):
    def test_straight_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        self.assertIn(Outcome("0", 35), wheel.bins[0].outcomes)
        self.assertIn(Outcome("1", 35), wheel.bins[1].outcomes)
        self.assertIn(Outcome("36", 35), wheel.bins[36].outcomes)
        self.assertIn(Outcome("00", 35), wheel.bins[37].outcomes)

    def test_split_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        self.assertIn(Outcome("1-2", 17), wheel.bins[1].outcomes)
        self.assertIn(Outcome("1-4", 17), wheel.bins[1].outcomes)
        self.assertIn(Outcome("33-36", 17), wheel.bins[36].outcomes)
        self.assertIn(Outcome("35-36", 17), wheel.bins[36].outcomes)

    def test_street_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        o1 = Outcome("1-2-3", 11)
        o2 = Outcome("34-35-36", 11)
        self.assertIn(o1, wheel.bins[1].outcomes)
        self.assertIn(o1, wheel.bins[2].outcomes)
        self.assertIn(o1, wheel.bins[3].outcomes)
        self.assertIn(o2, wheel.bins[34].outcomes)
        self.assertIn(o2, wheel.bins[35].outcomes)
        self.assertIn(o2, wheel.bins[36].outcomes)

    def test_corner_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        c1 = Outcome("1-2-4-5", 8)
        c2 = Outcome("4-5-7-8", 8)
        c3 = Outcome("2-3-5-6", 8)
        c4 = Outcome("5-6-8-9", 8)
        self.assertIn(c1, wheel.bins[1].outcomes)
        self.assertIn(c1, wheel.bins[4].outcomes)
        self.assertIn(c2, wheel.bins[4].outcomes)
        self.assertIn(c1, wheel.bins[5].outcomes)
        self.assertIn(c2, wheel.bins[5].outcomes)
        self.assertIn(c3, wheel.bins[5].outcomes)
        self.assertIn(c4, wheel.bins[5].outcomes)

    def test_line_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        l1 = Outcome("1-2-3-4-5-6", 5)
        l2 = Outcome("4-5-6-7-8-9", 5)
        self.assertIn(l1, wheel.bins[1].outcomes)
        self.assertIn(l1, wheel.bins[4].outcomes)
        self.assertIn(l2, wheel.bins[4].outcomes)

    def test_dozen_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        d1 = Outcome("Dozen 1", 2)
        d2 = Outcome("Dozen 2", 2)
        d3 = Outcome("Dozen 3", 2)
        self.assertIn(d1, wheel.bins[1].outcomes)
        self.assertIn(d2, wheel.bins[17].outcomes)
        self.assertIn(d3, wheel.bins[36].outcomes)

    def test_column_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        c1 = Outcome("Column 1", 2)
        c2 = Outcome("Column 2", 2)
        c3 = Outcome("Column 3", 2)
        self.assertIn(c1, wheel.bins[1].outcomes)
        self.assertIn(c2, wheel.bins[17].outcomes)
        self.assertIn(c3, wheel.bins[36].outcomes)

    def test_even_bets(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        low = Outcome("Low", 1)
        high = Outcome("High", 1)
        even = Outcome("Even", 1)
        odd = Outcome("Odd", 1)
        red = Outcome("Red", 1)
        black = Outcome("Black", 1)
        self.assertIn(low, wheel.bins[1].outcomes)
        self.assertIn(low, wheel.bins[17].outcomes)
        self.assertIn(low, wheel.bins[18].outcomes)
        self.assertIn(high, wheel.bins[36].outcomes)
        self.assertIn(odd, wheel.bins[1].outcomes)
        self.assertIn(odd, wheel.bins[17].outcomes)
        self.assertIn(even, wheel.bins[18].outcomes)
        self.assertIn(even, wheel.bins[36].outcomes)
        self.assertIn(red, wheel.bins[1].outcomes)
        self.assertIn(black, wheel.bins[17].outcomes)
        self.assertIn(red, wheel.bins[18].outcomes)
        self.assertIn(red, wheel.bins[36].outcomes)

    def test_five_bet(self):
        wheel = Wheel()
        build = BinBuilder(wheel)
        build.buildbins()
        five_out = Outcome("Five Bet", 6)
        self.assertIn(five_out, wheel.bins[0].outcomes)
        self.assertIn(five_out, wheel.bins[37].outcomes)
