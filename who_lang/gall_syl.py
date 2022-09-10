from gall_cir import Gall_cir as cir
from gall_let import Gall_let as g_let
from gall_pos import Gall_pos as gpos
from gall_vow import Gall_vow as g_vow
from diction import Diction
import common as cm
import config as cf

class Gall_syl(cir):

    diction = Diction(letter_dict={**cm.cDict,**cm.cDictVow})    
    
    def next_syl(self):
        syl = False
        for v in self.parent.children.values():
            if syl:
                return v
            elif v is self:
                syl = True
                
    def reset_dist(self):
        if self.cType is None or self.cType[0] in (0,3,4):
            dist = self.parent.radius*cf.T_STEM_DIST_RATIO
        elif self.cType[0] == 1:
            dist = self.parent.radius - self.prime.radius - cf.B_STEM_GAP
        elif self.cType[0] == 2:
            dist = self.parent.radius - self.prime.radius - cf.J_STEM_GAP
        else:
            dist = self.parent.radius
        self.pos.set_pos(False,dist=dist)
        self.update()
        
                
    def spawn_letters(self):
        self.ltr_dict = self.diction.str_to_sylDict(self.text)
        self.children = []
        for i in self.ltr_dict.values():
            if i in cm.vowels:
                char = g_vow(i,
                             cf.DEFAULT_VOWEL_SIZE,
                             gpos((0,0), center=self.pos),
                             parent=self)
            else:
                char = g_let(i,self.radius,self.pos,parent=self)
            self.children.append(char)
        self.prime = self.children[0]
        self.cType = self.prime.cType
        self.reset_dist()   
                
    @staticmethod
    def spawn_syllables():
        return

    @staticmethod
    def add_ext():
        print('Warning: Adding extended characters cannot be undone')
        Gall_syl.diction.diction.update(cm.cDictExt)