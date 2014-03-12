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
	showAll = 0
	
	# Machine Position
	xPos = 267/2
	yPos = 269.5/2
	zPos = 65#250

	# Items to display ############################################################################################
	# Group Toggles
	showPrintedParts = 1
	showManufacturedParts = 1
	showExtruderParts = 0
	showBedSurface = 0
	showFrame = 0
	showElectronics = 1
	
	# Printed Part Toggles
	showXCarriage = 0
	showXEnds = 0
	showYEndsIdle = 0
	showYEndsMotor = 0
	showZEndsUpper = 0
	showGantryMotorMounts = 0
	showZMotorMounts = 0
	showZCarriage = 0
	showToolHolder = 0
	showExtruderDriver = 0
	showExtruderIdler = 0
	
	#	Frame Brackets
	showSmallCornerBrackets = 0
	#	Bits
	showYStop = 0
	showXStop = 0
	showHotEndFanMount = 1
	showNozzleFanShroud = 0
	showPowerSupplyAMount = 0
	showRumbaMount = 0
	showRumbaFanMount = 0
	showControllerArm = 0
	showLedBracket = 0
	showLedPowerSupplyBracket = 0
	showDimmerMount = 0
	showVertConduit = 0
	showDialIndicatorHolder = 0
	
	
	
	# Frame Toggles
	showFrameUprights = 1
	showFrameRingA = 0
	showFrameRingB = 0
	showFrameRingC = 1
	showFrameYRodSupports = 1
	showFrameZRodSupports = 1
	showFrameZMotorSupports = 0

	# Part Toggles
	showHotEnds = 1
	showHotEndFan = 1
	showNozzleFan = 0
	
	# Gantry Parts
	showXRods = 0
	showXBushings = 0
	showYRods = 0
	showYBushings = 0
	
	showGantryMotors = 0
	showGantryAIdlers = 0  
	showGantryBIdlers = 0
	showGantryCIdlers = 0
	showGantryBelt = 0
	
	# Ulti Gantry Parts
	showUgXLiveBearing = 1
	showUgXDeadBearing = 1
	showUgYLiveBearing = 1
	showUgYDeadBearing = 1
	
	showUgXCarriageRod = 1
	showUgYCarriageRod = 1
	
	showUgXPullies = 1
	showUgYPullies = 1
	
	# Z Stage
	showZRods = 0
	showZScrews = 0
	showZMotors = 0
	showZBushings = 0
	showZLeadNuts = 0
	
	# Extruder Parts
	showExtruderIdleBearing = 1
	showExtruderMotor = 1
	showExtruderDriveGear = 1
	showExtruderSupportBearing = 0
	showExtruderScrews = 1
	showExtruderIdleScrew = 1
	
	
	# Electronics Toggles
	showPowerSupplies = 0
	showControlBoard = 0
	
	
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
	
	print2R = 0.2
	print2G = 0.2
	print2B = 0.2
	print2A = 50
