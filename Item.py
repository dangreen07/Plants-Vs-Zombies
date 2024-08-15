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
