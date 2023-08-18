from gall_cir import Gall_cir as cir
from gall_node import G_node
from gall_pos import Gall_pos as gpos
import custom as cus
import common as cm
import config as cf

class Gall_let(cir):
    
    thickness = cf.DEFAULT_LETTER_THICK
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text=self.text.lower()
        self.cType = self._get_cType(self.text)
        self._get_lett_angle()
    
    @staticmethod
    def _get_cType(text, cdict = {**cm.cDict,**cm.cDictVow, **cm.cDictExt}):
        return cdict[text]
    
    def _get_lett_angle(self):
        if self.cType[0] % 2 == 0:
            self.lett_max_angle = cm.PI*2
            self.lett_min_angle = 0
            self.half_angle_size = cm.PI
            self.allowed_ang = [(0,cm.PI*2)]
            return
        
        self.half_angle_size = abs(self.parent.parent.pos.distance**2-self.parent.pos.distance**2-self.radius**2)/(2*self.radius*self.parent.pos.distance)
        self.lett_min_angle = self.rel_to_real_ang(self.half_angle_size)
        self.lett_max_angle = self.rel_to_real_ang(-self.half_angle_size)
        
        if self.lett_min_angle  > self.lett_max_angle:
            self.allowed_ang = [(0, self.lett_max_angle),(self.lett_min_angle, cm.PI*2)]
        else:
            self.allowed_ang = [(self.lett_min_angle, self.lett_max_angle)]
    
    def rel_to_real_ang(self, angle):
        return cm.SmallPosAngle(angle + self.pos.angle)
    
    def real_to_rel_ang(self, angle):
        raw = angle - self.pos.angle
        if raw < -cm.PI:
            return raw + cm.PI*2
        else:
            raw = raw % (cm.PI*2)
            return raw % cm.PI
    
    def spawn_letters(self):
        return

    def spawn_nodes(self):
        if self.cType[2] > 0:
            ang_lst = iter(cus.dot_spread(self.cType, self.lett_min_angle, self.lett_max_angle))
            if self.cType[1] == 2:
                for _ in range(self.cType[2]):
                    self.nodes.add(G_node(
                        gpos((self.rel_to_real_ang(next(ang_lst)),self.radius),center=self.pos),
                        parent = self
                        ))
            else:
                self.children = []
                for _ in range(self.cType[2]):
                    self.children.append(cir(
                        "",
                        cf.DEFAULT_DOT_SIZE,
                        gpos((self.rel_to_real_ang(next(ang_lst)),self.radius),center=self.pos),
                        parent = self
                        ))
        return

    def set_radius(self, radius, relative=False):
        old = self.radius
        super().set_radius(radius, relative)
        ratio = self.radius/old
        for n in self.children:
            n.pos.set_pos(True, dist=ratio)
        for n in self.nodes:
            n.pos.set_pos(True, dist=ratio)
            
    def update(self):
        self.pos.update()
        self._get_lett_angle()
        for dot in self.children:
            dot.update()
        for nod in self.nodes:
            nod.pos.update()
