#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2019 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    runner.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @author  Jakob Erdmann
# @date    2009-03-26
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import time

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

'''
def generate_routefile():
    random.seed(42)  # make tests reproducible
    N = 3600  # number of time steps
    # demand per second from different directions
    pWE = 1. / 10
    pEW = 1. / 11
    pNS = 1. / 30
    with open("data/cross.rou.xml", "w") as routes:
        print("""<routes>
        <vType id="typeWE" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" \
guiShape="passenger"/>
        <vType id="typeNS" accel="0.8" decel="4.5" sigma="0.5" length="7" minGap="3" maxSpeed="25" guiShape="bus"/>

        <route id="right" edges="51o 1i 2o 52i" />
        <route id="left" edges="52o 2i 1o 51i" />
        <route id="down" edges="54o 4i 3o 53i" />""", file=routes)
        vehNr = 0
        for i in range(N):
            if random.uniform(0, 1) < pWE:
                print('    <vehicle id="right_%i" type="typeWE" route="right" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pEW:
                print('    <vehicle id="left_%i" type="typeWE" route="left" depart="%i" />' % (
                    vehNr, i), file=routes)
                vehNr += 1
            if random.uniform(0, 1) < pNS:
                print('    <vehicle id="down_%i" type="typeNS" route="down" depart="%i" color="1,0,0"/>' % (
                    vehNr, i), file=routes)
                vehNr += 1
        print("</routes>", file=routes)
'''
# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def run():#main part!!!
    """execute the TraCI control loop"""
    step = 0
    # we start with phase 2 where EW has green
    #traci.trafficlight.setPhase("0", 2)
    '''
    print(traci.trafficlight.getPhaseDuration("0"))
    print(traci.trafficlight.getPhase("0"))
    print(traci.trafficlight.getProgram("0"))
    print(traci.trafficlight.getRedYellowGreenState("0"))
    print(traci.trafficlight.getCompleteRedYellowGreenDefinition("0"))
    print()
    '''
    VehicleNumber = 0



    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
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


        
        step += 1

        #print(VehicleNumber)
    print(VehicleNumber)
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=True, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

def start_sim():
    #traci.start([sumoBinary, "-c", "osm.sumocfg",
    #                         "--tripinfo-output", "tripinfo.xml"])
    traci.start([sumoBinary, "-c", "osm.sumocfg"])                         
    run()
    

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')
    print(options.nogui)
    print(sumoBinary)

    # first, generate the route file for this simulation
    #generate_routefile()

    ## this is the normal way of using traci. sumo is started as a
    ## subprocess and then the python script connects and runs
    #traci.start([sumoBinary, "-c", "data/cross.sumocfg",
    #                         "--tripinfo-output", "tripinfo.xml"])
    #run()
    after_routefile()

    print("qqqqqqqqqqqqqqqqqqqqqqqqqq1")
    time.sleep(5)
    after_routefile()
    print("qqqqqqqqqqqqqqqqqqqqqqqqqqq2")