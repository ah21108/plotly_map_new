import unittest
import math_calcs

class TestMath(unittest.TestCase):
    
    def test_haversine(self):
        self.assertEquals(round(math_calcs.haversine(0,0,45,45),1),6671.7)
        self.assertEquals(round(math_calcs.haversine(0,0,-45,-45),1),6671.7)
        self.assertEquals(round(math_calcs.haversine(0,90,45,45),1),5003.8)
        self.assertEquals(round(math_calcs.haversine(-45,-45,45,45),1),13343.4)
        self.assertEquals(round(math_calcs.haversine(10,20,-45,45),1),5722.9)
        # self.assertEquals(round(math_calcs.haversine(0,0,-45,-45),1),6671.7)
        # self.assertEquals(round(math_calcs.haversine(0,90,45,45),1),13343.4)
        # self.assertEquals(round(math_calcs.haversine(-45,-45,45,45),1),13343.4)


if __name__ == '__main__':
    unittest.main()