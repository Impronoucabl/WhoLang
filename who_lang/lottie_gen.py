import os
import math
import config as cf
import common as cm
import lottie_anim


from lottie import objects, Point, Color
from lottie.exporters.core import export_lottie, export_embedded_html

def save_lottie(Anim, text, html = False):
    path = os.getcwd().split('\\')[:-1]
    path.append('lottie_output')
    path = ''.join([a + '\\' for a in path]) + text
    if html:
        export_embedded_html(Anim, path + ".html")
    else:
        export_lottie(Anim, path + ".json")

def _lottie_cir(rad, pos, group):
    circle = group.add_shape(objects.Ellipse())
    circle.size.value = Point(2*rad, 2*rad)
    circle.position.value = Point(pos.lottie_x(), pos.lottie_y())

def _lottie_ray(node, group):
    lin = group.add_shape(objects.Path())
    X = node.pos.lottie_x()
    Y = node.pos.lottie_y()
    angle = cm.GalRad2MathRad(node.pos.angle)
    
    node_pt = Point(X, Y)
    ray_pt = Point(350*math.cos(angle) + X, -350*math.sin(angle) + Y)
    
    lin.shape.value.add_point(node_pt)
    lin.shape.value.add_point(ray_pt)
    
def _lottie_anim(obj, anim_dict):
    for k,v in anim_dict.items():
        obj.opacity.add_keyframe(k,v)
    
def _mask_cir(radius, pos, mode = None):
    maskshape = objects.Ellipse()
    maskshape.position.value = Point(pos.lottie_x(), pos.lottie_y())
    maskshape.size.value = Point(2*radius, 2*radius)
    maskbez = maskshape.to_bezier()
    mask = objects.Mask(maskbez.shape.value)
    if mode is not None:
        mask.mode = mode
    return mask

def render_lottie(skel, lin_col = Color(1,0,0), vow_col = Color(0,0,1), let_col = Color(0,0,0), fade = False):
    'default viewport size is 512 x 512' 
    an = objects.Animation(100)
    'lottie thickness includes both inner & outer radii'
    'earlier layers are rendered over later layers' 
    "Add Fill after colors or it won't render"
    
    skel_lay = objects.SolidColorLayer(color='#ffffff')
    skel_lay.masks = [_mask_cir(skel.max_radius() + cf.SKEL_PADDING, skel.pos, mode='s')]
    an.add_layer(skel_lay)
    
    for wrd in skel.children:
        'make wrd_outer_msk early to add to letter masks if required'
        wrd_outer_msk = _mask_cir(wrd.max_radius(), wrd.pos)
        wrd_inner_msk = _mask_cir(wrd.min_radius(), wrd.pos, mode='s')
        wrd_msk = [wrd_outer_msk,wrd_inner_msk]
        vow_lay = objects.ShapeLayer()
        vow_grp = vow_lay.add_shape(objects.Group())
        vow_msk = []
        
        an.add_layer(vow_lay)

        for syl in wrd.children.values():
            lett_lay = objects.ShapeLayer()
            an.add_layer(lett_lay)
            lett_grp = lett_lay.add_shape(objects.Group())
            lett_msk = []
            
            if len(syl.children) < 3:
                'TODO: setup composite lettering'
                for lett in syl.children:
                    for dot in lett.children:
                        _lottie_cir(dot.max_radius(), dot.pos, vow_grp)
                    msk = _mask_cir(lett.min_radius(), lett.pos, mode = 's')
                    if lett.text in 'aeiou':
                        group = vow_grp
                        vow_msk.append(msk)
                    else:
                        group = lett_grp
                        lett_msk.append(msk)
                    _lottie_cir(lett.max_radius(), lett.pos, group)
                    if lett.cType[0] % 2 == 1:
                        lett_msk.append(wrd_outer_msk)
                        '-1 to help remove edge artifacts'
                        wrd_msk.append(_mask_cir(lett.max_radius() - 1, lett.pos, mode='s'))
            lett_lay.masks = lett_msk
            lett_fade = lett_grp.add_shape(objects.Fill(let_col))
            if fade:
                _lottie_anim(lett_fade, lottie_anim.Lett)
        wrd_lay = objects.SolidColorLayer(color='#000000')
        an.add_layer(wrd_lay)
        wrd_lay.masks = wrd_msk
        
        vow_fade = vow_grp.add_shape(objects.Fill(vow_col))
        if fade:
            _lottie_anim(vow_fade,lottie_anim.Vow)
        vow_lay.masks = vow_msk
        
    lin_lay = objects.ShapeLayer()
    lin_grp = lin_lay.add_shape(objects.Group())    
    an.add_layer(lin_lay)
    for nodes in skel.nodes:
        if nodes.visible:
            if nodes.pair is None: 
                if nodes.pair_lst is None:
                    _lottie_ray(nodes,lin_grp)
            else:
                if nodes.pair_lst is None:
                    'draw line between nodes'
                    lin = lin_grp.add_shape(objects.Path())
                    lin.shape.value.add_point(Point(nodes.pos.lottie_x(), nodes.pos.lottie_y()))
                    lin.shape.value.add_point(Point(nodes.pair.pos.lottie_x(), nodes.pair.pos.lottie_y()))
                    nodes.pair.visible = False
            nodes.visible = False
    stroke = lin_grp.add_shape(objects.Stroke(lin_col, cf.LIN_DEFAULT_STROKEW))
    if fade:
        _lottie_anim(stroke, lottie_anim.Lin)
    return an
