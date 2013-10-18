#le3p-v0.1.3 - Advanced Config

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

from config import basicConfig
from config import displayConfig

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()

# This defines the layout of the machine.
# messing around in here will likely break things

from config import partSizes

ps = partSizes.partSizes()

class advancedConfig:
  #Globals
	minthick = 5
	
	#Beam
	beamSize = 1
	if bc.beamType == 'OpenBeam':
		beamSize = 15
		
	if bc.beamType == 'Misumi20mm':
		beamSize = 20
		
	#HotEnd
	hotEndDia = 1
	hotEndLen = 1
	hotEndSpacing = 1
	hotEndMountLen = 1
	if bc.hotEndType == 'E3Dv4':
		hotEndDia = 25
		hotEndLen = 70
		hotEndSpacing = 5
		hotEndMountLen = 12
	
	
	#Envelope Size
	envelopeX = bc.bedSizeX - hotEndDia - hotEndSpacing - bc.extraBed*2
	envelopeY = bc.bedSizeY - bc.extraBed*2
	envelopeZ = bc.buildSizeZ
	
	#Machine Location
	mXpos = dc.xPos - envelopeX/2
	mYpos = dc.yPos - envelopeY/2
	mZpos = envelopeZ - dc.zPos
	
	#Bushing Selection
	xBushing = [1,1,1]
	yBushing = [1,1,1]
	zBushing = [1,1,1]
	
	#xbushing
	if bc.BushingType == 'LM10LUU':
		xBushing = ps.lm10luu
		xcarriagesizex = xBushing[2] + minthick * 2
		
	if bc.BushingType == 'igusMSM101650':
		xBushing = ps.igusMSM101650
		xcarriagesizex = xBushing[2] + minthick * 2
		
	if bc.BushingType == 'Printed':
		xBushing = ps.printed
		xcarriagesizex = xBushing[2] + minthick * 2
	
	#ybushing	
	if bc.BushingType == 'LM10LUU':
		yBushing = ps.lm10luu
		ycarriagesizey = yBushing[2] + minthick * 2
		
	if bc.BushingType == 'igusMSM101650':
		yBushing = ps.igusMSM101650
		ycarriagesizey = yBushing[2] + minthick * 2
		
	if bc.BushingType == 'Printed':
		yBushing = ps.printed
		ycarriagesizey = yBushing[2] + minthick * 2
	
	#zbushing	
	if bc.BushingType == 'LM10LUU':
		zBushing = ps.lm10luu
		
	if bc.BushingType == 'igusMSM101650':
		zBushing = ps.igusMSM101650
		
	if bc.BushingType == 'Printed':
		zBushing = ps.printed
	
	#Belt Selection
	beltWidth = 1
	beltThick = 1
	
	if bc.beltType == 'GT2-2mm':
		beltWidth = 6
		beltThick = 2
	
	beltSpace = 3
	beltPath = 2
	
	gantryMotor = ps.nema17x48
	zMotor = ps.nema17x48
	#Motor Selection
	if bc.gantryMotorType == 'Nema17-42L':
		gantryMotor = ps.nema17x42
	if bc.gantryMotorType == 'Nema17-35L':
		gantryMotor = ps.nema17x35
		
	if bc.zMotorType == 'Nema17-42L':
		zMotor = ps.nema17x42
	if bc.zMotorType == 'Nema17-35L':
		zMotor = ps.nema17x35
	
	#Electronics
	RUMBAsize = [75,135,30]
	PowerSupplyASize = [214,113,50]
	PowerSupplyBSize = [214,113,50]
	
	
	
	#Variations
	xcarriagefacethick = 1
	if bc.xCarriageType == 'T-Slot':
		xcarriagefacethick = beamSize
	if bc.xCarriageType == 'One-Piece':
		xcarriagefacethick = 6
	
	#Gantry Linear Layout
	xrodlen = (envelopeX/2 + xcarriagesizex/2 + minthick*2 + (yBushing[1] - bc.gantryRodDia))*2 + beamSize + bc.gantryRodDia + bc.gantryPulleyDia*2 + minthick*6
	xrodzcenter = envelopeZ + hotEndLen + hotEndMountLen
	xrodspacing = 70
	xrodypos = hotEndDia/2 + xBushing[1]/2 + minthick + xcarriagefacethick
	if xrodypos > yBushing[2]/2 + minthick*3:
		tailadd = xrodypos
	else:
		tailadd = yBushing[2]/2 + minthick*3
	
	yrodlen = envelopeY + ycarriagesizey + beamSize*2 + (bc.gantryIdlerDia + beltThick*2 - beamSize) + minthick + tailadd
	yrodxpos = xrodlen/2 - beamSize/2 - bc.gantryRodDia/2
	yrodzpos = xrodzcenter - xrodspacing/2 + xBushing[1]/2 + bc.gantryRodDia/2 + minthick
	ybushingypos = xrodypos/1.25
	
	#bed
	bedThick = bc.heatPlateThick + bc.glassPlateThick + bc.heaterOffset + bc.basePlateThick + beamSize
	bedThickAlt = 0
	bedBushOffset = 6
	
	if zBushing[2] > bedThick:
		bedThickAlt = bedThick
		bedThick = zBushing[2] + minthick
	
	#Frame
	framebasedeep = 80
	frameheadtall = 0
	frameringazpos = - bedThick - framebasedeep + beamSize/2
	frameringbzpos = - bedThick - beamSize/2 - minthick
	frameringczpos = envelopeZ + frameheadtall + hotEndLen + xrodspacing/2 + xBushing[1]/2 + minthick*4 + beamSize - beamSize/2
	frameuprightslen = envelopeZ + bedThick + framebasedeep + frameheadtall + hotEndLen + xrodspacing/2 + xBushing[1]/2 + minthick*4 + beamSize
	frameringxlen = xrodlen - beamSize
	frameringylen = yrodlen - beamSize*2
	frameysupportszpos = yrodzpos - bc.gantryRodDia/2 - beamSize/2
	framezsupportszpos = xrodzcenter - xrodspacing/2 - bc.gantryRodDia/2 - beamSize/2 - minthick *2
	
	bedXBeamLen = frameringxlen + beamSize - minthick*2
	
	#Gantry Drive Layout
	gantrybcidlerspacing = 4
	gantrydrivecenter = xrodzcenter + xrodspacing/2 - xrodspacing/3
	gantrymotorxpos = yrodxpos + bc.gantryRodDia/2 - bc.gantryPulleyDia/2 - beltThick - beltSpace
	gantrymotorypos = frameringylen/2 + tailadd + gantryMotor[0]/2 + minthick
	gantrymotorzpos = gantrydrivecenter - gantryMotor[3]/2
	
	gantryaidlerxpos = gantrymotorxpos + (bc.gantryPulleyDia - bc.gantryIdlerDia)/2
	gantryaidlerypos = -frameringylen/2 + tailadd/2 - beamSize + ps.z624[1]/2 + beltThick + beltSpace
	gantryaidlerzpos = gantrydrivecenter
	
	gantrybidlerxpos = gantryaidlerxpos - bc.gantryIdlerDia - beltThick
	gantrybidlerypos = xrodypos - bc.gantryIdlerDia/2 - beltThick - beltSpace/2
	
	gantrycidlerxpos = gantryaidlerxpos - bc.gantryIdlerDia/2 - bc.gantryPulleyDia/2 - (bc.gantryPulleyDia - bc.gantryIdlerDia)/2 - beltThick
	gantrycidlerypos = xrodypos + bc.gantryIdlerDia/2 + beltThick + beltSpace/2 + gantrybcidlerspacing
	
	beltLen = (gantrymotorypos - gantryaidlerypos)*4 + (gantrybidlerxpos)*4
	
	#Z Stage
	zrodlen = framezsupportszpos - frameringazpos + beamSize
	zrodxpos = frameringxlen/2 - bc.gantryRodDia/2 
	zrodspacing = bc.zRodDia*2 + zMotor[0] + beamSize*2
	zrodzpos = frameringazpos - beamSize/2
	framezmotorsupportsspacing = zrodspacing - beamSize - bc.gantryRodDia
	
	zscrewlen = zrodlen - framebasedeep
	zscrewxpos = zrodxpos + bc.gantryRodDia/2 - zMotor[0]/2 - minthick
	zscrewzpos = -bedThick
	
	
	
