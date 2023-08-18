import math

def GalRad2MathDeg(radian):
    return radian/math.pi*180 - 90
def GalRad2MathRad(radian):
    return radian - math.pi/2
def MathRad2GalRad(radian):
    return SmallPosAngle(radian + math.pi/2)
def SmallPosAngle(radian):
    return (radian + math.pi*2) % (2*math.pi)

vowels = tuple('aeiouAEIOU')
punc = tuple('.?!\'"-,;:')
PI = math.pi

cDict = {# (cType, feature Type, feature number)
    'b' : (1,0,0), #No features
    'j' : (2,0,0),
    't' : (3,0,0),
    'th': (4,0,0),
    'ch': (1,1,2), #Dots
    'k' : (2,1,2),
    'sh': (3,1,2),
    'y' : (4,1,2),
    'd' : (1,1,3),
    'l' : (2,1,3),
    'r' : (3,1,3),
    'z' : (4,1,3),
    'g' : (1,2,1), #Dashes
    'n' : (2,2,1),
    'v' : (3,2,1),
    'qu': (4,2,1),
    'h' : (1,2,2),
    'p' : (2,2,2),
    'w' : (3,2,2),
    'x' : (4,2,2),
    'f' : (1,2,3),
    'm' : (2,2,3),
    's' : (3,2,3),
    'ng': (4,2,3)
}
cDictVow = {
    'a' : (0,0,0), #vowels
    'e' : (0,0,0),
    'i' : (0,2,1),
    'o' : (0,0,0),
    'u' : (0,2,1)
}
cDictExt = {
    'ph': (2,1,1), #Extended alphabet
    'wh': (3,1,1),
    'gh': (4,1,1),
    'c' : (2,1,4),
    'q' : (4,1,4)
}