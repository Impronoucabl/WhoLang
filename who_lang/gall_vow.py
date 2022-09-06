# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 22:11:34 2022

@author: natha
"""
import math
import common as cm
import config as cf

from gall_let import Gall_let as g_let

class Gall_vow(g_let):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_pos()
        
    def reset_pos(self):
        if self.text == 'a':
            self.rel_ang = 0
            angle = self.parent.pos.angle
            dist = cf.DEFAULT_A_GAP + self.parent.parent.radius - self.parent.pos.distance
            self.pos.set_pos(False, ang=angle, dist=dist)
        elif self.text == 'o':
            self.rel_ang = math.pi
            angle = cm.SmallPosAngle(self.parent.pos.angle + math.pi)
            dist = self.parent.radius
        else:
            angle = 0
            dist = 0
        self.pos.set_pos(False, ang=angle, dist=dist)
        
    def update(self):
        if self.pos.distance != 0:
            angle = cm.SmallPosAngle(self.parent.pos.angle + self.rel_ang)
            self.pos.set_pos(False, ang=angle)
        super().update()
                
            