from gall_cir import Gall_cir as cir
import common as cm

class Gall_let(cir):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text=self.text.lower()
        self.cType = self._get_cType(self.text)
    
    @staticmethod
    def _get_cType(text, cdict = {**cm.cDict,**cm.cDictVow, **cm.cDictExt}):
        return cdict[text]
    
    def spawn_letters(self):
        return

    def spawn_nodes(self):
        'TODO'
        return

    def set_radius(self, radius, relative=False):
        old = self.radius
        super().set_radius(radius, relative)
        ratio = self.radius/old
        for n in self.children:
            n.pos.set_pos(True, dist=ratio)
