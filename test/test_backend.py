import unittest
from api import calculate_base_insurance_charge, calculate_insurance_premium_tax, calculate_final_insurance_charge

class TestInsuranceCalculator(unittest.TestCase):
    def test_uk_insurance_base_price(self): # 1%
        # Insurance charge is less than £9, so it result should be 9
        self.assertEqual(calculate_base_insurance_charge(15, 'United Kingdom'),9) 
        # Package value below is 25,000, so insurance charge should be £25
        self.assertEqual(calculate_base_insurance_charge(2500, 'United Kingdom'),25)

    def test_france_germany_netherlands_belgium_insurance_base_price(self): # 1.5%
        # Insurance charge is less than £9, so it result should be 9
        self.assertEqual(calculate_base_insurance_charge(15, 'Germany'),9)
        # Package value below is 25,000, so insurance charge should be £37.5
        self.assertEqual(calculate_base_insurance_charge(2500, 'Germany'),37.5)

    def test_other_country_insurance_base_price(self): # 4%
        # Insurance charge is less than £9, so it result should be 9
        self.assertEqual(calculate_base_insurance_charge(15, 'Japan'),9)
        # Package value below is 25,000, so insurance charge should be £100
        self.assertEqual(calculate_base_insurance_charge(2500, 'Japan'),100)

    def test_calculate_insurance_premium_tax(self): # 12.5% 
        # Insurance premium tax on 9 should be 1.125
        self.assertEqual(calculate_insurance_premium_tax(9),1.125)
        # Insurance premium tax on 100 should be 12.5
        self.assertEqual(calculate_insurance_premium_tax(100),12.5)

    def calculate_final_insurance_charge(self): # base_insurance_charge + insurance_prenium_tax
        # Insurance premium tax on 9 should be 1.125
        self.assertEqual(calculate_final_insurance_charge(9,1.125),10.125)
        # Insurance premium tax on 100 should be 12.5
        self.assertEqual(calculate_final_insurance_charge(100, 12.5),112.5)

if __name__ == '__main__':
    unittest.main()
