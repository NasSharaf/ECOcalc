from ECOMain import ECO, ELECTRIC_ENERGY_COSTS, HEATING_ENERGY_COST

class DestratifyingFan(ECO):
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