import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

def random_dur(default_dur, sigma=1):
	return np.random.normal(default_dur,sigma*np.ones(len(default_dur)),len(default_dur))

def evaluate():
	edit_net()
	#--> to sumo api
	return

def ga(default_dur):
	#parameters
	INIT_SIZE = 1000
	MAX_ITER = 10000
	SIGMA = 1
	P_CROSSOVER = 0.5
	P_MUTATION = 0.1

	#DEAP
	creator.create("FitnessMax",base.Fitness,weights=(1.0,)) #maximize traffic flow
	creator.create("Individual",list,fitness=creator.FitnessMax) #individuals are returned in list

	toolbox = base.Toolbox()
	toolbox.register("attr_item", random_dur, default_dur, SIGMA)
 	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_item)
 	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

 	toolbox.register("evaluate", evaluate)
 	toolbox.register("edit_net", edit_net)
 	toolbox.register("mate", tools.cxTwoPoint)
 	toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=SIGMA, indpb=0.1)
 	toolbox.register("select", tools.selTournament, tournsize=3)

 	pop = toolbox.population(n=INIT_SIZE)

 	hof = tools.HallofFame(1) #pick the best one
 	
 	pop,log = algorithms.eaSimple(pop,toolbox,cxpb=P_CROSSOVER,mutpb=P_MUTATION,ngen=MAX_ITER,halloffame=hof,verbose=True)

 	return hof


def get_default_TL(file_path):
	import xml.etree.ElementTree as ET

	tree = ET.ElementTree(file = file_path)
	net = tree.getroot()
	trafficLights = net.findall("tlLogic")

	id_TLs = []
	dur_TLs = []
	for tl in trafficLights:
		id_TLs.append(tl.attrib['id'])
		durations = [phase.attrib['duration'] for phase in tl]
		dur_TLs.append(durations)

	return id_TLs,dur_TLs

def edit_net(file_path,id_TLs,dur_TLs):
	import xml.etree.ElementTree as ET

	tree = ET.ElementTree(file = file_path)
	net = tree.getroot()
	#trafficLights = net.findall("tlLogic")

	for id in id_TLs:
		net.find('.//tlLogic[@id='+strid)



#get default phase duration from *.net.xml
MAP_PATH = "/home/zhenyuli/Sumo/2019-12-20-14-30-08/osm.net.xml"
id_TLs, dur_TLs = get_default_TL(MAP_PATH)

 best_solution = ga(dur_TLs,id_TLs)
 print(hof)
 print(hof.fitness.values)
