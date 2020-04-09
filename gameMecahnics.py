
import random


class gameMecahnics():
	def __init__(self):
		self.currentPlayer=None
		self.board=[]
		for i in range(9):
			self.board.append(None)

	def printBoard(self):
		count=0
		print 
		for i in range(0,8,3):
			print self.board[i],'\t',self.board[i+1],'\t',self.board[i+2]
			
	def setPlayer(self,player):
		self.currentPlayer = player
	
	def getCurrentPlayer(self):
		return self.currentPlayer
		
	def isValidMove(self, location):
		if self.board[location] == None:
			return True
		return False

	def setMove(self, location):
		self.board[location] = self.getCurrentPlayer()			
		return location
				

	def isWinner(self):
		if self.board[0] == self.getCurrentPlayer() and self.board[1] == self.getCurrentPlayer() and self.board[2] == self.getCurrentPlayer():
			return True
		if self.board[3] == self.getCurrentPlayer() and self.board[4] == self.getCurrentPlayer() and self.board[5] == self.getCurrentPlayer():
			return True
		if self.board[6] == self.getCurrentPlayer() and self.board[7] == self.getCurrentPlayer() and self.board[8] == self.getCurrentPlayer():
			return True
		if self.board[0] == self.getCurrentPlayer() and self.board[4] == self.getCurrentPlayer() and self.board[8] == self.getCurrentPlayer():
			return True
		if self.board[2] == self.getCurrentPlayer() and self.board[4] == self.getCurrentPlayer() and self.board[6] == self.getCurrentPlayer():
			return True	
		if self.board[0] == self.getCurrentPlayer() and self.board[3] == self.getCurrentPlayer() and self.board[6] == self.getCurrentPlayer():
			return True
		if self.board[1] == self.getCurrentPlayer() and self.board[4] == self.getCurrentPlayer() and self.board[7] == self.getCurrentPlayer():
			return True			
		if self.board[2] == self.getCurrentPlayer() and self.board[5] == self.getCurrentPlayer() and self.board[8] == self.getCurrentPlayer():
			return True			
		return False
		
	def setNextPlayer(self):
		if self.getCurrentPlayer() == 'x':
			self.setPlayer('o')
		else:
			self.setPlayer('x')

	def reset(self):
		self.currentPlayer=None
		self.board=[]
		for i in range(9):
			self.board.append(None)


	def isOver(self):
		if None in self.board:
			return False
		else:
			return True
