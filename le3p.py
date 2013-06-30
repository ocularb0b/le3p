#le3p v0.1.3

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
from FreeCAD import Matrix

from include.parts import E3Dv4
from include.parts import BoxExtrusion
from include.parts import CapHeadScrew
from include.parts import NemaMotor
from include.parts import TimingGear
from include.parts import StraightBushing
from include.parts import Bearing
from include.shapes import regPolygon
from include.shapes import BeltCorner
from include.shapes import TSlot
from include.shapes import RodClampSlice
from include.shapes import FilletFlange

test = FreeCAD.activeDocument()
if test == None:
  clear = 0
else:
	clear = 1

from config import basicConfig
from config import advancedConfig
from config import displayConfig
from config import partSizes

from assemblies import aBed 

from printed import pXCarriage
from printed import pXEnds
from printed import pYEnds
from printed import pZEnds
from printed import pGantryMotorMount
from printed import pZMotorMount
from printed import pBits
from printed import pZCarriage
from printed import pToolHolder
from printed import pExtruderDriver
from printed import pCornerBracket

if clear == 1:
	reload(basicConfig)
	reload(displayConfig)
	reload(advancedConfig)
	reload(partSizes)
	reload(aBed)
	reload(pXCarriage)
	reload(pXEnds)
	reload(pYEnds)
	reload(pZEnds)
	reload(pGantryMotorMount)
	reload(pZMotorMount)
	reload(pZCarriage)
	reload(pToolHolder)
	reload(pExtruderDriver)
	reload(pBits)
	reload(pCornerBracket)

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

# Preprocess
if dc.forPrint == 1:
	dc.showBedSurface = 0
	dc.showElectronics = 0
	dc.showFrame = 0
	dc.showManufacturedParts = 0
	dc.showExtruderParts = 0


# Layout Functions ###################################################################################################

# Manufactured Parts
def HotEndsLayout():
	t1 = E3Dv4()
	t1.translate(Vector(-ac.hotEndDia/2 - ac.hotEndSpacing/2,0, ac.hotEndLen))
	t1.translate(Vector(ac.mXpos, ac.mYpos, ac.envelopeZ))

	t2 = E3Dv4()
	t2.translate(Vector(ac.hotEndDia/2 + ac.hotEndSpacing/2,0, ac.hotEndLen))
	t2.translate(Vector(ac.mXpos, ac.mYpos, ac.envelopeZ))
		
	f1 = t1.fuse(t2)
	ts=f1		
	return ts
		
# Gantry
def XRodsLayout():
	xr=Part.makeCylinder(bc.gantryRodDia/2,ac.xrodlen)
	xr.rotate(Vector(0,0,0),Vector(0,1,0),90)
	xr.translate(Vector(-ac.xrodlen/2,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2))
	xr2=xr.copy()
	xr2.translate(Vector(0,0,-ac.xrodspacing))
	xr=xr.fuse(xr2)
	xr.translate(Vector(0,ac.mYpos,0))
	return xr
	
def XBushingsLayout():
	xb=StraightBushing(ac.xBushing)
	xb.rotate(Vector(0,0,0),Vector(0,1,0),90)
	xb.translate(Vector(-ac.xBushing[2]/2,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2))
	xb.translate(Vector(ac.mXpos,ac.mYpos,0))
	xb2=xb.copy()
	xb2.translate(Vector(0,0,-ac.xrodspacing))
	xb=xb.fuse(xb2)
	return xb
	
def YRodsLayout():
	yr=Part.makeCylinder(bc.gantryRodDia/2,ac.yrodlen)
	yr.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	yr.translate(Vector(ac.yrodxpos,-ac.yrodlen/2 + ac.tailadd/2,ac.yrodzpos))
	yr=yr.fuse(yr.mirror(Vector(0,0,0),Vector(1,0,0)))
	return yr
	
def YBushingsLayout():
	yb=StraightBushing(ac.yBushing)
	yb.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	yb.translate(Vector(ac.yrodxpos,ac.ybushingypos-ac.yBushing[2]/2,ac.yrodzpos))
	yb=yb.fuse(yb.mirror(Vector(0,0,0),Vector(1,0,0)))
	yb.translate(Vector(0,ac.mYpos,0))
	return yb
	
def GantryMotorsLayout():
	gm = NemaMotor(ac.gantryMotor)
	gm.translate(Vector(ac.gantrymotorxpos,ac.gantrymotorypos,ac.gantrymotorzpos))
	gm=gm.fuse(gm.mirror(Vector(0,0,0),Vector(1,0,0)))
	return gm
	
def GantryAIdlersLayout():
	ai = Bearing(ps.z624)
	ai.translate(Vector(ac.gantryaidlerxpos,ac.gantryaidlerypos,ac.gantrydrivecenter))
	ai2=ai.copy()
	ai2.translate(Vector(0,0,-ps.z624[2]))
	ai=ai.fuse(ai2)
	ai=ai.fuse(ai.mirror(Vector(0,0,0),Vector(1,0,0)))
	return ai
	
def GantryBIdlersLayout():
	bi = Bearing(ps.z624)
	bi.translate(Vector(ac.gantrybidlerxpos,ac.gantrybidlerypos,ac.gantrydrivecenter))
	bi2=bi.copy()
	bi2.translate(Vector(0,0,-ps.z624[2]))
	bi=bi.fuse(bi2)
	bi=bi.fuse(bi.mirror(Vector(0,0,0),Vector(1,0,0)))
	bi.translate(Vector(0,ac.mYpos,0))
	return bi
	
def GantryCIdlersLayout():
	ci = Bearing(ps.z624)
	ci.translate(Vector(ac.gantrycidlerxpos,ac.gantrycidlerypos,ac.gantrydrivecenter))
	ci2=ci.copy()
	ci2.translate(Vector(0,0,-ps.z624[2]))
	ci=ci.fuse(ci2)
	ci=ci.fuse(ci.mirror(Vector(0,0,0),Vector(1,0,0)))
	ci.translate(Vector(0,ac.mYpos,0))
	return ci

def GantryBeltLayout():
	m2ai=Part.makeBox(ac.beltThick,ac.gantrymotorypos - ac.gantryaidlerypos,ac.beltWidth)
	m2ai.translate(Vector(ac.gantryaidlerxpos + bc.gantryIdlerDia/2,ac.gantryaidlerypos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	ai2bi=Part.makeBox(ac.beltThick,-ac.gantryaidlerypos + ac.gantrybidlerypos + ac.mYpos,ac.beltWidth)
	ai2bi.translate(Vector(ac.gantryaidlerxpos - bc.gantryIdlerDia/2 - ac.beltThick,ac.gantryaidlerypos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	bi2bi=Part.makeBox(ac.gantrybidlerxpos*2,ac.beltThick,ac.beltWidth)
	bi2bi.translate(Vector(-ac.gantrybidlerxpos,ac.gantrybidlerypos + bc.gantryIdlerDia/2 + ac.mYpos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	ci2ci=Part.makeBox(ac.gantrycidlerxpos*2,ac.beltThick,ac.beltWidth)
	ci2ci.translate(Vector(-ac.gantrycidlerxpos,ac.gantrycidlerypos - bc.gantryIdlerDia/2 + ac.mYpos - ac.beltThick,ac.gantrydrivecenter-ac.beltWidth/2))
	
	ci2m=Part.makeBox(ac.beltThick,ac.gantrymotorypos - ac.gantrycidlerypos - ac.mYpos,ac.beltWidth)
	ci2m.translate(Vector(ac.gantrycidlerxpos + bc.gantryIdlerDia/2,ac.gantrycidlerypos + ac.mYpos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	mc = BeltCorner(bc.gantryPulleyDia,bc.gantryPulleyDia + ac.beltThick*2, ac.beltWidth, 180)
	mc.translate(Vector(ac.gantrymotorxpos,ac.gantrymotorypos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	aic = BeltCorner(bc.gantryIdlerDia,bc.gantryIdlerDia + ac.beltThick*2, ac.beltWidth, 180)
	aic.rotate(Vector(0,0,0),Vector(0,0,1),180)
	aic.translate(Vector(ac.gantryaidlerxpos,ac.gantryaidlerypos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	bic = BeltCorner(bc.gantryIdlerDia,bc.gantryIdlerDia + ac.beltThick*2, ac.beltWidth, 90)
	bic.rotate(Vector(0,0,0),Vector(0,0,1),0)
	bic.translate(Vector(ac.gantrybidlerxpos,ac.gantrybidlerypos + ac.mYpos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	cic = BeltCorner(bc.gantryIdlerDia,bc.gantryIdlerDia + ac.beltThick*2, ac.beltWidth, 90)
	cic.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	cic.translate(Vector(ac.gantrycidlerxpos,ac.gantrycidlerypos + ac.mYpos,ac.gantrydrivecenter-ac.beltWidth/2))
	
	gb = m2ai.fuse(ai2bi.fuse(ci2m))
	gb = gb.fuse(mc.fuse(aic.fuse(bic.fuse(cic))))
	gb=gb.fuse(gb.mirror(Vector(0,0,0),Vector(1,0,0)))
	gb=gb.fuse(bi2bi.fuse(ci2ci))
	return gb

# Z motion
def ZRodsLayout():
	zr = Part.makeCylinder(bc.zRodDia/2,ac.zrodlen)
	zr.translate(Vector(ac.zrodxpos,ac.zrodspacing/2,ac.zrodzpos))
	zr=zr.fuse(zr.mirror(Vector(0,0,0),Vector(1,0,0)))
	zr=zr.fuse(zr.mirror(Vector(0,0,0),Vector(0,1,0)))
	return zr

def ZScrewsLayout():
	zs = Part.makeCylinder(bc.zScrewDia/2,ac.zscrewlen)
	zs.translate(Vector(ac.zscrewxpos,0,ac.zscrewzpos))
	zs=zs.fuse(zs.mirror(Vector(0,0,0),Vector(1,0,0)))
	return zs

def ZMotorsLayout():
	zm = NemaMotor(ac.zMotor) 
	zm.translate(Vector(ac.zscrewxpos,0,ac.frameringazpos + ac.zMotor[1] - ac.beamSize/2))
	zm=zm.fuse(zm.mirror(Vector(0,0,0),Vector(1,0,0)))
	return zm
	
def ZCouplersLayout():
	cDia = 20
	cLen = 25
	cp = Part.makeCylinder(cDia/2,cLen)
	cp.translate(Vector(-ac.zscrewxpos,0,ac.frameringazpos-ac.beamSize/2+ac.zMotor[1]+cLen/2))
	
	return cp
	
def ZBushingsLayout():
	zb=StraightBushing(ac.zBushing)
	zb.translate(Vector(ac.zrodxpos,ac.zrodspacing/2,-ac.bedThick+ac.bedBushOffset))
	zb=zb.fuse(zb.mirror(Vector(0,0,0),Vector(0,1,0)))
	zb=zb.fuse(zb.mirror(Vector(0,0,0),Vector(1,0,0)))
	zb.translate(Vector(0,0,ac.mZpos))
	return zb
	
def ZLeadNutsLayout():
	lnspring=9
	lnsdia = 9
	#lower nut
	lnl = regPolygon(sides=6,radius=bc.zLeadNutDia/2,extrude=ps.m5n[2])
	lnl.translate(Vector(-ac.zscrewxpos,0,0))
	#upper nut
	lnu = lnl.copy()
	lnu.translate(Vector(0,0,ps.m5n[2]+lnspring))
	#spring
	lns=Part.makeCylinder(lnsdia/2,lnspring)
	lns.translate(Vector(-ac.zscrewxpos,0,ps.m5n[2]))
	#Clamps Screws
	cs = CapHeadScrew(l=30,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=0)
	cs.translate(Vector(-ac.zscrewxpos-ps.m3l[1]-2,0,ps.m5n[2]*2+lnspring+4))
	cs2 = cs.copy()
	cs2.rotate(Vector(-ac.zscrewxpos,0,0),Vector(0,0,1),120)
	cs3 = cs.copy()
	cs3.rotate(Vector(-ac.zscrewxpos,0,0),Vector(0,0,1),-120)
	
	cs=cs.fuse(cs2.fuse(cs3))
	
	zln = lnl.fuse(lnu.fuse(lns.fuse(cs)))
	zln.translate(Vector(0,0,-ac.bedThickAlt+ac.minthick))
	zln.translate(Vector(0,0,ac.mZpos))
	return zln

# Frame
def FrameUprightsLayout():
	ua = BoxExtrusion(size=ac.beamSize,length=ac.frameuprightslen)
	ua.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	ua.translate(Vector(ac.xrodlen/2,ac.yrodlen/2 - ac.beamSize/2,ac.frameringazpos - ac.beamSize/2))
	ua=ua.fuse(ua.mirror(Vector(0,0,0),Vector(1,0,0)))
	ua=ua.fuse(ua.mirror(Vector(0,0,0),Vector(0,1,0)))
	ua.translate(Vector(0,ac.tailadd/2,0))
	#Joint Screws
	screw = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1]+0.5,hh=ps.m3l[2],cut=1)
	xscrew = screw.copy()
	xscrew.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	yscrew = screw.copy()
	yscrew.rotate(Vector(0,0,0),Vector(1,0,0),90)
	jsyr = xscrew.copy()
	jsyr.translate(Vector(-ac.frameringxlen/2-ac.beamSize*0.75,-ac.frameringylen/2-ac.beamSize/2+ac.tailadd/2,ac.yrodzpos-bc.gantryRodDia/2-ac.beamSize/2))
	jszr = yscrew.copy()
	jszr.translate(Vector(-ac.frameringxlen/2-ac.beamSize/2,-ac.frameringylen/2-ac.beamSize*0.75+ac.tailadd/2,ac.framezsupportszpos))
	jsra = yscrew.copy()
	jsra.translate(Vector(-ac.frameringxlen/2-ac.beamSize/2,-ac.frameringylen/2-ac.beamSize*0.75+ac.tailadd/2,ac.frameringazpos))
	jsrb1 = yscrew.copy()
	jsrb1.translate(Vector(-ac.frameringxlen/2-ac.beamSize/2,-ac.frameringylen/2-ac.beamSize*0.75+ac.tailadd/2,ac.frameringbzpos))
	jsrb2 = xscrew.copy()
	jsrb2.translate(Vector(-ac.frameringxlen/2-ac.beamSize*0.75,-ac.frameringylen/2-ac.beamSize/2+ac.tailadd/2,ac.frameringbzpos+ac.beamSize))
	jsrc = xscrew.copy()
	jsrc.translate(Vector(-ac.frameringxlen/2-ac.beamSize*0.75,-ac.frameringylen/2-ac.beamSize/2+ac.tailadd/2,ac.frameringczpos))
	
	jss = jsyr.fuse(jszr.fuse(jsra.fuse(jsrb1.fuse(jsrb2.fuse(jsrc)))))
	jss = jss.fuse(jss.mirror(Vector(0,0,0),Vector(1,0,0)))
	jss = jss.fuse(jss.mirror(Vector(0,+ac.tailadd/2,0),Vector(0,1,0)))
	#ua = ua.fuse(jss)
	ua = ua.cut(jss)
	
	return ua
	
def FrameYRodSupportsLayout():
	ys = BoxExtrusion(size=ac.beamSize,length=ac.frameringxlen)
	ys.translate(Vector(-ac.frameringxlen/2,ac.yrodlen/2 - ac.beamSize/2,ac.frameysupportszpos))
	ys=ys.fuse(ys.mirror(Vector(0,0,0),Vector(0,1,0)))
	ys.translate(Vector(0,ac.tailadd/2,0))
	return ys
	
def FrameZRodSupportsLayout():
	zs = BoxExtrusion(size=ac.beamSize,length=ac.frameringylen)
	zs.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	zs.translate(Vector(-ac.frameringxlen/2 - ac.beamSize/2,ac.frameringylen/2,ac.framezsupportszpos))
	zs=zs.fuse(zs.mirror(Vector(0,0,0),Vector(1,0,0)))
	zs.translate(Vector(0,ac.tailadd/2,0))
	return zs

def FrameRingALayout():
	rx = BoxExtrusion(size=ac.beamSize,length=ac.frameringxlen)
	rx.translate(Vector(-ac.frameringxlen/2,ac.yrodlen/2 - ac.beamSize/2,ac.frameringazpos))
	rx=rx.fuse(rx.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	ry = BoxExtrusion(size=ac.beamSize,length=ac.frameringylen)
	ry.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	ry.translate(Vector(-ac.frameringxlen/2 - ac.beamSize/2,ac.frameringylen/2,ac.frameringazpos))
	ry=ry.fuse(ry.mirror(Vector(0,0,0),Vector(1,0,0)))
	#Bed Support Frame Screws
	screw = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1]+0.5,hh=ps.m3l[2],cut=1)
	screw.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	bsfs = screw.copy()
	bsfs.translate(Vector(-ac.frameringxlen/2-ac.beamSize*0.75,ac.zrodspacing/2 - ac.beamSize/2 - bc.gantryRodDia/2,ac.frameringazpos))
	bsfs=bsfs.fuse(bsfs.mirror(Vector(0,0,0),Vector(0,1,0)))
	bsfs=bsfs.fuse(bsfs.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	ra = rx.fuse(ry)
	ra.translate(Vector(0,ac.tailadd/2,0))
	ra = ra.cut(bsfs)
	return ra
	
def FrameRingBLayout():
	rx = BoxExtrusion(size=ac.beamSize,length=ac.frameringxlen)
	rx.translate(Vector(-ac.frameringxlen/2,ac.yrodlen/2 - ac.beamSize/2,ac.frameringbzpos+ac.beamSize))
	rx=rx.fuse(rx.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	ry = BoxExtrusion(size=ac.beamSize,length=ac.frameringylen)
	ry.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	ry.translate(Vector(-ac.frameringxlen/2 - ac.beamSize/2,ac.frameringylen/2,ac.frameringbzpos))
	ry=ry.fuse(ry.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	rb = rx.fuse(ry)
	rb.translate(Vector(0,ac.tailadd/2,0))
	return rb
	
def FrameRingCLayout():
	rx = BoxExtrusion(size=ac.beamSize,length=ac.frameringxlen)
	rx.translate(Vector(-ac.frameringxlen/2,ac.yrodlen/2 - ac.beamSize/2,ac.frameringczpos))
	rx=rx.fuse(rx.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	ry = BoxExtrusion(size=ac.beamSize,length=ac.frameringylen)
	ry.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	ry.translate(Vector(-ac.frameringxlen/2 - ac.beamSize/2,ac.frameringylen/2,ac.frameringczpos))
	ry=ry.fuse(ry.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	rc = rx.fuse(ry)
	rc.translate(Vector(0,ac.tailadd/2,0))
	return rc
	
def FrameZMotorSupportsLayout():
	zms = BoxExtrusion(size=ac.beamSize,length=ac.frameringxlen)
	zms.translate(Vector(-ac.frameringxlen/2,ac.framezmotorsupportsspacing/2,ac.frameringazpos))
	zms=zms.fuse(zms.mirror(Vector(0,0,0),Vector(0,1,0)))
	return zms

def SmallCornerBracketsLayout():
	cb1 = pCornerBracket.SmallCornerBracket()
	cb1.translate(Vector(-ac.frameringxlen/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize/2,ac.frameringazpos+ac.beamSize/2))
	cb2 = pCornerBracket.SmallCornerBracket()
	cb2.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	cb2.translate(Vector(-ac.frameringxlen/2,-ac.frameringylen/2+ac.tailadd/2,ac.frameringazpos))
	cb1 = cb1.fuse(cb2)
	cb1 = cb1.fuse(cb1.mirror(Vector(0,ac.tailadd/2,0),Vector(0,1,0)))
	cb3 = pCornerBracket.SmallCornerBracket()
	cb3.rotate(Vector(0,0,0),Vector(1,0,0),180)
	cb3.rotate(Vector(0,0,0),Vector(0,0,1),90)
	cb3.translate(Vector(-ac.frameringxlen/2-ac.beamSize/2,-ac.frameringylen/2+ac.tailadd/2,ac.frameuprightslen - ac.framebasedeep - ac.bedThick - ac.beamSize))
	cb4 = pCornerBracket.SmallCornerBracket()
	cb4.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	cb4.translate(Vector(-ac.frameringxlen/2,-ac.frameringylen/2+ac.tailadd/2,ac.frameuprightslen - ac.framebasedeep - ac.bedThick - ac.beamSize/2))
	cb3 = cb3.fuse(cb4)
	cb3 = cb3.fuse(cb3.mirror(Vector(0,ac.tailadd/2,0),Vector(0,1,0)))
	brackets = cb1.fuse(cb3)
	brackets = brackets.fuse(brackets.mirror(Vector(0,0,0),Vector(1,0,0)))
	return brackets

#Bits
def CableGuidesLayout():
	step = 70
	rr = pBits.cableClip(ac.beamSize)
	rr.translate(Vector(ac.frameringxlen/2+ac.beamSize/2,ac.frameringylen/2+ac.beamSize + ac.tailadd/2,ac.frameringbzpos + ac.beamSize))
	rr1=rr.copy()
	rr1.translate(Vector(0,0,step))
	rr2=rr1.copy()
	rr2.translate(Vector(0,0,step))
	rr3=rr2.copy()
	rr3.translate(Vector(0,0,step))
	rr4=rr3.copy()
	rr4.translate(Vector(0,0,step))
	guides = rr
	guides = guides.fuse(rr1.fuse(rr2.fuse(rr3.fuse(rr4))))
	guides = guides.fuse(guides.mirror(Vector(0,0,0),Vector(1,0,0)))
	return guides

def PowerSupplyMountsLayout():
	am1=pBits.PowerSupplyMount(reach=8)
	if dc.forPrint == 0:
		am1.translate(Vector(30,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize,ac.frameringazpos-ac.beamSize/2))
	if dc.forPrint == 1:
		am1.translate(Vector(-(ac.beamSize+ac.minthick)*2+ac.minthick/2,2,8+ac.beamSize))
	am2=pBits.PowerSupplyMount(reach=8)
	am2.rotate(Vector(0,0,0),Vector(0,0,1),180)
	if dc.forPrint == 0:
		am2.translate(Vector(-105,-ac.frameringylen/2+ac.tailadd/2+ac.PowerSupplyASize[1]+ac.beamSize+17,ac.frameringazpos-ac.beamSize/2))
	if dc.forPrint == 1:
		am2.translate(Vector((ac.beamSize+ac.minthick)*2-ac.minthick/2,-2,8+ac.beamSize))
	am = am1.fuse(am2)
	bm1=pBits.PowerSupplyMount(reach=31)
	if dc.forPrint == 0:
		bm1.translate(Vector(30,ac.frameringylen/2+ac.tailadd/2-ac.beamSize-ac.PowerSupplyASize[1]-60,ac.frameringazpos-ac.beamSize/2))
	if dc.forPrint == 1:
		bm1.translate(Vector(ac.minthick/2,2,31+ac.beamSize))
	bm2=pBits.PowerSupplyMount(reach=28)
	bm2.rotate(Vector(0,0,0),Vector(0,0,1),180)
	if dc.forPrint == 0:
		bm2.translate(Vector(-105,ac.frameringylen/2+ac.tailadd/2+ac.beamSize,ac.frameringazpos-ac.beamSize/2))
	if dc.forPrint == 1:
		bm2.translate(Vector(-ac.minthick/2,-2,28+ac.beamSize))
	bm=bm1.fuse(bm2)
	mounts = am.fuse(bm)
	return mounts

def RumbaMountLayout():
	rm = pBits.RumbaMount()
	rm.translate(Vector(-ac.beamSize/2,-30,-ac.beamSize))
	rm.rotate(Vector(0,0,0),Vector(0,1,0),180)
	rms=rm.copy()
	if dc.forPrint == 1:
		for i in range(-2,2):
			a=rm.copy()
			a.translate(Vector((ac.beamSize+3)*i,0,0))
			rms=rms.fuse(a)
		rms.translate(Vector(ac.beamSize/2+1,0,0))
	return rms
	
def RumbaFanMountLayout():
	rfm = pBits.RumbaFanMount()
	return rfm

def CableClipsLayout():
	cc = pBits.CableClip()
	return cc
	
def HotEndFanMountLayout():
	hef = pBits.HotEndFanMount()
	return hef

# Electronics
def PowerSupplyALayout():
	psa = Part.makeBox(ac.PowerSupplyASize[0],ac.PowerSupplyASize[1],ac.PowerSupplyASize[2])
	psa.translate(Vector(-36 -ac.PowerSupplyASize[0]/2,ac.frameringylen/2+ac.tailadd/2 -ac.PowerSupplyASize[1] -28,ac.frameringazpos+ac.beamSize/2))
	return psa
	
def PowerSupplyBLayout(): #bright
	psb = Part.makeBox(ac.PowerSupplyBSize[0],ac.PowerSupplyBSize[1],ac.PowerSupplyBSize[2])
	psb.translate(Vector(-36 -ac.PowerSupplyBSize[0]/2,-ac.frameringylen/2+ac.tailadd/2 + 8,ac.frameringazpos+ac.beamSize/2))
	return psb

def ControlBoardLayout():
	cnt = Part.makeBox(ac.RUMBAsize[0],ac.RUMBAsize[1],ac.RUMBAsize[2])
	cnt.translate(Vector(ac.frameringxlen/2-ac.RUMBAsize[0]-ac.minthick*3,ac.frameringylen/2+ac.tailadd/2-ac.RUMBAsize[1]-ac.minthick*2,ac.frameringazpos+ac.beamSize/2+ac.minthick))
	return cnt

######################################################################################################################
def makeLE3P():
	doc = FreeCAD.activeDocument()
	if doc == None:
		doc = FreeCAD.newDocument("le3p")
	Frame = doc.addObject("App::DocumentObjectGroup",  "Frame")
	Bed = doc.addObject("App::DocumentObjectGroup",  "Bed")
	Printed = doc.addObject("App::DocumentObjectGroup",  "Printed")
	Motion = doc.addObject("App::DocumentObjectGroup", "Motion")
	Hardware = doc.addObject("App::DocumentObjectGroup",  "Hardware")
	Extruder = doc.addObject("App::DocumentObjectGroup",  "Extruder")
	Electronics = doc.addObject("App::DocumentObjectGroup",  "Electronics")
	
	if dc.showHotEnds == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "HotEnds")
		tool.Shape = HotEndsLayout()
		tool.Label = "Hot Ends"
		Extruder.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("HotEnds").ShapeColor = (0.6,0.6,0.6)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_HotEnds.stl'))
		
	#Bed
	#if dc.showBedSurface == 1:
	#	xye=doc.addObject("Part::Feature",  "Kapton")
	#	xye.Shape = aBed.Kapton()
	#	xye.Label = "Bed Tape"
	#	Bed.addObject(xye)
	#	FreeCADGui.getDocument("le3p").getObject("Kapton").ShapeColor = (0.9,0.6,0.0)
	#	FreeCADGui.getDocument("le3p").getObject("Kapton").Transparency = (0)
	#	if dc.doSTLexport == 1 and dc.printedOnly == 0:
	#		xye.Shape.exportStl(bc.exportpath % ('bed/export_BedKapton.stl'))
		
	if dc.showBedSurface == 1 or dc.showAll == 1:
		xye=doc.addObject("Part::Feature",  "GlassPlate")
		xye.Shape = aBed.GlassPlate()
		xye.Label = "Glass Plate"
		Bed.addObject(xye)
		FreeCADGui.getDocument("le3p").getObject("GlassPlate").ShapeColor = (0.9,0.9,0.7)
		FreeCADGui.getDocument("le3p").getObject("GlassPlate").Transparency = (0)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			xye.Shape.exportStl(bc.exportpath % ('bed/export_BedGlassPlate.stl'))
		
	if dc.showBedSurface == 1 or dc.showAll == 1:
		xye=doc.addObject("Part::Feature",  "HeatPlate")
		xye.Shape = aBed.HeatPlate()
		xye.Label = "Heat Plate"
		Bed.addObject(xye)
		FreeCADGui.getDocument("le3p").getObject("HeatPlate").ShapeColor = (0.8,0.0,0.0)
		FreeCADGui.getDocument("le3p").getObject("HeatPlate").Transparency = (0)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			xye.Shape.exportStl(bc.exportpath % ('bed/export_BedHeatPlate.stl'))
		
	if dc.showBedSurface == 1 or dc.showAll == 1:
		xye=doc.addObject("Part::Feature",  "BasePlate")
		xye.Shape = aBed.BasePlate()
		xye.Label = "Base Plate"
		Bed.addObject(xye)
		FreeCADGui.getDocument("le3p").getObject("BasePlate").ShapeColor = (0.8,0.8,0.8)
		FreeCADGui.getDocument("le3p").getObject("BasePlate").Transparency = (0)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			xye.Shape.exportStl(bc.exportpath % ('bed/export_BedBasePlate.stl'))
			
	if dc.showBedSurface == 1 or dc.showAll == 1:
		xye=doc.addObject("Part::Feature",  "BedFrame")
		xye.Shape = aBed.BedFrame()
		xye.Label = "Bed Frame"
		Bed.addObject(xye)
		FreeCADGui.getDocument("le3p").getObject("BedFrame").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
		FreeCADGui.getDocument("le3p").getObject("BedFrame").Transparency = (0)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			xye.Shape.exportStl(bc.exportpath % ('bed/export_BedFrame.stl'))
	
	#Gantry
	if dc.showXRods == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "XRods")
		tool.Shape = XRodsLayout()
		tool.Label = "X Rods"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("XRods").ShapeColor = (dc.rodsR,dc.rodsG,dc.rodsB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryXRods.stl'))
		
	if dc.showXBushings == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "XBushings")
		tool.Shape = XBushingsLayout()
		tool.Label = "X Bushings"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("XBushings").ShapeColor = (dc.bushingsR,dc.bushingsG,dc.bushingsB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryXBushings.stl'))
		
	if dc.showYRods == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "YRods")
		tool.Shape = YRodsLayout()
		tool.Label = "Y Rods"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("YRods").ShapeColor = (dc.rodsR,dc.rodsG,dc.rodsB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryYRods.stl'))
		
	if dc.showYBushings == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "YBushings")
		tool.Shape = YBushingsLayout()
		tool.Label = "Y Bushings"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("YBushings").ShapeColor = (dc.bushingsR,dc.bushingsG,dc.bushingsB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryYBushings.stl'))
		
	if dc.showGantryMotors == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "GantryMotors")
		tool.Shape = GantryMotorsLayout()
		tool.Label = "Gantry Motors"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("GantryMotors").ShapeColor = (0.15,0.15,0.15)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryMotors.stl'))
		
	if dc.showGantryAIdlers == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "GantryAIdlers")
		tool.Shape = GantryAIdlersLayout()
		tool.Label = "Gantry A Idlers"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("GantryAIdlers").ShapeColor = (0.7,0.7,0.9)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryAIdlers.stl'))
		
	if dc.showGantryBIdlers == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "GantryBIdlers")
		tool.Shape = GantryBIdlersLayout()
		tool.Label = "Gantry B Idlers"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("GantryBIdlers").ShapeColor = (0.7,0.7,0.9)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryBIdlers.stl'))
		
	if dc.showGantryCIdlers == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "GantryCIdlers")
		tool.Shape = GantryCIdlersLayout()
		tool.Label = "Gantry C Idlers"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("GantryCIdlers").ShapeColor = (0.7,0.7,0.9)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryCIdlers.stl'))
		
	if dc.showGantryBelt == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "GantryBelt")
		tool.Shape = GantryBeltLayout()
		tool.Label = "Gantry Belt"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("GantryBelt").ShapeColor = (dc.beltR,dc.beltG,dc.beltB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryBelt.stl'))
	
	# Z Motion
	if dc.showZRods == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZRods")
		tool.Shape = ZRodsLayout()
		tool.Label = "Z Rods"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZRods").ShapeColor = (dc.rodsR,dc.rodsG,dc.rodsB)
		
	if dc.showZScrews == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZScrews")
		tool.Shape = ZScrewsLayout()
		tool.Label = "Z Screws"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZScrews").ShapeColor = (dc.rodsR-0.2,dc.rodsG-0.2,dc.rodsB-0.25)
		
	if dc.showZMotors == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZMotors")
		tool.Shape = ZMotorsLayout()
		tool.Label = "Z Motors"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZMotors").ShapeColor = (0.15,0.15,0.15)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_ZMotors.stl'))
		
	if dc.showZMotors == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZCouplers")
		tool.Shape = ZCouplersLayout()
		tool.Label = "Z Couplers"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZCouplers").ShapeColor = (0.65,0.65,0.65)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_ZCouplers.stl'))
	
	if dc.showZBushings == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZBushings")
		tool.Shape = ZBushingsLayout()
		tool.Label = "Z Bushings"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZBushings").ShapeColor = (dc.bushingsR,dc.bushingsG,dc.bushingsB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryZBushings.stl'))
			
	if dc.showZLeadNuts == 1 and dc.showManufacturedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZLeadNuts")
		tool.Shape = ZLeadNutsLayout()
		tool.Label = "Z LeadNuts"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZLeadNuts").ShapeColor = (0.7,0.7,0.2)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_GantryZLeadNuts.stl'))
	
	
	# Extruder
	if dc.showExtruderMotor == 1 and dc.showExtruderParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ExtruderMotor")
		tool.Shape = pExtruderDriver.ExtruderMotor()
		tool.Label = "Extruder Motor"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ExtruderMotor").ShapeColor = (0.7,0.7,0.7)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_ExtruderMotor.stl'))
			
	if dc.showExtruderSupportBearing == 1 and dc.showExtruderParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ExtruderSupportBearing")
		tool.Shape = pExtruderDriver.ExtruderSupportBearing()
		tool.Label = "Extruder Support Bearing"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ExtruderSupportBearing").ShapeColor = (0.6,0.6,0.7)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_ExtruderSupportBearing.stl'))
			
	if dc.showExtruderDriveGear == 1 and dc.showExtruderParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ExtruderDriveGear")
		tool.Shape = pExtruderDriver.ExtruderDriveGear()
		tool.Label = "Extruder Drive Gear"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ExtruderDriveGear").ShapeColor = (0.6,0.6,0.7)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_ExtruderDriveGear.stl'))
			
	if dc.showExtruderIdleBearing == 1 and dc.showExtruderParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ExtruderIdleBearing")
		tool.Shape = pExtruderDriver.ExtruderIdleBearing()
		tool.Label = "Extruder Idle Bearing"
		Motion.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ExtruderIdleBearing").ShapeColor = (0.6,0.6,0.7)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('manufactured/export_ExtruderIdleBearing.stl'))

	# Frame
	if dc.showFrameUprights == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "FrameUprights")
		tool.Shape = FrameUprightsLayout()
		tool.Label = "Frame Uprights"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("FrameUprights").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
		if dc.doSTLexport == 1 and dc.printedOnly == 0:
			tool.Shape.exportStl(bc.exportpath % ('frame/export_FrameUprights.stl'))
		
	if dc.showFrameYRodSupports == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "FrameYRodSupports")
		tool.Shape = FrameYRodSupportsLayout()
		tool.Label = "Frame Y Rod Supports"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("FrameYRodSupports").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
		
	if dc.showFrameZRodSupports == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "FrameZRodSupports")
		tool.Shape = FrameZRodSupportsLayout()
		tool.Label = "Frame Z Rod Supports"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("FrameZRodSupports").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
		
	if dc.showFrameRingA == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "FrameRingA")
		tool.Shape = FrameRingALayout()
		tool.Label = "Frame Ring A"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("FrameRingA").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
		
	if dc.showFrameRingB == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "FrameRingB")
		tool.Shape = FrameRingBLayout()
		tool.Label = "Frame Ring B"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("FrameRingB").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
	
	if dc.showFrameRingC == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "FrameRingC")
		tool.Shape = FrameRingCLayout()
		tool.Label = "Frame Ring C"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("FrameRingC").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
		
	if dc.showFrameZMotorSupports == 1 and dc.showFrame == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZMotorSupports")
		tool.Shape = FrameZMotorSupportsLayout()
		tool.Label = "ZMotorSupports"
		Frame.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZMotorSupports").ShapeColor = (dc.frameR,dc.frameG,dc.frameB)
	
	# Printed Parts
	if dc.showXCarriage == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "XCarriage")
		tool.Shape = pXCarriage.xCarriage()
		tool.Label = "X Carriage"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("XCarriage").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("XCarriage").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_XCarriageSet.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_XCarriage.stl'))
		
	if dc.showXEnds == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "XEnds")
		tool.Shape = pXEnds.XEnds()
		tool.Label = "X Ends"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("XEnds").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("XEnds").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_XEndsSet.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_XEnds.stl'))
		
	if dc.showYEndsIdle == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "YEndsIdle")
		tool.Shape = pYEnds.yEndIdle()
		tool.Label = "Y Ends Idle"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("YEndsIdle").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("YEndsIdle").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_YEndsIdle.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_YEndsIdle.stl'))
		
	if dc.showYEndsMotor == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "YEndsMotor")
		tool.Shape = pYEnds.yEndMotor()
		tool.Label = "Y Ends Motor"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("YEndsMotor").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("YEndsMotor").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_YEndsMotor.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_YEndsMotor.stl'))
		
	if dc.showZEndsUpper == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZEndsUpper")
		tool.Shape = pZEnds.zEnds()
		tool.Label = "Z Ends Upper"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZEndsUpper").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("ZEndsUpper").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_ZEnds.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_ZEnds.stl'))
		
	if dc.showGantryMotorMounts == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "GantryMotorMounts")
		tool.Shape = pGantryMotorMount.gantryMotorMounts()
		tool.Label = "Gantry Motor Mounts"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("GantryMotorMounts").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("GantryMotorMounts").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_GantryMotorMounts.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_GantryMotorMounts.stl'))
		
	if dc.showZMotorMounts == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZMotorMounts")
		tool.Shape = pZMotorMount.zMotorMounts()
		tool.Label = "Z Motor Mounts"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZMotorMounts").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("ZMotorMounts").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_ZMotorMounts.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_ZMotorMounts.stl'))
	
	if dc.showCableGuides == 1 and dc.showPrintedParts == 1:
		tool=doc.addObject("Part::Feature",  "CableGuides")
		tool.Shape = CableGuidesLayout()
		tool.Label = "Cable Guides"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("CableGuides").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("CableGuides").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/export_CableGuides.stl'))
			
	if dc.showCableClips == 1 and dc.showPrintedParts == 1:
		tool=doc.addObject("Part::Feature",  "CableClips")
		tool.Shape = CableClipsLayout()
		tool.Label = "Cable Clips"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("CableClips").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("CableClips").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/forprint_CableClips.stl'))
			
	if dc.showHotEndFanMount == 1 and dc.showPrintedParts == 1:
		tool=doc.addObject("Part::Feature",  "HotEndFanMount")
		tool.Shape = HotEndFanMountLayout()
		tool.Label = "HotEndFanMount"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("HotEndFanMount").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("HotEndFanMount").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/forprint_HotEndFanMount.stl'))
			
	if dc.showYStop == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "YStop")
		tool.Shape = pBits.yStop()
		tool.Label = "Y Stop"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("YStop").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("YStop").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_YStop.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_YStop.stl'))

	if dc.showZCarriage == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ZCarriage")
		tool.Shape = pZCarriage.zCarriage()
		tool.Label = "Z Carriage"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ZCarriage").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("ZCarriage").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_ZCarriage.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_ZCarriage.stl'))
			
	if dc.showToolHolder == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ToolHolder")
		tool.Shape = pToolHolder.DualE3d()
		tool.Label = "Tool Holder"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ToolHolder").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("ToolHolder").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_ToolHolder.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_ToolHolder.stl'))

	if dc.showExtruderDriver == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ExtruderDriver")
		tool.Shape = pExtruderDriver.ExtruderDriver()
		tool.Label = "Extruder Driver"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ExtruderDriver").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("ExtruderDriver").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			if dc.forPrint == 1:
				tool.Shape.exportStl(bc.exportpath % ('printed/forprint_ExtruderDriver.stl'))
			else:
				tool.Shape.exportStl(bc.exportpath % ('printed/export_ExtruderDriver.stl'))
			
	if dc.showExtruderDriverMount == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ExtruderDriverMount")
		tool.Shape = pExtruderDriver.MountPlate()
		tool.Label = "Extruder Driver Mount"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ExtruderDriverMount").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("ExtruderDriverMount").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/export_ExtruderDriver.stl'))

			
	if dc.showSmallCornerBrackets == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "SmallCornerBrackets")
		tool.Shape = SmallCornerBracketsLayout()
		tool.Label = "Small Corner Brackets"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("SmallCornerBrackets").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("SmallCornerBrackets").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/export_SmallCornerBrackets.stl'))

	if dc.showRumbaMount == 1 and dc.showPrintedParts == 1:
		tool=doc.addObject("Part::Feature",  "RumbaMount")
		tool.Shape = RumbaMountLayout()
		tool.Label = "RumbaMount"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("RumbaMount").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("RumbaMount").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/forprint_RumbaMount.stl'))
			
	if dc.showRumbaFanMount == 1 and dc.showPrintedParts == 1:
		tool=doc.addObject("Part::Feature",  "RumbaFanMount")
		tool.Shape = RumbaFanMountLayout()
		tool.Label = "RumbaFanMount"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("RumbaFanMount").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("RumbaFanMount").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/forprint_RumbaFanMount.stl'))

	if dc.showPowerSupplyAMount == 1 and dc.showPrintedParts == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "PowerSupplyMounts")
		tool.Shape = PowerSupplyMountsLayout()
		tool.Label = "Power Supply Mounts"
		Printed.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("PowerSupplyMounts").ShapeColor = (dc.print1R,dc.print1G,dc.print1B)
		FreeCADGui.getDocument("le3p").getObject("PowerSupplyMounts").Transparency = (dc.print1A)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('printed/export_PowerSupplyMounts.stl'))

	# Electronics
	if dc.showElectronics == 1 and dc.showPowerSupplies == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "PowerSupplyA")
		tool.Shape = PowerSupplyALayout()
		tool.Label = "Power Supply A"
		Electronics.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("PowerSupplyA").ShapeColor = (0.8,0.4,0.0)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('electronics/export_PowerSupplyA.stl'))
			
	if dc.showElectronics == 1 and dc.showPowerSupplies == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "PowerSupplyB")
		tool.Shape = PowerSupplyBLayout()
		tool.Label = "Power Supply B"
		Electronics.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("PowerSupplyB").ShapeColor = (1.0,0.3,0.0)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('electronics/export_PowerSupplyB.stl'))

	if dc.showElectronics == 1 and dc.showControlBoard == 1 or dc.showAll == 1:
		tool=doc.addObject("Part::Feature",  "ControlBoard")
		tool.Shape = ControlBoardLayout()
		tool.Label = "Control Board"
		Electronics.addObject(tool)
		FreeCADGui.getDocument("le3p").getObject("ControlBoard").ShapeColor = (0.0,0.6,0.0)
		if dc.doSTLexport == 1:
			tool.Shape.exportStl(bc.exportpath % ('electronics/export_ControlBoard.stl'))


def BOM():
	# Info Output
	print '---------------------------------------------------'
	print 'le3p v0.1.3'
	print '---------------------------------------------------'
	print 'X Envelope = {x}mm'.format(x=ac.envelopeX)
	print 'Y Envelope = {x}mm'.format(x=ac.envelopeY)
	print 'Z Envelope = {x}mm'.format(x=ac.envelopeZ)
	print ''
	print '--Part Selections'
	print 'Using "{t}" extrusions'.format(t=bc.beamType)
	print 'Bushings are "{t}"'.format(t=bc.BushingType)
	print ''
	print '--Linear Rod Lengths'
	print '2X - {y}mm x {x}mm - X Rods'.format(y=bc.gantryRodDia,x=ac.xrodlen)
	print '2X - {y}mm x {x}mm - Y Rods'.format(y=bc.gantryRodDia,x=ac.yrodlen)
	print '4X - {y}mm x {x}mm - Z Rods'.format(y=bc.gantryRodDia,x=ac.zrodlen)
	print 'Total Length = {x}mm'.format(x=ac.xrodlen*2 + ac.yrodlen*2 + ac.zrodlen*4)
	print ''
	print '--Extrusion Lengths'
	print '4X  - {z}mm Uprights'.format(z=ac.frameuprightslen)
	print '10X - {x}mm XRings'.format(x=ac.frameringxlen)
	print '8X  - {y}mm YRings'.format(y=ac.frameringylen)
	print '2X  - {x}mm BedFrameX'.format(x=ac.bedXBeamLen)
	print 'Total Length = {x}mm'.format(x=ac.frameuprightslen*4 + ac.frameringxlen*10 + ac.frameringylen*8 + ac.bedXBeamLen*2)
	print ''
	print '--Parts and Hardware'
	print 'Belt is type {t} {w}mm wide aprox {m}mm in length'.format(t=bc.beltType, m=ac.beltLen, w=ac.beltWidth)
	print ''
	#print '24X  - 20mm M3 Counter Sink Frame Screws'
	#print '6X   - 20mm M3 Counter Sink Bed Frame Screws'
	#print '2x   - 40mm M3 Caphead Adjustable Belt Clamp Screws'
	print ''
	print ''
	print '--Drill Locations'
	print '----Uprights'
	print '------X Side - from bottom up'
	print '{n}mm - frame ring A'.format(n=ac.beamSize/2)
	print '{n}mm - lower zrod supports'.format(n=-(ac.frameringazpos - ac.frameringbzpos)+ac.beamSize/2)
	print '------X Side - from top down'
	print '{n}mm - upper zrod supports'.format(n=(ac.frameringczpos-ac.framezsupportszpos)+ac.beamSize/2)
	print ''
	print '------Y Side - from bottom up'
	print '{n}mm - frame ring B'.format(n=-(ac.frameringazpos - ac.frameringbzpos)+ac.beamSize/2+ac.beamSize)
	print ''
	print '------Y Side - from top down'
	print '{n}mm - frame ring C'.format(n=ac.beamSize/2)
	print '{n}mm - Y rod supports'.format(n=(ac.frameringczpos - ac.frameysupportszpos)+ac.beamSize/2)
	print ''
	print '------Y Horizontals - from each end'
	print '{n}mm - Z MotorSupports from front'.format(n=(ac.frameringylen/2-ac.framezmotorsupportsspacing/2-ac.tailadd/2))
	print '{n}mm - Z MotorSupports from front'.format(n=(ac.frameringylen/2-ac.framezmotorsupportsspacing/2+ac.tailadd/2))
	print '.'
	

# Generate le3p ######################################################################################################
if clear == 1:
	App.getDocument("le3p").getObject("Frame").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Frame")
	App.getDocument("le3p").getObject("Bed").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Bed")
	App.getDocument("le3p").getObject("Printed").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Printed")
	App.getDocument("le3p").getObject("Extruder").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Extruder")
	App.getDocument("le3p").getObject("Electronics").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Electronics")
	App.getDocument("le3p").getObject("Hardware").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Hardware")
	App.getDocument("le3p").getObject("Motion").removeObjectsFromDocument()
	App.getDocument("le3p").removeObject("Motion")

makeLE3P()
BOM()

#t = FilletFlange(innerdia=ac.zBushing[1],filletdia=ac.zBushing[1],filletthick=20)
#Part.show(t)
