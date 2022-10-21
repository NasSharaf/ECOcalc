import ECOLib as eco 
import numpy as np
import unittest

def test_chilledWaterReset():
    OAtemps = np.arange(-2.5, 95.5, 5)
    binhours = [14, 69, 400, 465, 703, 603, 1060, 708, 693, 595, 540, 853, 705, 523, 334, 298, 112, 50, 29, 6]
    cwReset = eco.ChilledWaterReset(OAtemps, binhours)
    cwReset.calculateReset()

def test_coolingTowerVFD():
    OAtemps = [39.9, 42, 44.1, 45.9, 47.1, 49, 50.9, 53, 54.9, 56.9, 58.9, 60.1, 62.3, 63.3, 64.2, 65.1, 65.9, 66.2, 67.4, 68.1, 69.9, 72.1, 74.1, 74.3]
    binhours = [252, 211, 265, 284, 276, 431, 271, 139, 301, 390, 377, 289, 306, 309, 392, 208, 93, 166, 155, 146, 99, 53, 16, 14]
    ctVFD = eco.CoolingTowerVFD(OAtemps, binhours, 50.0, 1000.0, 2, .7)
    ctVFD.setAssumptions()
    ctVFD.calcVFD()

def test_destratifyingFan():
    fanSavings = eco.DestratifyingFanSavings(2000, 80, 70, 75, 16, 200, 5000)
    fanSavings.setAssumptions()
    assert fanSavings.calcFanSavings(70) == 149