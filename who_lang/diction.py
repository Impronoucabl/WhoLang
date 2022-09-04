# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 13:04:18 2022

@author: natha
"""
import common as cm

class Diction():
    
    done = []
    capital = False
    
    def __init__(self, letter_dict = None):
        if letter_dict is None:
            self._clear_dict()
        self._clear_buff()
    
    def _clear_buff(self):
        self.syllables = {}
        self.buffer = ''
        self.index = 0
        
    def _clear_dict(self):
        self.diction = {**self._vowelGrab(cm.cDict), **cm.cDictVow}
        if self.capital:
            self._set_capital()
    
    @staticmethod
    def _UpperDict(cdict):
        return {k.capitalize():v for (k,v) in cdict.items()}
    
    @staticmethod
    def _doubleDict(cdict):
        return {k*2:v for (k,v) in cdict.items()}
    
    @staticmethod
    def _extDict(cdict):
        return {**cdict,**cm.cDictExt}
    
    @staticmethod
    def _stackDict(cDict):
        new_dict = {**cDict}
        for (k1,v1) in cDict.items():
            for (k2,v2) in cDict.items():
                if v1[0] == v2[0]:
                    new_dict[k1+k2]=v1
        return new_dict
    
    'always call last'                
    @staticmethod
    def _vowelGrab(cDict):
        new_dict = {**cDict}
        for i in cm.cDictVow:
            new_dict.update({k+i:v for (k,v) in cDict.items()})
        return new_dict
    
    def _nxt_ind(self, n):
        self.syllables[self.index] = self.buffer
        self.buffer = ''
        self.index = n
    
    def _set_capital(self):
        self.capital = True
        self.diction.update(self.UpperDict(self.diction))
    
    def str_to_sylDict(self, text):
        text = text.strip()
        self._clear_buff()
        numeric = False
        for n,i in enumerate(text):
            if i.isspace():
                self._nxt_ind(n + 1)
            elif i in cm.punc:
                self._nxt_ind(n)
                self.buffer += i
                self._nxt_ind(n + 1)
            elif numeric:
                if i.isnumeric():
                    self.buffer += i
                else:
                    self._nxt_ind(n)
                    self.buffer += i
                    numeric = False
            elif i.isupper():
                if not self.capital:
                    self._set_capital()
                self._nxt_ind(n)
                self.buffer += i
            elif self.buffer == '':
                self.buffer += i
            elif self.buffer + i in self.diction:
                self.buffer += i
            elif self.buffer in self.diction:
                self._nxt_ind(n)
                self.buffer += i
            else:
                raise SyntaxError('A non-literal "c" or "q" was given without an extended diction.')
        self.syllables[self.index] = self.buffer
        
        self.done.append([text, self.syllables])
        return self.syllables