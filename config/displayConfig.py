#le3p-v0.1.3 - display Configuration

# le3p - A larger envelope, t-slot extrusion based, H-Gantry 3D printer.
#
# Copyright (c) 2013 Scott Maher scott.a.maher@gmail.com
#
# This file is part of le3p

# le3p is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# le3p is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with le3p.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import sys

#from config import advancedConfig
#ac = advancedConfig.advancedConfig()

class displayConfig:
# STL generation ##############################################################################################
	doSTLexport = 1
	# Display #####################################################################################################
	printedOnly = 0 #will only export STL's for printed parts
	forPrint = 0 #will turn off all but printed parts and place for printing
	noMirror = 0
	showAll = 1
	
	# Machine Position
	xPos = 239/2
	yPos = 269/2
	zPos = 125#250

	# Items to display ############################################################################################
	# Group Toggles
	showPrintedParts = 1
	showManufacturedParts = 1
	showExtruderParts = 1
	showBedSurface = 1
	showFrame = 1
	showElectronics = 1
	
	# Printed Part Toggles
	showXCarriage = 1
	showXEnds = 1
	showYEndsIdle = 1
	showYEndsMotor = 1
	showZEndsUpper = 1
	showGantryMotorMounts = 1
	showZMotorMounts = 1
	showZCarriage = 1
	showToolHolder = 1
	showExtruderDriver = 1
	showExtruderDriverMount = 1
	#	Frame Brackets
	showSmallCornerBrackets = 1
	#	Bits
	showCableGuides = 0
	showCableClips = 0
	showYStop = 0
	showHotEndFanMount = 0
	showPowerSupplyAMount = 1
	showRumbaMount = 1
	showRumbaFanMount = 0
	showControllerArm = 0
	
	
	
	# Frame Toggles
	showFrameUprights = 1
	showFrameRingA = 1
	showFrameRingB = 1
	showFrameRingC = 1
	showFrameYRodSupports = 1
	showFrameZRodSupports = 1
	showFrameZMotorSupports = 1

	# Part Toggles
	showHotEnds = 1
	
	# Gantry Parts
	showXRods = 1
	showXBushings = 1
	showYRods = 1
	showYBushings = 1
	
	showGantryMotors = 1
	showGantryAIdlers = 1
	showGantryBIdlers = 1
	showGantryCIdlers = 1
	showGantryBelt = 1
		
	# Z Stage
	showZRods = 1
	showZScrews = 1
	showZMotors = 1
	showZBushings = 1
	showZLeadNuts = 1
	
	# Extruder Parts
	showExtruderIdleBearing = 1
	showExtruderMotor = 1
	showExtruderDriveGear = 1
	showExtruderSupportBearing = 1
	
	
	# Electronics Toggles
	showPowerSupplies = 1
	showControlBoard = 1
	
	
	# Part Colors #################################################################################################
	rodsR = 0.4
	rodsG = 0.4
	rodsB = 0.5
	
	bushingsR = 1.0
	bushingsG = 1.0
	bushingsB = 0.0
	
	frameR = 0.8
	frameG = 0.8
	frameB = 0.8
	
	beltR = 0.2
	beltG = 0.2
	beltB = 0.2
	
	print1R = 0.0
	print1G = 0.1568
	print1B = 0.4078
	#print1R = 0.2
	#print1G = 0.8
	#print1B = 0.3
	print1A = 0
	
	print2R = 0.6
	print2G = 0.6
	print2B = 0.6
	print2A = 0
