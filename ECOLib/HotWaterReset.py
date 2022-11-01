from ECOMain import ECO, ELECTRIC_ENERGY_COSTS

class HotWaterReset(ECO):
    """
    Similar to chilled water reset, gradually reset the water temperature in the boiler 
    as the heaitng load increases. the lower the heating load, the less warm the water from
    the boiler needs to be. 

    :param binhour: number of hours per year at a given temperature range
    :type binhour: int

    :param OAtemp: The outside air temperature at the given bin hour
    :type OAtemp: float

    :param boilerPeakLoad: 100% load for the boiler, assume 30 btu/sq-ft
    :type boilerPeakLoad: int

    :param boilerEfficency: efficiency of the boiler plant
    :type boilerEfficency: float

    :param designHotWaterSupplyTemp: input design or maximum hot water supply temperature
    :type designHotWaterSupplyTemp: float

    :param designIndoorAirTemp: input design temperature of indoor air during the heating season
    :type designIndoorAirTemp: float

    :param hotWaterReset: amount to reset hot water temperature by (limit to 60 degF)
    :type hotWaterReset: float

    :param minimumBoilerLoad: minmum firing rate of the boiler before it turns off
    :type minimumBoilerLoad: int
    """
    def __init__(self, binhours, OATemp,
        boilerPeakLoad: int = 8050000,  # btu/hr
        boilerEfficency: float = .80, 
        designHotWaterSupplyTemp: float = 180, # degF
        designIndoorAirTemp: float = 68, # degF
        designOutdoorAirTemp: float = -2.5, # degF
        hotWaterReset: float = 50,  #degF 
        minimumBoilerLoad: int = 1000000, # btu/hr
    ):
        super().__init__(binhours, OATemp)
        self.boilerPeakLoad = boilerPeakLoad
        self.boilerEfficency = boilerEfficency
        self.designHotWaterSupplyTemp = designHotWaterSupplyTemp
        self.designIndoorAirTemp = designIndoorAirTemp
        self.designOutdoorAirTemp = designOutdoorAirTemp
        self.hotWaterReset = hotWaterReset
        self.minimumBoilerLoad = minimumBoilerLoad

    def setAssumptions(self,
        resetFactor: float = .08,
        heatingSeasonInitiate: float = 70, # degF
    ):
        """
        Addiitonal assumptions that can be modified.

        :param resetFactor: industry rule of thumb, if design hot water is above 180, use 0.14 else use .08
        :type resetFactor: float

        :param heatingSeasonInitiate: at what temperature the boiler turns on
        :type heatingSeasonInitiate: float
        """
        if self.designHotWaterSupplyTemp > 180:
            self.resetFactor = 0.14
        else:
            self.resetFactor = 0.08
        self.heatingSeasonInitiate = heatingSeasonInitiate

    def calculateReset(self):
        """ 
        Calculates hot water reset savings for every OA Temperature and bin hour
        """
        for (binhour, OAtemp) in zip(self.OATemp, self.binhours):
            
            # Formula
            hotWaterSupplyTemp = self.designIndoorAirTemp + (self.designHotWaterSupplyTemp - self.designIndoorAirTemp)/((self.designIndoorAirTemp - self.designOutdoorAirTemp) * (self.designIndoorAirTemp - OAtemp))
            if OAtemp < self.heatingSeasonInitiate:
                buildingLoad = self.boilerPeakLoad * ((OAtemp - self.heatingSeasonInitiate)/(self.designOutdoorAirTemp - self.heatingSeasonInitiate))
                if buildingLoad > self.minimumBoilerLoad:
                    boilerLoad = buildingLoad
                else:
                    boilerLoad = self.minimumBoilerLoad
            else:
                boilerLoad = 0
            energyUse = ((boilerLoad * binhour) /self.boilerEfficency)/1000000
            resetPotential = (self.boilerPeakLoad - boilerLoad)/self.boilerPeakLoad
            resetTemp = resetPotential * self.hotWaterReset
            energySavings = (boilerLoad * binhour * self.resetFactor * (resetTemp / 40)) / 1000000
            energyCost = energySavings * ELECTRIC_ENERGY_COSTS
            # Results
            print(energySavings)