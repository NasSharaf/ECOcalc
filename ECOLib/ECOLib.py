import numpy as np
import math
from ECOMain import ECO
from ChilledWaterReset import ChilledWaterReset
from CoolingTowerVFD import CoolingTowerVFD
from HotWaterReset import HotWaterReset
from EnergyEfficientMotorReplacement import EnergyEfficientMotorReplacement
from PowerFactorCorrection import PowerFactorCorrection

####### VERY COMPLICATED, NEED TO FOCUS SEPARATELY #######
class DemandControlVentilation(ECO):
    """
    :param binhour: number of hours per year at a given temperature range
    :type binhour: int

    :param OAtemp: The outside air temperature at the given bin hour
    :type OAtemp: float
    """
    def __init__(self, 
        binhours, OATemp,
        weeklyOp, percentOA, supplyFanVolume, reductionOA, enthalpyOA, tempRA, enthalpyRA,
    ):
        super().__init__(binhours, OATemp),
        self.weeklyOp = weeklyOp, 
        self.percentOA = percentOA, 
        self.supplyFanVolume = supplyFanVolume, 
        self.reductionOA = reductionOA, 
        self.enthalpyOA = enthalpyOA, 
        self.tempRA = tempRA, 
        self.enthalpyRA = enthalpyRA

    def calcDCV(self, weeklyOp, percentOA, supplyFanVolume, reductionOA, binhours, tempOA, enthalpyOA, tempRA, enthalpyRA):
        # Assumptions
        clgSeasonWeeks = 10
        htgSeasonWeeks = 42
        boilerEfficiency = .85
        chillerEfficiency = 1.2 #kW/ton
        distributionEfficiency = .90
        avgSpaceEnthalpy = 28 #btu/lb-air
        enthalpySA = 23 #btu/lb-air
        variableAirVolumeAdjustment = .90
        # Formula
        tempMA = (percentOA * (tempOA - tempRA)) - tempRA
        enthalpyMA = (percentOA * (enthalpyOA - enthalpyRA)) - enthalpyRA
        enthalpyDiff = enthalpyMA - enthalpySA
        coolingLoad = 4.5 * supplyFanVolume * enthalpyDiff * binhours *(1/1000)
        coolingEnergy = coolingLoad * (1/12) * chillerEfficiency
        coolingCost = coolingEnergy * ELECTRIC_ENERGY_COSTS
        heatingLoad = 1.08 * supplyFanVolume * enthalpyDiff * binhours *(1/1000)
        heatingEnergy = heatingLoad *(1/1000) * (1/boilerEfficiency) * (1/distributionEfficiency)
        heatingCost = heatingEnergy * HEATING_ENERGY_COST
        # Results
        return


class DryBulbEconomizer(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def dryBulbEconomizer(self, OAEnthalpy, RATemp, RAEnthalpy, RAVolume):
        """
        """
        # Assumptions
        elevationLocation = 600
        AHUCapacity = 60000 #cfm
        percentVentilationAir = .034
        coolingEfficiency = 1.2 #kW/Ton
        summerRATenthalpy = 28.9
        winterRATenthalpy = 22.8
        dryBulbSetpoint = 60 #degF
        coolingSeasonOAT = 50 #degF
        heatingSeasonOAT = 49 #degF
        coolingSATTemp = 55 #degF
        coolingSATEnthalpy = 23 #btu/lb-air
        # Formula
        MATemp = (percentVentilationAir * (OATemp - RATemp)) - RATemp
        MAEnthalpy = (percentVentilationAir * (OAEnthalpy - RAEnthalpy)) - RAEnthalpy
        coolingLoad = 4.5 * RAVolume * (MAEnthalpy - RAEnthalpy)
        if OATemp > coolingSeasonOAT:
            chillerLoad = coolingLoad
        economizerSavings = 4.5 * RAVolume * (MAEnthalpy - OAEnthalpy)
        totalCoolingLoad = coolingLoad * binhours / 1000 #MBH
        coolingEnergy = coolingLoad / 12 * coolingEfficiency
        RAQuantity = AHUCapacity * percentVentilationAir

        # Results
        return


class EnthalpyEconomizer(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def enthalpyEconomizer(self):
        return


class LightingRetrofit(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def lightingRetrofit(self, operatingPeriod, numFixtures, wattPerFixture, opHours, 
        clgHrsPerWeek, clgWeeksPerYear, clgMonthsPerYear,
        htgHrsPerWeek, htgWeeksPerYear, htgMonthsPerYear,
        ):
        """
        """
        # Assumptions
        utilizationFactor = .80
        avgHeatLossCoeff = .41
        clgSysEfficiency = 6.00
        htgSysEfficiency = .70
        # Formula
        electricalUse = numFixtures * wattPerFixture * opHours
        electricalDemand = numFixtures * wattPerFixture
        lightClgHeatLoad = electricalDemand * utilizationFactor * clgHrsPerWeek * clgWeeksPerYear
        lightHtgHeatLoad = electricalDemand * utilizationFactor * htgHrsPerWeek * htgWeeksPerYear
        lightClgHeatLoadUse = lightClgHeatLoad * htgSysEfficiency / clgSysEfficiency
        # Results
        return

## These Might need a separate 'Scheduler' function ##
class OutsideAirDamperControl(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def outsideAirDamperControl(self):
        """
        """
        # Assumptions
        # Formula
        # Results
        return

## These Might need a separate 'Scheduler' function ##
class OccupancyLighting(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def occupancyLighting(self):
        """
        """
        # Assumptions
        # Formula
        # Results
        return

## These Might need a separate 'Scheduler' function ##
class OccupancyTempSetback(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def occupancyTempSetback(self):
        """
        """
        # Assumptions
        # Formula
        # Results
        return

## These Might need a separate 'Scheduler' function ##
class PeakDemandLimiting(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def peakDemandLimiting(self):
        """
        """
        # Assumptions
        # Formula
        # Results
        return

class PipeInsulation(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def pipeInsulation(self, hoursOp, weeksOp, heatingMedia, pipingMaterial, ambientTemp, pipeDia, pipeLength):
        """
        """
        # Assumptions
        minPipingInsulation = 2
        circTemp = 210 #degF
        htgEfficiency = .60
        insulationConductivity = .29
        # Formula

        # Results
        return

class SteamTrapSavings(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def steamTrapSavings(opHoursPerWeek, htgWeeksPerYear, sizeOfFailedTrap, sysPressure, numFailedTraps):
        """
        """
        # Assumptions
        boilerEfficiency = .75
        # Formula

        # Results
        return

## These Might need a separate 'Scheduler' function ##
class TimeOfDayScheduling(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)
            
    def timeOfDayScheduling():
        """
        """
        # Assumptions
        # Formula
        # Results
        return

class VariableVolumePumping(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def variableVolumePumping(opHoursTotal, motorHP, motorEfficiency, chilledWaterCosts, hotWaterCosts, percentFlow, exponent, percentTimeAtFlow):
        """
        """
        # Assumptions
        demandUseFactor = .80
        opMonthsPerYear = 8
        pumpLoadFactor = .70
        valveLeakage = .10
        # Formula
        pumpPowerDraw = (motorHP * pumpLoadFactor * percentFlow**exponent * .746 / motorEfficiency ) * opHoursTotal * percentTimeAtFlow
        pumpDemand = (motorHP * pumpLoadFactor * percentFlow**exponent * .746 / motorEfficiency) * opMonthsPerYear * demandUseFactor * percentTimeAtFlow
        hotWaterLeakageSaving = valveLeakage * hotWaterCosts
        chilledWaterLeakageSavings = valveLeakage * chilledWaterCosts
        # Results
        return


if __name__ == "__main__":
    # OAtemps = [39.9, 42, 44.1, 45.9, 47.1, 49, 50.9, 53, 54.9, 56.9, 58.9, 60.1, 62.3, 63.3, 64.2, 65.1, 65.9, 66.2, 67.4, 68.1, 69.9, 72.1, 74.1, 74.3]
    # binhours = [252, 211, 265, 284, 276, 431, 271, 139, 301, 390, 377, 289, 306, 309, 392, 208, 93, 166, 155, 146, 99, 53, 16, 14]
    # fanSavings = DestratifyingFanSavings(2000, 80, 70, 75, 16, 200, 5000)
    # fanSavings.setAssumptions()
    # fanSavings.calcFanSavings(70) 
    

    OAtemps = np.arange(-2.5, 95.5, 5)
    binhours = [14, 69, 400, 465, 703, 603, 1060, 708, 693, 595, 540, 853, 705, 523, 334, 298, 112, 50, 29, 6]
    # cwReset = ChilledWaterReset(OAtemps, binhours)
    # cwReset.calculateReset()
    # hwReset = HotWaterReset(OAtemps, binhours)
    # hwReset.setAssumptions()
    # hwReset.calculateReset()

    pfCorr = PowerFactorCorrection(5976, 5200, 6600, .50, .40)
    pfCorr.setAssumptions("Adjustment", .9, .9, 1.1, 1.33)
    print(pfCorr.calcCorrection())
    print(pfCorr.__dict__.keys())