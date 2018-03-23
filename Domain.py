'''
Created on Sep 20, 2017

@author: Radu
'''

class Formula:
    '''
    :cDate: creation date
    '''
    def __init__(self, name, lines, text, keyWords = [], index = 0, cDate = None):
        self._name = name 
        if keyWords == ['']: self._keyWords = []
        else: self._keyWords = keyWords
        self._lines = lines 
        self._text = text
        self._index = index
        self._cDate = cDate
    
    def __eq__(self, other):
        return self._name == other._name
    
    def __lt__(self, other):
        return self._name < other._name
    
    def __str__(self):
        
        strV = ''
        strV += self._name + '\n'
    
        strV += str(len(self._keyWords)) + '\n'
        
        for key in self._keyWords:
            strV += key + '\n'
            
        strV += str(len(self._lines)) + '|' + str(len(self._text)) + '\n'
    
        for line in self._lines:
            strV += str(line) + '\n'
            
        for txt in self._text:
            strV += str(txt) + '\n'
            
        strV += self._cDate
    
        return strV