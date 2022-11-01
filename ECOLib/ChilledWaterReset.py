from ECOMain import ECO, ELECTRIC_ENERGY_COSTS

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
        Calculates Chilled water reset savings over all OA Temperatures and binhours
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