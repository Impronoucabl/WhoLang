# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 22:02:17 2022

@author: natha
"""

from gall_pos import Gall_pos as gpos

class G_node():
    
    visible = False
    id_count = 0
    radius = 0
    pair = None
    pair_lst = None
    
    def __init__(self, pos, parent, *args):
        if isinstance(pos, gpos):
            self.pos = pos
        else:
            raise TypeError('Invalid pos type')
        self.parent = parent
        self.n_id = (G_node.id_count,)
        G_node.id_count += 1
        
    def __hash__(self):
        return hash(self.n_id)
        
    def __eq__(self, other):
        return (self.pos == other.pos and self.radius == other.radius)
    
    def ang_check(self, angle = None):
        if angle is None:
            angle = self.pos.angle
        if self.parent is None:
            return True
        elif self.parent.allowed_ang is None:
            return True
        elif any([ang[0] < angle < ang[1] for ang in self.parent.allowed_ang]):
            return True
        else:
            return False
        
    def pair_to(self, other):
        self.pair = other
        angle = self.parent.pos.angle_to(other.pos.center)
        self.pos.set_pos(False, ang=angle)
        self.visible = True
    
    