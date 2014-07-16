import unittest
from pricer import inputs


class TestValuationInputs(unittest.TestCase):

    def setUp(self):
        disc_factors = inputs.FlatCurve(0.05)
        survival_curve = inputs.FlatCurve(0.0166)
        self.cdsflat = inputs.ValuationInput(0.01, 5.0, 10.e6, 0.4,
                                             disc_factors, survival_curve)

    def test_initialization(self):
        self.assertEqual(self.cdsflat.coupon, 0.01)

    def test_build_cashflow_frame(self):
        cash_flows = self.cdsflat.build_cashflow_frame()
        self.assertEqual(cash_flows.index[1], 0.25)
        self.assertEqual(cash_flows.index[2], 0.5)
        self.assertAlmostEqual(cash_flows.SurvivalProb[1.0], 0.983537)
        self.assertAlmostEqual(cash_flows.DiscountFactor[1.0], 0.95122942)
        self.assertEqual(cash_flows.shape[0], 21)

    def test_build_cashflow_frame_at_midpoints(self):
        cash_flows = self.cdsflat.build_cashflow_frame(at_mid_points=True)
        self.assertEqual(cash_flows.index[1], 0.125)
        self.assertEqual(cash_flows.index[2], 0.375)
        self.assertAlmostEqual(cash_flows.SurvivalProb[1.125], 0.98149829)
        self.assertAlmostEqual(cash_flows.DiscountFactor[1.125], 0.94530278)
        self.assertEqual(cash_flows.shape[0], 21)


class TestCurves(unittest.TestCase):

    def test_flat_curve_values(self):
        curve = inputs.FlatCurve(0.05)
        self.assertAlmostEqual(curve.value(1.0), 0.951229, 6)
        self.assertAlmostEqual(curve.value(2.0), 0.904837, 6)
        self.assertAlmostEqual(curve.value(1.5), 0.927743, 6)


if __name__ == '__main__':
    unittest.main()
