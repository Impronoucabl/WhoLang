#import math
#import common as cm
import gall_pos.Gall_pos as gpos


class Gall_cir():
    
    children = None
    parent = None
    thickness = 5
    
    def __init__(self, text, radius, pos, **kwargs):
        
        self.children = {}
        for kw in kwargs:
            if kw == 'children':
                self.children = kwargs[kw]
            elif kw == 'parent':
                if isinstance(kwargs[kw], Gall_cir):
                    self.parent = kwargs[kw]
                else:
                    raise TypeError('Parent is not a Gall_cir') 
            if kw == 'thickness':
                if isinstance(kwargs[kw], (int,float)):
                    self.thickness = kwargs[kw]
                else:
                    print('Warning: Thickness given was ignored')
                
        if isinstance(text, str):
            self.text = text
        else: 
            raise TypeError('Invalid text to construct circle')
            
        if isinstance(pos, gpos) or pos == (0,0):
            self.pos = pos
        elif self.parent is not None:
            if isinstance(pos, (list,tuple)) and len(pos) == 2:
                self.pos = gpos(pos, center=self.parent, circle=self, **kwargs)
            elif pos is None:
                self.pos = gpos(center=self.parent, circle=self, **kwargs)
            else:
                raise TypeError('Invalid pos to construct circle')
        else:
            raise SyntaxError('Invalid pos without center')
            
        if isinstance(radius, (int,float)):
            self.radius = radius
        else:
            raise TypeError('Invalid radius to construct circle)')
            
    def set_radius(self, radius, relative = False):
        if relative:
            self.radius *= radius
        else:
            self.radius = radius
    
    def dist_between(self, other):
        total = self.pos.distance_to(other)
        if isinstance(other, Gall_cir):
            oth_rad = other.radius
        else:
            oth_rad = 0
        return  total - self.radius - oth_rad
        
        
        
