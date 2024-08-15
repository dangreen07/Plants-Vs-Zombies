import tkinter as tk
import time
from math import *
import random
import winsound
## Frame import
class Frame:
	def __init__(self, main):
		self.main = main
		self.frame = tk.Frame(self.main)
	def createButton(self, text="", fg="black", command=""):
		return tk.Button(self.frame, text=text, fg=fg, command=self.remove)
	def pack(self):
		self.frame.pack()
	def hide(self):
		self.frame.pack_forget()
	def remove(self):
		self.frame.pack_forget()
## Tilemap import
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
				c = self.canvas.create_rectangle(xOffset,
								 yOffset,
								 self.width,
								 self.height)
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

## Item import
class Item:
	def __init__(self,item):
		self.item = item
		self.__player = False
		self.listIndex = 0
		self.collisionMesh = "all"
	def setWidth(self,width):
		self.__width = width
	def getWidth(self):
		return self.__width
	def setHeight(self,height):
		self.__height = height
	def getHeight(self):
		return self.__height
	def setRadius(self,radius):
		self.__radius = radius
	def getRadius(self,):
		return self.__radius
	def setPlayer(self,player):
		self.__player = player
	def getPlayer(self):
		return self.__player
	def setCoordX(self,x):
		self.__x = x
	def getCoordX(self):
		return self.__x
	def setCoordY(self,y):
		self.__y = y
	def getCoordY(self):
		return self.__y
	def setHealth(self,health):
		self.__health = health
	def getHealth(self):
		return self.__health
	def setAbilityNum(self,numb):
		self.__abilitynum = numb
	def getAbilityNum(self):
		return self.__abilitynum
	def setAbilityVar(self,var):
		self.__abilityvar = var
	def getAbilityVar(self):
		return self.__abilityvar
	def setLineNum(self,num):
		self.__lineNum = num
	def getLineNum(self):
		return self.__lineNum
##This is propietary software do not copy!
##This was made by Daniel Green
##Any copying will result in legal action!!
##I have way to much time on my hands

class GameEngine:
	def __init__(self, width=852, height=480):
		self.width = width
		self.height = height
		self.main = tk.Tk()
		self.main.geometry(str(self.width)+"x"+str(self.height))
	def __defaultCallback():
		print("Button Pressed!")
	def run(self):
		self.main.mainloop()
	def setBackgroundColor(self, color):
		self.main.configure(bg=color)
	def setWindowIcon(self, imageName):
		photo = tk.PhotoImage(file = imageName)
		self.main.iconphoto(False, photo)
	def setTitle(self, title):
		self.main.title(title)
	def setResizable(self, Value):
		self.main.resizable(Value, Value)
	## Building the UI
	def createButton(self, text="", fg="black", command=__defaultCallback,
			 height=3,
			 width=10,
			 font=("Courier",14)):
		return tk.Button(self.main, text=text, fg=fg, command=command,
				 height=height,
				 width=width,
				 font=font)
	def createText(self,text="",font=("Courier",14)):
		return tk.Label(self.main,text=text,font=font)
	def boundCheck(self, x,y,a,b,c,d):
	    final = False
	    if((a < x < c) and (b < y < d)):
		    final = True
	    else:
		    final = False
	    return final
	def delay(self, time, function):
		main = self.main
		main.after(time, function)
	def remove(self):
		self.main.destroy()
	def protocol(self,event, function):
		if(event == 'WindowClose'):
			self.main.protocol("WM_DELETE_WINDOW", function)
		else:
			pass
		return
	def input(self, function, keyType="ALL"):
		key = ''
		if(keyType == "ESCAPE"):
			key = '<Escape>'
		elif(keyType == "LEFTCLICK"):
			key = '<Button-1>'
		elif(keyType == "MOUSEMOVE"):
			key = '<Motion>'
		else:
			key = '<KeyPress>'
		self.main.bind(key, function)
	def playSound(self,soundName):
		winsound.PlaySound(soundName, winsound.SND_ALIAS | winsound.SND_ASYNC)
	def stopSound(self):
		winsound.PlaySound(None, winsound.SND_PURGE)


		
class Canvas:
	def __init__(self, root, width=852, height=480, bg="white"):
		self.root = root
		self.width = width
		self.height = height
		self.bg = bg
		self.photos = []
		self.items = []
		self.animation = []
		self.animationRunning = []
		self.currentAnimations = 0
		self.itemDict = {}
		self.tkItems = []
		self.canvas = tk.Canvas(root, height=self.height, width=self.width, bg=self.bg)
	def getLocation(self, item):
		final = 0
		try:
			x = self.canvas.coords(item.item)[0]
			y = self.canvas.coords(item.item)[1]
			final = (x,y)
		except:
			final = (0,0)
		return final
	def getDistance(self,id1, id2):
		x1, y1 = self.getLocation(id1)
		x2, y2 = self.getLocation(id2)
		calculate = sqrt(((x2-x1)**2) + ((y2-y1)**2))
		return calculate
	def create_rectangle(self, x, y, width, height, outline="black",tag=('all')):
		centerX = (self.width/2)
		centerY = self.height/2
		a = (centerX+x)-(width/2)
		b = ((centerY+y)-(height/2))
		c = ((centerX+x)+(width/2))
		d = ((centerY+y)+(height/2))
		final = self.canvas.create_rectangle(a,b,c,d,outline=outline,tag=tag)
		item = Item(final)
		return final
	def create_text(self,x,y,text="Edit Me!", fill="black",font=('Helvetica 15 bold')):
		return self.canvas.create_text(x+(self.width/2),y+(self.height/2),text=text,fill=fill,font=font)
	def updateText(self,item,text="Edit Me!"):
		self.canvas.itemconfig(item[0],text=text)
	def followMouse(self,item,x,y):
		x1,y1 = self.getLocation(item)
		x2 = x-x1
		y2 = y-y1
		self.move(x2,y2,item)
	def create_circle(self, x, y, radius):
		centerX = (self.width/2)
		centerY = self.height/2
		x = centerX+x
		y = centerY+y
		e = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius)
	def create_image(self, x, y, imageName, width=100, height=100,
			 player=False,
			 radius=0,
			 health=100,
			 doCollision=True,
			 collisionMesh="everyone"):
		x = (self.width/2)+x
		y = (self.height/2)+y
		c = tk.PhotoImage(file=imageName)
		w = c.width()
		h = c.height()
		scale_w = w/width
		scale_h = h/height
		d = radius
		if (scale_w > 1) and (scale_h > 1):
			c = c.subsample(round(abs(scale_w)), round(abs(scale_h)))
		elif (scale_w < 1) and (scale_h > 1):
			scale_w = width/w
			c = c.zoom(round(scale_w), 1)
			c = c.subsample(1, round(scale_h))
		elif (scale_w > 1) and (scale_h < 1):
			scale_h = height/h
			c = c.zoom(1, round(scale_h))
			c = c.subsample(round(scale_w), 1)
		else:
			scale_w = width/w
			scale_h = height/h
			c = c.zoom(round(scale_w), round(scale_h))
		w2 = c.width()
		h2 = c.height()
		self.photos.append(c)
		e = self.canvas.create_image(x, y, image=self.photos[-1],tags=(collisionMesh))
		bounds = self.canvas.bbox(e)
		try:
			x1 = bounds[3]-bounds[0]
			y1 = bounds[3]-bounds[1]
		except:
			x1 = 0
			y1 = 0
		if d == 0:
			if(x1 > y1):
				d = x1/2
			else:
				d = y1/2
		item = Item(e)
		item.setWidth(w2)
		item.setHeight(h2)
		item.setRadius(d)
		item.setPlayer(player)
		item.setCoordX(x)
		item.setCoordY(y)
		item.listIndex = len(self.items)+1
		item.setHealth(health)
		item.collisionMesh = collisionMesh
		if(doCollision == True):
			self.items.append(item)
			self.itemDict[e] = item
			self.tkItems.append(e)
		## [e,w2, h2,d, player, x, y,len(self.items),health]
		return item
	def __animate(self,item,images, ogImages,ms,animationNumb):
		c = next(images, "potato")
		if(c == "potato"):
			images = iter(ogImages)
			c = next(images)
			self.animation[animationNumb] = None
		w = c.width()
		h = c.height()
		width = item.getWidth()
		height = item.getHeight()
		scale_w = w/item.getWidth()
		scale_h = h/item.getHeight()
		if (scale_w > 1) and (scale_h > 1):
			c = c.subsample(round(abs(scale_w)), round(abs(scale_h)))
		elif (scale_w < 1) and (scale_h > 1):
			scale_w = width/w
			c = c.zoom(round(scale_w), 1)
			c = c.subsample(1, round(scale_h))
		elif (scale_w > 1) and (scale_h < 1):
			scale_h = height/h
			c = c.zoom(1, round(scale_h))
			c = c.subsample(round(scale_w), 1)
		else:
			scale_w = width/w
			scale_h = height/h
			c = c.zoom(round(scale_w), round(scale_h))
		w2 = c.width()
		h2 = c.height()
		self.animation[animationNumb] = c
		e = self.canvas.itemconfig(item.item, image=self.animation[animationNumb])
		root = self.root
		if(self.animationRunning[animationNumb] == True):
			root.after(ms, lambda: self.__animate(item,images ,ogImages,ms,animationNumb))
	def animateImage(self, item, ms,images):
		images2 = []
		for i in images:
			images2.append(tk.PhotoImage(file=i))
		images3 = iter(images2)
		root = self.root
		animationNumb = self.currentAnimations
		self.animation.append(None)
		self.animationRunning.append(True)
		root.after(ms, lambda: self.__animate(item,images3, images2,ms, animationNumb))
		self.currentAnimations += 1
		return animationNumb
	def stopAnimation(self,number):
		self.animationRunning[number] = False
	def stopAllAnimations(self):
		for i in range(len(self.animationRunning)):
			self.animationRunning[i] = False
	def delete(self,item):
		self.canvas.delete(item.item)
	def removeFromCollision(self,item):
		self.items.pop(item.listIndex)
	def destroy(self):
		self.canvas.destroy()
	def create_background(self, x, y, imageName, width=100, height=100):
		x = (self.width/2)+x
		y = (self.height/2)+y
		c = tk.PhotoImage(file=imageName)
		w = c.width()
		h = c.height()
		scale_w = w/width
		scale_h = h/height
		if (scale_w > 1) and (scale_h > 1):
			c = c.subsample(round(abs(scale_w)), round(abs(scale_h)))
		elif (scale_w < 1) and (scale_h > 1):
			scale_w = width/w
			c = c.zoom(round(scale_w), 1)
			c = c.subsample(1, round(scale_h))
		elif (scale_w > 1) and (scale_h < 1):
			scale_h = height/h
			c = c.zoom(1, round(scale_h))
			c = c.subsample(round(scale_w), 1)
		else:
			scale_w = width/w
			scale_h = height/h
			c = c.zoom(round(scale_w), round(scale_h))
		w2 = c.width() - (width/2)
		h2 = c.height() - (height/2)
		self.photos.append(c)
		e = self.canvas.create_image(x, y, image=self.photos[-1])
		return e
	async def backgroundCollision(self,playerItem,tag='eveyone'):
		final = False
		hitItem = None
		j = 0
		o = self.canvas.find_withtag(tag)
		o = list(o)
		try:
			o.remove(playerItem.item)
		except:
			pass
		playerBox = self.canvas.bbox(playerItem.item)
		coll = []
		for i in o:
		      radi = 0
		      if(playerItem.getRadius() > self.itemDict[i].getRadius()):
			      radi = playerItem.getRadius()
		      else:
			      radi = self.itemDict[i].getRadius()
		      if(self.getDistance(playerItem,self.itemDict[i]) <= radi):
			      final = True
			      hitItem = self.itemDict[i]
		l = 0
		for i in self.items:
			if(i == hitItem):
				j = l
			l += 1
		return [final,hitItem,j]
	def collision(self, playerItem,tag='everyone'):
		final = False
		hitItem = None
		j = 0
		o = self.canvas.find_withtag(tag)
		o = list(o)
		try:
			o.remove(playerItem.item)
		except:
			pass
		playerBox = self.canvas.bbox(playerItem.item)
		coll = []
		for i in o:
		      radi = 0
		      if(playerItem.getRadius() > self.itemDict[i].getRadius()):
			      radi = playerItem.getRadius()
		      else:
			      radi = self.itemDict[i].getRadius()
		      if(self.getDistance(playerItem,self.itemDict[i]) <= radi):
			      final = True
			      hitItem = self.itemDict[i]
		l = 0
		for i in self.items:
			if(i == hitItem):
				j = l
			l += 1
		return [final,hitItem,j]
	def showCollision(self, item):
		x = item[5]
		y = item[6]
		self.canvas.create_circle(x,y,item[3])
	def bindTag(self, obj, function, buttonType='LEFT'):
		button = ''
		if(buttonType == 'RIGHT'):
			button = '<Button-3>'
		if(buttonType == 'MIDDLE'):
			button = '<Button-2>'
		else:
			button = '<Button-1>'
		self.canvas.tag_bind(obj, button, lambda e: function)
	def bbox(self, item):
		bounds = self.canvas.bbox(item.item)
		a = bounds[0]
		b = bounds[1]
		c = bounds[2]
		d = bounds[3]
		return((a,b,c,d))
	def move(self, x, y, item):
		    self.canvas.move(item.item, x, y)
		    self.canvas.update()
	def hide(self):
		self.canvas.pack_forget()
	def pack(self):
		self.canvas.pack()

