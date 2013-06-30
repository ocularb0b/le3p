#le3p-v0.1.3 - pZCarriage.py

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
from include.shapes import RodClampSlice
from include.shapes import ThinSlice
from include.shapes import LE3Plogolong
from include.shapes import FilletFlange
from include.shapes import regPolygon

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()


def zCarriageOld():
  #Body Blank
	bbx = (ac.zrodxpos - ac.zscrewxpos) + ac.minthick *2 + ac.zBushing[1]/2 + bc.zLeadNutDia/2
	bby = ac.zrodspacing 
	bbz = ac.beamSize + ac.minthick * 2
	bb = Part.makeBox(bbx,bby,bbz)
	bb.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,-bby/2,-ac.bedThickAlt))
	bb=bb.makeFillet(bc.zLeadNutDia/2+ac.minthick,[bb.Edges[4],bb.Edges[6]])
	bb = bb.makeFillet(ac.minthick-1,[bb.Edges[8],bb.Edges[9]])
	#Bed Frame Cuts
	size = ac.frameringxlen + ac.beamSize - ac.minthick*2
	bfc = Part.makeBox(size,ac.beamSize+bc.beamTolerance,ac.beamSize+bc.beamTolerance)
	bfc.translate(Vector(-size/2,-ac.zrodspacing/4-ac.beamSize/2-bc.beamTolerance/2,\
		-bc.glassPlateThick - bc.heatPlateThick -bc.heaterOffset - bc.basePlateThick - ac.beamSize+bc.beamTolerance/2))
	bfc = bfc.fuse(bfc.mirror(Vector(0,0,0),Vector(0,1,0)))

	
	#Bushing Housing
	bh = Part.makeCylinder(ac.zBushing[1]/2 + ac.minthick,ac.zBushing[2]+ac.minthick)
	bh.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThick))
	bh = bh.makeFillet(ac.minthick,[bh.Edges[0],bh.Edges[2]])
	#	fillet
	ff = FilletFlange(innerdia = ac.zBushing[1] + ac.minthick*2,filletdia = (ac.bedThick-ac.bedThickAlt)*1,filletthick = bbz)
	ff.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThickAlt))
	ff = ff.makeFillet(ac.minthick,[ff.Edges[1],ff.Edges[2]])
	#	back side cut
	bsc = Part.makeBox(bbx,bby*2,ac.zBushing[2]+ac.minthick)
	bsc.translate(Vector(-ac.zrodxpos-ac.zBushing[1]/2-ac.minthick-bbx,-bby,-ac.bedThick))
	#	out side cut
	osc = Part.makeBox(bbx,ac.zBushing[1]+ac.minthick*2,ac.zBushing[2]+ac.minthick)
	osc.translate(Vector(-ac.zrodxpos-bbx/2,-ac.zrodspacing/2 -(ac.zBushing[1]+ac.minthick*2),-ac.bedThick))
	
	#	Assembly
	bh = bh.fuse(ff)
	bh = bh.cut(bsc)
	bh = bh.fuse(bh.mirror(Vector(0,0,0),Vector(0,1,0)))

	#Leadnut Housing
	lh = Part.makeCylinder(bc.zLeadNutDia/2 + ac.minthick,bc.zLeadNutLen+ac.minthick)
	lh.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt + ac.minthick))
	lh=lh.makeFillet(ac.minthick,[lh.Edges[0]])
	#	fillet
	ff = FilletFlange(innerdia = bc.zLeadNutDia + ac.minthick*2,filletdia = (bc.zLeadNutLen-bbz)*2-0.01,filletthick = bbz)
	ff.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt))
	ff = ff.makeFillet(ac.minthick,[ff.Edges[2]])
	
	#	lower cut
	lc = Part.makeCylinder(bc.zLeadNutDia/2 + ac.minthick+(bc.zLeadNutLen-bbz)*2,(bc.zLeadNutLen-bbz)*2)
	lc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt + ac.minthick-((bc.zLeadNutLen-bbz)*2)))
	
	#	bed side cut
	bsc = Part.makeBox((bc.zLeadNutLen-bbz)*2-0.01,bby,bc.zLeadNutLen+ac.minthick)
	bsc.translate(Vector(-ac.zscrewxpos+bc.zLeadNutDia/2+ac.minthick,-bby/2,-ac.bedThickAlt))
	
	#	Assembly
	lh = lh.fuse(ff)
	lh = lh.cut(lc)
	lh = lh.cut(bsc)
	
	#Spines
	bs = Part.makeBox(ac.minthick,ac.zBushing[1],ac.zBushing[2])
	bs.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,-ac.zrodspacing/2 -ac.zBushing[1]/2,-ac.bedThick+ac.minthick/2))
	bs = bs.makeFillet(ac.minthick,[bs.Edges[8],bs.Edges[9],bs.Edges[10],bs.Edges[11]])
	bs = bs.fuse(bs.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	cs = Part.makeBox(bbx - ac.minthick,ac.minthick*2,bc.zLeadNutLen+ac.minthick*1.5)
	cs.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,-ac.minthick,-ac.bedThickAlt))
	csb = Part.makeBox(bbx - ac.minthick,ac.minthick*4,bbz)
	csb.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,-ac.minthick*2,-ac.bedThickAlt))
	cs=cs.fuse(csb)
	
	cs = cs.makeFillet(ac.minthick-0.01,[cs.Edges[1],cs.Edges[3],cs.Edges[7],cs.Edges[11]])
	
	#Bushing Cuts
	bcs = Part.makeCylinder(ac.zBushing[1]/2 + bc.bushingTolerance,ac.zBushing[2])
	bcs.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThick))
	bcs = bcs.fuse(bcs.mirror(Vector(0,0,0),Vector(0,1,0)))
	#Rod Cuts
	rcs = Part.makeCylinder(bc.zRodDia/2 + bc.rodClearance,ac.zBushing[2]+ac.minthick)
	rcs.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThick))
	rcs = rcs.fuse(rcs.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	#Leadscrew cut
	lsc = Part.makeCylinder(bc.zScrewDia/2+bc.rodClearance,bc.zLeadNutLen + ac.minthick*2)
	lsc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt))
	
	#Leadnut Cut
	lnc = regPolygon(sides=6,radius=bc.zLeadNutDia/2,extrude=bc.zLeadNutLen)
	lnc.rotate(Vector(0,0,0),Vector(0,0,1),30)
	lnc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt))
	
	#rear cutout
	rco = Part.makeBox(bbx/2,bby/4,ac.beamSize)
	rco.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,-bby/8,-ac.bedThickAlt))
	rco=rco.makeFillet(ac.minthick,[rco.Edges[4],rco.Edges[5],rco.Edges[6],rco.Edges[9],rco.Edges[11]])
	
	#Beam Mount Screws
	bms1 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	bms1.translate(Vector(-size/2 + (bbx-ac.minthick)/4,-ac.zrodspacing/4-ac.beamSize/2-bc.beamTolerance/2+ac.beamSize/2,-ac.bedThickAlt + bbz - ps.m3l[2]))
	bms2 = bms1.copy()
	bms2.translate(Vector((bbx-ac.minthick)/2,0,0))
	bms = bms1.fuse(bms2)
	bms = bms.fuse(bms.mirror(Vector(0,0,0),Vector(0,1,0)))
	bms = bms.fuse(bms.mirror(Vector(0,0,-ac.bedThickAlt + ac.minthick + ac.beamSize/2),Vector(0,0,1)))
	
	#Assembly
	zc = bb.fuse(bh.fuse(lh))
	zc = zc.cut(bfc)
	zc = zc.fuse(bs.fuse(cs))
	zc = zc.cut(bcs.fuse(rcs))
	zc = zc.cut(lsc)
	zc = zc.cut(lnc)
	zc = zc.cut(rco)
	zc = zc.cut(bms)
	
	zcl = zc
	zcr= zc.copy()
	zcr = zcr.mirror(Vector(0,0,0),Vector(1,0,0))
	
	#logo
	logol = LE3Plogolong(size=ac.beamSize,deep=3)
	logol.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	logol.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,ac.zrodspacing/2+ac.zBushing[1]/3,-ac.bedThickAlt+ac.minthick))
	
	logor = LE3Plogolong(size=ac.beamSize,deep=3)
	logor.rotate(Vector(0,0,0),Vector(0,0,1),90)
	logor.translate(Vector(ac.zrodxpos + ac.zBushing[1]/2 + ac.minthick,ac.zrodspacing/2+ac.zBushing[1]/3-34,-ac.bedThickAlt+ac.minthick))
	
	
	zcl = zcl.cut(logol)
	zcr = zcr.cut(logor)
	if dc.forPrint == 1:
		zcl.translate(Vector(ac.xrodlen/2+1.5,0,-2))
		zcl.rotate(Vector(0,0,0),Vector(0,1,0),-90)
		zcr.translate(Vector(-ac.xrodlen/2-1.5,0,-2))
		zcr.rotate(Vector(0,0,0),Vector(0,1,0),90)
	if dc.noMirror == 0:
		zc = zcl.fuse(zcr)
		zc.translate(Vector(0,0,ac.mZpos))
	else:
		zc = zcl
		zc.translate(Vector(0,0,ac.mZpos))
	return zc

def zCarriage():
	#bushing holder blanks
	bh = Part.makeCylinder((ac.zBushing[1]+ac.minthick*2)/2,ac.zBushing[2]+ac.minthick)
	bh.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThick+ac.bedBushOffset))
	bh=bh.makeFillet(ac.minthick,[bh.Edges[0],bh.Edges[2]])
	bh=bh.fuse(bh.mirror(Vector(0,0,0),Vector(0,1,0)))
	#Leadnut holder blank
	lnhdia = 30
	lnhlen = bc.zLeadNutLen+ac.minthick*4
	lnh = Part.makeCylinder(lnhdia/2,lnhlen)
	lnh.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt-ac.minthick))
	lnh=lnh.makeFillet(ac.minthick,[lnh.Edges[0],lnh.Edges[2]])
	# Body Blank
	bbw=ac.zrodspacing
	bb = Part.makeBox(50,bbw,ac.beamSize+ac.minthick*2)
	bb.translate(Vector(-ac.zrodxpos-(ac.zBushing[1]+ac.minthick*2)/2,-(bbw)/2,-ac.bedThickAlt-ac.minthick))
	bb=bb.makeFillet(ac.minthick*2,[bb.Edges[4],bb.Edges[6]])
	bb=bb.makeFillet(ac.minthick,[bb.Edges[0],bb.Edges[3]])
	#Bushing Spine
	bsp = Part.makeBox((ac.zBushing[1]+ac.minthick*2)/2,ac.zBushing[1],ac.zBushing[2]+ac.minthick)
	bsp.translate(Vector(-ac.zrodxpos-(ac.zBushing[1]+ac.minthick*2)/2,-ac.zrodspacing/2-ac.zBushing[1]/2,-ac.bedThick+ac.bedBushOffset))
	bsp=bsp.makeFillet(ac.minthick,[bsp.Edges[8],bsp.Edges[9],bsp.Edges[10],bsp.Edges[11]])
	bsp=bsp.fuse(bsp.mirror(Vector(0,0,0),Vector(0,1,0)))
	#Leadnut Spine
	lsp = Part.makeBox(30,lnhdia/2,lnhlen)
	lsp.translate(Vector(-ac.zrodxpos-(ac.zBushing[1]+ac.minthick*2)/2,-lnhdia/4,-ac.bedThickAlt-ac.minthick))
	lsp=lsp.makeFillet(ac.minthick,[lsp.Edges[9],lsp.Edges[11]])
	#body assembly
	bb=bb.fuse(bsp)
	bb=bb.makeFillet(ac.minthick,[bb.Edges[32],bb.Edges[34]])
	bb=bb.fuse(lsp)
	bb=bb.makeFillet(ac.minthick,[bb.Edges[20],bb.Edges[33]])
	#bed frame cuts
	size = ac.frameringxlen + ac.beamSize - ac.minthick*2
	bfc = Part.makeBox(size,ac.beamSize+bc.beamTolerance,ac.beamSize+bc.beamTolerance)
	bfc.translate(Vector(-size/2,-ac.zrodspacing/4-ac.beamSize/2-bc.beamTolerance/2,\
		-bc.glassPlateThick - bc.heatPlateThick -bc.heaterOffset - bc.basePlateThick - ac.beamSize+bc.beamTolerance/2))
	bfc = bfc.fuse(bfc.mirror(Vector(0,0,0),Vector(0,1,0)))
	#Bushing Cuts
	bcs = Part.makeCylinder(ac.zBushing[1]/2 + bc.bushingTolerance,ac.zBushing[2])
	bcs.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThick+ac.bedBushOffset))
	bcs = bcs.fuse(bcs.mirror(Vector(0,0,0),Vector(0,1,0)))
	#Rod Cuts
	rcs = Part.makeCylinder(bc.zRodDia/2 + bc.rodClearance,ac.zBushing[2]+ac.minthick)
	rcs.translate(Vector(-ac.zrodxpos,-ac.zrodspacing/2,-ac.bedThick+ac.bedBushOffset))
	rcs = rcs.fuse(rcs.mirror(Vector(0,0,0),Vector(0,1,0)))
	#Leadscrew cut
	lsc = Part.makeCylinder(bc.zScrewDia/2+bc.rodClearance/2,lnhlen)
	lsc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt-ac.minthick))
	#Leadnut Cut
	lnc = regPolygon(sides=6,radius=bc.zLeadNutDia/2,extrude=ps.m5n[2]-0.2)
	lnc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt+ac.minthick+ps.m5n[2]+9+0.2))
	#Leadnut Holder Clearance
	lhc = Part.makeCylinder(lnhdia/2-ac.minthick/2,lnhlen-ac.minthick*2-ps.m5n[2])
	lhc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt-ac.minthick))
	#Clamps Screws
	cs = CapHeadScrew(l=30,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	cs.translate(Vector(-ac.zscrewxpos-ps.m3l[1]-2,0,-ac.bedThickAlt-ac.minthick+30))
	cs2 = cs.copy()
	cs2.rotate(Vector(-ac.zscrewxpos,0,0),Vector(0,0,1),120)
	cs3 = cs.copy()
	cs3.rotate(Vector(-ac.zscrewxpos,0,0),Vector(0,0,1),-120)
	cs=cs.fuse(cs2.fuse(cs3))
	#Beam Mount Screws
	bms = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	bms.rotate(Vector(0,0,0),Vector(0,1,0),180)
	bms.translate(Vector(-ac.zscrewxpos+8,-ac.zrodspacing/4-ac.beamSize/2-bc.beamTolerance/2+ac.beamSize/2,-ac.bedThickAlt-ac.minthick+2.5))
	bms = bms.fuse(bms.mirror(Vector(0,0,0),Vector(0,1,0)))
	#logo
	logol = LE3Plogolong(size=ac.beamSize,deep=3)
	logol.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	logol.translate(Vector(-ac.zrodxpos - ac.zBushing[1]/2 - ac.minthick,ac.zrodspacing/2+ac.zBushing[1]/4,-ac.bedThickAlt))
	
	logor = LE3Plogolong(size=ac.beamSize,deep=3)
	logor.rotate(Vector(0,0,0),Vector(0,0,1),90)
	logor.translate(Vector(ac.zrodxpos + ac.zBushing[1]/2 + ac.minthick,ac.zrodspacing/2+ac.zBushing[1]/4-34,-ac.bedThickAlt))
	
	####################################################################
	#Nut Clamp
	ncb = Part.makeCylinder(lnhdia/2-ac.minthick/2-0.8,ac.minthick*2)
	ncb.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt-ac.minthick+ps.m5n[2]-1))
	ncb=ncb.cut(cs)
	#inserts
	ci = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	ci.translate(Vector(-ac.zscrewxpos-ps.m3l[1]-2,0,-ac.bedThickAlt-ac.minthick+ps.m5n[2]-1))
	ci2 = ci.copy()
	ci2.rotate(Vector(-ac.zscrewxpos,0,0),Vector(0,0,1),120)
	ci3 = ci.copy()
	ci3.rotate(Vector(-ac.zscrewxpos,0,0),Vector(0,0,1),-120)
	ci=ci.fuse(ci2.fuse(ci3))
	ncb=ncb.cut(ci)
	#Low Leadnut Cut
	llnc = regPolygon(sides=6,radius=bc.zLeadNutDia/2,extrude=ps.m5n[2]-0.2)
	llnc.translate(Vector(-ac.zscrewxpos,0,-ac.bedThickAlt+ac.minthick))
	ncb=ncb.cut(llnc.fuse(lsc))

	zc = bh.fuse(lnh.fuse(bb))
	zc = zc.cut(bfc.fuse(bcs.fuse(rcs.fuse(lsc.fuse(lnc.fuse(lhc))))))
	zc = zc.cut(cs.fuse(bms))
	zc = zc.fuse(ncb)
	zcl = zc
	zcr = zc.mirror(Vector(0,0,0),Vector(1,0,0))
	zcl=zcl.cut(logol)
	zcr=zcr.cut(logor)
	#hall sensor pocket
	hsp=Part.makeBox(3,10,3)
	hsp=hsp.makeFillet(1.2,[hsp.Edges[8],hsp.Edges[9],hsp.Edges[10],hsp.Edges[11]])
	hsp.translate(Vector(ac.zrodxpos+(ac.zBushing[1]+ac.minthick*2)/2-3,-ac.zrodspacing/2-5,-ac.bedThick+ac.bedBushOffset+ac.zBushing[2]+ac.minthick-1.5-25))
	zcr=zcr.cut(hsp)
	
	if dc.noMirror == 0:
		zcs=zcl.fuse(zcr)
	else:
		zcs=zcl
	zcs.translate(Vector(0,0,ac.mZpos))
	return zcs
