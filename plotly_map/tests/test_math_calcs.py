import math_calcs

def test_haversine():
    assert round(math_calcs.haversine(0,0,45,45),1) == 6671.7
    assert round(math_calcs.haversine(0,0,-45,-45),1) == 6671.7
    assert round(math_calcs.haversine(0,90,45,45),1) == 5003.8
    assert round(math_calcs.haversine(-45,-45,45,45),1) == 13343.4
    assert round(math_calcs.haversine(10,20,-45,45),1) == 5722.9

