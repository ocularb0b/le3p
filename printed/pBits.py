#le3p-v0.1.3 - pBits.py

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
from include.shapes import TSlot

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

def cableClip(tall=10):
    gap=0.1
    tb = TSlot(length = tall)
    tb.rotate(Vector(0,0,0),Vector(0,0,1),180)
    clip = Part.makeBox(ac.beamSize,ac.beamSize,tall)
    clip.translate(Vector(-ac.beamSize/2,0,0))
    clip=clip.makeFillet(ac.beamSize/2-0.01,[clip.Edges[2],clip.Edges[6]])
    cc=Part.makeCylinder(ac.beamSize/3,tall)
    cc.translate(Vector(0,ac.beamSize/2,0))
    sl=Part.makeBox(ac.beamSize,gap,tall)
    sl.translate(Vector(0,ac.beamSize/2-gap/2,0))
    th=Part.makeCylinder(1,tall)
    th.translate(Vector(ac.beamSize/3,ac.beamSize/6,0))
    th=th.fuse(th.mirror(Vector(0,0,0),Vector(1,0,0)))
    clip = clip.cut(cc.fuse(sl.fuse(th)))
    clip = clip.fuse(tb)
    clip=clip.makeFillet(ac.beamSize/8,[clip.Edges[40],clip.Edges[36]])
    return clip

def CableClip():
	tall = 3
	t=TSlot(length = tall)
	zrrad = 8
	zrtall = 3.5
	zrthick = 2.5
	cwide = 8
	cthick = zrthick + 4
	ctall = 8
	cl = Part.makeBox(cwide,cthick,ctall)
	cl.translate(Vector(-cwide/2,-cthick,0))
	cl=cl.makeFillet(1,[cl.Edges[0],cl.Edges[4]])
	zr = Part.makeCylinder(zrrad,zrtall)
	zr = zr.cut(Part.makeCylinder(zrrad-zrthick,zrtall))
	zr.translate(Vector(0,-zrrad-0.5,-zrtall/2+ctall/2))
	cc=t.fuse(cl)
	cc=cc.cut(zr)
	return cc

def yStop():
	pair = 1
	xsize = bc.gantryRodDia+ac.minthick
	ysize = 10
	zsize = bc.gantryRodDia+ac.minthick
	clipslot = bc.gantryRodDia-2
	bb = Part.makeBox(xsize+2,ysize,zsize)
	bb=bb.makeFillet(xsize/2-0.01,[bb.Edges[1],bb.Edges[3]])
	bb.translate(Vector(-xsize/2,0,-zsize/2))
	#switch body
	sb=Part.makeBox(bc.gantrySwitchY,bc.gantrySwitchX,bc.gantrySwitchZ)
	sb.translate(Vector(xsize/2,-bc.gantrySwitchX+ysize+1,-bc.gantrySwitchZ/2))
	
	rc=Part.makeCylinder(bc.gantryRodDia/2-0.1,ysize)
	rc.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	rs=Part.makeBox(xsize/2,ysize,clipslot)
	rs.translate(Vector(-xsize/2,0,-clipslot/2))
	zs = bb.cut(rc.fuse(rs))
	zs=zs.makeFillet(1,[zs.Edges[12],zs.Edges[23]])
	#switch screws
	ss=CapHeadScrew(l=10,d=ps.m2c[0],hd=ps.m2c[1],hh=ps.m2c[2],cut=1)
	ss.rotate(Vector(0,0,0),Vector(0,1,0),90)
	ss.translate(Vector(xsize/2+8,ysize-bc.gantrySwitchScrewOffset,+bc.gantrySwitchScrewSpacing/2))
	ss=ss.fuse(ss.mirror(Vector(0,0,0),Vector(0,0,1)))
	zs=zs.cut(ss)
	#zs=zs.fuse(sb)
	
	if dc.forPrint == 1:
		zs.rotate(Vector(0,0,0),Vector(1,0,0),90)
		if pair == 1:
			zs=zs.fuse(zs.mirror(Vector(xsize/2+3,0,0),Vector(1,0,0)))
	else:
		zs.translate(Vector(-ac.yrodxpos,-ac.yrodlen/2+ac.tailadd/2+20,ac.yrodzpos))
	
	if dc.noMirror == 0:
		zs=zs.mirror(Vector(0,0,0),Vector(1,0,0))
		if pair == 1 and dc.forPrint == 0:
			zs=zs.fuse(zs.mirror(Vector(0,0,0),Vector(0,1,0)))
	else:
		if pair == 1 and dc.forPrint == 0:
			zs=zs.fuse(zs.mirror(Vector(0,ac.tailadd/2,0),Vector(0,1,0)))
	
	return zs

def xStop():
    gapmod=2
    rc = Part.makeCylinder(bc.gantryRodDia/2+ac.minthick,ac.minthick)
    rc.rotate(Vector(0,0,0),Vector(0,1,0),90)
    rc.translate(Vector(0,0,ac.xrodspacing/2))
    rc = rc.fuse(rc.mirror(Vector(0,0,0),Vector(0,0,1)))
    bb = Part.makeBox(ac.minthick,ac.minthick,ac.xrodspacing)
    bb.translate(Vector(0,-bc.gantryRodDia/2-ac.minthick,-ac.xrodspacing/2))
    es = Part.makeBox(ac.minthick,ac.minthick+bc.gantryRodDia,ac.xrodspacing/4)
    es.translate(Vector(0,-bc.gantryRodDia/2-ac.minthick,-ac.xrodspacing/5))
    es = es.makeFillet(ac.minthick,[es.Edges[10],es.Edges[11]])
    cs = Part.makeBox(ac.minthick,bc.gantryRodDia/2+ac.minthick,bc.gantryRodDia-gapmod)
    cs.translate(Vector(0,0,-(bc.gantryRodDia-gapmod)/2+ac.xrodspacing/2))
    rd = Part.makeCylinder(bc.gantryRodDia/2,ac.minthick)
    rd.rotate(Vector(0,0,0),Vector(0,1,0),90)
    rd.translate(Vector(0,0,ac.xrodspacing/2))
    rd=rd.fuse(cs)
    rd = rd.fuse(rd.mirror(Vector(0,0,0),Vector(0,0,1)))
    
    xs = rc.fuse(bb)
    xs = xs.makeFillet(bc.gantryRodDia/2-0.01,[xs.Edges[0],xs.Edges[5]])
    xs = xs.fuse(es)
    xs = xs.makeFillet(bc.gantryRodDia/2-0.01,[xs.Edges[24],xs.Edges[60]])
    xs = xs.cut(rd)
    xs = xs.makeFillet(ac.minthick/2,[xs.Edges[73],xs.Edges[74],xs.Edges[107],xs.Edges[111]])
    if dc.forPrint == 0:
        xs.translate(Vector(-ac.xrodlen/2+50,ac.xrodypos,ac.xrodzcenter))
    else:
        xs.rotate(Vector(0,0,0),Vector(0,1,0),90)
        xs.translate(Vector(0,0,ac.minthick))
    return xs

def RumbaMount():
	ysize = 60
	rm = Part.makeBox(ac.beamSize,ysize,ac.beamSize)
	rm=rm.makeFillet(ac.beamSize/2-0.01,[rm.Edges[0],rm.Edges[4],rm.Edges[3],rm.Edges[7]])
	rmc = Part.makeBox(ac.beamSize,ysize,ac.beamSize)
	rmc.translate(Vector(0,-ac.minthick*1.5,-ac.minthick*1.5))
	rmc=rmc.makeFillet(ac.beamSize/2-0.01,[rmc.Edges[11]])
	rm=rm.cut(rmc)
	rms=Part.makeBox(ps.m3l[0]+0.2,ysize-ac.minthick*3-ac.beamSize/2,ac.beamSize)
	rms.translate(Vector(-(ps.m3l[0]+0.2)/2+ac.beamSize/2,ac.beamSize/2,0))
	rms=rms.makeFillet((ps.m3l[0]+0.2)/2-0.01,[rms.Edges[0],rms.Edges[2],rms.Edges[4],rms.Edges[6]])
	rm=rm.cut(rms)
	rmsu=Part.makeBox(ps.m3n[1]+0.1,ysize-ac.minthick*3-ac.beamSize/2+(ps.m3n[1]-ps.m3l[0])*2,ac.beamSize)
	rmsu.translate(Vector(-(ps.m3n[1]+0.1)/2+ac.beamSize/2,ac.beamSize/2-(ps.m3n[1]-ps.m3l[0]),-ac.minthick))
	rmsu=rmsu.makeFillet((ps.m3n[1]+0.1)/2-0.01,[rmsu.Edges[0],rmsu.Edges[2],rmsu.Edges[4],rmsu.Edges[6]])
	rm=rm.cut(rmsu)
	rmms=CapHeadScrew(l=12,d=ps.m3l[0]+0.1,hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	rmms.rotate(Vector(0,0,0),Vector(1,0,0),90)
	rmms.translate(Vector(ac.beamSize/2,ysize-ac.minthick,ac.beamSize/2))
	rm=rm.cut(rmms)
	return rm

def RumbaFanMount():
	xsize = 14
	ysize = 8
	zsize = 40
	
	bb = Part.makeBox(xsize,ysize,zsize)
	bb=bb.makeFillet(2,[bb.Edges[0],bb.Edges[2],bb.Edges[4],bb.Edges[6]])
	bc = Part.makeBox(xsize,ysize,zsize)
	bc=bc.makeFillet(xsize-0.1,[bc.Edges[3]])
	bc.translate(Vector(6,0,10))
	bb=bb.cut(bc)
	bb=bb.makeFillet(2,[bb.Edges[19]])
	
	pin = Part.makeCylinder(0.5,7)
	pins = pin
	for i in range(0,5):
		for j in range(0,2):
			p = pin.copy()
			p.translate(Vector(2.54*i,2.54*j,0))
			pins=pins.fuse(p)
	pins.translate(Vector(2,2.5,0))
	
	mh = Part.makeCylinder(1.8,zsize/2)
	mh.translate(Vector(3,ysize/2,zsize/2))
	
	os = Part.makeCylinder(3.5,zsize)
	os.translate(Vector(-5,ysize/2,0))
	omh = Part.makeCylinder(1.8,zsize/2)
	omh.translate(Vector(-5,ysize/2,zsize/2))
	os=os.cut(omh)
	
	rfm = bb.cut(pins.fuse(mh))
	rfm = rfm.fuse(os)
	return rfm

def HotEndFanMount():
	fansize = 40
	screwspacing = 32
	thick = 7
	hemountdia = 16
	wide = ac.hotEndDia*2 + ac.hotEndSpacing-2
	bb = Part.makeBox(wide,hemountdia+2,thick)
	bb.translate(Vector(-wide/2,-hemountdia/2-6,0))
	hec=Part.makeCylinder(hemountdia/2,thick)
	hec.translate(Vector(-ac.hotEndSpacing/2-ac.hotEndDia/2,0,0))
	hec=hec.fuse(hec.mirror(Vector(0,0,0),Vector(1,0,0)))
	#fan
	f=Part.makeBox(fansize,10,fansize)
	f.translate(Vector(-20,-hemountdia-6,-fansize+thick+(fansize-screwspacing)/4))
	
	#screw
	ss = Part.makeCylinder(2.9/2,5)
	ss.rotate(Vector(0,0,0),Vector(1,0,0),90)
	ss.translate(Vector(screwspacing/2,-hemountdia/2+1-2,thick/2))
	ss=ss.fuse(ss.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	#tenslot
	tsw=6
	ts=Part.makeBox(tsw,hemountdia,thick)
	ts.translate(Vector(-tsw/2,-2,0))
	ts=ts.makeFillet(0.8-0.01,[ts.Edges[0],ts.Edges[4]])
	
	#fan clearance
	fc=Part.makeCylinder(fansize/2-1,10)
	fc.rotate(Vector(0,0,0),Vector(1,0,0),90)
	fc.translate(Vector(0,-4,-fansize/2+thick))
	fc=fc.makeFillet(10-0.01,[fc.Edges[2]])
	
	hef=bb.cut(hec)
	hef=hef.makeFillet(1.2,[hef.Edges[0],hef.Edges[2],hef.Edges[5],hef.Edges[15],hef.Edges[24],hef.Edges[26],hef.Edges[27],hef.Edges[29]])
	hef=hef.cut(ss.fuse(ts))
	hef=hef.cut(fc)
	#hef=hef.fuse(f)
	
	hef.rotate(Vector(0,0,thick/2),Vector(0,1,0),180)
	
	return hef

def PowerSupplyMount(reach=8):
	xsize = ac.beamSize
	ysize = ac.beamSize+reach
	zsize = ac.beamSize*1.5 + 12
	lr = Part.makeBox(xsize,ysize,zsize)
	lr = lr.makeFillet(ac.beamSize/2-0.01,[lr.Edges[0],lr.Edges[1],lr.Edges[3],lr.Edges[4],lr.Edges[5],lr.Edges[7]])
	fc = Part.makeBox(xsize,ysize,zsize)
	fc = fc.makeFillet(ac.minthick,[fc.Edges[10]])
	fc.translate(Vector(0,-ac.minthick,ac.beamSize+ac.minthick))
	bmc = Part.makeBox(ac.beamSize+bc.beamTolerance,ac.beamSize+bc.beamTolerance,ac.beamSize+bc.beamTolerance)
	bmc.translate(Vector(0,0,0))
	s1=CapHeadScrew(l=12,d=ps.m3l[0],hd=ps.m3l[1],hh=-8,cut=1)
	s1.translate(Vector(ac.beamSize/2,ac.beamSize/2,ac.beamSize+ac.minthick-ps.m3l[2]))
	s2=CapHeadScrew(l=50,d=ps.m3l[0],hd=ps.m3l[1],hh=-8,cut=1)
	s2.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	s2.translate(Vector(ac.beamSize/2,ac.beamSize+ac.minthick-ps.m3l[2],ac.beamSize/2))
	s3=CapHeadScrew(l=12,d=ps.m3l[0],hd=ps.m3l[1],hh=-8,cut=1)
	s3.rotate(Vector(0,0,0),Vector(1,0,0),90)
	s3.translate(Vector(ac.beamSize/2,ac.beamSize+reach-ac.minthick+ps.m3l[2],zsize-ac.beamSize/2))
	ss=s1.fuse(s2.fuse(s3))
	psam = lr.cut(fc)
	psam = psam.cut(bmc)
	psam = psam.cut(ss)
	if dc.forPrint == 1:
		psam.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	psamb = psam.copy()
	if dc.forPrint == 0:
		psamb.translate(Vector(-150,0,0))
	else:
		psamb.translate(Vector(xsize+ac.minthick,0,0))
	psam=psam.fuse(psamb)
	return psam

def ControllerArm(seglen = 80):
	cat=Part.makeBox(10,10,10)
	
	ca = cat
	return ca







