'Co-ordinate system for the entire library. Angles start at the bottom of circles & rotate counterclockwise'

'Positions at 0 distance have undefined angle.'

import math
import common as cm

''' 
self.abs_x & self.abs_y are absolute units - The global cartesian co-ordinates
self.x & self.y are relative absolute units - The cartesian coordinates with the origin at self.center
self.angle & self.distance are radial units - The radial coordinates with the origin at self.center
'''

class Gall_pos():
    'If no center is given, assume the natural origin is the center'
    'Generally, we should avoid referencing this class variable, unless the position was defined by absolut units only.'
    center = (0,0)

    def __len__():
        return 2

    '''
    Construct the position object. Keyword arguments take priority over optional arguements.
    '''

    def __init__(self, *args, **kwargs) -> None:
        if 'pos_type' in kwargs:
            pos_type = kwargs['pos_type']
        elif args[1] is not None:
            pos_type = args[1]
        elif isinstance(args[0], str):
            pos_type = args[0]
        else:
            pos_type = 'radial'

        if args[0] is not None:
            if isinstance(args[0], dict):
                args[0].update(kwargs)
                kwargs = args[0]
            else:
                coords = args[0]
                if len(coords) != 2:
                    raise LookupError('Invalid Co-ordinate length')
                if pos_type == 'absolute':
                    self.abs_x, self.abs_y = coords
                    self._reset_from_abs()
                else:
                    if 'center' not in kwargs:
                        'Radial positions are always relative.'
                        raise LookupError('Missing center argument for relative coords')
                    else:
                        self.center = kwargs['center']
                        if pos_type == 'rel_abs':
                            self.x, self.y = coords
                            self._set_rad_pos()
                            self._set_abs_pos()
                        elif pos_type == 'radial':
                            self.angle, self.distance = coords
                            self._set_rel_abs_pos()
                            self._set_abs_pos()
                        else:
                            raise TypeError('Bad pos_type given')

        self._parse_kw(False, **kwargs)
        if None not in (self.abs_x, self.abs_y):
            self._reset_from_abs()
        else:
            if self.center == (0,0):
                raise SyntaxError('Center unspecified without absolute units')
            elif None not in (self.x, self.y):
                self._set_rad_pos()
            elif None not in (self.angle, self.distance):
                self._set_rel_abs_pos()
            else:
                raise IndexError('Insufficient data to constrain position')
            self._set_abs_pos()

    def angle_to(self, other, MathAng = False):
        ang = math.atan2(self.Y_to(other),self.X_to(other))
        if MathAng:
            return ang
        else:
            return cm.MathRad2GalRad(ang)

    def distance_to(self, other, square = False):
        sq = self.Y_to(other)**2 + self.X_to(other)**2
        if square:
            return sq
        else:
            return math.sqrt(sq)
    
    def _parse_kw(self, relative, **kwargs):
        for kw in kwargs:
            if isinstance(kwargs[kw], (int, float)):
                if kw in ('x', 'X', 'rel_x', 'rel_X'):
                    if relative:
                        self.x *= kwargs[kw]
                    else:
                        self.x = kwargs[kw]
                elif kw in ('y', 'Y', 'rel_y', 'rel_Y'):
                    if relative:
                        self.y *= kwargs[kw]
                    else:
                        self.y = kwargs[kw]
                elif kw in ('abs_x', 'abs_X'):
                    self.abs_x = kwargs[kw]
                elif kw in ('abs_y', 'abs_Y'):
                    self.abs_y = kwargs[kw]
                elif kw in ('ang', 'Ang', 'angle', 'Angle'):
                    if relative:
                        self.angle += kwargs[kw]
                    else:
                        self.angle = kwargs[kw]
                elif kw in ('d', 'dist', 'Dist', 'distance', 'Distance'):
                    if relative:
                        self.distance *= kwargs[kw]
                    else:
                        self.distance = kwargs[kw]
                else:
                    print(f"Warning: Value {kw} = {kwargs[kw]} was ignored.")
            elif kw in ('center'):
                self.center = kwargs[kw]
            elif kw in ('circle'):
                self.circle = kwargs[kw]
            else:
                print(f"Warning: Keyword {kw} = {kwargs[kw]} was ignored.")

    def set_pos(self, relative, **kwargs):
        self._parse_kw(relative, **kwargs)
        if 'abs_x' in kwargs or 'abs_y' in kwargs:
            self._reset_from_abs()
        else:
            rel = False
            for rel_abs in ('x', 'X', 'rel_x', 'rel_X', 'y', 'Y', 'rel_y', 'rel_Y'):
                if rel_abs in kwargs:
                    self._set_rad_pos()
                    rel = True
                    break
            if not rel:
                for radial in ('ang', 'Ang', 'angle', 'Angle', 'd', 'dist', 'Dist', 'distance', 'Distance'):
                    if radial in kwargs:
                        self._set_rel_abs_pos()
                        break
            self._set_abs_pos()

    def update(self):
        self._set_abs_pos()

    def X_to(self, other):
        if isinstance(other,Gall_pos):
            X2 = other.abs_x
        elif isinstance(other.pos, Gall_pos):
            X2 = other.pos.abs_x
        elif isinstance(other,(list, tuple)):
            if len(other) != 2:
                raise LookupError('Sequential is too large')
            else:
                X2 = other[0]
        elif isinstance(other,(int, float)):
            X2 = other
        else:
            raise TypeError('Invalid type given')
        return X2 - self.abs_x

    def Y_to(self, other):
        if isinstance(other,Gall_pos):
            Y2 = other.abs_y
        elif isinstance(other.pos, Gall_pos):
            Y2 = other.pos.abs_y
        elif isinstance(other,(list, tuple)):
            if len(other) != 2:
                raise LookupError('Sequential is too large')
            else:
                Y2 = other[-1]
        elif isinstance(other,(int, float)):
            Y2 = other
        else:
            raise TypeError('Invalid type given')
        return Y2 - self.abs_y

    def _reset_from_abs(self):
        'overwrite x,y & ang,d based on abs_pos'
        if isinstance(self.center, Gall_pos):
            x_offset = self.center.abs_x
            y_offset = self.center.abs_y
        elif isinstance(self.center, (list,tuple)):
            x_offset = self.center[0]
            y_offset = self.center[1]
        else:
            raise TypeError('Center is not a list, tuple or Gall_pos')
        self.x = self.abs_x - x_offset
        self.y = self.abs_y - y_offset
        self._set_rad_pos()

    def _set_abs_pos(self):
        'overwrite abs_pos based on x,y'
        if isinstance(self.center, Gall_pos):
            self.abs_x = self.center.abs_x + self.x
            self.abs_y = self.center.abs_y + self.y
        elif isinstance(self.center, (list,tuple)):
            self.abs_x = self.center[0] + self.x
            self.abs_y = self.center[1] + self.y
        else:
            raise TypeError('Center is not a list, tuple or Gall_pos')
    
    def _set_rad_pos(self):
        'overwrite ang,d based on x,y'
        self.angle = cm.MathRad2GalRad(math.atan2(self.y, self.x))
        self.distance = math.sqrt(self.y**2 + self.x**2)

    def _set_rel_abs_pos(self):
        'overwrite x,y based on (ang,d)'
        self.x = self.distance*math.cos(cm.GalRad2MathRad(self.angle))
        self.y = self.distance*math.sin(cm.GalRad2MathRad(self.angle))