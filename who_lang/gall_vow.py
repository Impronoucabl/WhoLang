# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 22:11:34 2022

@author: natha
"""

import common as cm
import config as cf

from gall_let import Gall_let as g_let

class Gall_vow(g_let):
    
    thickness = cf.DEFAULT_VOWEL_THICK
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_pos()
        
    def reset_pos(self):
        if self.text == 'a':
            self.rel_ang = 0
            angle = self.parent.pos.angle
            dist = cf.DEFAULT_A_GAP + self.parent.parent.radius - self.parent.pos.distance
        elif self.text == 'o':
            self.rel_ang = cm.PI
            angle = cm.SmallPosAngle(self.parent.pos.angle + cm.PI)
            dist = self.parent.radius
        else:
            angle = 0
            dist = 0
        self.pos.set_pos(False, ang=angle, dist=dist)
        
    def set_to_rel_ang(self):
        self.pos.set_pos(False, ang=cm.SmallPosAngle(self.parent.pos.angle + self.rel_ang))
    
    def _get_lett_angle(self):
        if self.text == 'i':
            self.lett_min_angle = self.rel_to_real_ang(cm.PI/2)
            self.lett_max_angle = self.rel_to_real_ang(-cm.PI/2)
        elif self.text == 'u':
            self.lett_min_angle = self.rel_to_real_ang(-cm.PI/2)
            self.lett_max_angle = self.rel_to_real_ang(cm.PI/2)
        else:
            self.lett_max_angle = cm.PI*2
            self.lett_min_angle = 0
            self.half_angle_size = cm.PI
            self.allowed_ang = [(0,cm.PI*2)]
            return
        self.half_angle_size = cm.PI/2
        if self.lett_min_angle  > self.lett_max_angle:
            self.allowed_ang = [(0, self.lett_max_angle),(self.lett_min_angle, cm.PI*2)]
        else:
            self.allowed_ang = [(self.lett_min_angle, self.lett_max_angle)]
    
    def update(self):
        if self.pos.distance != 0:
            self.reset_pos()
            self.set_to_rel_ang()
        super().update()
                
            