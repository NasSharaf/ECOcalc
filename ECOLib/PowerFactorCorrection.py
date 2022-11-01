import math
from ECOMain import ECO, ELECTRIC_ENERGY_COSTS, ELECTRIC_DEMAND_COSTS

class PowerFactorCorrection(ECO):
    """
    """
    def __init__(self,
        powerKW,
        powerKVAR,
        powerKVA,
        powerFactorKVARCharge: float = .50,
        powerFactorKVACharge: float = .40,
    ):
        """
        Utilities charge customers for poor power factor since poor power factor 
        forces the utilities to provide more power than is actually needed by the
        facilities. Correcting this with capacitors can reduce the penalties accrued
        and lead to energy savings. 

        :param powerKW: year to date demand in KW off of utility bills
        :type powerKW: float

        :param powerKVAR: year to date KVAR off of utility bills
        :type powerKVAR: float

        :param powerKVA: year to date KVA off of utility bills
        :type powerKVA: float

        :param powerFactorKVARCharge: cost per KVAR
        :type powerFactorKVARCharge: float

        :param powerFactorKVACharge: cost per KVA
        :type powerFactorKVACharge: float
        """
        self.powerKW = powerKW
        self.powerKVAR = powerKVAR
        self.powerKVA = powerKVA
        self.powerFactorKVARCharge = powerFactorKVARCharge
        self.powerFactorKVACharge = powerFactorKVACharge

    def setAssumptions(self,
        powerFactorChargeType: str = "Multiplier",
        minimumPFPenalty: float = .90,
        proposedCorrection: float = .90,
        existingMultiplier: float = 1.10,
        existingAdjustment: float = 1.33,
    ):
        """
        Addiitonal assumptions that can be modified.

        :param powerFactorChargeType: method power factor penalties are charged. Either KVAR, KVA, Multiplier or adjustment
        :type powerFactorChargeType: str

        :param minimumPFPenalty: minimum power factor utilities requir before a penalty is accrued
        :type minimumPFPenalty: float

        :param proposedCorrection: corrected power factor that is required
        :type proposedCorrection: float

        :param existingMultiplier: multiplier on the utility bill
        :type existingMultiplier: float

        :param existingAdjustment: adjustment on the utility bill
        :type existingAdjustment: float
        """
        self.powerFactorChargeType = powerFactorChargeType
        self.minimumPFPenalty = minimumPFPenalty
        self.proposedCorrection = proposedCorrection
        self.existingMultiplier = existingMultiplier
        self.existingAdjustment = existingAdjustment

    def calcCorrection(self):
        """
        Calculates and returns 
        """
        powerFactorFromKVA = math.sin(math.atan(self.powerKVAR/self.powerKW))
        powerFactorFromMultiplier = (1/self.existingMultiplier)
        powerFactorFromRKVA = math.cos(math.atan(self.powerKVA/self.powerKW))
        if self.existingMultiplier > 1:
            powerFactorFromAdjust = .85 - (self.existingMultiplier-1)
        elif self.existingMultiplier < 1:
            powerFactorFromAdjust = (1-self.existingMultiplier + .85)
        demandCost = self.powerKW * ELECTRIC_DEMAND_COSTS
        costKVA = self.powerKVA * self.powerFactorKVACharge
        costKVAR = self.powerKVAR * self.powerFactorKVARCharge
        multiplierCostSavings = demandCost * (self.existingMultiplier -1)
        adjustmentCostSavings = demandCost * (self.existingAdjustment - 1)
        correctiveCapacitanceRequired = self.powerKVA * math.sin(math.acos(powerFactorFromKVA) - math.acos(self.minimumPFPenalty)) 
        # Results
        if self.powerFactorChargeType == "Multiplier":
            return costKVA
        elif self.powerFactorChargeType == "KVAR":
            return costKVAR
        elif self.powerFactorChargeType == "KVA":
            return multiplierCostSavings
        elif self.powerFactorChargeType == "Adjustment":
            return adjustmentCostSavings