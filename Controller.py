'''
Created on Sep 20, 2017

@author: Radu
'''

class Ctrl:
    
    def __init__(self, repo):
        self._repo = repo
    
    def search(self, name):
        return self._repo.search(name)
    
    def add(self, f):
        self._repo.add(f)
        
    def remove(self, name):
        self._repo.remove(name)
    
    def searchKey(self, name, keyWords = []):
        return self._repo.searchKey(name, keyWords)
    
    def update(self, name, newName, newKeys):
        self._repo.update(name, newName, newKeys)
    
    def sort(self):
        self._repo.sort()    
    
    def getRepo(self):
        return self._repo.getList()
    
    def addKeyWord(self, name, word):
        self._repo.addKeyWord(name, word)
        
    def removeKeyWord(self, name, word):
        self._repo.removeKeyWord(name, word)
    
    #TODO
    def save(self):
        self._repo.save()