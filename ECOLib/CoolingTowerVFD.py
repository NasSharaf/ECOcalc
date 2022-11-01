from ECOMain import ECO, ELECTRIC_ENERGY_COSTS

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