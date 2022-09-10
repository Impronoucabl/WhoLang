# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 00:18:41 2022

@author: natha
"""

from gall_cir import Gall_cir as cir 
from gall_pos import Gall_pos as gpos
from gall_wrd import G_word

class Gall_skel(cir):
    
    pair = None
    pair_lst = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wrd_lst = self.text.split()
    
    def spawn_words(self):
        self.children = []
        for wrd in self.wrd_lst:
            self.children.append(G_word(wrd, self.radius, gpos((0,0), center=self.pos), parent=self))
            
    def node_prep(self):
        pass
        
    def node_done(self):
        for nodes in self.nodes:
            if not nodes.visible:
                'TODO: check node is within min & max angles'
                nodes.visible = True