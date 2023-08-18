# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 19:26:30 2022

@author: natha
"""
import lottie_gen
from gall_skel import Gall_skel

def generate(text):
    A = Gall_skel(text, 150, Gall_skel.origin)
    A.spawn_words()
    A.spawn_syllables()
    A.spawn_letters()
    A.spawn_nodes()
    A.node_prep()
    return A

if __name__ == "__main__":
    text = input('Type in text to translate:')
    A = generate(text)
    'customise manually here before rendering'
    '''
    A = Gall_skel(text, 150, Gall_skel.origin, thickness=18)
    A.spawn_words()
    A.spawn_syllables()
    A.spawn_letters()
    A.spawn_nodes()
    A.node_prep()
    '''
    B = lottie_gen.render_lottie(A)
    lottie_gen.save_lottie(B, text, True)

        
