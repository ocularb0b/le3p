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

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

motoroffset = -8

gearDia = 11.6
gearHubDia = 12.55
gearLen = 11
gearBore = 5
gearCenter = 8
gearClearance = 0.85

idleClearance = 0.65

supportBearingAngle = 28

filamentDia = 1.75

fittingDia = 10.2
fittingDepth = 6

lowerFittingDia = 10.2
lowerFittingDepth = 6

positionOnMachine = 1
if dc.forPrint == 1:
	positionOnMachine = 0
makeDual = 1

def PG35GearStepper():
	n=[1,-1]
	facesize = 38
	facethick = 5
	bodydia = 35
	bodylen = 45
	mountscrewdia = 3.5
	mountscrewspacing = 42
	
	shaftdia = 5
	shaftlen = 8
	shaftpostdia = 10
	shaftpostlen = 4.7
	
	body = Part.makeCylinder(bodydia/2,bodylen)
	body.translate(Vector(0,0,-bodylen))
	
	faceblank = Part.makeBox(facesize,facesize,facethick)
	faceblank.translate(Vector(-facesize/2,-facesize/2,-facethick))
	faceblank.rotate(Vector(0,0,0),Vector(0,0,1),45)
	fb = faceblank.makeFillet(3,[faceblank.Edges[4],faceblank.Edges[6],faceblank.Edges[0],faceblank.Edges[2]])
	topcut = Part.makeBox(facesize*2,facesize,facethick)
	topcut.translate(Vector(-facesize,6,-facethick))
	fb = fb.cut(topcut)
	bottomcut = Part.makeBox(facesize*2,facesize,facethick)
	bottomcut.translate(Vector(-facesize,-12-facesize,-facethick))
	fb = fb.cut(bottomcut)
	
	for i in n:
		screw = Part.makeCylinder(mountscrewdia/2,facethick)
		screw.translate(Vector(mountscrewspacing/2*i,0,-facethick))
		fb=fb.cut(screw)
		
	sp = Part.makeCylinder(shaftpostdia/2,shaftpostlen)
	fb = fb.fuse(sp)
	
	sh = Part.makeCylinder(shaftdia/2,shaftpostlen+shaftlen)
	fb = fb.fuse(sh)
	
	pgs=body.fuse(fb)
	
	return pgs

def ExtruderMotor():
	m = PG35GearStepper()
	m.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	m.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	m.translate(Vector(gearDia/2+filamentDia/2,motoroffset,0))
	m.translate(Vector(-(filamentDia/2+gearDia/2+35/2),0,0))
	if positionOnMachine == 1:
		m.rotate(Vector(0,0,0),Vector(0,0,1),180)
		m.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	if makeDual == 1:
		m2 = m.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		m2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		m = m.fuse(m2)
	return m

def ExtruderSupportBearing():
	b = Part.makeCylinder(ps.z623[1]/2,ps.z623[2])
	h = Part.makeCylinder(ps.z623[0]/2,ps.z623[2])
	b=b.cut(h)
	b.translate(Vector(0,0,-ps.z623[2]/2))
	b.rotate(Vector(0,0,0),Vector(1,0,0),90)
	b.translate(Vector(gearDia/2+gearHubDia/2+ps.z623[1]/2+filamentDia/2,0,0))
	c=b.copy()
	b.rotate(Vector(gearDia/2+filamentDia/2,0,0),Vector(0,1,0),supportBearingAngle)
	c.rotate(Vector(gearDia/2+filamentDia/2,0,0),Vector(0,1,0),-supportBearingAngle)
	b = b.fuse(c)
	b.translate(Vector(-(filamentDia/2+gearDia/2+35/2),0,0))
	if positionOnMachine == 1:
		b.rotate(Vector(0,0,0),Vector(0,0,1),180)
		b.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	if makeDual == 1:
		b2 = b.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		b2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		b = b.fuse(b2)
	return b
	
def ExtruderIdleBearing():
	b = Part.makeCylinder(ps.z624[1]/2,ps.z624[2])
	h = Part.makeCylinder(ps.z624[0]/2,ps.z624[2])
	b=b.cut(h)
	b.translate(Vector(0,0,-ps.z624[2]/2))
	b.rotate(Vector(0,0,0),Vector(1,0,0),90)
	b.translate(Vector(-ps.z624[1]/2-filamentDia/2,0,0))
	b.translate(Vector(-(filamentDia/2+gearDia/2+35/2),0,0))
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
	b.translate(Vector(gearDia/2+filamentDia/2,0,-gearCenter))
	b.rotate(Vector(0,0,0),Vector(1,0,0),90)
	b.translate(Vector(-(filamentDia/2+gearDia/2+35/2),0,0))
	if positionOnMachine == 1:
		b.rotate(Vector(0,0,0),Vector(0,0,1),180)
		b.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	if makeDual == 1:
		b2 = b.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		b2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		b = b.fuse(b2)
	return b

#Printed

def ExtruderDriver():
	xsize = gearDia/2+35/2 + fittingDia/2 + ac.minthick/2+8
	ysize = -motoroffset+ps.z623[2]/2+ps.m4l[2]+ac.minthick/2
	zsize = 52
	ibx = ps.z623[1]+ac.minthick/2
	ibz = zsize - zsize/3 - 1
	
	d = Part.makeBox(xsize,ysize,zsize)
	d = d.makeFillet(ac.minthick,[d.Edges[1],d.Edges[3],d.Edges[10],d.Edges[11]])
	d.translate(Vector(-xsize+filamentDia/2+gearDia/2+35/2+8,motoroffset,-zsize/2))
	tc = Part.makeBox(xsize,ysize,gearHubDia+gearClearance*2)
	tc.translate(Vector(-xsize+filamentDia/2+gearDia/2+gearHubDia/2+gearClearance,motoroffset,-(gearHubDia+gearClearance*2)/2))
	tc = tc.makeFillet((gearHubDia+gearClearance*2)/2-0.01,[tc.Edges[5],tc.Edges[7]])
	fc = Part.makeBox(xsize,ysize,zsize/3)
	fc=fc.makeFillet(ac.minthick,[fc.Edges[4],fc.Edges[7],fc.Edges[8]])
	fc.translate(Vector(-xsize+filamentDia/2+gearDia/2+35/2,motoroffset+ac.minthick,gearHubDia/2+gearCenter+ac.minthick/2))
	fc=fc.fuse(fc.mirror(Vector(0,0,0),Vector(0,0,1)))
	#support bearing cuts
	sbc=Part.makeBox(xsize,ps.z623[2]+1,ps.z623[1]+idleClearance+0.4)
	sbc=sbc.makeFillet(ps.z623[1]/2,[sbc.Edges[3]])
	sbc.translate(Vector(gearHubDia-2,-(ps.z623[2]+1)/2,-(ps.z623[1]+idleClearance)-0.2))
	sbc = sbc.fuse(sbc.mirror(Vector(0,0,0),Vector(0,0,1)))
	#support bearing screws
	sbs=CapHeadScrew(l=14,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	sbs.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	sbs.translate(Vector(gearDia/2+gearHubDia/2+ps.z623[1]/2+filamentDia/2,ps.z623[2]+ac.minthick/2+1.2-ps.m3l[2],0))
	sbs.rotate(Vector(gearDia/2+filamentDia/2,0,0),Vector(0,1,0),supportBearingAngle)
	sbs = sbs.fuse(sbs.mirror(Vector(0,0,0),Vector(0,0,1)))
	#fittings
	zpos = 0
	fthick = 8
		#add
	ufa = Part.makeCylinder(fittingDia/2+fthick/2,15)
	ufa.translate(Vector(0,0,zsize/2 - 15))
	ufa = ufa.makeFillet(fittingDia/2+ac.minthick/2-0.01,[ufa.Edges[2]])
	ufa = ufa.makeFillet(ac.minthick/3,[ufa.Edges[2]])
	lfa = Part.makeCylinder(lowerFittingDia/2+fthick/2,15)
	lfa.translate(Vector(0,0,-zsize/2))
	lfa = lfa.makeFillet(lowerFittingDia/2+ac.minthick/2-0.01,[lfa.Edges[0]])
	lfa = lfa.makeFillet(ac.minthick/3,[lfa.Edges[2]])
	
			
		#cut
	ufc = Part.makeCylinder(fittingDia/2,fittingDepth)
	ufc.translate(Vector(0,0,zsize/2 - fittingDepth))
	lfc = Part.makeCylinder(lowerFittingDia/2,lowerFittingDepth)
	lfc.translate(Vector(0,0,-zsize/2 ))
	#Motor Mount Screws
	mms = Part.makeCylinder(ps.m3l[0]/2-0.3,16)
	mms.rotate(Vector(0,0,0),Vector(1,0,0),90)
	mms.translate(Vector(gearDia/2+filamentDia/2,0,21))
	mms = mms.fuse(mms.mirror(Vector(0,0,0),Vector(0,0,1)))
	#Filament Path
	fp = Part.makeCylinder(filamentDia/2+0.35,400)
	fp.translate(Vector(0,0,-200))
	fpc=Part.makeCone(filamentDia,filamentDia/2,filamentDia*2)
	fpc.translate(Vector(0,0,gearHubDia/2+gearClearance))
	fpc = fpc.fuse(fpc.mirror(Vector(0,0,0),Vector(0,0,1)))
	fp=fp.fuse(fpc)
	#Mount Screws
	ms = CapHeadScrew(l=12,d=ps.m3l[0]+0.2,hd=ps.m3l[1],hh=ps.m3l[2]-3,cut=1)
	ms.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	ms.translate(Vector(filamentDia/2+gearDia/2+35/2-ps.m3l[2]+6,0,zsize/2-ac.minthick))
	ms = ms.fuse(ms.mirror(Vector(0,0,0),Vector(0,0,1)))
	if ac.beamSize < ysize:
		ms.translate(Vector(0,(ysize-ac.beamSize),0))
	#	idle clamp screws insert clearance
	icicl = Part.makeCylinder(ps.m3i[0]/2+0.5,xsize)
	icicl.translate(Vector(0,0,-40-ps.m3i[1]))
	icicl.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	icicl.translate(Vector(0,ysize/2-ac.minthick/1.5,ibz/2-ac.minthick/1.5))
	icicl = icicl.fuse(icicl.mirror(Vector(0,0,0),Vector(0,1,0)))
	icicl = icicl.fuse(icicl.mirror(Vector(0,0,0),Vector(0,0,1)))
	
	#	idle clamp screw inserts
	icic = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	icic.translate(Vector(0,0,-ps.m3i[1]-3))
	icic.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	icic.translate(Vector(0,ysize/2-ac.minthick/1.5,ibz/2-ac.minthick/1.5))
	icic = icic.fuse(icic.mirror(Vector(0,0,0),Vector(0,1,0)))
	icic = icic.fuse(icic.mirror(Vector(0,0,0),Vector(0,0,1)))
	
	#Back Fat Cut
	bfc = Part.makeBox(xsize,ysize,zsize)
	bfc.translate(Vector(-xsize/2,motoroffset-ysize,-zsize/2))
	
	d = d.cut(tc)
	d = d.makeFillet(ac.minthick,[d.Edges[28],d.Edges[16]])
	d = d.cut(fc)
	d = d.makeFillet(ac.minthick/2,[d.Edges[59],d.Edges[61]])
	d = d.cut(sbc)
	d = d.cut(sbs)
	d = d.fuse(ufa.fuse(lfa))
	d = d.cut(ufc.fuse(lfc))
	d = d.cut(fp)
	d = d.cut(ms)
	d = d.cut(icicl)
	d = d.cut(icic)
	d = d.cut(mms)
	d = d.cut(bfc)
	
	#idle block
	ib = Part.makeBox(ibx,ysize,ibz)
	ib = ib.makeFillet(ac.minthick/2,[ib.Edges[8],ib.Edges[9],ib.Edges[10],ib.Edges[11]])
	ib.translate(Vector(-ibx-ac.minthick/3+1,motoroffset,-ibz/2))
	ibc = Part.makeBox(ibx,ysize,ibz/2)
	ibc = ibc.makeFillet(ac.minthick+0.5,[ibc.Edges[3]])
	ibc.translate(Vector(-filamentDia*2-ps.z623[1]/2,motoroffset,gearHubDia/2-0.5))
	ibc = ibc.fuse(ibc.mirror(Vector(0,0,0),Vector(0,0,1)))
	ib=ib.cut(ibc)
	ib.translate(Vector(-1.5,0,0))
	ib = ib.makeFillet(gearHubDia/2-0.01,[ib.Edges[36],ib.Edges[37]])
	#	idle bearing cut
	ibbc = Part.makeCylinder(ps.z624[1]/2+idleClearance,ps.z624[2]+1.5)
	ibbc.translate(Vector(0,0,-(ps.z624[2]+1.5)/2))
	ibbc.translate(Vector(-ps.z624[1]/2-filamentDia/2,0,0))
	ibbc.rotate(Vector(0,0,0),Vector(1,0,0),90)
	ib=ib.cut(ibbc)
	#	idle bearing window
	ibw = Part.makeBox(ps.z624[1],ps.z624[2]+1.5,ps.z624[1]/2)
	ibw.translate(Vector(-ps.z624[1]/2-filamentDia/2-ps.z624[1],-(ps.z624[2]+1.5)/2,-(ps.z624[1]/2)/2))
	ib=ib.cut(ibw)
	#	idle screw cut
	isc = CapHeadScrew(l=14,d=ps.m4l[0],hd=ps.m4l[1],hh=ps.m4l[2],cut=1)
	isc.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	isc.translate(Vector(-ps.z624[1]/2-filamentDia/2,ysize/2-ps.m4l[2],0))
	ib = ib.cut(isc)
	#	idle clamp screws cut
	icsc = Part.makeCylinder(ps.m3l[0]/2+0.1,80)
	icsc.translate(Vector(0,0,-40))
	icsc.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	icsc.translate(Vector(0,ysize/2-ac.minthick/1.5,ibz/2-ac.minthick/1.5))
	icsc = icsc.fuse(icsc.mirror(Vector(0,0,0),Vector(0,1,0)))
	icsc = icsc.fuse(icsc.mirror(Vector(0,0,0),Vector(0,0,1)))
	ib = ib.cut(icsc)
	d = d.cut(icsc)
	
	
	if dc.forPrint == 1:
		d.rotate(Vector(0,0,0),Vector(0,1,0),90)
		d.translate(Vector(0,0,xsize+filamentDia/2-ac.beamSize/2-0.1))
		ib.translate(Vector(ps.z623[1]+ac.minthick-0.333,-18,0))
		ib.rotate(Vector(0,0,0),Vector(0,1,0),-90)
		ds = d.fuse(ib)
		if makeDual == 1:
			ds = ds.fuse(ds.mirror(Vector(0,ac.beamSize-ac.minthick,0),Vector(0,1,0)))
		return ds
	else:
		d.translate(Vector(-(filamentDia/2+gearDia/2+35/2),0,0))
		ib.translate(Vector(-(filamentDia/2+gearDia/2+35/2),0,0))
		ds = d.fuse(ib)
	
	
	if positionOnMachine == 1:
		ds.rotate(Vector(0,0,0),Vector(0,0,1),180)
		ds.translate(Vector(ac.frameringxlen/2+ac.beamSize+ac.minthick+3,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2+0.5,(ac.frameringczpos+ac.framezsupportszpos)/2+ac.minthick*3))
	
	if makeDual == 1:
		ds2 = ds.mirror(Vector(ac.frameringxlen/2+ac.beamSize/2,0,0),Vector(1,0,0))
		ds2.rotate(Vector(ac.frameringxlen/2+ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,0),Vector(0,0,1),90)
		ds = ds.fuse(ds2)
	return ds
