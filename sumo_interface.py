#sumo-interface

#from __future__ import absolute_import
#from __future__ import print_function

import os
import sys
import optparse
import random
import time

def start_sim(path,gui=False):
	# we need to import python modules from the $SUMO_HOME/tools directory
	if 'SUMO_HOME' in os.environ:
	    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	    sys.path.append(tools)
	else:
	    sys.exit("please declare environment variable 'SUMO_HOME'")

	from sumolib import checkBinary
	import traci

	if gui:
		sumoBinary = checkBinary('sumo-gui')
	else:
		sumoBinary = checkBinary('sumo')

	traci.start([sumoBinary, "-c", path,"--tripinfo-output","result.xml"])
	#traci.start([sumoBinary, "-c", path])


	#VehicleNumber = 0
	while traci.simulation.getMinExpectedNumber() > 0:
		traci.simulationStep()
		'''
		VehicleNumber += traci.inductionloop.getLastStepVehicleNumber("e1Detector_-51508352#1_0_2") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_51508352#1_0_1") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_376401312#0_0_4") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_376401312#0_1_5") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_362368395#9_1_6") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_362368395#9_0_7") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_344664988#1_0_8") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_-344664988#1_0_9") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_27222779#3_0_10") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_-27222779#3_0_11") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_134941607#2_0_12") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_147557400#0_1_13") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_147557400#0_0_14") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_-40317921#0_0_15") \
					+ traci.inductionloop.getLastStepVehicleNumber("e1Detector_40317921#0_0_16")
		'''
		

	traci.close()
	#return VehicleNumber
