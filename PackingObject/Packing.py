import tkinter as tk
from tkinter import Tk
from Form import Form
from math import pi

class Packing:
    def __init__(self,root):
        self.list_form:list[Form] = []
        self.root = root
        self.root.geometry("900x600") 

        self.setup_ui()

    def setup_ui(self):
        self.canevas = tk.Canvas(self.root,bg="#0a090f",bd=2,relief="sunken")
        self.canevas.pack(padx=10,pady=10,fill="both",side="left", expand=True)
        self.canevas.bind("<Button-1>",self.on_canevas_click)
        self.visualizationBoard = tk.Frame(self.root,width=250)
        self.visualizationBoard.pack(padx=10,pady=10,expand=True,fill="both")
        
    def showInfo(self,form:Form):
        pass

    def drawForm(self):
        for form in self.list_form:
            form.draw(self.canevas)

    def on_canevas_click(self,event):
        print("canevas clicked")
        print(f"position : x:{event.x} y{event.y} ")
        if len(self.list_form)>0:
            for form in self.list_form:
                x,y = form.getPosition()
                if event.x > x and event.x < self.canevas.winfo_width():
                    if event.y > y and event.y < self.canevas.winfo_height():
                        print(f"x{event.x} y{event.y} inside {x},{y} and {self.canevas.winfo_width()} {self.canevas.winfo_height()}")


    def addForm(self,form:Form):
        self.list_form.append(form)


form1 = Form()
form1.setType("T")
form1.setPosition(15,15)
form1.setSizing({
    "w":125,
    "h":125
    # "d":125
})
form1.setRotation(pi/6)

form2 = Form()
form2.setType("T")
form2.setPosition(200,200)
form2.setSizing({
    "w":125,
    "h":125
    # "d":125
})

form3 = Form()
form3.setType("R")
form3.setPosition(200,125)
form3.setSizing({
    "w":125,
    "h":300
    # "d":125
})
form3.setRotation(pi/2)


root = tk.Tk()
packingUI = Packing(root)

packingUI.addForm(form1)
packingUI.addForm(form2)
packingUI.addForm(form3)
packingUI.drawForm()
root.mainloop()