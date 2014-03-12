#le3p-v0.1.3 - Basic Configuration

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


class basicConfig():
    #important stuff
	exportpath = "/home/scott/Projects/eclipseworkspace/le3p/stls/%s"
	
	#Machine Size
	#bedSize is the size of the build surface: glass plate, garolite sheet, etc.
	#I've chosen 305mm as the default to be compatible with 1x1ft plates, for availabilty without custom cutting(in the US).
	#300mm should be fairly available in Metric land and will work fine with the same machine. 
	bedSizeX = 305
	bedSizeY = 305.5
	buildSizeZ = 250.5
	
	extraBed = 18 # This is to add a bit of border around the bed for clamping(added to all sides)
	
	gantryType = 'Hgantry' #UltiStyle or 'Hgantry'
	
	#Parts to Use
	beamType = 'OpenBeam'
	#beamType = 'Misumi20mm'

	hotEndType = 'DualE3Dv4'  #DualE3Dv4 Kraken
	
	extruderDriveType = 'DirectNEMA17' # 'DirectPG35'
	
	beltType = 'GT2-2mm'

	BushingType = 'LM10LUU'

	gantryPulleyDia = 13 # This is the pitch diameter of the pulleys you will use
	gantryIdlerDia = 13 # This is the diameter of your idler bearings
	gantryRodDia = 10 
	gantryMotorType = 'Nema17-48L'
	
	
	
	zRodDia = 10
	zScrewDia = 5
	zLeadNutDia = 7.85
	zLeadNutLen = 18
	zMotorType = 'Nema17-48L'
	
	glassPlateThick = 5
	heatPlateThick = 5
	heaterOffset = 12
	basePlateThick = 6
	
	#Variations
	#xCarriageType = 'T-Slot'
	xCarriageType = 'One-Piece'
	
	#Gantry EndStops size
	gantrySwitchX = 15
	gantrySwitchY = 7
	gantrySwitchZ = 15
	gantrySwitchScrewDia = 2.2
	gantrySwitchScrewSpacing = 6.25
	gantrySwitchScrewOffset = 5
	
	
	#Tolerances
	rodClearance = 1.5
	rodTolerance = 0.25
	bushingTolerance = 0.5
	beamTolerance = 0.5
	
	
