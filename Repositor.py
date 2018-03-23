'''
Created on Sep 20, 2017

@author: Radu
'''
from __future__ import print_function
from Shapes import Line, TextBox
from Domain import Formula
import os
from copy import deepcopy


class Repo:
    
    def __init__(self):
        self._repo = []
    
    def search(self, name):
        for f in self._repo:
            if f._name == name:
                return f
    
    def add(self, formula):
        for f in self._repo:
            if f == formula:
                return 
        self._repo.append(formula)
        
    def remove(self, name):
        for f in self._repo:
            if f._name == name:
                del self._repo[self._repo.index(f)]
    
    def searchKey(self, name, keyWords):
        resultList = []
        
        if name == "": name = None
        if keyWords == ['']: keyWords = []
        
        for f in self._repo:
            for k1 in keyWords:
                for k2 in f._keyWords:
                    if k1 == k2:
                        resultList.append(f._name)
            if name != None:
                if f._name == name or name in f._name:
                    resultList.append(f._name)            
            
        return resultList
    
    def update(self, name, newName, keys):
        
        for f in self._repo:
            if f._name == name:
                if newName != '' :  f._name = deepcopy(newName)
                if keys != ['']  :  f._keyWords = deepcopy(keys)
                
    def sort(self):
        self._repo.sort()                
    
    def getList(self):
        return self._repo
    
    def removeKeyWord(self, name, word):
        for f in self._repo:
            if f._name == name:
                del f._keyWords[f._keyWords.index(word)]
                
    def addKeyWord(self, name, word):
        for f in self._repo:
            if f._name == name:
                if word not in f._keyWords:
                    f._keyWords += word
    
    #TODO
    def save(self):
              
        Filename = 'save'

        open(Filename, 'w').close()
        File = open(Filename, 'w')
        for f in self._repo:
            print(str(f), file = File)
        
        File.close()
        
    def load(self):
        
        Filename = 'save'
        
        try:
            File = open(Filename, 'r')
        except IOError:
            open(Filename, 'w').close()
            File = open(Filename, 'r')
        
        while True:
            
            name = ""
            keys = []
            lines = []
            text = []
            
            line = File.readline()
            if not line : break
            
            name = line[:-1]
            
            line = File.readline()
            if not line : break
            nrK = int(line)
            
            for i in range(nrK):
                line = File.readline()
                if not line : break
                key = line[:-1]
                keys.append(key)
            
            line = File.readline()
            if not line : break  
            nrs = line.split('|')
            nrL = int(nrs[0])
            nrT = int(nrs[1])

            for i in range(nrL):
                line = File.readline()
                if not line : break
                
                ls = line.split('|')
                pos1 = (float(ls[0]), float(ls[1]))
                pos2 = (float(ls[2]), float(ls[3]))
                l = Line(pos1, pos2)
                lines.append(l)
                
            for i in range(nrT):
                line = File.readline()
                if not line : break
                
                ls = line.split('|')
                pos1 = (float(ls[0]), float(ls[1]))
                string = ls[2][:-1]
                t = TextBox(pos1, string)
                text.append(t)
                
            line = File.readline()
            if not line : break  
            
            cDate = line[:-1]
            
            f = Formula(name, lines, text, keys, cDate = cDate)
            self._repo.append(f)