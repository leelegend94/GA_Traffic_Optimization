import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

from sumo_interface import start_sim

def random_dur(default_dur, sigma=1):
	default_dur = sum(default_dur,[])
	return np.clip(np.random.normal(default_dur,sigma*np.ones(len(default_dur)),len(default_dur)),1,60)

def evaluation(file_path,id_TLs,dur_TLs):
	edit_net(file_path,id_TLs,dur_TLs)
	#--> to sumo api


	#flow = start_sim("/home/lynn/workspace/Untitled Folder/GA_Traffic_Optimization/demo_sumo/osm.sumocfg")
	start_sim("/home/zhenyuli/workspace/GA_Traffic_Optimization/demo_sumo/osm.sumocfg")
	import xml.etree.ElementTree as ET
	from numpy import mean
	tree = ET.ElementTree(file = "/home/zhenyuli/workspace/GA_Traffic_Optimization/result.xml")
	trip_infos = tree.getroot()
	timeLoss = mean([float(trip.attrib['timeLoss']) for trip in trip_infos])

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
                for i in xrange(len(child)):
                    if child[i] > max:
                        child[i] = max
                    elif child[i] < min:
                        child[i] = min
            return offspring
        return wrapper
    return decorator



def ga(file_path,default_dur,id_TLs):
	#parameters
	INIT_SIZE = 1000
	MAX_ITER = 10000
	SIGMA = 1
	P_CROSSOVER = 0.5
	P_MUTATION = 0.1
	MIN = 1
	MAX = 60

	#DEAP
	creator.create("FitnessMin",base.Fitness,weights=(1.0,)) #maximize traffic flow
	creator.create("Individual",list,fitness=creator.FitnessMin) #individuals are returned in list

	toolbox = base.Toolbox()
	toolbox.register("attr_item", random_dur, default_dur, SIGMA)
	toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_item)
	toolbox.register("population", tools.initRepeat, list, toolbox.individual)

	toolbox.register("evaluate", evaluation, file_path,id_TLs)
	toolbox.register("edit_net", edit_net,file_path,id_TLs,dur_TLs)
	toolbox.register("start_sim",start_sim,file_path)
	toolbox.register("mate", tools.cxTwoPoint)
	toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=SIGMA, indpb=0.1)

	toolbox.decorate("mutate", checkBounds(MIN, MAX))# Bounds are still needed to be set.

	toolbox.register("select", tools.selTournament, tournsize=3)

	pop = toolbox.population(n=INIT_SIZE)

	hof = tools.HallOfFame(1) #pick the best one
	stats = tools.Statistics(lambda ind: ind.fitness.values)

	pop,log = algorithms.eaSimple(pop,toolbox,cxpb=P_CROSSOVER,mutpb=P_MUTATION,ngen=MAX_ITER,halloffame=hof,verbose=True)

	return hof


def get_default_duration(file_path):
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
	trafficLights = net.findall("tlLogic")

	tl_idx = [[tl.attrib['id'] for tl in trafficLights].index(id) for id in id_TLs]

	for i in tl_idx:
		nb_phase = len(trafficLights[i])
		for j in range(nb_phase):
			trafficLights[i][j].attrib["duration"] = str(dur_TLs.pop(0))
		#for j in range(len(dur_TLs[i])):
		#	trafficLights[i][j].attrib["duration"] = dur_TLs[i][j]

	tree.write(file_path)


#get default phase duration from *.net.xml
MAP_PATH = "/home/lynn/workspace/Untitled Folder/GA_Traffic_Optimization/demo_sumo/osm.net.xml"
#MAP_PATH = "/home/zhenyuli/workspace/GA_Traffic_Optimization/demo_sumo/osm.net.xml"
id_TLs, dur_TLs = get_default_duration(MAP_PATH)

best_solution = ga(MAP_PATH,dur_TLs,id_TLs)
print(hof)
print(hof.fitness.values)
