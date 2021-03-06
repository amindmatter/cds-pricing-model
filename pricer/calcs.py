class Valuation():
    # TODO: Should use lazy properties to cache results

    def __init__(self, inputs):
        self.inputs = inputs

    def rpv01(self):
        cf = self.inputs.build_cashflow_frame()
        surv = cf.shift(1).SurvivalProb + cf.SurvivalProb
        surv[0] = 0.0
        discounted_1bps_vec = cf.YearFracDiff * cf.DiscountFactor * surv
        result = 0.5 * discounted_1bps_vec.sum()
        return result

    def pv_premium_leg(self):
        return self.inputs.notional * self.inputs.coupon * self.rpv01()

    def pv_protection_leg(self):
        cf = self.inputs.build_cashflow_frame(at_mid_points=True)
        loss_given_default = (1.0 - self.inputs.recovery_rate)
        hazard = -1 * cf.diff(1).SurvivalProb
        hazard[0] = 0.0
        unit_pv = loss_given_default * (hazard * cf.DiscountFactor).sum()
        return self.inputs.notional * unit_pv

    def puf(self):
        return self.pv_protection_leg() - self.pv_premium_leg()

    def parspread(self):
        return self.pv_protection_leg() / self.rpv01()
