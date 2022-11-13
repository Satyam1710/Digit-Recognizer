# Part 1. importing libraries and load the dataset
from calendar import EPOCH
from ctypes.wintypes import HWND
from msilib import sequence
from sqlite3 import converters
from unicodedata import digit
from asyncio.windows_events import NULL
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense , Dropout , Flatten
from keras.layers import Conv2D , MaxPool2D
from keras import backend as K

# Part 6. Create GUI to predict digits
from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui  # we had to import win32gui 
from PIL import ImageGrab, ImageOps
import numpy as np

model = load_model('D:\codes\Project_1\mnist.h5')

def predict_digit(img):
   img = img.resize((28,28)) #resize image to 28 X 28 pixels
   img=img.convert('L')
   img=ImageOps.invert(img)
   img=np.array(img)
   #reshapping to support our model input and normalizing
   img=img.reshape(1,28,28,1)
   img=img/255.0
   # Predicting the class
   res=model.predict([img])[0]
   return np.argmax(res), max(res)
class App(tk.Tk):
   def __init__(self):
      tk.Tk.__init__(self)
      self.x=self.y=0

      # Creating elements
      self.canvas = tk.Canvas(self, width=400,height=400,bg="white",cursor="arrow")
      self.label = tk.Label(self,text="Draw a digit"+"\n"+"in Range 0 to 9",font=("Helvetica",48),bg="green",fg="orange")
      self.calssify_btn = tk.Button(self,text="Predict_",command= self.classify_handwriting,fg="black",bg="green") 
      self.button_clear = tk.Button(self,text="Clear",command=self.clear_all,fg="black",bg="green")

       # Grid structure
      self.canvas.grid(row=0, column=0, pady=2, sticky=W)
      self.label.grid(row=0, column=1, pady=2, padx=2)
      self.calssify_btn.grid(row=1, column=1, pady=10, padx=10)
      self.button_clear.grid(row=1, column=0, pady=2)

      self.canvas.bind("<B1-Motion>", self.draw_lines)
   def clear_all(self):
      self.canvas.delete("all")
   
   def classify_handwriting(self):
      HWND=self.canvas.winfo_id()  # get the handle of the canvas
      rect=win32gui.GetWindowRect(HWND) # get the coordinate of canvas
      a,b,c,d=rect
      rect=(a+4,b+4,c+100,d+100)
      im=ImageGrab.grab(rect)
      digit,acc=predict_digit(im)
      
      self.label.configure(text="Digit : "+str(digit)+'\n'+"Accuracy : "+str(int(acc*100))+'%')
      
   def draw_lines(self,event):
      self.x = event.x
      self.y = event.y
      r=8
      self.canvas.create_oval(self.x-r,self.y-r,self.x+r,self.y+r,fill='black')
app = App()
mainloop()