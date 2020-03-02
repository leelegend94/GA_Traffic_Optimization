# GA_Traffic_Optimization
Optimize traffic condition by using genetic algorithm.

## Simulation Environment
We chose SUMO as the traffic simulator for the project. SUMO is an open source traffic simulator implemented by DLR. Read more about the simulator: https://sumo.dlr.de/docs/

## How to run?
It is recommend to use Linux. Otherweise you may encounter with some problems about SUMO.

### prerequistes
#### Install SUMO
The latest version of SUMO is required

	sudo add-apt-repository ppa:sumo/stable
	sudo apt-get update
	sudo apt-get install sumo sumo-tools sumo-doc

#### Install DEAP
DEAP is a novel evolutionary computation framework for rapid prototyping and testing of ideas. Read more: https://deap.readthedocs.io/en/master/

	pip3 install deap

### Setup your map
If you only want to test the code with the default map from Wuhan, you can just skip this part.

Please follow this tutorial https://sumo.dlr.de/docs/Tutorials/OSMWebWizard.html to configure and download your own map.

### Run
	python3 traffic_opt.py <path-to-your-map-files>
you can leave the path argument empty, so that the default map is used.

There is a jupyter notebook version available, you can find it in the folder deprecated.