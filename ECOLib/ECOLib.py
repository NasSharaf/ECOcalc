import numpy as np
import math

ELECTRIC_ENERGY_COSTS = 0.05
ELECTRIC_DEMAND_COSTS = 11.43
GAS_ENERGY_COSTS = 6.00
HEATING_ENERGY_COST = 0.50
COOLING_ENERGY_COST = 10.00
DAY_OF_WEEK = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
DEFAULT_EXISTING_OP_HOURS = {
            "Sunday": 8,
            "Monday": 16,
            "Tuesday": 16,
            "Wednesday": 16,
            "Thursday": 16,
            "Friday": 16,
            "Saturday": 8,
        }
DEFAULT_PROPOSED_OP_HOURS = {
            "Sunday": 0,
            "Monday": 8,
            "Tuesday": 8,
            "Wednesday": 8,
            "Thursday": 8,
            "Friday": 8,
            "Saturday": 0,
        }

class Value:
    """
    """

    def __init__(self, value, unit, type_of):
        self.value = value
        self.unit = unit
        self.type_of = value.type_of()

    def getValue(self):
        """
        """
        return self.value

    def setValue(self, newVal):
        """
        """
        self.value = newVal

    def convert(self, fromUnit, toUnit):
        """
        make utils library, convert units there
        """


class ECO:
    """
    Energy Conservation Opportunitiies or ECOs (also called FIMS - 
    facility improvement measures and ECMs - energy conservation measures/methods)
    are methods to reduce the energy use of a building. This class provides common
    functions most or all ECOs will require. 

    :param binhour: number of hours per year at a given temperature range
    :type binhour: int

    :param OAtemp: The outside air temperature at the given bin hour
    :type OAtemp: float
    """
    def __init__(self, binhours, OATemp):
        self.binhours = binhours
        self.OATemp = OATemp

    def scheduleCalcEnergy(self, energyDraw, opHoursPerWeek, opWeeksPerYear):
        """
        """
        energyUse = energyDraw * opHoursPerWeek * opWeeksPerYear
        return energyUse

    def scheduleCalcCostEnergy(self, energyDraw, opHoursPerWeek, opWeeksPerYear, costEnergy):
        """
        """
        energyCost = energyDraw * opHoursPerWeek * opWeeksPerYear * costEnergy
        return energyCost
        
    def compare(self, prevEnergyUse, newEnergyUse):
        """
        """
        energySavings = prevEnergyUse - newEnergyUse
        return energySavings

    def compareCosts(self, prevEnergyUse, newEnergyUse, energyCost):
        """
        """
        energyCostSavings = (prevEnergyUse - newEnergyUse) * energyCost
        return energyCostSavings

class ChilledWaterReset(ECO):
    """
    A chilled water reset steps gradually resets the temperature of the water in a 
    chiller as the cooling load increases. The lower the cooling load, the less chilled 
    the water needs to be to meet the cooling load. 

    :param binhour: number of hours per year at a given temperature range
    :type binhour: int

    :param OAtemp: The outside air temperature at the given bin hour
    :type OAtemp: float

    :param chillerPeakLoad: The maximum tonnage of cooling a chiller can provide
    :type chillerPeakLoad: float

    :param chillerEfficiency: The rated efficiency of the chiller
    :type chillerEfficiency: float

    :param chilledWaterReset: The amount to reduce the the chilled water temperature
    :type chilledWaterReset: float

    :param resetFactor: The multiple to help calculate the energy savings
    :type resetFactor: float

    :param outsideAirInitiates: The outside air temperature at which the chiller is turned on
    :type outsideAirInitiates: float

    :param minimumChillerLoad: The minimum tonnage of cooling the chiller will supply when turned on
    :type minimumChillerLoad: float

    :param designOATemp: The minimum tonnage of cooling the chiller will supply when turned on
    :type designOATemp: float
    """
    def __init__(self, 
        binhours, 
        OATemp,
        chillerPeakLoad = 500.0, 
        chillerEfficiency = 1.0, 
        chilledWaterReset = 6, 
        resetFactor = .023, 
        outsideAirInitiates = 55.0, 
        minimumChillerLoad = 20.0,
        designOATemp = 92.5
    ):
        super().__init__(binhours, OATemp)
        self.chillerPeakLoad = chillerPeakLoad
        self.chillerEfficiency = chillerEfficiency
        self.chilledWaterReset = chilledWaterReset
        self.resetFactor = resetFactor
        self.outsideAirInitiates = outsideAirInitiates
        self.minimumChillerLoad = minimumChillerLoad
        self.designOATemp = designOATemp

    def calculateReset(self):
        """
        """
        for (OAtemp, binhr) in zip(self.OATemp, self.binhours):
            buildingLoad = (self.chillerPeakLoad * (OAtemp - self.outsideAirInitiates)/(self.designOATemp - self.outsideAirInitiates))
            if buildingLoad > self.minimumChillerLoad:
                chillerLoad = buildingLoad
            else:
                chillerLoad = self.minimumChillerLoad
            energyUse = chillerLoad * self.chillerEfficiency * binhr
            resetPotential = (self.chillerPeakLoad - chillerLoad)/ self.chillerPeakLoad
            resetTemp = resetPotential * self.chilledWaterReset
            energySavings = chillerLoad * self.chillerEfficiency * binhr * resetTemp * self.resetFactor
            # Results
            energySaved = self.compare(energyUse, energySavings)
            energyCostSaved = self.compareCosts(energyUse, energySavings, ELECTRIC_ENERGY_COSTS)
            print(energySaved)
            print(energyCostSaved)

####### THIS ONE NEEDS WORK< THERE IS AN ISSUE #######
class CoolingTowerVFD(ECO):
    """
    Adding a variable frequency drive on a cooling tower fan can vary the speed of the fan,
    and thus modulate the fan depending on the heat rejection the chilled water system requires

    :param binhour: number of hours per year at a given temperature range
    :type binhour: int

    :param OAtemp: The outside air temperature at the given bin hour
    :type OAtemp: float
    """
    def __init__(self,
        binhours, 
        OATemps, 
        motorHP: float, 
        towerTon: float, 
        fanType: int, 
        fanspeed: float
    ):
        super().__init__(OATemps, binhours)
        self.motorHP = motorHP 
        self.towerTon = towerTon
        self.fanType = fanType
        self.fanspeed = fanspeed

    def setAssumptions(self,
        motorLoading: float = .70,
        motorEfficiency: float = .90,
        powerReductionExponent: float = 2.7,
        minimumVFDSpeed: float = .10
    ):
        self.motorLoading = motorLoading
        self.motorEfficiency = motorEfficiency
        self.powerReductionExponent = powerReductionExponent
        self.minimumVFDSpeed = minimumVFDSpeed

    def calcVFD(self):
        # Formula
        for binhr in self.binhours:
            fanEnergy = self.motorHP * .746 * self.motorLoading / self.motorEfficiency
            percentMotorLoad = self.fanspeed**self.powerReductionExponent
            if self.fanType == 1:
                fanEnergyKWH = fanEnergy * binhr * self.fanspeed
            elif self.fanType == 2:
                if self.fanspeed < .50:
                    dutyCycle = self.fanspeed**2
                else:
                    dutyCycle = 1.0
                fanEnergyKWH = fanEnergy * binhr * dutyCycle
            fanEnergyVSD = fanEnergy*binhr*percentMotorLoad
            # Results
            energySaved = self.compare(fanEnergyKWH, fanEnergyVSD)
            energyCostSaved = self.compareCosts(fanEnergyKWH, fanEnergyVSD, ELECTRIC_ENERGY_COSTS)
            print(fanEnergyVSD)
            # print(energyCostSaved)

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

class DestratifyingFanSavings(ECO):
    """
    A destratifying fan is used in high ceiling areas that stratify the air into a 
    layer of warm air near the ceiling and cooler air near the floor. Installing a 
    fan and destratifying the air can increase occupant comfort and provide some 
    energy savings by reducing excess heating a building might be providing to
    cause such stratification.

    :param supplyAirVolume: amount of air the AHU is pushing out of the supply duct
    :type supplyAirVolume: float

    :param ceilingTemp: temperature at the ceiling/height of stratified area
    :type ceilingTemp: float

    :param floorTemp: temperature at the floor/lowest point of stratified area
    :type floorTemp: float

    :param existingAvgTemp: average temperature of stratified area before adding destratification fan
    :type existingAvgTemp: float

    :param hoursOp: hours the stratified space is in operation
    :type hoursOp: int

    :param hoursOp: days the stratified space is in operation
    :type hoursOp: int

    :param hoursPerHtgSeason: hours the heating system will need to be operational per year
    :type hoursPerHtgSeason: int
    """
    def __init__(self, 
        supplyAirVolume : float, 
        ceilingTemp: float, 
        floorTemp: float, 
        existingAvgTemp: float, 
        hoursOp: int, 
        daysOp: int, 
        hoursPerHtgSeason: int
    ):
        self.supplyAirVolume = supplyAirVolume
        self.ceilingTemp = ceilingTemp
        self.floorTemp = floorTemp
        self.existingAvgTemp = existingAvgTemp
        self.hoursOp = hoursOp
        self.daysOp = daysOp
        self.hoursPerHtgSeason = hoursPerHtgSeason

    def setAssumptions(self,
        htgSysEfficiency: float = .80,
        motorLoadFactor: float = .70,
        motorEfficiency: float  = .80, 
        ceilingFanHP: float  = 1 #HP
    ):
        """
        Addiitonal assumptions that can be modified.

        :param htgSysEfficiency: efficiency of the boiler/heating system
        :type htgSysEfficiency: float

        :param motorLoadFactor: load incurred on the statifying fan motor
        :type motorLoadFactor: float

        :param motorEfficiency: efficiency of the stratifying fan motor
        :type motorEfficiency: float

        :param ceilingFanHP: horsepower of the stratifying fan motor
        :type ceilingFanHP: float
        """
        self.htgSysEfficiency = htgSysEfficiency
        self.motorLoadFactor = motorLoadFactor
        self.motorEfficiency = motorEfficiency
        self.ceilingFanHP = ceilingFanHP

    def calcFanSavings(self, propAvgTemp: float):
        """
        Performs destratifying fan saving calculation. Returns total savings. 

        :param propAvgTemp: proposed average temperature of stratified area aferadding destratification fan
        :type propAvgTemp: float
        """
        annualEnergySavings = 1.08 * self.supplyAirVolume * self.hoursPerHtgSeason * (self.existingAvgTemp - propAvgTemp) / self.htgSysEfficiency / 100000
        annualEnergyCostSavings = annualEnergySavings * HEATING_ENERGY_COST
        motorEnergyUse = self.ceilingFanHP * .746 * self.motorLoadFactor / self.motorEfficiency
        annualElectricUse = motorEnergyUse * self.hoursPerHtgSeason
        annualElectricCost = annualElectricUse * ELECTRIC_ENERGY_COSTS
        totalSavings = annualEnergyCostSavings - annualElectricCost
        # Results
        return totalSavings

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

class EnergyEfficientMotorReplacement(ECO):
    """
    Replace an existing motor with a more energy efficient motor
    """
    def __init__(self,
        motorSize: int, 
        motorEfficiency: float, 
        motorVoltage: int, 
        loadRPM: float, 
        hoursOfUse: int,
        motorKW: float,
        newMotorSize: int, 
        newmotorEfficiency: float, 
        newmotorVoltage: int, 
        newloadRPM: float, 
        newhoursOfUse: int,
        newmotorKW: float
    ):
        self.motorSize = motorSize
        self.motorEfficiency = motorEfficiency
        self.motorVoltage = motorVoltage
        self.loadRPM = loadRPM
        self.hoursOfUse = hoursOfUse
        self.motorKW = motorKW
        self.newMotorSize = newMotorSize
        self.newmotorEfficiency = newmotorEfficiency
        self.newmotorVoltage = newmotorVoltage
        self.newloadRPM = newloadRPM
        self.newhoursOfUse = newhoursOfUse
        self.newmotorKW = newmotorKW

    def setAssumptions(self,
        existingMotorLoadFactor:float = .75,
        newMotorLoadFactor: float = .75,
        powerFactor:float = .85,
        demandUseFactor:float = .80,
        peakLoadMonths:int = 6
    ):
        self.existingMotorLoadFactor = existingMotorLoadFactor
        self.newMotorLoadFactor = newMotorLoadFactor
        self.powerFactor = powerFactor
        self.demandUseFactor = demandUseFactor
        self.peakLoadMonths = peakLoadMonths

    def energyEfficientMotorReplacement(self):
        """
        
        """
        motorKW = motorSize * .746 * existingMotorLoadFactor
        newMotorKW = newMotorSize * .746 * existingMotorLoadFactor
        speedRatioCorrFactor = (newLoadRPM/loadRPM)**3
        existingEnergyUse = motorKW/motorEfficiency * hoursOfUse
        existingDemandUse = motorKW/motorEfficiency * peakLoadMonths * demandUseFactor
        newEnergyUse = newMotorKW/newMotorEfficiency * newHoursOfUse
        newDemandUse = newMotorKW/newMotorEfficiency * peakLoadMonths * demandUseFactor * speedRatioCorrFactor
        # Results
        energyUseSavings = (existingEnergyUse - newEnergyUse) * ELECTRIC_ENERGY_COSTS
        energyDemandSavings = (existingDemandUse - newDemandUse) * ELECTRIC_DEMAND_COSTS
        totalSavings = energyUseSavings + energyDemandSavings
        return totalSavings

class EnthalpyEconomizer(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def enthalpyEconomizer(self):
        return

class FanPressureReduction(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def fanPressureReduction(self, sysPressure, newSysPressure, fanEfficiency, motorEfficiency, fanVolume, newFanVolume, hoursOfUse):
        """
        Fan system pressure reduction to new static pressure setpoint
        """
        # Formula
        fanBHP = (fanVolume * sysPressure)/(6356 * fanEfficiency)
        newFanBHP = (newFanVolume * newSysPressure)/(6356 * fanEfficiency)
        fanEnergyUse = fanBHP * .746 * hoursOfUse / motorEfficiency
        fanDemandUse = fanBHP * .746 / motorEfficiency
        newEnergyUse = newFanBHP * .746 * hoursOfUse / motorEfficiency
        newDemandUse = newFanBHP * .746 / motorEfficiency
        # Results
        energyUseSavings = (fanEnergyUse - newEnergyUse) * ELECTRIC_ENERGY_COSTS
        energyDemandSavings = (fanDemandUse - newDemandUse) * ELECTRIC_DEMAND_COSTS
        totalSavings = energyUseSavings + energyDemandSavings
        return

class HotWaterReset(ECO):
    """
    Similar to chilled water reset, gradually reset the water temperature in the boiler 
    as the heaitng load increases. the lower the heating load, the less warm the water from
    the boiler needs to be. 
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def calcHotWaterReset(self, OATemp, binhours):
        """ 
        """
        # Assumptions
        boilerPeakLoad = 8050000 # btu/hr
        boilerEfficency = .80
        designHotWaterSupplyTemp = 180 # degF
        designIndoorAirTemp = 68 # degF
        designOutdoorAirTemp = -2.5 # degF
        hotWaterReset = 50 #degF 
        resetFactor = .08
        heatingSeasonInitiate = 70 # degF
        minimumBoilerLoad = 1000000 # btu/hr
        # Formula
        hotWaterSupplyTemp = designIndoorAirTemp + (designHotWaterSupplyTemp - designIndoorAirTemp)/(designIndoorAirTemp - designOutdoorAirTemp) * (designIndoorAirTemp - OATemp)
        buildingLoad = boilerPeakLoad *((OATemp - heatingSeasonInitiate)/(designOutdoorAirTemp - heatingSeasonInitiate))
        if buildingLoad > minimumBoilerLoad:
            boilerLoad = buildingLoad
        else:
            boilerLoad = minimumBoilerLoad
        energyUse = boilerLoad /(boilerEfficency * binhours)
        resetPotential = (boilerPeakLoad - boilerLoad)/boilerPeakLoad
        resetTemp = resetPotential * hotWaterReset
        energySavings = energyUse * binhours * resetFactor * (resetTemp / 40) / 1000000
        energyCost = energySavings * ELECTRIC_ENERGY_COSTS
        # Results
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

class PowerFactorCorrection(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def powerFactorCorrection(powerKW, powerKVAR, powerKVA):
        """
        """
        # Assumptions
        powerFactorChargeType = "Multiplier"
        powerFactorKVARCharge = .50
        powerFactorKVACharge = .40
        minimumPFPenalty = .90
        proposedCorrection = .90
        existingMultiplier = 1.10
        existingAdjustment = 1.33
        # Formula
        powerFactorFromeKVA = math.sin(math.atan(powerKVAR/powerKW))
        powerFactorFromMultiplier = (1/existingMultiplier)
        powerFactorFromKVA = math.cos(math.atan(powerKVA/powerKW))
        if existingMultiplier > 1:
            powerFactorFromAdjust = .85 - (existingMultiplier-1)
        elif existingMultiplier < 1:
            powerFactorFromAdjust = (1-existingMultiplier + .85)
        demandCost = powerKW * ELECTRIC_DEMAND_COSTS
        costKVA = powerKVA * powerFactorKVACharge
        costKVAR = powerKVAR * powerFactorKVARCharge
        multiplierCostSavings = demandCost * (existingMultiplier -1)
        adjustmentCostSavings = demandCost * (existingAdjustment - 1)
        correctiveCapacitanceRequired = powerKVA * math.sin(math.acos(powerFactorFromKVA) - math.acos(minimumPFPenalty)) 
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

class VariableAirVolumeConversion(ECO):
    """
    """
    def __init__(self, binhours, OATemp):
        super().__init__(binhours, OATemp)

    def variableAirVolumeConversion(
        opHours, percentAirFlow, percentTimeAirFlow, fanExponent,
        supplyFanVolume, supplyFanHP, supplyFanEfficiency, 
        returnFanVolume, returnFanHP, returnFanEfficiency, 
        htgCoilEnterTemp, htgCoilLeavingtemp, 
        clgCoilEnterEnthalpy, clgCoilLeavingEnthalpy
        ):
        """
        """
        # Assumptions
        demandUseFactor = .80
        opMonthsPerYear = 12
        supplyFanLoadFactor = .70
        returnFanLoadFactor = .70
        # Throw error if > 8760
        totalHoursCooling = 2245
        totalHoursHeating = 5035
        totalHoursEquipmentOp = 7280
        percentTotalHoursClg = .35
        percentTotalHoursHtg = .30
        # Formula
        supplyFanPowerDraw = ((supplyFanHP * supplyFanLoadFactor * percentAirFlow**fanExponent) * .746 / supplyFanEfficiency) * totalHoursEquipmentOp * percentTimeAirFlow
        supplyFanDemand = ((supplyFanHP * supplyFanLoadFactor * percentAirFlow**fanExponent) * .746 / supplyFanEfficiency) * percentTimeAirFlow * demandUseFactor * opMonthsPerYear
        returnFanPowerDraw = ((returnFanHP * returnFanLoadFactor * percentAirFlow**fanExponent) * .746 / returnFanEfficiency) * totalHoursEquipmentOp * percentTimeAirFlow
        returnFanDemand = ((returnFanHP * returnFanLoadFactor * percentAirFlow**fanExponent) * .746 / returnFanEfficiency) * percentTimeAirFlow * demandUseFactor * opMonthsPerYear
        heatingLoad = (1.08 * supplyFanVolume * percentAirFlow * (htgCoilLeavingtemp - htgCoilEnterTemp) * opHours * percentTimeAirFlow * (totalHoursHeating / totalHoursEquipmentOp) * percentTotalHoursHtg) / 1000000
        coolingLoad = (4.5 * supplyFanVolume * percentAirFlow * (clgCoilLeavingEnthalpy - clgCoilEnterEnthalpy) * opHours * percentTimeAirFlow * (totalHoursCooling / totalHoursEquipmentOp) * percentTotalHoursClg) / 1000000
        # Results
        return

if __name__ == "__main__":
    # OAtemps = [39.9, 42, 44.1, 45.9, 47.1, 49, 50.9, 53, 54.9, 56.9, 58.9, 60.1, 62.3, 63.3, 64.2, 65.1, 65.9, 66.2, 67.4, 68.1, 69.9, 72.1, 74.1, 74.3]
    # binhours = [252, 211, 265, 284, 276, 431, 271, 139, 301, 390, 377, 289, 306, 309, 392, 208, 93, 166, 155, 146, 99, 53, 16, 14]
    fanSavings = DestratifyingFanSavings(2000, 80, 70, 75, 16, 200, 5000)
    fanSavings.setAssumptions()
    fanSavings.calcFanSavings(70) 