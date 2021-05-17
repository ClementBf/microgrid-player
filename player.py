# python 3
# this class combines all basic features of a generic player
import numpy as np
import pandas as pd
import matplotlib
import pulp



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
		self.pmax= 1000*np.ones(self.horizon)
		self.lNF = np.zeros(self.horizon)
		self.HR = np.zeros(self.horizon)
		self.lHP = np.zeros(self.horizon)
		self.HDC = np.zeros(self.horizon)
		self.alpha = np.ones(self.horizon)

		df = pd.read_csv('data_center_scenarios.csv',sep=';')
		self.lIT= df['cons (kW)']

	def set_scenario(self, scenario_data):
		self.data = scenario_data

	def set_lNF(self):
		lNF = np.zeros(self.horizon)
		for i in range(self.horizon):
			lNF[i] = self.lIT[i] * (1.0 + 1.0 / (self.eer*self.deltat))
		self.lNF=lNF


	def set_prices(self, prices):
		self.prices = prices

	def compute_HR(self):
		HR = np.zeros(self.horizon)
		for i in range(self.horizon):
			HR[i] = self.lIT[i] * self.cop_cs/self.eer

		self.HR = HR

	def global_decision(self):
		lp = pulp.LpProblem('data_center', pulp.LpMinimize)
		lp.setSolver()
		alphao = {}
		for t in range(self.horizon):
			var_name = 'alphao_' + str(t)
			alphao[t] = pulp.LpVariable(var_name, 0.0, 1.0)

			constraint_name = "limitation_" + str(t)
			lp += self.cop_hp * self.deltat * alphao[t] * self.lIT[t] * (self.cop_cs/self.eer) / ((self.cop_hp - 1)*self.deltat)<=10
			constraint_name = "puissancemax_" + str(t)
			lp += self.lIT[t] + self.lIT[t] * (1.0 + 1.0 / (self.eer*self.deltat)) + alphao[t] * self.lIT[t] * self.cop_cs/self.eer / ((self.cop_hp - 1)*self.deltat) <= self.pmax[t]

		lp.setObjective(pulp.lpSum([(self.lIT[t]+self.lIT[t] * (1 + 1 / (self.eer*self.deltat)))*self.prices[t] +alphao[t] * self.lIT[t] * self.cop_cs/self.eer / ((self.cop_hp - 1)*self.deltat)*self.prices[t]
									-self.cop_hp * self.deltat * alphao[t] * self.lIT[t] * self.cop_cs/self.eer / ((self.cop_hp - 1)*self.deltat)*self.prices_hw[t] for t in range(self.horizon)]))
		lp.solve()

		for t in range(self.horizon):
			self.alpha[t] = alphao[t].varValue

	def compute_lHP(self):
		for i in range(self.horizon):
			self.lHP[i] = self.alpha[i] * self.HR[i] / ((self.cop_hp - 1)*self.deltat)

	def compute_HDC(self):
		for i in range(self.horizon):
			self.HDC[i] = self.cop_hp * self.deltat * self.lHP[i]

	def compute_all_load(self):
		load = np.zeros(self.horizon)
		for time in range(self.horizon):
		 	load[time]= self.lIT[time]+self.lNF[time]+self.lHP[time]
		return load

	def compute_bill(self):
		self.bill= np.sum((self.lIT+self.lNF)*self.prices +self.lHP*self.prices -self.HDC*self.prices_hw)

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
	mon_acteur.set_lNF()
	mon_acteur.compute_HR()
	mon_acteur.global_decision()
	mon_acteur.compute_lHP()
	mon_acteur.compute_HDC()
	load= mon_acteur.compute_all_load()
	print(load)
	print(mon_acteur.alpha)