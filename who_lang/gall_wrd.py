# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:34:12 2022

@author: natha
"""
import math

from gall_cir import Gall_cir as cir
from gall_syl import Gall_syl as syl
from gall_pos import Gall_pos as gpos
from diction import Diction

class G_word(cir):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'diction' not in kwargs:
            self.diction = Diction()
    
    def spawn_syllables(self):
        self.children == {}
        syllables = self.diction.str_to_sylDict(self.text)
        radius = 100
        ang_sep = 2*math.pi/len(syllables)
        curr_ang = 0
        for (k,v) in syllables.items():
            pos = gpos((curr_ang,200),center=self.pos)
            self.children[k] = syl(v, radius, pos, parent=self)
            curr_ang += ang_sep
        
    