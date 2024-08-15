import tkinter as tk
import time
from math import *
import random
import numpy as np
import winsound

class Frame:
	def __init__(self, main):
		self.main = main
		self.frame = tk.Frame(self.main)
	def createButton(self, text="", fg="", command=""):
		return tk.Button(self.frame, text=text, fg=fg, command=self.remove)
	def pack(self):
		self.frame.pack()
	def hide(self):
		self.frame.pack_forget()
	def remove(self):
		self.frame.pack_forget()
