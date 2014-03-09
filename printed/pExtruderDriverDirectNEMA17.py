#le3p-v0.1.3 - pExtruderDriver.py

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
import FreeCAD, Part, math
from FreeCAD import Vector

from config import basicConfig
from config import advancedConfig
from config import displayConfig
from config import partSizes

from include.parts import CapHeadScrew
from include.parts import NemaMotor

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

motoroffset = -11

gearDia = 11.6
gearHubDia = 12.55
gearLen = 11
gearBore = 5
gearCenter = 8
gearClearance = 0.85

idleClearance = 0.65

supportBearingAngle = 28

filamentDia = 1.78

fittingDia = 10.2
fittingDepth = 6

lowerFittingDia = 10.2
lowerFittingDepth = 6

positionOnMachine = 0
if dc.forPrint == 1:
	positionOnMachine = 0
makeDual = 0



def ExtruderMotor():
	m = NemaMotor(ps.nema17x48)
	#m.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	m.rotate(Vector(0,0,0),Vector(0,1,0),90)
	m.translate(Vector(motoroffset,0,0))
	if positionOnMachine == 1:
		m.rotate(Vector(0,0,0),Vector(0,0,1),180)
		m.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	if makeDual == 1:
		m2 = m.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		m2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		m = m.fuse(m2)
	return m

def ExtruderScrews():
	#idle pivot screw
	ips = CapHeadScrew(l=20)
	ips.rotate(Vector(0,0,0),Vector(0,1,0),90)
	ips.translate(Vector(motoroffset+15,-15.5,-15.5))
	#mount screws
	ms = CapHeadScrew(l=20)
	ms.rotate(Vector(0,0,0),Vector(0,1,0),90)
	ms.translate(Vector(motoroffset+15,15.5,-15.5))
	ms = ms.fuse(ms.mirror(Vector(0,0,0),Vector(0,0,1)))
	
	es = ips.fuse(ms)
	return es

def ExtruderIdleScrew():
	ia = CapHeadScrew(l=12,d=4,hd=6.8,hh=2.75)
	ia.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	ia.translate(Vector(-5,-ps.z624[1]/2-filamentDia/2-gearDia/2,0))
	
	return ia
	
def ExtruderIdleBearing():
	b = Part.makeCylinder(ps.z624[1]/2,ps.z624[2])
	h = Part.makeCylinder(ps.z624[0]/2,ps.z624[2])
	b=b.cut(h)
	b.translate(Vector(0,0,-ps.z624[2]/2))
	b.rotate(Vector(0,0,0),Vector(0,1,0),90)
	b.translate(Vector(0,-ps.z624[1]/2,0))
	b.translate(Vector(0,-filamentDia/2-gearDia/2,0))
	if positionOnMachine == 1:
		b.rotate(Vector(0,0,0),Vector(0,0,1),180)
		b.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	if makeDual == 1:
		b2 = b.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		b2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		b = b.fuse(b2)
	return b
	
def ExtruderDriveGear():
	b = Part.makeCylinder(gearHubDia/2,gearLen)
	h = Part.makeCylinder(gearBore/2,gearLen)
	t=Part.makeTorus(gearDia/2+filamentDia/2,filamentDia/2)
	t.translate(Vector(0,0,gearCenter))
	b=b.cut(h.fuse(t))
	b.translate(Vector(0,0,-gearCenter))
	b.rotate(Vector(0,0,0),Vector(0,1,0),90)
	if positionOnMachine == 1:
		b.rotate(Vector(0,0,0),Vector(0,0,1),180)
		b.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	if makeDual == 1:
		b2 = b.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		b2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		b = b.fuse(b2)
	return b

#Printed

def ExtruderIdler():
	bb = Part.makeBox(15,11,36)
	lp = Part.makeCylinder(11/2,12)
	lp.rotate(Vector(0,0,0),Vector(0,1,0),90)
	lp.translate(Vector(0,11/2,0))
	#pivot clearance
	pc = Part.makeCylinder(11/2,12)
	pcb = Part.makeBox(12,24,12)
	pcb.translate(Vector(0,-12,0))
	pc = pc.fuse(pcb)
	pc = pc.makeFillet(5,[pc.Edges[18],pc.Edges[20]])
	pc.rotate(Vector(0,0,0),Vector(0,1,0),90)
	pc.translate(Vector(12,11/2,0))
	#bs
	bs = Part.makeCylinder(11/2,15)
	bs.rotate(Vector(0,0,0),Vector(0,1,0),90)
	bs.translate(Vector(0,21-ps.z624[1]/2-filamentDia/2-gearDia/2,15.5))
	
	bb=bb.fuse(lp)
	bb=bb.cut(pc)
	bb=bb.fuse(bs)
	bb.translate(Vector(-8,-21,-15.5))
	
	ei = bb
	return ei

def ExtruderDriver():
	bb = Part.makeBox(10,10,10)
	
	ed = bb
	return ed
