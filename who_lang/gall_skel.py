# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 00:18:41 2022

@author: natha
"""

import math
import custom as cus

from gall_cir import Gall_cir as cir 
from gall_pos import Gall_pos as gpos
from gall_wrd import G_word

class Gall_skel(cir):
    
    pair = None
    pair_lst = None
    mode = 'radial'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrd_lst = self.text.split()
    
    def spawn_words(self):
        self.children = []
        angle = ang_sep = 0
        distance = 0
        radius = self.radius
        if self.mode == 'radial':
            ang_sep = math.pi*2/len(self.wrd_lst)
            if len(self.wrd_lst) > 1:
                distance = 2/3*self.radius
                radius *= 1/3
        elif self.mode == 'absolute':
            ang_sep = 2*self.radius
            angle = distance = self.radius
        for wrd in self.wrd_lst:
            pos = gpos((angle,distance), center=self.pos)
            angle += ang_sep
            self.children.append(G_word(wrd, radius, pos, parent=self, pos_type=self.mode))
            
    def node_prep(self):
        'put all custom pairing funcs here'
        cus.node_pair(self.nodes)
        
        'remaining unpaired nodes are rendered as rays.'
        unpaired = False
        for nodes in self.nodes:
            if not nodes.visible:
                nodes.visible = True
                unpaired = True
        if unpaired:
            'Warning: Some nodes were left unpaired'