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
    fanSavings = eco.DestratifyingFan(2000, 80, 70, 75, 16, 200, 5000)
    fanSavings.setAssumptions()
    assert fanSavings.calcFanSavings(70) == 149

def test_motorReplacement():
    motorReplace = eco.EnergyEfficientMotorReplacement(25, .83, 208, 1800, 2400, 14, 25, .90, 208, 1800, 2400, 14)
    motorReplace.setAssumptions()
    assert motorReplace.calcReplacementSavings() == 229

def test_fanPressureReduction():
    fpr = eco.StaticPressureReset(1500, 1200, .79, .90, 55000, 55000, 4800)
    assert fpr.calcPressureReduction() == 1027

def test_hotWaterReset():
    OAtemps = np.arange(-2.5, 95.5, 5)
    binhours = [14, 69, 400, 465, 703, 603, 1060, 708, 693, 595, 540, 853, 705, 523, 334, 298, 112, 50, 29, 6]
    hwReset = eco.HotWaterReset(OAtemps, binhours)
    hwReset.setAssumptions()
    hwReset.calculateReset()

def test_powerFactorCorrectionMultiplier():
    pfCorr = eco.PowerFactorCorrection(5976, 5200, 6600, .50, .40)
    pfCorr.setAssumptions("Multiplier", .9, .9, 1.1, 1.33)
    assert pfCorr.calcCorrection() == 2640

def test_powerFactorCorrectionKVAR():
    pfCorr = eco.PowerFactorCorrection(5976, 5200, 6600, .50, .40)
    pfCorr.setAssumptions("KVAR", .9, .9, 1.1, 1.33)
    assert pfCorr.calcCorrection() == 2600

def test_powerFactorCorrectionKVA():
    pfCorr = eco.PowerFactorCorrection(5976, 5200, 6600, .50, .40)
    pfCorr.setAssumptions("KVA", .9, .9, 1.1, 1.33)
    assert pfCorr.calcCorrection() == 6831

def test_powerFactorCorrectionAdjustment():
    pfCorr = eco.PowerFactorCorrection(5976, 5200, 6600, .50, .40)
    pfCorr.setAssumptions("Adjustment", .9, .9, 1.1, 1.33)
    assert pfCorr.calcCorrection() == 5980