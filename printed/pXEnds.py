#le3p-v0.1.3 - 
from __future__ import division
import sys
import FreeCAD, Part, math
from FreeCAD import Vector

from config import basicConfig
from config import advancedConfig
from config import displayConfig
from config import partSizes

from include.parts import CapHeadScrew
from include.shapes import RodClampSlice
from include.shapes import ThinSlice
from include.shapes import LE3Plogolong

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

def XEnds():
  bpx = (ac.xrodlen/2 - ac.gantrycidlerxpos) + bc.gantryIdlerDia/2
	bpy = bc.gantryRodDia+ac.minthick*2
	bpz = ac.xrodspacing + bc.gantryRodDia+ac.minthick*2
	#big pill
	bp = Part.makeBox(bpx,bpy,bpz)
	bp = bp.makeFillet(bpy/2-0.01,[bp.Edges[8],bp.Edges[9],bp.Edges[10],bp.Edges[11]])
	bp.translate(Vector(-ac.xrodlen/2,-bpy/2 + ac.xrodypos,ac.xrodzcenter - ac.xrodspacing/2 - bc.gantryRodDia/2 - ac.minthick))
	#rod cut
	rc = Part.makeCylinder((bc.gantryRodDia+bc.rodTolerance*2)/2,bpx)
	rc.rotate(Vector(0,0,0),Vector(0,1,0),90)
	rc.translate(Vector(-ac.xrodlen/2,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2))
	rc2=rc.copy()
	rc2.translate(Vector(0,0,-ac.xrodspacing))
	bp=bp.cut(rc.fuse(rc2))
	#Bushing Body
	bb = Part.makeCylinder((ac.yBushing[1]+ac.minthick*2)/2,ac.yBushing[2])
	bb.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	bb.translate(Vector(-ac.yrodxpos,ac.ybushingypos-ac.yBushing[2]/2,ac.yrodzpos))
	
	bbc = Part.makeBox(10,ac.yBushing[2]+12,bpz)
	bbc.translate(Vector(-ac.xrodlen/2-10,ac.ybushingypos-ac.yBushing[2]/2,ac.xrodzcenter - ac.xrodspacing/2 - bc.gantryRodDia/2 - ac.minthick))
	bb = bb.cut(bbc)
	
	#Bushing cut
	buc = Part.makeCylinder((ac.yBushing[1]+ bc.bushingTolerance*2)/2,ac.yBushing[2])
	buc.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	buc.translate(Vector(-ac.yrodxpos,ac.ybushingypos-ac.yBushing[2]/2,ac.yrodzpos))
	bb=bb.cut(buc)
	
	xe=bp.fuse(bb)
	if bc.BushingType == 'LM10LUU':
		xe = xe.makeFillet(ac.minthick,[xe.Edges[16],xe.Edges[34]])
	if bc.BushingType == 'Printed':
		xe = xe.makeFillet(ac.minthick,[xe.Edges[16],xe.Edges[34]])
	
	#Belt Thru
	bt = Part.makeBox(ac.beltThick+ac.beltSpace*2,bpy+40,ac.beltWidth+ac.beltSpace)
	bt.translate(Vector(-ac.gantrymotorxpos-bc.gantryPulleyDia/2-ac.beltThick/2 -(ac.beltThick+ac.beltSpace*2)/2,ac.xrodypos - bpy/2 - 20,ac.gantrydrivecenter-(ac.beltWidth+ac.beltSpace)/2))
	
	
	#Idler Holder Block
	#ihx = (ac.xrodlen/2-ac.gantrybidlerxpos) + (bc.gantryIdlerDia+ac.beltThick*2+ac.beltSpace)/2
	ihx = bpx + 2
	ihy = (ac.gantrycidlerypos-ac.gantrybidlerypos)+bc.gantryIdlerDia+ac.beltThick
	ihz = ps.z624[2]*2+2+ac.minthick*3
	ihb = Part.makeBox(ihx,ihy,ihz)
	ihb.translate(Vector(-ac.xrodlen/2 - 2,(ac.gantrycidlerypos+ac.gantrybidlerypos)/2-ihy/2,ac.gantrydrivecenter-ihz/2))
	ihb = ihb.makeFillet((bc.gantryIdlerDia+ac.beltThick*2+ac.beltSpace/2)/2-0.01,[ihb.Edges[0],ihb.Edges[2],ihb.Edges[4],ihb.Edges[6]])
	ihb = ihb.makeFillet(ac.minthick,[ihb.Edges[0],ihb.Edges[3]])
	ihbc = Part.makeCylinder(bpx/2,ihy)
	ihbc.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	ihbc.translate(Vector(-ac.xrodlen/2 + bpx/2,(ac.gantrycidlerypos+ac.gantrybidlerypos)/2-ihy/2,\
		ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia/2-ps.m3l[0]/2-0.5+bpx/2 - ps.m3l[1]/2 -ac.minthick/2))
	
	xe=xe.fuse(ihb.cut(ihbc))
	#fat cut
	ihbfc = Part.makeBox(ihx+ac.beltSpace,ihy,ps.z624[2]*2+2)
	ihbfc.translate(Vector(-ac.xrodlen/2,(ac.gantrycidlerypos+ac.gantrybidlerypos)/2-ihy/2,ac.gantrydrivecenter -(ps.z624[2]*2+2)/2))
	ihbc = bp.copy()
	ihbc.translate(Vector(-ps.z624[1]-ac.beltThick-ac.beltSpace/2,0,0))
	ihbfc = ihbfc.cut(ihbc)
	
	#Idler Slot
	isc = Part.makeBox(bc.gantryIdlerDia+ac.beltThick*2+ac.beltSpace,ihy,ps.z624[2]*2+2)
	isc.translate(Vector(-ac.gantrybidlerxpos-(bc.gantryIdlerDia+ac.beltThick*2+ac.beltSpace)/2,(ac.gantrycidlerypos+ac.gantrybidlerypos)/2-ihy/2,ac.gantrydrivecenter -(ps.z624[2]*2+2)/2))
	isc = ihbfc
	isc = isc.makeFillet(ac.minthick,[isc.Edges[21],isc.Edges[22],isc.Edges[7],isc.Edges[15],isc.Edges[8],isc.Edges[12],isc.Edges[16],isc.Edges[19]])
	#return isc
	
	xe=xe.cut(isc)
	xe=xe.cut(bt)
	
	#Rod Clamp Slots
	#	upper
	rcs = RodClampSlice(size=bc.gantryRodDia*2,thick=1,wide=bpy,rad=ps.m3l[1]/2+ac.minthick/2)
	rcs.rotate(Vector(0,0,0),Vector(0,1,0),-45)
	rcs.translate(Vector(-ac.xrodlen/2 + bpx/2,ac.xrodypos - bpy/2,ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia-ac.minthick+1))
	rci = RodClampSlice(size=bc.gantryRodDia+ac.minthick,thick=bc.gantryRodDia,wide=ac.minthick/2,rad=ps.m3l[1]/2+ac.minthick/2)
	rci.rotate(Vector(0,0,0),Vector(0,1,0),-45)
	rci.translate(Vector(-ac.xrodlen/2 + bpx/2,ac.xrodypos - ac.minthick/4,ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia-ac.minthick+1))
	rcs = rcs.fuse(rci)
	#screw and insert
	cs = CapHeadScrew(l=30,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	cs.rotate(Vector(0,0,0),Vector(1,0,0),90)
	cs.translate(Vector(-ac.xrodlen/2+bpx/2,ac.xrodypos-bpy/2+ps.m3l[2],ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia/2-ps.m3l[0]/2-0.5))
	ci = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	ci.rotate(Vector(0,0,0),Vector(1,0,0),90)
	ci.translate(Vector(-ac.xrodlen/2+bpx/2,ac.xrodypos+bpy/2,ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia/2-ps.m3l[0]/2-0.5))
	
	css = cs.fuse(ci)
	#	lower
	lrcsx = ps.m3l[1]+ac.minthick*2
	lrcs = Part.makeBox(lrcsx,ac.minthick/2,ac.xrodspacing/3)
	lrcs = lrcs.makeFillet(ac.minthick/4-0.01,[lrcs.Edges[9],lrcs.Edges[11]])
	lrcs.translate(Vector(-ac.xrodlen/2+bpx-lrcsx,ac.xrodypos-ac.minthick/4,ac.xrodzcenter-ac.xrodspacing/2))
	
	ls = ThinSlice(size=bc.gantryRodDia*2.25,thick=1,wide=bpy+ac.minthick*2)
	ls.rotate(Vector(0,0,0),Vector(0,1,0),-45)
	ls.translate(Vector(-ac.xrodlen/2+bpx-lrcsx-ac.minthick*1.6,ac.xrodypos - bpy/2-ac.minthick,ac.xrodzcenter-ac.xrodspacing/2))
	
	#clamp screws and inserts
	cs = CapHeadScrew(l=30,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	cs.rotate(Vector(0,0,0),Vector(1,0,0),90)
	cs.translate(Vector(-ac.xrodlen/2+bpx/2,ac.xrodypos-bpy/2+ps.m3l[2],ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia/2-ps.m3l[0]/2-0.5))
	ci = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	ci.rotate(Vector(0,0,0),Vector(1,0,0),90)
	ci.translate(Vector(-ac.xrodlen/2+bpx/2,ac.xrodypos+bpy/2,ac.xrodzcenter+ac.xrodspacing/2-bc.gantryRodDia/2-ps.m3l[0]/2-0.5))
	cs2 = CapHeadScrew(l=30,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	cs2.rotate(Vector(0,0,0),Vector(1,0,0),90)
	cs2.translate(Vector(-ac.xrodlen/2+bpx-ps.m3l[1]/2-ac.minthick,ac.xrodypos-bpy/2+ps.m3l[2],ac.xrodzcenter-ac.xrodspacing/2+bc.gantryRodDia/2+ps.m3l[0]/2+0.5))
	ci2 = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	ci2.rotate(Vector(0,0,0),Vector(1,0,0),90)
	ci2.translate(Vector(-ac.xrodlen/2+bpx-ps.m3l[1]/2-ac.minthick,ac.xrodypos+bpy/2,ac.xrodzcenter-ac.xrodspacing/2+bc.gantryRodDia/2+ps.m3l[0]/2+0.5))
	css = cs.fuse(ci.fuse(cs2.fuse(ci2)))
	
	#Idle Screws
	isb = CapHeadScrew(l=24,d=ps.m4l[0],hd=ps.m4l[1],hh=-8,cut=1)
	isb.rotate(Vector(0,0,0),Vector(1,0,0),180)
	isb.translate(Vector(-ac.gantrybidlerxpos,ac.gantrybidlerypos,ac.gantrydrivecenter-ihz/2+ps.m4l[2]-1))
	isc = CapHeadScrew(l=24,d=ps.m4l[0],hd=ps.m4l[1],hh=-8,cut=1)
	isc.rotate(Vector(0,0,0),Vector(1,0,0),180)
	isc.translate(Vector(-ac.gantrycidlerxpos,ac.gantrycidlerypos,ac.gantrydrivecenter-ihz/2+ps.m4l[2]-1))
	
	iss=isb.fuse(isc)
	
	#zip-tie slots
	ztwide = 4
	blk1 = Part.makeBox(ac.minthick*2,ztwide,ac.yBushing[1]+ac.minthick)
	blk1.translate(Vector(-ac.yrodxpos-ac.yBushing[1]/2-ac.minthick,ac.ybushingypos-ac.yBushing[2]/2+ztwide,ac.yrodzpos-ac.yBushing[1]/2-ac.minthick/2)) 
	blk2 = Part.makeBox(ac.minthick*2,ztwide,ac.yBushing[1]+ac.minthick)
	blk2.translate(Vector(-ac.yrodxpos-ac.yBushing[1]/2-ac.minthick,ac.ybushingypos+ac.yBushing[2]/2-ztwide*2,ac.yrodzpos-ac.yBushing[1]/2-ac.minthick/2)) 
	
	rng1 = Part.makeCylinder(ac.yBushing[1]/2+ac.minthick+1,ztwide)
	rng1 = rng1.cut(Part.makeCylinder(ac.yBushing[1]/2+ac.minthick-1,ztwide))
	rng1.rotate(Vector(0,0,0),Vector(1,0,0),90)
	rng1.translate(Vector(-ac.yrodxpos,ac.ybushingypos-ac.yBushing[2]/2+ztwide*2,ac.yrodzpos))
	rng2 = Part.makeCylinder(ac.yBushing[1]/2+ac.minthick+1,ztwide)
	rng2 = rng2.cut(Part.makeCylinder(ac.yBushing[1]/2+ac.minthick-1,ztwide))
	rng2.rotate(Vector(0,0,0),Vector(1,0,0),90)
	rng2.translate(Vector(-ac.yrodxpos,ac.ybushingypos+ac.yBushing[2]/2-ztwide,ac.yrodzpos))
	
	zts = blk1.fuse(blk2.fuse(rng1.fuse(rng2)))
	
	xe = xe.cut(bbc)
	xe = xe.cut(buc)
	xe = xe.cut(rcs)
	xe = xe.cut(lrcs)
	xe = xe.cut(ls)
	xe = xe.cut(css)
	xe = xe.cut(iss)
	xe = xe.cut(zts)
	
	xel = xe
	xer = xe.copy()
	xer=xer.mirror(Vector(0,0,0),Vector(1,0,0))
		
	logol = LE3Plogolong(size = 12,deep = 2)
	logol.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	logol.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	logol.translate(Vector(-ac.xrodlen/2,ac.xrodypos-6,ac.yrodzpos + 10))
	
	logor = LE3Plogolong(size = 12,deep = 2)
	logor.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	logor.rotate(Vector(0,0,0),Vector(0,0,1),90)
	logor.translate(Vector(ac.xrodlen/2,ac.xrodypos+6,ac.yrodzpos + 10))
	
	xel = xel.cut(logol)	
	xer = xer.cut(logor)
	
	if dc.forPrint == 1:
		xel.translate(Vector(ac.xrodlen/2,-ac.xrodypos + ps.lm10luu[2]/2 + ac.minthick/2,-ac.xrodzcenter))
		xel.rotate(Vector(0,0,0),Vector(0,1,0),-90)
		xer.translate(Vector(-ac.xrodlen/2,-ac.xrodypos - ps.lm10luu[2]/2 - ac.minthick/2,-ac.xrodzcenter))
		xer.rotate(Vector(0,0,0),Vector(0,1,0),90)
	
	if dc.noMirror == 1:
		return xel
	else:
		xe = xel.fuse(xer)
	xe.translate(Vector(0,ac.mYpos,0))
	return xe
