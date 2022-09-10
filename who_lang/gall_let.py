from gall_cir import Gall_cir as cir
from gall_node import G_node
from gall_pos import Gall_pos as gpos
import custom as cus
import common as cm
import config as cf
import math

class Gall_let(cir):
    
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
            self.lett_max_angle = math.pi*2
            self.lett_min_angle = 0
            self.half_angle_size = math.pi
            return
        
        self.half_angle_size = (self.parent.parent.pos.distance**2-self.parent.pos.distance**2-self.radius**2)/(2*self.radius*self.parent.pos.distance)
        self.lett_min_angle = self.rel_to_real_ang(self.half_angle_size)
        self.lett_max_angle = self.rel_to_real_ang(-self.half_angle_size)
    
    def rel_to_real_ang(self, angle):
        return cm.SmallPosAngle(angle + self.pos.angle)
    
    def real_to_rel_ang(self, angle):
        raw = angle - self.pos.angle
        if raw < -math.pi:
            return raw + math.pi*2
        else:
            raw = raw % (math.pi*2)
            return raw % math.pi
    
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
                        parent = self,
                        thickness = cf.DEFAULT_DOT_SIZE
                        ))
        return

    def set_radius(self, radius, relative=False):
        old = self.radius
        super().set_radius(radius, relative)
        ratio = self.radius/old
        for n in self.children:
            n.pos.set_pos(True, dist=ratio)
            
    def update(self):
        self.pos.update()
        self._get_lett_angle()
        for nod in self.nodes:
            nod.pos.update()
