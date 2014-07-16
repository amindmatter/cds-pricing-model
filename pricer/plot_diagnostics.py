import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from pricer import inputs
from pricer import calcs


def generate_diagnositic_plots():
    pdf = PdfPages('plot_diagnostics.pdf')

    plt.figure()
    for reca in [0.4, 0.6, 0.8]:
        frm = calc_at_varying_hazard_rates(reca)
        plt.plot(frm.HazardRate, frm.PUF, label='%s%% Recovery' % (reca * 100))
    plt.title('PUF vs Default Intensity Rate')
    plt.xlabel('Default Intensity Rate')
    plt.ylabel('PUF')
    plt.legend(loc="lower right")
    pdf.savefig()
    plt.close()

    plt.figure()
    frm = calc_at_varying_maturities()
    plt.plot(frm.Maturity, frm.RPV01)
    plt.title('RPV01 vs Maturity')
    plt.xlabel('Maturity (years)')
    plt.ylabel('RPV01')
    pdf.savefig()
    plt.close()

    pdf.close()


def calc_at_varying_hazard_rates(recovery=0.4):
    haz_rates = np.linspace(0.0, 0.10)
    pufs = []
    for hz in haz_rates:
        cdsflat = generic_inputs(haz_rate=hz)
        cdsflat.recovery_rate = recovery
        val = calcs.Valuation(cdsflat)
        pufs.append(val.puf())
    result = pd.DataFrame(dict(HazardRate=haz_rates, PUF=pufs))
    return result


def calc_at_varying_maturities():
    maturities = range(1, 10)
    rpv01s = []
    for tenor in maturities:
        cdsflat = generic_inputs()
        cdsflat.maturity = tenor
        val = calcs.Valuation(cdsflat)
        rpv01s.append(val.rpv01())
    result = pd.DataFrame(dict(Maturity=maturities, RPV01=rpv01s))
    return result


def generic_inputs(disc_rate=0.05, haz_rate=0.0166):
    coupon = 0.01
    maturity = 5.0
    notional = 1.0
    recovery = 0.4
    cdsflat = inputs.ValuationInput(
        coupon, maturity, notional, recovery, 
        inputs.FlatCurve(disc_rate), inputs.FlatCurve(haz_rate)
    )
    return cdsflat

