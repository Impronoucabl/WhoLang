#from lottie.utils import script
from lottie import objects
from lottie.exporters.core import export_lottie
from lottie import Point, Color
from gall_wrd import G_word

def main(text):
    A = G_word(text, 400, G_word.origin)
    A.spawn_syllables()
    A.spawn_letters()
    A.spawn_nodes()
    B = render_lottie(A)
    export_lottie(B, "test.json")
    #script.script_main(B)

def render_lottie(word):
    'default viewport size is 512 x 512' 
    'lottie thickness includes both inner & outer radii'
    an = objects.Animation(100)
    
    layer1 = objects.ShapeLayer()
    group = layer1.add_shape(objects.Group())
    ball = group.add_shape(objects.Ellipse())
    ball.size.value = Point(word.radius, word.radius)
    'group.add_shape(objects.Stroke(Color(1, 0, 0), word.thickness))'
    group.add_shape(objects.Fill(Color(0,0,0)))
    group.transform.position.value = Point(word.pos.lottie_x(), word.pos.lottie_y())
    an.add_layer(layer1)
    
    
    
    for syl in word.children.values():
        layer2 = None
        group2 = None
        syllables = None
        layer2 = objects.ShapeLayer()
        for lett in syl.children:
            
            group2 = layer2.add_shape(objects.Group())
            syllables = group2.add_shape(objects.Ellipse())
            syllables.size.value = Point(lett.radius, lett.radius)
            'group.add_shape(objects.Fill(Color(0,0,0)))'
            group2.transform.position.value = Point(lett.pos.lottie_x(), lett.pos.lottie_y())
    
        group2.add_shape(objects.Stroke(Color(1, 0, 0), 8))
        an.add_layer(layer2)
    
    maskshape = objects.Ellipse()
    maskshape.position.value = Point(256, 256)
    maskshape.size.value = Point(256, 256)
    maskbez = maskshape.to_bezier()
     
    mask = objects.Mask(maskbez.shape.value)
    mask.mode = 's'
    an.layers[0].masks = [mask]
    
    return an


if __name__ == "__main__":
    main(input('Type in text to translate:'))
