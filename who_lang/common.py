import math

def GalRad2MathDeg(radian):
    return radian/math.pi*180 - 90
def GalRad2MathRad(radian):
    return radian - math.pi/2
def MathRad2GalRad(radian):
    return SmallPosAngle(radian + math.pi/2)
def SmallPosAngle(radian):
    return (radian + math.pi*2) % (2*math.pi)