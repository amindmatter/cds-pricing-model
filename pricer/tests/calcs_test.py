import unittest
from pricer import inputs
from pricer import calcs


class TestValuation(unittest.TestCase):

    def setUp(self):
        disc_factors = inputs.FlatCurve(0.05)
        survival_curve = inputs.FlatCurve(0.01666666)
        self.cdsflat = inputs.ValuationInput(0.01, 5.0, 1.0, 0.4,
                                             disc_factors, survival_curve)

    def test_premium_leg(self):
        val = calcs.Valuation(self.cdsflat)
        self.assertAlmostEqual(val.rpv01(), 4.225498, 3)
        self.assertAlmostEqual(val.pv_premium_leg(), 0.04225498, 5)

    def test_protection_leg(self):
        val = calcs.Valuation(self.cdsflat)
        self.assertAlmostEqual(val.pv_protection_leg(), 0.04136499, 5)

    def test_parspread(self):
        val = calcs.Valuation(self.cdsflat)
        self.assertAlmostEqual(val.parspread(), 0.009789, 5)

    def test_puf(self):
        val = calcs.Valuation(self.cdsflat)
        self.assertAlmostEqual(val.puf(), -0.0008898, 5)

if __name__ == '__main__':
    unittest.main()
