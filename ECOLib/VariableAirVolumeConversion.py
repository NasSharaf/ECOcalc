from ECOMain import ECO

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