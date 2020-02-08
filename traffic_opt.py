import numpy as np
import copy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from sumo_interface import start_sim

def random_dur(default_dur, sigma=1):
	default_dur = sum(default_dur,[])
	result =  np.clip(np.random.normal(default_dur,sigma*np.ones(len(default_dur)),len(default_dur)),0.5,60)
	#print("generated: ",result)
	return result

def evaluation(file_path,id_TLs,dur_TLs_):
	dur_TLs = copy.deepcopy(dur_TLs_)
	#print("eval ind: ",dur_TLs)
	edit_net(file_path,id_TLs,dur_TLs)
	#--> to sumo api

	#start_sim("/home/lynn/workspace/Untitled Folder/GA_Traffic_Optimization/demo_sumo/osm.sumocfg")
	start_sim(file_path+"/osm.sumocfg")
	import xml.etree.ElementTree as ET
	from numpy import mean
	tree = ET.ElementTree(file = "/home/lin/workspace/GA/GA_Traffic_Optimization/result.xml")
	#tree = ET.ElementTree(file = "/home/zhenyuli/workspace/GA_Traffic_Optimization/result.xml")
	trip_infos = tree.getroot()
	timeLoss = mean([float(trip.attrib['timeLoss']) for trip in trip_infos.findall("tripinfo")])

	print("##############################################################")
	print("##############################################################")
	print("avg time loss: ", timeLoss)
	print("##############################################################")
	print("##############################################################")
	return timeLoss,

def checkBounds(min, max):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for child in offspring:
                for i in range(len(child)):
                    if child[i] > max:
                        child[i] = max
                    elif child[i] < min:
                        child[i] = min
            return offspring
        return wrapper
    return decorator
'''
def printsel():
    def decorator(func):
        def wrapper(*args, **kargs):
            print(*args)
            result = func(*args, **kargs)
            print("selected",result)
            return result
        return wrapper
    return decorator
'''
def ga(file_path,default_dur,id_TLs):
	#parameters
	INIT_SIZE = 6
	MAX_ITER = 2
	SIGMA = 1
	P_CROSSOVER = 0.5
	P_MUTATION = 0.1
	MIN = 0.5
	MAX = 60

	#DEAP
	creator.create("FitnessMin",base.Fitness,weights=(-1.0,)) 
	creator.create("Individual",list,fitness=creator.FitnessMin) #individuals are returned in list

	toolbox = base.Toolbox()
	toolbox.register("attr_item", random_dur, default_dur, SIGMA)
	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_item)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluation, file_path,id_TLs)
	toolbox.register("edit_net", edit_net,file_path,id_TLs,dur_TLs)
	toolbox.register("start_sim",start_sim,file_path)
	toolbox.register("mate", tools.cxOnePoint)
	#toolbox.register("mate", crossover)23.789012557077626
	toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=SIGMA, indpb=0.1)
	toolbox.decorate("mutate", checkBounds(MIN, MAX))# Bounds are still needed to be set.

	toolbox.register("select", tools.selTournament, tournsize=5)
	#toolbox.decorate("select", printsel())

	pop = toolbox.population(n=INIT_SIZE)

	hof = tools.HallOfFame(1) #pick the best one
	stats = tools.Statistics(lambda ind: ind.fitness.values)
	stats.register("avg", np.mean)
	stats.register("std", np.std)
	stats.register("min", np.min)
	stats.register("max", np.max)

	pop,log = algorithms.eaSimple(pop,toolbox,cxpb=P_CROSSOVER,mutpb=P_MUTATION,ngen=MAX_ITER,stats=stats,halloffame=hof,verbose=True)

	return hof,log


def get_default_duration(file_path):
	import xml.etree.ElementTree as ET

	tree = ET.ElementTree(file = file_path+"/osm.net.xml")
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

	tree = ET.ElementTree(file = file_path+"/osm.net.xml")
	net = tree.getroot()
	trafficLights = net.findall("tlLogic")

	tl_idx = [[tl.attrib['id'] for tl in trafficLights].index(id) for id in id_TLs]

	for i in tl_idx:
		nb_phase = len(trafficLights[i])
		for j in range(nb_phase):
			trafficLights[i][j].attrib["duration"] = str(dur_TLs.pop(0))
		#for j in range(len(dur_TLs[i])):
		#	trafficLights[i][j].attrib["duration"] = dur_TLs[i][j]

	tree.write(file_path+"/osm.net.xml")


#get default phase duration from *.net.xml
MAP_PATH = "/home/lin/workspace/GA/GA_Traffic_Optimization/wuhan"
#MAP_PATH = "/home/zhenyuli/workspace/GA_Traffic_Optimization/wuhan"
id_TLs, dur_TLs = get_default_duration(MAP_PATH)

best_solution,log = ga(MAP_PATH,dur_TLs,id_TLs)
print("best solution is: ",best_solution[0])
print("best time loss", best_solution[0].fitness.values)

gen = log.select("gen")
fit_mins = log.select("avg")
import plotly.graph_objects as go
import numpy as np

#x = np.arange(10)

fig = go.Figure(data=go.Scatter(x=gen, y=fit_mins, mode='lines+markers'))
fig.update_layout(title='The performance of GA')
fig.show()