from gall_cir import Gall_cir as cir
from gall_let import Gall_let as g_let
from diction import Diction
import common as cm

class Gall_syl(cir):

    diction = Diction(letter_dict={**cm.cDict,**cm.cDictVow})        

    def spawn_letters(self):
        self.ltr_dict = self.diction.str_to_sylDict(self.text)
        self.children = []
        for i in self.ltr_dict.values():
            radius = 20
            self.children.append(g_let(i,radius,self.pos,parent=self))

    def next_syl(self):
        syl = False
        for v in self.parent.children.values():
            if syl:
                return v
            elif v is self:
                syl = True
                
    @staticmethod
    def spawn_syllables():
        return

    @staticmethod
    def add_ext():
        print('Warning: Adding extended characters cannot be undone')
        Gall_syl.diction.diction.update(cm.cDictExt)