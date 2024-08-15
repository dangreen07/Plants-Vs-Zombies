import tkinter as tk
import time
from math import *
import random
import numpy as np
import winsound

class Tilemap:
	def __init__(self, x,y,canvas,rows=2,collumns=2,width=100,height=100):
		self.x = x
		self.xCoord = (canvas.width/2)-x
		self.canvas = canvas
		self.y = y
		self.yCoord = (canvas.height/2)-y
		self.rows = rows
		self.collumns = collumns
		self.width = width
		self.height = height

		self.rectangles = []
	def draw(self):
		w = 0
		xOffset = self.x
		for x in range(self.rows):
			xOffset += self.width
			yOffset = self.y
			for y in range(self.collumns):
				c = self.canvas.create_rectangle(xOffset, yOffset,self.width,self.height)
				self.rectangles.append(c)
				yOffset += self.height
	def boxBounds(self):
		final = []
		for i in self.rectangles:
			a,b = self.canvas.getLocation([i,0,0])
			c = a+self.width
			d = b+self.height
			final.append([a,b,c,d])
	def hide(self):
		for i in self.rectangles:
			self.canvas.canvas.itemconfig(i,outline="")
	def show(self):
		for i in self.rectangles:
			self.canvas.canvas.itemconfig(i,outline="black")
