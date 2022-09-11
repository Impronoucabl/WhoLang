# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 11:34:12 2022

@author: natha
"""
import math
import config as cf

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
        ang_sep = 2*math.pi/len(syllables)
        curr_ang = 0
        for (k,v) in syllables.items():
            pos = gpos((curr_ang,self.radius),center=self.pos)
            self.children[k] = syl(v, cf.DEFAULT_LETTER_SIZE, pos, parent=self)
            curr_ang += ang_sep
        
    def expand_syl(self, *iterable, speed = 1):
        if len(iterable) > 0:
            looper = iterable[0]
        else:
            looper = self.children.values()
        for syll in looper:
            syll.set_radius(syll.prime.radius + speed, relative = False)
            syll.reset_dist()
    
    def collision_detect(self, *iterable):
        if len(iterable) > 0:
            looper = iterable[0]
        else:
            looper = self.children.values()
        for syl1 in looper:
            for syl2 in looper:
                if syl2 is syl1:
                    continue
                if syl1.pos.distance_to(syl2) < syl1.prime.max_radius() + syl2.prime.max_radius():
                    return True, syl1
        return False, None
    
    def explode_syl(self):
        count = 0
        if self.collision_detect()[0]:
            return
        while not self.collision_detect()[0]:
            self.expand_syl()
            if count > 500:
                print('explode_syl loop timed out')
                break
            count += 1
        'shrink by 1'
        self.expand_syl(speed = -1)
        return
    