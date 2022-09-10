# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 20:34:22 2022

@author: natha
"""
import math

def dot_spread(cType, min_ang, max_ang):
    if cType[2] == 1:
        lst = [0]
    elif cType[2] == 2:
        lst = [-1,1]
    elif cType[2] == 3:
        lst = [-math.pi/3,0,math.pi/3]
    else:
        lst = [-1.5,-0.5,0.5,1.5]
    return [x + math.pi for x in lst]

def node_pair(node_set):
    done_set = node_set
    for node1 in node_set:
        done_set.remove(node1)
        if node1.visible:
            continue
        for node2 in done_set:
            'test for pairing'
            pass
        
        