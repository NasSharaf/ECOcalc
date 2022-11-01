from ECOMain import ECO, ELECTRIC_ENERGY_COSTS, ELECTRIC_DEMAND_COSTS

class EnergyEfficientMotorReplacement(ECO):
    """
    Replace an existing motor with a more energy efficient motor. 

    :param motorSize: Size of the existing motor in horsepower
    :type motorSize: int

    :param motorEfficiency: Efficiency of the existing motor, measured or off of nameplate
    :type motorEfficiency: float

    :param motorVoltage: Voltage of the existing motor in volts, measured or off of nameplate
    :type motorVoltage: int

    :param loadRPM: load of the existing motor in recolutions per minute (RPM), measured or off of nameplate
    :type loadRPM: float

    :param hoursOfUse: hours existing motor is active per year
    :type hoursOfUse: int 

    :param newMotorSize: Size of the new motor in horsepower
    :type motorSize: int

    :param newMotorEfficiency: Efficiency of the new motor, measured or off of nameplate
    :type motorEfficiency: float

    :param newMotorVoltage: Voltage of the new motor in volts, measured or off of nameplate
    :type motorVoltage: int

    :param newLoadRPM: load of the new motor in recolutions per minute (RPM), measured or off of nameplate
    :type loadRPM: float

    :param newHoursOfUse: hours new motor is active per year
    :type hoursOfUse: int 
    """
    def __init__(self,
        motorSize: int, 
        motorEfficiency: float, 
        motorVoltage: int, 
        loadRPM: float, 
        hoursOfUse: int,
        motorKW: float,
        newMotorSize: int, 
        newMotorEfficiency: float, 
        newMotorVoltage: int, 
        newLoadRPM: float, 
        newHoursOfUse: int,
        newMotorKW: float
    ):
        self.motorSize = motorSize
        self.motorEfficiency = motorEfficiency
        self.motorVoltage = motorVoltage
        self.loadRPM = loadRPM
        self.hoursOfUse = hoursOfUse
        self.motorKW = motorKW
        self.newMotorSize = newMotorSize
        self.newMotorEfficiency = newMotorEfficiency
        self.newMotorVoltage = newMotorVoltage
        self.newLoadRPM = newLoadRPM
        self.newHoursOfUse = newHoursOfUse
        self.newMotorKW = newMotorKW

    def setAssumptions(self,
        existingMotorLoadFactor:float = .75,
        newMotorLoadFactor: float = .75,
        powerFactor:float = .85,
        demandUseFactor:float = .80,
        peakLoadMonths:int = 6
    ):
        """
        Addiitonal assumptions that can be modified.

        :param existingMotorLoadFactor: average load the existing motor runs as a percentage of the full load per year (assumed 75%)
        :type existingMotorLoadFactor: float

        :param newMotorLoadFactor: average load the new motor will run as a percentage of the full load per year (assumed 75%)
        :type newMotorLoadFactor: float

        :param powerFactor: ratio of Real power (kW) to apparent power (kVA)
        :type powerFactor: float

        :param demandUseFactor: percentage of motor use (kW) that will most affect electric billed demand
        :type demandUseFactor: float

        :param peakLoadMonths: months of operation that will most affect electric billed demand
        :type peakLoadMonths: int
        """
        self.existingMotorLoadFactor = existingMotorLoadFactor
        self.newMotorLoadFactor = newMotorLoadFactor
        self.powerFactor = powerFactor
        self.demandUseFactor = demandUseFactor
        self.peakLoadMonths = peakLoadMonths

    def calcReplacementSavings(self):
        """
        Calculates savings from replacing motor with newer energy efficient motor
        """
        motorKW = self.motorSize * .746 * self.existingMotorLoadFactor
        newMotorKW = self.newMotorSize * .746 * self.existingMotorLoadFactor
        speedRatioCorrFactor = (self.newLoadRPM/self.loadRPM)**3
        existingEnergyUse = motorKW/self.motorEfficiency * self.hoursOfUse
        existingDemandUse = motorKW/self.motorEfficiency * self.peakLoadMonths * self.demandUseFactor
        newEnergyUse = newMotorKW/self.newMotorEfficiency * self.newHoursOfUse
        newDemandUse = newMotorKW/self.newMotorEfficiency * self.peakLoadMonths * self.demandUseFactor * speedRatioCorrFactor
        # Results
        energySavings = self.compare(existingEnergyUse, newEnergyUse)
        energyUseSavings = self.compareCosts(existingEnergyUse, newEnergyUse, ELECTRIC_ENERGY_COSTS)
        energyDemandSavings = self.compareCosts(existingDemandUse, newDemandUse, ELECTRIC_DEMAND_COSTS)
        totalSavings = energyUseSavings + energyDemandSavings
        return totalSavings