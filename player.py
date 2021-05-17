# python 3
# this class combines all basic features of a generic player
import numpy as np
import pandas as pd
import matplotlib


class Player:

	def __init__(self):
		# some player might not have parameters
		self.parameters = 0
		self.horizon = 48
		self.eer = 4
		self.cop_cs = self.eer + 1
		self.cop_hp = 0.4 * (60 + 273) / 25
		self.prices_hw = np.random.rand(48)
		self.prices = np.random.rand(48)
		self.deltat=0.5

	def set_scenario(self, scenario_data):
		self.data = scenario_data

	def set_lNF(self):
		df_nf = (self.data).copy()
		lNF = np.zeros(self.horizon)
		for i in range(len(self.data)):
			lNF[i] = df_nf['cons (kW)'][i] * (1 + 1 / ((self.eer)*(self.deltat))
		self.lNF = lNF


	def set_prices(self, prices):
		self.prices = prices

	def compute_HR(self):
		HR = np.zeros(self.horizon)
		for i in range(len(self.data)):
			HR[i] = self.data['cons (kW)'][i] * self.cop_cs/self.eer

		self.HR = HR

	def compute_all_load(self):
		load = np.zeros(self.horizon)
		for time in range(self.horizon):
		 	load[time]=0
		return load

	def compute_lHP(self):
		self.lHP = np.zeros(self.horizon)
		for i in range(self.horizon):
			self.lHP[i] = self.alpha[i] * self.HR[i] / ((self.cop_hp - 1)*self.deltat)

	def compute_HDC(self):
		self.HDC = np.zeros(self.horizon)
		for i in range(self.horizon):
			self.HDC[i] = self.cop_hp * self.deltat * self.lHP[i]

	def compute_bill(self):
		self.bill= np.sum(self.data['cons (kW)']+self.lNF)*self.lambd +lHP(alpha,lIT,deltat)*lambd -HDC(alpha,lIT,deltat)*price)

	def take_decision(self, time):
		# TO BE COMPLETED
		return 0

	def compute_load(self, time):
		load = self.take_decision(time)
		# do stuff ?
		return load

	def reset(self):
		# reset all observed data
		pass

if __name__ =='__main__' :
	mon_acteur=Player()
	load_0=mon_acteur.compute_load(0)
	load_1=mon_acteur.compute_load(1)