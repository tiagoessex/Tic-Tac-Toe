

from direct.gui.DirectGui import *				# gui shits - buttons
from panda3d.core import *


class getPlayer():
	def __init__(self):
		self.setMenu()
		self.currentplayer=None
		
	def setMenu(self):	
	
		text = TextNode('sslect_player')
		text.setText("SELECT PIECE")
		self.textNodePath = aspect2d.attachNewNode(text)
		self.textNodePath.setScale(0.20)
		text.setTextColor(1,0,1,1)
		self.textNodePath.setPos(-0.6,0,0.6)
		
		self.buttonX = DirectButton(pos=(-0.5, 0, 0), command=self.playerSelected,extraArgs=['x'])		
		self.buttonX['image']='pics/x.png'
		self.buttonX['image_scale']=0.4
		self.buttonX['borderWidth']=(0,0)	
		self.buttonX.resetFrameSize()
		
		self.buttonO = DirectButton(pos=(0.5, 0, 0), command=self.playerSelected,extraArgs=['o'])		
		self.buttonO['image']='pics/o.png'
		self.buttonO['image_scale']=0.4
		self.buttonO['borderWidth']=(0,0)
		self.buttonO.resetFrameSize()
	
	def playerSelected(self,player):		
		self.buttonX.destroy()
		self.buttonO.destroy()
		self.textNodePath.removeNode()
		self.currentplayer = player
		print "------------------------- ", player
	
	def getSelectedPlayer(self):
		return self.currentplayer




