'''
Created on Sep 21, 2017

@author: Radu
'''

from UI import UI
from Controller import Ctrl
from Repositor import Repo
from Tkinter import Tk

def main():
    r = Repo()
    r.load()
    c = Ctrl(r)
    root = Tk()  
    root.title("Femo")
    a = UI(c, root)
    a.mainloop()
    
main()