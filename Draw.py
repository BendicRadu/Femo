'''
Created on Sep 19, 2017

@author: Radu
'''

import math
import pygame
from Shapes import Line, Button, TextBox
from pygame.constants import K_BACKSPACE
from Domain import Formula
from copy import deepcopy
import threading


class Draw:
    
    def __init__(self, h = 600, w = 740, fontSize = 20, lines = [], text = [], name = 'Femo window'):
        pygame.init()
        pygame.display.set_caption(name)
        
        self._h = h 
        self._w = w
        self._f = fontSize
        
        self._screen = pygame.display.set_mode((w, h))
        self._clock = pygame.time.Clock()
        self._done = False
        self._screen.fill((255, 255, 255))
        
        #Lines and text to be renderd
        self._lines = deepcopy(lines)
        self._text = deepcopy(text)
        
        #Mouse point bool
        self._isP1 = False
        self._isP2 = False
        
        self._firstPos = None
        self._secondPos = None
        
        self._mode = "Line"
        self._myfont = pygame.font.SysFont("TkDefaultFont", self._f)
        
        self._isHex = False
        self._centerHex = None
        
        self._plusLine1 = None 
        self._plusLine2 = None
        
        self._isPlus = False         
        
        self._isText = False
        self._textPos = None
        self._textStr = ""
        
        self._buttonList = []
        self._buttonNames = ["Line", "Contineous", "Arrow", "Double", "Hexagon", "Plus", "Text", "Erase", "Save", "buf"]
        self._buttonCoords = None
        self._buttonDict = {}
        self._curentButton = None
        
        self._lastAction = []
    
        
        self._isSaved = False
        
        
    
    def drawUI(self):
        
        k = 0
        
        for i in range(0, self._w, self._w // (len(self._buttonNames) - 1)):
            x1 = i
            y1 = 0
            x2 = i + self._w // (len(self._buttonNames) - 1)
            y2 = self._h // 20
            
            pygame.draw.line(self._screen, (0, 0, 0), (x1, y1), (x2, y1))
            pygame.draw.line(self._screen, (0, 0, 0), (x1, y1), (x1, y2))
            pygame.draw.line(self._screen, (0, 0, 0), (x1, y2), (x2, y2))
            pygame.draw.line(self._screen, (0, 0, 0), (x2, y2), (x2, y1))
            
            label = self._myfont.render(self._buttonNames[k], 1, (0, 0, 0))
            self._screen.blit(label, (x1 + self._w // 200, y1, x2, y2))
        
        
            newButton = Button(x1, y1, x2, y2, self._buttonNames[k])
            self._buttonDict[self._buttonNames[k]] = newButton
            k += 1
        
            self._buttonList.append(newButton)

    
    def strLine(self):
        
        p1 = self._firstPos
        p2 = self._secondPos
        
        P1 = list(p1)
        P2 = list(p2)
        
        x = abs(p2[0])
        y = abs(p2[1])
        
        if x > y: P2[1] = P1[1]
        else: P2[0] = P1[0]

        p1 = tuple(P1)
        p2 = tuple(P2)
        
        return [p1, p2]
    
    def drawLineEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 3:
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
                
                return
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
            
            if not self._isP1:
                self._firstPos = event.pos
                self._isP1 = True
            else:
                k = Line(self._firstPos, self._secondPos)
                self._lines.append(k)
                self._lastAction.append(["Line", 1])
                self._isSaved = False
                
                
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
            
        if event.type == pygame.MOUSEMOTION and self._isP1:
            self._secondPos = event.pos
            self._isP2 = True
            
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                if self._isP1 != None and self._isP2 != None:
                    self.strLine()
                
            
    def drawLine(self):
            
        if self._isP1 and self._firstPos != None:
            pygame.draw.circle(self._screen, (0, 0, 0), self._firstPos, 1)
            
        if self._isP2 and self._secondPos != None:
            pygame.draw.line(self._screen, (0, 0, 0), self._firstPos, self._secondPos)
        
    
    
    def drawContEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
                
                
            if event.button == 3:
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
                
                return
            
            if not self._isP1:
                self._firstPos = event.pos
                self._isP1 = True
            else:
                k = Line(self._firstPos, self._secondPos)
                self._lines.append(k)
                self._lastAction.append(["Line", 1])
                self._isSaved = False
                
                self._isP2 = False
                
                self._firstPos = self._secondPos
                self._secondPos = None
            
        if event.type == pygame.MOUSEMOTION and self._isP1:
            self._secondPos = event.pos
            self._isP2 = True
            
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self._firstPos = None
                self._secondPos = None
                
                self._isP1 = False
                self._isP2 = False
            
    
    def drawCont(self):
    
        if self._isP1 and self._firstPos != None:
            pygame.draw.circle(self._screen, (0, 0, 0), self._firstPos, 1)
            
        if self._isP2 and self._secondPos != None:
            pygame.draw.line(self._screen, (0, 0, 0), self._firstPos, self._secondPos)
    
    def drawArrowEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 3:
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
                
                return
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
            
            if not self._isP1:
                self._firstPos = event.pos
                self._isP1 = True
            else:
                k = Line(self._firstPos, self._secondPos)
                
                
                x1 = self._firstPos[0]
                x2 = self._secondPos[0]
                
                if x1 < x2:
                    x3 = x2 - self._w // 50
                    y3 = self._secondPos[1] + 10
                    x4 = x2 - self._w // 50
                    y4 = self._secondPos[1] - 10
                
                else:
                    x3 = x2 + self._w // 50
                    y3 = self._secondPos[1] - 10
                    x4 = x2 + self._w // 50
                    y4 = self._secondPos[1] + 10
                pos1, pos2 = (x3, y3), (x4, y4)
                
                k1 = Line(self._secondPos, pos1)
                k2 = Line(self._secondPos, pos2)
                
                self._lines.append(k)
                self._lastAction.append(["Line", 1])
                self._lines.append(k1)
                self._lastAction.append(["Line", 1])
                self._lines.append(k2)
                self._lastAction.append(["Line", 1])
                
                self._isSaved = False
                
                
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
            
        if event.type == pygame.MOUSEMOTION and self._isP1:
            
            sP = list(event.pos)
            sP[1] = self._firstPos[1]
            
            e = list(event.pos)
            e[1] = self._firstPos[1]
            
            self._secondPos = tuple(e)
            self._isP2 = True
    
                
            
    def drawArrow(self):
            
        if self._isP1 and self._firstPos != None:
            pygame.draw.circle(self._screen, (0, 0, 0), self._firstPos, 1)
            
        if self._isP2 and self._secondPos != None:
            pygame.draw.line(self._screen, (0, 0, 0), self._firstPos, self._secondPos)
            
            x1 = self._firstPos[0]
            x2 = self._secondPos[0]
            
            if x1 < x2:
                x3 = x2 - self._w // 50
                y3 = self._secondPos[1] + 10
                x4 = x2 - self._w // 50
                y4 = self._secondPos[1] - 10
                
            else:
                x3 = x2 + self._w // 50
                y3 = self._secondPos[1] - 10
                x4 = x2 + self._w // 50
                y4 = self._secondPos[1] + 10
            
            pos1, pos2 = (x3, y3), (x4, y4)
            
            pygame.draw.line(self._screen, (0, 0, 0), self._secondPos, pos1)
            pygame.draw.line(self._screen, (0, 0, 0), self._secondPos, pos2)
    
    
    def getArowPos(self, x1, x2):
    
        if x1 < x2:
            x3 = x2 - self._w // 50
            y3 = self._secondPos[1] + 10
            x4 = x2 - self._w // 50
            y4 = self._secondPos[1] - 10
            
        else:
            x3 = x2 + self._w // 50
            y3 = self._secondPos[1] - 10
            x4 = x2 + self._w // 50
            y4 = self._secondPos[1] + 10    
            
        return (x3, y3), (x4, y4)
    
    def drawDoubleArrowEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 3:
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
                
                return
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
            
            if not self._isP1:
                self._firstPos = event.pos
                self._isP1 = True
            else:
                k = Line(self._firstPos, self._secondPos)
                
                
                x1 = self._firstPos[0]
                x2 = self._secondPos[0]
                
            
                pos1, pos2 = self.getArowPos(x1, x2)
                pos3, pos4 = self.getArowPos(x2, x1)
                
                k1 = Line(self._secondPos, pos1)
                k2 = Line(self._secondPos, pos2)
                
                k3 = Line(self._firstPos, pos3)
                k4 = Line(self._firstPos, pos4)
                
                self._lines.append(k)
                self._lastAction.append(["Line", 1])
                self._lines.append(k1)
                self._lastAction.append(["Line", 1])
                self._lines.append(k2)
                self._lastAction.append(["Line", 1])
                self._lines.append(k3)
                self._lastAction.append(["Line", 1])
                self._lines.append(k4)
                self._lastAction.append(["Line", 1])
                
                self._isSaved = False
                
                
                self._isP1 = False
                self._isP2 = False
                
                self._firstPos = None
                self._secondPos = None
            
        if event.type == pygame.MOUSEMOTION and self._isP1:
            
            sP = list(event.pos)
            sP[1] = self._firstPos[1]
            
            e = list(event.pos)
            e[1] = self._firstPos[1]
            
            self._secondPos = tuple(e)
            self._isP2 = True
    
    
    def drawDoubleArrow(self):
            
        if self._isP1 and self._firstPos != None:
            pygame.draw.circle(self._screen, (0, 0, 0), self._firstPos, 1)
            
        if self._isP2 and self._secondPos != None:
            pygame.draw.line(self._screen, (0, 0, 0), self._firstPos, self._secondPos)
            
            x1 = self._firstPos[0]
            x2 = self._secondPos[0]
            
            pos1, pos2 = self.getArowPos(x1, x2)
            pos3, pos4 = self.getArowPos(x2, x1)
            
            
            pygame.draw.line(self._screen, (0, 0, 0), self._firstPos, pos3)
            pygame.draw.line(self._screen, (0, 0, 0), self._firstPos, pos4)
            
            
            pygame.draw.line(self._screen, (0, 0, 0), self._secondPos, pos1)
            pygame.draw.line(self._screen, (0, 0, 0), self._secondPos, pos2)
            
            
            
    
    def createHexLines(self):
        
        if not self._isHex: return 

        c = list(self._centerHex)
        
        k1 = (self._w + self._h) // 20
        k2 = k1 / 2
        
        pos1 = (c[0] - k1, c[1] + k2)
        pos2 = (c[0], c[1] + k1)
        pos3 = (c[0] + k1, c[1] + k2)
        pos4 = (c[0] + k1, c[1] - k2)
        pos5 = (c[0], c[1] - k1)
        pos6 = (c[0] - k1, c[1] - k2)
        
        k1 = Line(pos1, pos2)
        k2 = Line(pos2, pos3)
        k3 = Line(pos3, pos4)
        k4 = Line(pos4, pos5)
        k5 = Line(pos5, pos6)
        k6 = Line(pos6, pos1)
        
        return [k1, k2, k3, k4, k5, k6]
                
    
    def drawHexEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
            
            
            if event.button == 3:
                self._isHex = False
                self._centerHex = None
                return
            
            if self._centerHex != None:
                self._lines += self.createHexLines()
                self._lastAction.append(["Line", 9])
                self._isSaved = False
            
            
        if event.type == pygame.MOUSEMOTION:
            
            if event.pos[1] < self._h // 20 + (self._w + self._h) // 20:
                self._centerHex = None 
                self._isHex = False
                return
            
            self._centerHex = event.pos
            self._isHex = True
            
            
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self._isHex = False
                self._centerHex = None
            
    
    def drawHex(self):
    
        lines = self.createHexLines()
        
        if not self._isHex: return
        
        for line in lines:
            pygame.draw.line(self._screen, (0, 0, 0), line._p1, line._p2)
    
    
    def drawPlusEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
            
            
            if event.button == 3:
                self._isPlus = False
                self._plusLine1 = None
                self._plusLine2 = None
                return
            
            if self._isPlus:
                
                self._lines.append(self._plusLine1)
                self._lines.append(self._plusLine2)
                self._lastAction.append(["Line", 1])
                self._lastAction.append(["Line", 1])
                self._isSaved = False
            
            
        if event.type == pygame.MOUSEMOTION:
            
            if event.pos[1] < self._h // 20 + (self._w + self._h) // 20:
                self._plusLine1 = None 
                self._plusLine2 = None
                self._isPlus = False
                return
            
            self._isPlus = True
            
            e = event.pos
            
            x1 = e[0] + 10
            y1 = e[1]
            x2 = e[0] - 10
            y2 = e[1]
            
            x3 = e[0]
            y3 = e[1] + 10
            x4 = e[0]
            y4 = e[1] - 10
            
            l1 = Line((x1, y1), (x2, y2))
            l2 = Line((x3, y3), (x4, y4))
            
            self._plusLine1 = l1 
            self._plusLine2 = l2
            
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self._isPlust = False
                self._plusLine1 = None 
                self._plusLine2 = None
            
    
    def drawPlus(self):

        if not self._isPlus: return
        
        pygame.draw.line(self._screen, (0, 0, 0), self._plusLine1._p1, self._plusLine1._p2)
        pygame.draw.line(self._screen, (0, 0, 0), self._plusLine2._p1, self._plusLine2._p2)

    
    
    def drawTextEvent(self, event):
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
                
                
            if event.button == 3:
                self._isText = False
                self._textStr = ""
                self._textPos = None
                
                return
            
            self._isText = True
            self._textPos = event.pos
            
        if event.type == pygame.MOUSEMOTION and self._isP1:
            self._secondPos = event.pos
            self._isP2 = True
            
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                k = TextBox(self._textPos, self._textStr, self._f)
                self._text.append(k)
                self._lastAction.append(["Text", 1])
                self._isSaved = False
                self._textStr = ""
                return
            
                
                
            key = event.key
            
            if key == K_BACKSPACE:
                self._textStr = self._textStr[:-1]
            
            elif key >= 97 and key <= 122:
                self._textStr += chr(key - 32)
            
            elif key <= 127:
                self._textStr += chr(key)
            
            
    def drawText(self):
            
        if self._isText:
            pygame.draw.circle(self._screen, (0, 0, 0), self._textPos, 1)
            
            label = self._myfont.render(self._textStr, 1, (0, 0, 0))
            self._screen.blit(label, (self._textPos))
    
    @staticmethod
    def distance(a, b):
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    
    def delThread(self, event, buff):

        for line in self._lines:
            if int(self.distance(line._p1, event.pos) + self.distance(event.pos, line._p2)) == int(self.distance(line._p1, line._p2)):
                del self._lines[self._lines.index(line)]
    
        for txt in self._text:
            if txt.isInside(event.pos):
                del self._text[self._text.index(txt)]

    def erase(self, event):
        
        pygame.mouse.set_cursor(*pygame.cursors.diamond)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            for but in self._buttonList:
                if but.isInside(event.pos):
                    self._mode = but.textVar
                    return
            
            threading.Thread(target=self.delThread, args = (event, 1)).start()
                        
            
    
    def loop(self):
        
        while not self._done:
            self._screen.fill((255, 255, 255))
        
            for event in pygame.event.get():   
                
                if self._mode != "Erase": pygame.mouse.set_cursor(*pygame.cursors.arrow)
                if self._mode != "Text": self._textStr = ''
                
                if self._mode == "Line": self.drawLineEvent(event)
                if self._mode == "Contineous": self.drawContEvent(event)
                if self._mode == "Hexagon": self.drawHexEvent(event)
                if self._mode == "Text": self.drawTextEvent(event)
                if self._mode == "Erase": self.erase(event)
                if self._mode == "Arrow": self.drawArrowEvent(event)
                if self._mode == "Double": self.drawDoubleArrowEvent(event)
                if self._mode == "Plus": self.drawPlusEvent(event)
                if self._mode == "Save": self._done = True; pygame.quit(); return [self._lines, self._text]
                
                
                
                if event.type == pygame.QUIT:
                    self._done = True
                    pygame.quit()
                    return None 
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pass
                                              
                        
                    elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        
                        if len(self._lastAction) >= 1:
                            
                            k = self._lastAction[-1]
                            for i in range(k[1]):
                                if k[0] == "Line":
                                    del self._lines[-1]
                                else:
                                    del self._text[-1]
                                    
                            if k[0] == "Line": del self._lastAction[-1]
                            else: del self._lastAction[-1]
            
            self.drawUI()
            
            self._curentButton = self._buttonDict[self._mode]
            self._buttonCoords = self._buttonDict[self._mode].getPosAndDim()
            
            pygame.draw.rect(self._screen, (100, 100, 100), self._buttonCoords)
            
            
            self.drawUI()
                    
            
            if self._mode == "Line": self.drawLine()
            if self._mode == "Contineous": self.drawCont()
            if self._mode == "Hexagon": self.drawHex()
            if self._mode == "Text": self.drawText()
            if self._mode == "Arrow": self.drawArrow()
            if self._mode == "Double": self.drawDoubleArrow()
            if self._mode == "Plus": self.drawPlus()
            
            for line in self._lines:
                pygame.draw.line(self._screen, (0, 0, 0), line._p1, line._p2)
    
            for txt in self._text: 
                label = self._myfont.render(txt._textVar, 1, (0, 0, 0))
                self._screen.blit(label, (txt._pos))
        
            pygame.display.flip()