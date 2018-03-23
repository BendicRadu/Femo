'''
Created on Sep 20, 2017

@author: Radu
'''

from Tkinter import *
from Domain import Formula
import tkMessageBox
import tkFont
from Draw import Draw
from cgitb import small
import time


class AddFrame(Frame):
    
    def __init__(self, ctrl, root = None):
        Frame.__init__(self, root)
        self._root = root 
        self._ctrl = ctrl
        
        self._f = None
        
        self.grid()
        self.createWidgets()

    
    def add(self):
        
        name = self._nameEntry.get()
        
        if name == "" : tkMessageBox.showinfo("No name", "Names can not be blank"); return 
        if self._ctrl.search(name) != None : tkMessageBox.showinfo("Name invalid", "Name already taken"); return 
        
        keyWordsRaw = self._keyEntry.get()
        keyWords = []
        
        for w in keyWordsRaw.split('|'):
            keyWords.append(w)
        
        k = Draw(name = name)
        data = k.loop()
        
        if data == None:
            self._f = None
            self.quit()
            self._root.destroy()
            return
        
        d1 = (time.strftime("%d/%m/%Y"))
            
        f = Formula(name, data[0], data[1], keyWords, cDate = d1)
        self._f = f
        self._root.destroy()
        self.quit()
    
    def end(self):
        self._root.destroy()
        self.quit() 
    
    def createWidgets(self):
        
        self._nameLabel = Label(self._root, text = "Name: ")
        self._nameLabel.grid(row = 0, column = 0)
        
        self._nameEntry = Entry(self._root, width = 25)
        self._nameEntry.grid(row = 0, column = 1)
        
        self._keyLabel = Label(self._root,text = "*Key Words: ")
        self._keyLabel.grid(row = 1, column = 0)
        
        self._keyEntry = Entry(self._root, width = 25)
        self._keyEntry.grid(row = 1, column = 1)
        
        self._quit = Button(self._root,text = "Cancel", command = self.end , width = 23)
        self._quit.grid(row = 2, column = 0)
        self._ok = Button(self._root,text = "Next", command = self.add, width = 23)
        self._ok.grid(row = 2, column = 1)
        
        self._auxLabel = Label(self._root,text = "* key words are optional, but can be used to search for the formula\n please separate the keywords with \'|\'")
        self._auxLabel.grid(row = 3, column = 0, columnspan = 2)



class UpdateFrame(Frame):
    
    def __init__(self, ctrl, root = None):
        Frame.__init__(self, root)
        self._root = root 
        self._ctrl = ctrl
        
        self._name = ''
        self._keys = [""]
        
        self.grid()
        self.createWidgets()
    
    def update(self):
        
        name = self._nameEntry.get()
        
        if self._ctrl.search(name) != None : tkMessageBox.showinfo("Name invalid", "Name already taken"); return 
    
        keyWordsRaw = self._keyEntry.get()
        keyWords = []
        
        for w in keyWordsRaw.split('|'):
            keyWords.append(w)
            
        self._name = name 
        self._keys = keyWords
        
        self._root.destroy()
        self.quit()
        
    def end(self):
        self._root.destroy()
        self.quit() 
    
    def createWidgets(self):
        
        self._nameLabel = Label(self._root, text = "*Update name: ")
        self._nameLabel.grid(row = 0, column = 0)
        
        self._nameEntry = Entry(self._root, width = 25)
        self._nameEntry.grid(row = 0, column = 1)
        
        self._keyLabel = Label(self._root,text = "**Update key Words: ")
        self._keyLabel.grid(row = 1, column = 0)
        
        self._keyEntry = Entry(self._root, width = 25)
        self._keyEntry.grid(row = 1, column = 1)
        
        self._quit = Button(self._root,text = "Cancel", command = self.end , width = 23)
        self._quit.grid(row = 2, column = 0)
        self._ok = Button(self._root,text = "Update", command = self.update, width = 23)
        self._ok.grid(row = 2, column = 1)
        
        self._auxLabel = Label(self._root,text = "** Key words are optional, but can be used to search for the formula\n please separate the keywords with \'|\' \n * Leave blank to not update name or key")
        self._auxLabel.grid(row = 3, column = 0, columnspan = 2)


class UI(Frame):
    
    def __init__(self, ctrl, root = None):
        Frame.__init__(self, master = root)
        
        self._root = root
        self._ctrl = ctrl
        
        self._root.bind("<Escape>", self.exit)
        
        self.grid()
        self.createWidgets()
        self.populateList()
    
    def populateList(self):
        
        for f in self._ctrl.getRepo():
            self._fList.insert(END, f._name)
    
    def exit(self, event):
        self.quit()    
    
    def add(self):
        b = AddFrame(self._ctrl, Toplevel())
        b.mainloop()
        
        if b._f != None:
            self._fList.insert(0, b._f._name)
            self._ctrl.add(b._f)
            self._ctrl.save()
        
    def remove(self):
        
        if self._fList.curselection() == (): tkMessageBox.showinfo("No selection", "Nothing is selected"); return 
        
        name = self._fList.get(self._fList.index(self._fList.curselection()))
        self._ctrl.remove(name)
        self._fList.delete(self._fList.curselection())
        
        self._ctrl.save()

    def view(self):
        name = self._fList.get(self._fList.index(self._fList.curselection()))
        f = self._ctrl.search(name)
        
        k = Draw(lines = f._lines, text = f._text, name = f._name)
        data = k.loop()
        
        if data != None:
            f1 = Formula(name, data[0], data[1], f._keyWords)
            self._ctrl.remove(name)
            self._ctrl.add(f1)
            self._ctrl.save()
        
    def search(self):
        
        for i, entry in enumerate(self._fList.get(0, END)):
            self._fList.itemconfig(i, bg = "white")
            
        name = self._seachEntry.get()
        rawKey  = self._keyEntry.get()
        key = []
        
   
        for w in rawKey.split('|'):
            key.append(w)    
        results = self._ctrl.searchKey(name, key)
        
        
        for r in results:
            for i, entry in enumerate(self._fList.get(0, END)):
                if entry == r:
                    name = self._fList.get(i)
                    self._fList.delete(i)
                    self._fList.insert(0, name)
                    self._fList.itemconfig(0, bg = "#64db82")
        
        self._ctrl.save()
                   
    def update(self):
            
        if self._fList.curselection() == (): tkMessageBox.showinfo("No selection", "Nothing is selected"); return 
        
        index = self._fList.index(self._fList.curselection())
        oldName = self._fList.get(index)
        
        b = UpdateFrame(self._ctrl, Toplevel())
        b.mainloop()
        
        name = b._name
        keys = b._keys
        
        if name != "" or keys != [""]:
    
            self._ctrl.update(oldName, name, keys)
            
            self._ctrl.save()
            
            if name != '': oldName = name
                    
            self._fList.delete(self._fList.curselection())
            self._fList.insert(index, oldName)

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def popupKey(self, event):
        try:
            self._popup_menuKey.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self._popup_menuKey.grab_release()
            
    def sort(self):
        
        self._fList.delete(0, END)
        self._ctrl.sort()
        
        r = self._ctrl.getRepo()

        for f in r:
            self._fList.insert(END, f._name)
            
        self._ctrl.save()
   
   
    def showKeyWords(self):
        
        if self._fList.curselection() == (): tkMessageBox.showinfo("No selection", "Nothing is selected from the main list"); return 
        self._infoName = self._fList.get(self._fList.index(self._fList.curselection()))
        f = self._ctrl.search(self._infoName)
        
        top = Toplevel()
        top.grid()
        
        top.title(f._name)
        
        small_font = tkFont.Font(size = 10)
        
        
        
        nameLabel1 = Label(top, text = 'Name: ', anchor = 'w', font = small_font, width = 9)
        nameLabel1.grid(row = 0, column = 0)
        
        nameLabel2 = Label(top, text = self._infoName, anchor = 'w', font = small_font, width = 9)
        nameLabel2.grid(row = 0, column = 1) 
        
        keyStr = ''
        
        for k in f._keyWords:
            keyStr += k + '\n'

        
        self._keyList = Listbox(top, font = small_font, width = 9, height = 5)
        self._keyList.grid(row = 1, column = 1)
        
        
        self._keyList.bind("<Button-3>", self.popupKey)
        
        
        for k in f._keyWords:
            self._keyList.insert(END, k)

        keyLabel = Label(top, text = 'Key words: ', anchor = 'nw', font = small_font, height = 5)
        keyLabel.grid(row = 1, column = 0)
        
        
        dateLabel = Label(top, text = "Date created: " + str(f._cDate), font = small_font)
        dateLabel.grid(row = 2, column = 0, columnspan = 2)
            
        
        self._popup_menuKey = Menu(top, tearoff=0)
        self._popup_menuKey.add_command(label = "Add", command = self.addKey)
        self._popup_menuKey.add_command(label = "Remove", command = self.removeKey)
            
            
        top.mainloop()


    def removeKey(self):
        
        if self._keyList.curselection() == (): tkMessageBox.showinfo("No selection", "Nothing is selected from\nthe key word list"); return 
        
        name = self._infoName 
        word = self._keyList.get(self._keyList.index(self._keyList.curselection()))
        
        self._ctrl.removeKeyWord(name, word)
        self._keyList.delete(self._keyList.curselection())
        
        self._ctrl.save()

    def addKey(self):
        
        self._topKey = Toplevel()
        self._topKey.grid()
        
        self._topKey.title("Add key word")
        
        Label(self._topKey, text = "*Keys: ").grid(row = 0, column = 0)
        self._entryNewKey = Entry(self._topKey, width = 10)
        self._entryNewKey.grid(row = 0, column = 1)
        
        Button(self._topKey, text = "Cancel", command = self._topKey.quit).grid(row = 1, column = 0)
        Button(self._topKey, text = "Enter", command = self.addKeyAux).grid(row = 1, column = 1)
        
        Label(self._topKey, text = "*Any number of keys can be entered,\nas long as they're seperated by \'|\'").grid(row = 2, column = 0, columnspan = 2)
        
    def addKeyAux(self):
        
        self._topKey.quit()
        self._topKey.destroy()
        
        keyWordsRaw = self._entryNewKey.get()
        keyWords = []
        
        for w in keyWordsRaw.split('|'):
            keyWords.append(w)
        
        self._ctrl.addKeyWord(self._infoName, keyWords)
    
    def createWidgets(self):
        
        self._buffLabel0 = Label(height = 3, text = "Search: _______________________________________________________________________________________", anchor = "w")
        self._buffLabel0.grid(row = 0, column = 0, columnspan = 4)
        
        self._nLabel = Label(text = 'Name: ')
        self._nLabel.grid(row = 1, column = 0)
        
        self._kLabel = Label(text = '*Key words: ')
        self._kLabel.grid(row = 2, column = 0)
        
        self._searchButton = Button(relief = RIDGE, text = "Search", command = self.search, width = 17, height = 2)
        self._searchButton.grid(row = 1, column = 2, rowspan = 2)
        
        self._seachEntry = Entry(width = 25)
        self._seachEntry.grid(row = 1, column = 1)
        
        self._keyEntry = Entry(width = 25)
        self._keyEntry.grid(row = 2, column = 1)
        
        self._buffLabel1 = Label(height = 3, text = "Manage: _______________________________________________________________________________________", anchor = "w")
        self._buffLabel1.grid(row = 3, column = 0, columnspan = 4)
        
        self._addButton = Button(relief = RIDGE, text = "Add new", command = self.add, width = 25, height = 3)
        self._addButton.grid(row = 4, column = 0)
        
        self._removeButton = Button(relief = RIDGE, text = "Remove", command = self.remove, width = 25, height = 3)
        self._removeButton.grid(row = 5, column = 0)
        
        self._loadButton = Button(relief = RIDGE, text = "View", command = self.view, width = 25, height = 3)
        self._loadButton.grid(row = 6, column = 0)
        
        self._updateButton = Button(relief = RIDGE, text = "Update", command = self.update, width = 25, height = 3)
        self._updateButton.grid(row = 7, column = 0)
        
        self._bufLabel  = Label(height = 20)
        self._bufLabel.grid(row = 8, column = 0)
        
        
        small_font = tkFont.Font(size = 20)
        
        self._fList = Listbox(width = 20, height = 18, font = small_font)
        self._fList.grid(row = 4, column = 1, rowspan = 200, columnspan = 3)
        
        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label = "Sort", command = self.sort)
        self.popup_menu.add_command(label = "Show info", command = self.showKeyWords)
        
        
        self._fList.bind("<Button-3>", self.popup)
        
        self._2Label = Label(text = "*Key words are optional.\nPlease separate key words by \'|\'.")
        self._2Label.grid(row = 203, column = 0)
        
    
        
        
        