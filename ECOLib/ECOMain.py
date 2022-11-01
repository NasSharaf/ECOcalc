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