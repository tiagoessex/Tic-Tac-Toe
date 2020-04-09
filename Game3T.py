from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import *

from gameMecahnics import gameMecahnics		# game internal
from getPlayer import getPlayer

# collision shits
from pandac.PandaModules import CollisionTraverser
from pandac.PandaModules import CollisionNode


import sys										# for exit()

from pandac.PandaModules import ClockObject		# for FPS

from direct.gui.DirectGui import *				# gui shits - buttons
from panda3d.core import *


import math

STARTING_Z = 10 



class Game3T(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		#base.setFrameRateMeter(True)
		
		OnscreenText(text = '3T', pos = (0, 0.85), scale = 0.2, fg=(0.3,0.2,8,1))
		OnscreenText(text = 'by: Hellmaster - 2011', pos = (0, -0.9), scale = 0.1, fg=(0.5,0,8,1))
		
		FPS = 30
		globalClock = ClockObject.getGlobalClock()
		globalClock.setMode(ClockObject.MLimited)
		globalClock.setFrameRate(FPS)

		# ***************** SETUP SHITS *****************
		base.disableMouse()
		self.nextmove = True
		self.camera_plane_angle = 0
				
		# ***************** LOAD GAME LOGIC AND OTHERS CLASSES *************
		self.game = gameMecahnics()		
		
		
		# ***************** LOAD MODELS AND SOUNDS ******************
		self.loadModels()		
		self.loadSounds()
		
		
		
				
		
		
		# ***************** SELECT PLAYER ******************
		
		self.a=getPlayer()
		
		base.taskMgr.add(self.selectPlayer, "selectPlayer")

	
	def rotateCamera(self, task):
		dt = globalClock.getDt()
		self.camera_plane_angle += dt
		if self.camera_plane_angle >360:
			self.camera_plane_angle = 0		
		self.cam.setPos(30*math.cos(self.camera_plane_angle), 30*math.sin(self.camera_plane_angle),30)
		self.cam.lookAt(0,0,0)		
		return task.cont

	def selectPlayer(self,task):		
		self.player = self.a.getSelectedPlayer()
		if self.player != None:
			#print "player selectecd"
			base.taskMgr.add(self.gameLoop, "gameLoop")
			return task.done
		return task.cont

	


	def gameLoop(self,task):		
		#print "game task"


		# ***************** SET CAMERA ******************
					
		base.taskMgr.add(self.rotateCamera, "rotateCamera")

		self.game.setPlayer(self.player)

		
		# ***************** PICKABLE SHITS ***************
		# setup the pickable suqre planes on the board
		planes=[]	
		id_plane = 0
		for k in range (3):
			for i in range (3):
				#print "adding plane: ", id_plane
				p=addPlane(3)
				p.setPos(3*i-2.5,3*k-2.5,3.1)
				p.setTag('pickable', str(id_plane)) 
				p.hide()
				planes.append(p)
				id_plane += 1
						
		# set picks
		pickerNode = CollisionNode('mouseRay')
		pickerNP = self.cam.attachNewNode(pickerNode)
		pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
		self.pickerRay = CollisionRay()		
		pickerNode.addSolid(self.pickerRay)
		#pickerNP.show()
		self.rayQueue = CollisionHandlerQueue()
		self.cTrav = CollisionTraverser()		
		self.cTrav.addCollider(pickerNP, self.rayQueue)		
		
		# set action in case of pick
		self.accept('mouse1',self.picked)
		
	
	
		
	

	def loadModels(self):
		self.arena = loader.loadModel("models/arena/arena")
		self.arena.reparentTo(render)
		self.arena.setPos(0,0,0)		
		
		self.playero = loader.loadModel("models/players/o")
	
		self.playerx = loader.loadModel("models/players/x")

	def loadSounds(self):
		self.sound1 = loader.loadSfx("sounds/sound1.ogg")
		self.sound2 = loader.loadSfx("sounds/sound2.ogg")

	
	# detects if mouse picks some shit
	# if yes =>  set piece if valid and must wait 3 seconds for next move else do shit
	def picked(self):
		if base.mouseWatcherNode.hasMouse():
			mpos = base.mouseWatcherNode.getMouse()
			self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())				
			self.cTrav.traverse(render)
			if self.rayQueue.getNumEntries() > 0:
				self.rayQueue.sortEntries()
				pickedNP = self.rayQueue.getEntry(0).getIntoNodePath()
				if pickedNP.hasNetTag('pickable'):
					if self.nextmove:
						#print "picked: ", pickedNP, " | id 1: ", pickedNP.findNetTag('pickable'), " id 2: ", pickedNP.getNetTag('pickable')
						move = int(pickedNP.getNetTag('pickable'))
						if self.game.isValidMove(move):
							#print "------VALID------", move
							self.putPieceIN(move)
							self.game.setMove(move)							
							
							self.nextmove = False							
						#else:
							#print "------INVALID------"
					#self.game.printBoard()
					
					
					
	def changeNextMoveValue(self,task):
		self.nextmove = True
		return task.done

	def putPieceIN(self,pos):
		if self.game.getCurrentPlayer() == 'o':
			self.newPiece = self.playero.copyTo(render)
		else:
			self.newPiece = self.playerx.copyTo(render)
		base.taskMgr.add(self.falling, "falling")
		if pos == 0:
			self.newPiece.setPos(-3,-3,STARTING_Z)
			return 0
		if pos == 1:
			self.newPiece.setPos(0,-3,STARTING_Z)
			return 0
		if pos == 2:
			self.newPiece.setPos(3,-3,STARTING_Z)
			return 0
		if pos == 3:
			self.newPiece.setPos(-3,0,STARTING_Z)
			return 0
		if pos == 4:
			self.newPiece.setPos(0,0,STARTING_Z)
			return 0
		if pos == 5:
			self.newPiece.setPos(3,0,STARTING_Z)
			return 0
		if pos == 6:
			self.newPiece.setPos(-3,3,STARTING_Z)
			return 0
		if pos == 7:
			self.newPiece.setPos(0,3,STARTING_Z)
			return 0
		if pos == 8:
			self.newPiece.setPos(3,3,STARTING_Z)			
			return 0
		return -1

	
	def falling(self, task):
		dt = globalClock.getDt() 		
		self.newPiece.setZ(self.newPiece.getZ()-dt*10)
		if self.newPiece.getZ()<3:
			self.nextmove = True
			if self.game.isWinner() or self.game.isOver():
				self.gameOver()
			else:
				self.game.setNextPlayer()
			if self.game.getCurrentPlayer() == 'o':
				self.sound1.play()
			else:
				self.sound2.play()
			return task.done		
		return task.cont
			
		
	def gameOver(self):
		#print "--------------------------"
		#print "-------- GAME OVER -------"
		#print "--------------------------"
		if self.game.isWinner():			
			printWinner(self.game.getCurrentPlayer())
		else:
			printWinner(None)
		print "--------------------------"
		button_exit = DirectButton(text='Exit Game', pos=(0, 0, -0.4), scale=0.1, command=exitProg)
		



def exitProg():
	sys.exit()


def printWinner(winner):
	myFrame = DirectFrame(frameColor=(0.1, 0.1, 0.9, 1),
							frameSize=(-1, 1, -0.5, 0.5),
							pos=(0, 0, 0))
	myFrame['frameTexture'] = 'pics/frame.jpeg'
	myFrame.resetFrameSize()
	OnscreenText(text = 'Game Over', pos = (0, 0.1), scale = 0.3, fg=(1,0,0,1))
	
	if winner != None:
		if winner == 'x':
			OnscreenText(text = 'x wins', pos = (0, -0.2), scale = 0.2,fg=(1,0,0,1))
		else:
			OnscreenText(text = 'o wins', pos = (0, -0.2), scale = 0.2,fg=(1,0,0,1))
		
		
		

def addPlane(size):
	cm = CardMaker("plane")
	cm.setFrame(-size/2, size/2, -size/2, size/2)
	plane = render.attachNewNode(cm.generate())
	plane.setP(270)
	return plane
		


# Run the engine.
q=Game3T()
run()




