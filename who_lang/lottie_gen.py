import os

#from lottie.utils import script
from lottie import objects
from lottie.exporters.core import export_lottie
from lottie import Point, Color
from gall_skel import Gall_skel

def main(text):
    A = Gall_skel(text, 150, Gall_skel.origin, thickness=18)
    A.spawn_words()
    A.spawn_syllables()
    A.spawn_letters()
    A.spawn_nodes()
    A.node_prep()
    B = render_lottie(A)
    path = os.getcwd().split('\\')[:-1]
    path.append('lottie_output')
    export_lottie(B,''.join([a + '\\' for a in path]) + A.text + ".json")
    #script.script_main(B)

def lottie_cir(outer_rad, inner_rad, pos, anim = None, layer = None, Col = Color(0,0,0)):
    if layer is None:
        layer = objects.ShapeLayer()
    else:
        anim = None
    group = layer.add_shape(objects.Group())
    circle = group.add_shape(objects.Ellipse())
    circle.size.value = Point(2*outer_rad, 2*outer_rad)
    group.add_shape(objects.Fill(Col))
    group.transform.position.value = Point(pos.lottie_x(), pos.lottie_y())
    
    if anim is not None:
        mask = mask_cir(inner_rad,pos, mode='s')
        anim.add_layer(layer)
        anim.layers[-1].masks = [mask]
    return layer

def mask_cir(radius, pos, mode = None):
    maskshape = objects.Ellipse()
    maskshape.position.value = Point(pos.lottie_x(), pos.lottie_y())
    maskshape.size.value = Point(2*radius, 2*radius)
    maskbez = maskshape.to_bezier()
    mask = objects.Mask(maskbez.shape.value)
    if mode is not None:
        mask.mode = mode
    return mask

def lottie_ray(node):
    pass

def render_lottie(skel):
    'default viewport size is 512 x 512' 
    an = objects.Animation(1)
    'lottie thickness includes both inner & outer radii'
    'earlier layers are rendered over later layers' 
    
    lin_lay = objects.ShapeLayer()
    vow_lay = objects.ShapeLayer()
    vow_msk = []
    an.add_layer(lin_lay)
    an.add_layer(vow_lay)
    
    for nodes in skel.nodes:
        if nodes.visible:
            if nodes.pair is None: 
                if nodes.pair_lst is None:
                    'draw a straight line'
                    pass
            else:
                if nodes.pair_lst is None:
                    'draw line between nodes'
                    nodes.pair.visible = False
                    nodes.visible = False
    for wrd in skel.children:
        w_mask = mask_cir(wrd.lottie_radius(), wrd.pos)
        m_lst = []
        'render letters, and then vowels just before the end'
        for syl in wrd.children.values():
            for lett in syl.children:
                for dot in lett.children:
                    lottie_cir(
                        dot.lottie_radius(),
                        0,
                        dot.pos,
                        layer =  vow_lay)
                'Dots done. Now do letters'
                if lett.text in 'aeiou':
                    layer = vow_lay
                    vow_msk.append(mask_cir(
                        lett.lottie_Mradius(),
                        lett.pos,
                        mode = 's'))
                else:
                    layer = None
                lottie_cir( 
                           lett.lottie_radius(), 
                           lett.lottie_Mradius(), 
                           lett.pos, 
                           anim = an,
                           layer = layer,
                           Col=Color(0,0,0))
                if lett.cType[0] % 2 == 1:
                    an.layers[-1].masks.append(w_mask)
                    m_lst.append(mask_cir(lett.lottie_radius(), lett.pos, mode='s'))
                '''elif lett.cType[0] == 4:
                    m_lst.append(mask_cir(lett.lottie_radius(), lett.pos, mode='s'))'''
        
        lottie_cir(
                    wrd.lottie_radius(), 
                    wrd.lottie_Mradius(), 
                    wrd.pos,
                    Col=Color(1,0,0),
                    anim = an)
        
        an.layers[-1].masks += m_lst
    an.layers[1].masks = vow_msk
    return an


if __name__ == "__main__":
    main(input('Type in text to translate:'))
