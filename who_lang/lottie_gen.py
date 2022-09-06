#from lottie.utils import script
from lottie import objects
from lottie.exporters.core import export_lottie
from lottie import Point, Color
from gall_wrd import G_word

def main(text):
    A = G_word(text, 150, G_word.origin, thickness=18)
    A.spawn_syllables()
    A.spawn_letters()
    A.spawn_nodes()
    B = render_lottie(A)
    export_lottie(B, A.text + ".json")
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

def render_lottie(word):
    'default viewport size is 512 x 512' 
    'lottie thickness includes both inner & outer radii'
    an = objects.Animation(1)
    w_mask = mask_cir(word.lottie_radius(), word.pos)
    'render nodes first'
    '''
    for lines in word.lines: #<----?
    for syl in word.children.values():
        for lett in syl.children:
            for node in lett.children:
                pass
    '''        
    m_lst = []
    vow_msk = []
    'render letters, and then vowels just before the end'
    vow_lay = objects.ShapeLayer()
    for syl in word.children.values():
        for lett in syl.children:
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
    an.add_layer(vow_lay)
    an.layers[-1].masks = vow_msk
    lottie_cir(
                word.lottie_radius(), 
                word.lottie_Mradius(), 
                word.pos,
                anim = an)
    an.layers[-1].masks += m_lst
    return an


if __name__ == "__main__":
    main(input('Type in text to translate:'))
