'''
Created on Sep 19, 2017

@author: Radu
'''

import math

class Line:
    def __init__(self, pos1, pos2):
        self._p1 = pos1 
        self._p2 = pos2
    
    def __eq__(self, other):
        return self._p1 == other._p1 and self._p2 == other._p2    
    
    def __repr__(self):
        return str(self._p1[0]) + "|" + str(self._p1[1]) + "|" + str(self._p2[0]) + "|" + str(self._p2[1])
        
class Button:

    def __init__(self, x1, y1, x2, y2, textVar):
        self._x1 = x1; self._y1 = y1; self._x2 = x2; self._y2 = y2
        self.textVar = textVar
    
    def __eq__(self, textVar):
        return self.textVar == textVar
    
    def isInside(self, pos):
        return pos[0] > self._x1 and pos[0] < self._x2 and pos[1] > self._y1 and self._y2 > pos[1]         
    
    def getCoords(self):
        return tuple([self._x1, self._y1, self._x2, self._y2])
    
    #returns x, y, width, height
    def getPosAndDim(self):
        return tuple([self._x1, self._y1, math.fabs(self._x2 - self._x1), math.fabs(self._y2 - self._y1)])

class TextBox:
    
    def __init__(self, pos, textVar, fontSize = 15):
        self._pos = pos; self._textVar = textVar; self._f = fontSize
        
    def __repr__(self):
        return str(self._pos[0]) + '|' + str(self._pos[1]) + '|' + str(self._textVar)
    
    def isInside(self, pos):
        
        p1 = list(self._pos)
        p2 = list(self._pos)
        
        p2[1] += self._f
        p2[0] += len(self._textVar) * self._f // 2
        
        return  pos[0] > p1[0] and pos[0] < p2[0] and pos[1] > p1[1] and p2[1] > pos[1]         
    
        
        
    
    
    