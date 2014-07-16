import numpy as np
import pandas as pd


class ValuationInput():

    def __init__(self, coupon, maturity, notional,
                 recovery_rate, disc_factors, surv_probs):
        self.coupon = coupon
        self.maturity = maturity
        self.notional = notional
        self.recovery_rate = recovery_rate
        self.disc_factors = disc_factors
        self.surv_probs = surv_probs
        self.coupon_freq = 4.0

    def build_cashflow_frame(self, at_mid_points=False):
        year_frac, year_frac_diff = self._calc_year_frac(at_mid_points)

        num_payments = self.maturity * self.coupon_freq
        coupon_in_period = self.coupon / self.coupon_freq
        coupon_payments = coupon_in_period * np.ones(num_payments + 1)
        coupon_payments[0] = 0.0
        recovery = self.recovery_rate * np.ones(num_payments + 1)

        surv_prob_at_t = [self.surv_probs.value(yy) for yy in year_frac]
        disc_factor_at_t = [self.disc_factors.value(yy) for yy in year_frac]

        series = [
            pd.Series(coupon_payments, year_frac, name='CouponPayments'),
            pd.Series(recovery, year_frac, name='Recovery'),
            pd.Series(year_frac_diff, year_frac, name='YearFracDiff'),
            pd.Series(surv_prob_at_t, year_frac, name='SurvivalProb'),
            pd.Series(disc_factor_at_t, year_frac, name='DiscountFactor'),
        ]
        cash_flows = pd.concat(series, axis=1)
        return cash_flows

    def _calc_year_frac(self, at_mid_points=False):
        # could extend to include day count conventions
        num_payments = self.maturity * self.coupon_freq
        year_frac = np.linspace(0.0, self.maturity, num_payments + 1)
        year_frac_diff = np.ones(num_payments + 1) / self.coupon_freq
        year_frac_diff[0] = 0.0
        if at_mid_points:
            interval = (1.0 / self.coupon_freq)
            year_frac = year_frac - 0.5 * interval
            year_frac[0] = 0.0
            year_frac_diff[1] = 0.5 * interval
        return year_frac, year_frac_diff


class FlatCurve():

    def __init__(self, rate):
        self.rate = rate

    def value(self, year_frac):
        return np.exp(-1 * self.rate * year_frac)
