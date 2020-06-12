import tkinter
from tkinter import messagebox

class tkinterStuff():
    def newWindow(self, title):
        root = tkinter.Tk()
        root.wm_title(title)
        return root
    def showError(self,error):
        messagebox.showerror("Error",error)
    def showStartWindow(self):
        root = self.newWindow("Bienvenido")
        entry1 = tkinter.Entry(root)
        entry1.pack()
        entry2 = tkinter.Entry(root)
        entry2.pack()
        entry3 = tkinter.Entry(root)
        entry3.pack()
        root.mainloop()