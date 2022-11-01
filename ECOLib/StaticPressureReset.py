from ECOMain import ECO, ELECTRIC_ENERGY_COSTS, ELECTRIC_DEMAND_COSTS

class StaticPressureReset(ECO):
    """
    Fan system pressure reduction to new static pressure setpoint

    :param sysPressure: Existing pressure in either supply or exhaust in inches water column
    :type sysPressure: float

    :param newSysPressure: New pressure in either supply or exhaust in inches water column
    :type sysPressure: float

    :param fanEfficiency: Existing efficiency of either the supply or exhaust fan. Fan efficiency vary with operating points, refer to fan curves
    :type fanEfficiency: float

    :param motorEfficiency: Existing efficiency of the motor of the fan
    :type motorEfficiency: float    

    :param fanVolume: Volume of air supplied in cubic feet per minute (CFM)
    :type fanVolume: float   

    :param newFanVolume: Proposed volume of air to be supplied in cubic feet per minute (CFM)
    :type newFanVolume: float 

    :param hoursOfUse: Hours of operation of the fan
    :type hoursOfUse: float     
    """
    def __init__(self,
    sysPressure: float, 
    newSysPressure: float, 
    fanEfficiency: float, 
    motorEfficiency: float, 
    fanVolume: float, 
    newFanVolume: float, 
    hoursOfUse: int
    ):
        self.sysPressure = sysPressure
        self.newSysPressure = newSysPressure
        self.fanEfficiency = fanEfficiency
        self.motorEfficiency = motorEfficiency
        self.fanVolume = fanVolume
        self.newFanVolume = newFanVolume
        self.hoursOfUse = hoursOfUse

    def calcPressureReduction(self):
        """
        Calculates fan system pressure reduction to new static pressure setpoint
        """
        # Formula
        fanBHP = (self.fanVolume * self.sysPressure)/(6356 * self.fanEfficiency)
        newFanBHP = (self.newFanVolume * self.newSysPressure)/(6356 * self.fanEfficiency)
        fanEnergyUse = fanBHP * .746 * self.hoursOfUse / self.motorEfficiency
        fanDemandUse = fanBHP * .746 / self.motorEfficiency
        newEnergyUse = newFanBHP * .746 * self.hoursOfUse / self.motorEfficiency
        newDemandUse = newFanBHP * .746 / self.motorEfficiency
        # Results
        energyUseSavings = (fanEnergyUse - newEnergyUse) * ELECTRIC_ENERGY_COSTS 
        energyDemandSavings = (fanDemandUse - newDemandUse) * ELECTRIC_DEMAND_COSTS * 12
        totalSavings = energyUseSavings + energyDemandSavings
        return totalSavings