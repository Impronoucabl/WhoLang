from gall_cir import Gall_cir as cir

class Gall_let(cir):
    
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
