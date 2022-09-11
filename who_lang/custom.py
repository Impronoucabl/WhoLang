# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 20:34:22 2022

@author: natha
"""

import common as cm
import config as cf

def dot_spread(cType, min_ang, max_ang):
    if cType[2] == 1:
        lst = [0]
    elif cType[2] == 2:
        lst = [-1,1]
    elif cType[2] == 3:
        lst = [-cm.PI/3,0,cm.PI/3]
    else:
        lst = [-1.5,-0.5,0.5,1.5]
    return [x + cm.PI for x in lst]

def node_pair(node_set):
    working_set = node_set.copy()
    paired = False
    for node1 in node_set:
        if node1.visible or node1.pair is not None:
            continue
        
        for node2 in working_set:
            'test if sibling'
            if node2.pair is not None:
                continue
            if node1.parent is node2.parent:
                continue
            'test for existing pairs'
            angle = node1.parent.pos.angle_to(node2.pos.center)
            
            if any([x.pair is not None and abs(x.pos.angle - angle) <= cf.ANG_COLL_DIST for x in node1.parent.nodes]):
                continue
            if any([x.pair is not None and abs(x.pos.angle - cm.SmallPosAngle(cm.PI+angle)) <= cf.ANG_COLL_DIST for x in node2.parent.nodes]):
                continue
            
            'test for pairing'
            if node1.ang_check(angle) and node2.ang_check(cm.SmallPosAngle(angle + cm.PI)):
                node1.pair_to(node2)
                node2.pair_to(node1)
                paired = True
                break
        if paired:
            working_set.remove(node1.pair)
            working_set.remove(node1)
            paired = False
    return working_set
        