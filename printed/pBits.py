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
from include.shapes import regPolygon
from include.shapes import LE3Plogolong

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

def BeamClip(tall=10): #fairly useless on it's own
	wall = 3
	finger = 3
	rib = 3
	ribdepth = 1.5
	#body blank
	bb = Part.makeBox(ac.beamSize/2+wall+rib/2+finger,ac.beamSize/2+wall+rib/2+finger,tall)
	bb.translate(Vector(+ac.beamSize/2-rib/2-finger,+ac.beamSize/2-rib/2-finger,0))
	#beam cut
	bc = Part.makeBox(ac.beamSize,ac.beamSize,tall)
	bb = bb.cut(bc)
	bb = bb.makeFillet(wall-0.01,[bb.Edges[2],bb.Edges[4],bb.Edges[17]])
	bb.translate(Vector(-ac.beamSize/2,-ac.beamSize/2,0))
	#beam rib
	br = Part.makeBox(rib,ribdepth,tall)
	br.translate(Vector(-rib/2,ac.beamSize/2-ribdepth,0))
	if rib <= ribdepth:
		br = br.makeFillet(rib-0.01,[br.Edges[0]])
	else:
		br = br.makeFillet(ribdepth-0.01,[br.Edges[0]])
	br = br.fuse(br.mirror(Vector(0,0,0),Vector(-1,1,0)))
	
	clip = bb.fuse(br)
	return clip

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

def LedBracket():
	striplen = 50
	wallthick = 3
	ribthick = 3
	fingergriplen = wallthick
	coverad = 19.5
	coveyoff = 0.75
	
	#body blank
	bb = Part.makeBox(striplen,ac.beamSize/2+ribthick/2+wallthick+fingergriplen,ac.beamSize/2+ribthick/2+wallthick+fingergriplen)
	bb.translate(Vector(-striplen/2,-ribthick/2-ac.beamSize/2-fingergriplen,-ribthick/2-fingergriplen))
	#beam cut
	bc = Part.makeBox(striplen,ac.beamSize,ac.beamSize)
	bc.translate(Vector(-striplen/2,-ac.beamSize,-ac.beamSize/2))
	#clip ribs
	cr = Part.makeCylinder(ribthick/2,striplen)
	cr.translate(Vector(0,0,-striplen/2))
	cr.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	cr2 = Part.makeCylinder(ribthick/2,striplen)
	cr2.translate(Vector(0,0,-striplen/2))
	cr2.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	cr2.translate(Vector(0,-ac.beamSize/2,ac.beamSize/2))
	cr = cr.fuse(cr2)
	#lamp cove
	lc = Part.makeCylinder(coverad+wallthick*2,striplen)
	lc.translate(Vector(0,0,-striplen/2))
	lc.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	lc.translate(Vector(0,coverad+wallthick+coveyoff,0))
	lcc = regPolygon(sides = 12,radius=coverad,extrude=striplen)
	lcc.translate(Vector(0,0,-striplen/2))
	lcc.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	lcc.translate(Vector(0,coverad+wallthick+coveyoff,0))
	lcbc=Part.makeBox(striplen,coverad*2+wallthick*4,coverad+wallthick*2)
	lcbc.translate(Vector(-striplen/2,coveyoff-wallthick,-coverad-wallthick*2))
	lcfc=Part.makeBox(striplen,coverad*2+wallthick*2,coverad+wallthick*2)
	lcfc.translate(Vector(-striplen/2,coveyoff+coverad+wallthick,))
	lc=lc.cut(lcc.fuse(lcbc.fuse(lcfc)))
	lc.translate(Vector(0,0,-fingergriplen-ribthick/2))
	lc=lc.makeFillet(wallthick,[lc.Edges[2]])

	lb = bb
	lb = lb.fuse(lc)
	lb = lb.cut(bc)
	lb = lb.makeFillet(wallthick-0.01,[lb.Edges[3],lb.Edges[8],lb.Edges[22]])
	lb = lb.fuse(cr)
	
	
	if dc.forPrint == 0:
		lb.translate(Vector(0,-ac.frameringylen/2+ac.tailadd/2,ac.frameysupportszpos))
		lb2=lb.copy()
		lb2.translate(Vector(-striplen,0,0))
		lb3=lb.copy()
		lb3.translate(Vector(-striplen*2,0,0))
		lb4=lb.copy()
		lb4.translate(Vector(striplen,0,0))
		lb5=lb.copy()
		lb5.translate(Vector(striplen*2,0,0))
		lb6=lb.copy()
		lb6.translate(Vector(striplen*3,0,0))
		lb = lb.fuse(lb2.fuse(lb3.fuse(lb4.fuse(lb5.fuse(lb6)))))
		lb.translate(Vector(-striplen/2,0,0))
	else:
		lb.rotate(Vector(0,0,0),Vector(0,1,0),90)
		lb.translate(Vector(0,0,+striplen/2))
	return lb

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
	thick = 12
	rc = Part.makeCylinder(bc.gantryRodDia/2+ac.minthick,thick)
	rc.rotate(Vector(0,0,0),Vector(0,1,0),90)
	rc.translate(Vector(0,0,ac.xrodspacing/2))
	rc = rc.fuse(rc.mirror(Vector(0,0,0),Vector(0,0,1)))
	bb = Part.makeBox(thick,ac.minthick,ac.xrodspacing)
	bb.translate(Vector(0,-bc.gantryRodDia/2-ac.minthick,-ac.xrodspacing/2))
	es = Part.makeBox(thick,ac.minthick+bc.gantryRodDia,ac.xrodspacing/4)
	es.translate(Vector(0,-bc.gantryRodDia/2-ac.minthick,-ac.xrodspacing/5))
	es = es.makeFillet(ac.minthick,[es.Edges[10],es.Edges[11]])
	cs = Part.makeBox(thick,bc.gantryRodDia/2+ac.minthick,bc.gantryRodDia-gapmod)
	cs.translate(Vector(0,0,-(bc.gantryRodDia-gapmod)/2+ac.xrodspacing/2))
	rd = Part.makeCylinder(bc.gantryRodDia/2,thick)
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
		xs.translate(Vector(0,0,thick))
	return xs

def DialIndicatorHolder():
	gapmod=2
	thick = 40
	clampscrewdia = 6.8
	clampscrewlen = 47
	clampscrewshoulder = 6.5
	clampscrewshoulderlen = 3
	
	mountx = 6.5
	mounty = 18
	mountz = 18
	mountxcenter = 12
	mountzcenter = -15
	mountycenter = 0
	
	outerz = ac.xrodspacing/2 + bc.gantryRodDia/2 + ac.minthick
	
	rc = Part.makeCylinder(bc.gantryRodDia/2+ac.minthick,thick)
	rc.rotate(Vector(0,0,0),Vector(0,1,0),90)
	rc.translate(Vector(0,0,ac.xrodspacing/2))
	rc = rc.fuse(rc.mirror(Vector(0,0,0),Vector(0,0,1)))
	bb = Part.makeBox(thick,ac.minthick,outerz*2)
	bb = bb.makeFillet(ac.minthick,[bb.Edges[1],bb.Edges[3],bb.Edges[5],bb.Edges[7]])
	bb.translate(Vector(0,-bc.gantryRodDia/2-ac.minthick,-outerz))
	es = Part.makeBox(thick,ac.minthick+bc.gantryRodDia+4.25,ac.xrodspacing/2)
	es.translate(Vector(0,-bc.gantryRodDia/2-ac.minthick,-ac.xrodspacing/2))
	es = es.makeFillet(ac.minthick,[es.Edges[11]])
	cs = Part.makeBox(thick,bc.gantryRodDia/2+ac.minthick,bc.gantryRodDia-gapmod)
	cs.translate(Vector(0,0,-(bc.gantryRodDia-gapmod)/2+ac.xrodspacing/2))
	rd = Part.makeCylinder(bc.gantryRodDia/2,thick)
	rd.rotate(Vector(0,0,0),Vector(0,1,0),90)
	rd.translate(Vector(0,0,ac.xrodspacing/2))
	rd=rd.fuse(cs)
	rd = rd.fuse(rd.mirror(Vector(0,0,0),Vector(0,0,1)))
	#clamp screw
	cs = Part.makeCylinder(clampscrewdia/2,clampscrewlen)
	cs.rotate(Vector(0,0,0),Vector(0,1,0),90)
	cs.translate(Vector(clampscrewshoulderlen,mountycenter,mountzcenter))
	csh = Part.makeBox(clampscrewshoulderlen,clampscrewshoulder,clampscrewshoulder)
	csh.translate(Vector(0,-clampscrewshoulder/2,-clampscrewshoulder/2))
	csh.translate(Vector(0,mountycenter,mountzcenter))
	cs=cs.fuse(csh)
	#dial indicator slot
	di = Part.makeBox(mountx,mounty+10,mountz)
	di.translate(Vector(-mountx/2,0,-mountz/2))
	di.translate(Vector(mountxcenter,-bc.gantryRodDia/2-ac.minthick,mountzcenter))
	
	xs = rc.fuse(bb)
	xs = xs.fuse(es)
	xs = xs.cut(rd)
	xs = xs.cut(cs)
	xs = xs.cut(di)
	
	xs = xs.makeFillet(bc.gantryRodDia/2-0.01,[xs.Edges[114],xs.Edges[115]])
	xs = xs.makeFillet(ac.minthick/2,[xs.Edges[56],xs.Edges[80],xs.Edges[138],xs.Edges[163]])
	
	
	
	if dc.forPrint == 0:
		#xs.translate(Vector(-ac.xrodlen/2+50,ac.xrodypos,ac.xrodzcenter))
		return xs
	else:
		xs.rotate(Vector(0,0,0),Vector(1,0,0),90)
		xs.translate(Vector(0,0,bc.gantryRodDia/2+ac.minthick))
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

def HotEndFanMountOld():
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
	
	if dc.forPrint == 1:
		hef.rotate(Vector(0,0,thick/2),Vector(0,1,0),180)
	
	if dc.forPrint == 0:
		hef.translate(Vector(ac.mXpos,ac.mYpos,ac.envelopeZ + ac.hotEndLen - ac.hotEndMountLen-7.4))
	
	return hef

def HotEndFanMount():
	fansize = 40
	screwspacing = 32
	thick = 3
	space = 5
	hemountdia = 25
	fanoffset = 3
	
	#Body Blank
	bb = Part.makeBox(ac.hotEndDia*2+space*2+thick*2+ac.hotEndSpacing,ac.hotEndDia+space*2+thick*2,fansize+thick)
	bb.translate(Vector(-(ac.hotEndDia*2+space*2+thick*2+ac.hotEndSpacing)/2,-(ac.hotEndDia+space*2+thick*2)/2,-ac.hotEndLen+18))
	bb = bb.makeFillet((ac.hotEndDia+space*2+thick*2)/2-0.01,[bb.Edges[0],bb.Edges[2],bb.Edges[4],bb.Edges[6]])
	#Back fat
	bf = Part.makeBox(ac.hotEndDia*2+space*2+thick*2+ac.hotEndSpacing,ac.hotEndDia+space*2+thick*2,fansize+thick)
	bf.translate(Vector(-(ac.hotEndDia*2+space*2+thick*2+ac.hotEndSpacing)/2,+(ac.hotEndDia+space*2+thick*2)/2-space,-ac.hotEndLen+18))
	bb = bb.cut(bf)
	bb = bb.makeFillet((ac.hotEndDia+space+thick)/2,[bb.Edges[14],bb.Edges[20]])
	
	#main cut
	mc = Part.makeBox(ac.hotEndDia*2+space*2+ac.hotEndSpacing,ac.hotEndDia+space*2,fansize+thick)
	mc.translate(Vector(-(ac.hotEndDia*2+space*2+ac.hotEndSpacing)/2,-(ac.hotEndDia+space*2)/2,-ac.hotEndLen+18+thick))
	mc = mc.makeFillet((ac.hotEndDia+space*2)/2-0.01,[mc.Edges[0],mc.Edges[2],mc.Edges[4],mc.Edges[6]])
	#Back fat
	mcbf = Part.makeBox(ac.hotEndDia*2+space*2+ac.hotEndSpacing,ac.hotEndDia+space*2,fansize+thick)
	mcbf.translate(Vector(-(ac.hotEndDia*2+space*2+ac.hotEndSpacing)/2,+(ac.hotEndDia+space*2)/2-space,-ac.hotEndLen+18+thick))
	mc = mc.cut(mcbf)
	mc = mc.makeFillet((ac.hotEndDia+space)/2-1,[mc.Edges[14],mc.Edges[20]])
	
	hef = bb.cut(mc)
	
	if dc.forPrint == 1:
		#hef.rotate(Vector(0,0,thick/2),Vector(0,1,0),180)
		return hef
	
	if dc.forPrint == 0:
		hef.translate(Vector(ac.mXpos,ac.mYpos,ac.envelopeZ + ac.hotEndLen))
	
	return hef

def NozzelFanShroud():
	fs = Part.makeBox(10,10,10)
	#if dc.forPrint == 0:
		#nfs.translate(Vector(-ac.hotEndSpacing/2-ac.hotEndDia/2,0,ac.envelopeZ+torthick/2+1))
	return fs

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

def LedPowerSupplyBracket():
	psy = 30
	psz = 20
	wide = 20
	thick = 3
	
	pb = Part.makeBox(wide,psy+thick*2,psz+thick+ac.beamSize/2 + thick)
	bc = Part.makeBox(wide,ac.beamSize,ac.beamSize)
	bc.translate(Vector(0,(psy+thick*2)/2-ac.beamSize/2,-ac.beamSize/2+1.5))
	pb = pb.cut(bc)
	
	pc = Part.makeBox(wide,psy,psz+thick)
	pc.translate(Vector(0,thick,ac.beamSize/2 + thick + 1.5))
	pb = pb.cut(pc)
	
	fc = Part.makeBox(wide,((psy+thick*2)-ac.beamSize)/2-thick,ac.beamSize/2+1.5)
	fc = fc.makeFillet(ac.minthick,[fc.Edges[11]])
	fc = fc.fuse(fc.mirror(Vector(0,(psy+thick*2)/2,0),Vector(0,1,0)))
	pb = pb.cut(fc)
	pb = pb.makeFillet(thick-0.01,[pb.Edges[51],pb.Edges[21],pb.Edges[1],pb.Edges[46],pb.Edges[43],pb.Edges[42]])
	
	bt = Part.makeCylinder(3/2,wide)
	bt.rotate(Vector(0,0,0),Vector(0,1,0),90)
	bt.translate(Vector(0,((psy+thick*2)-ac.beamSize)/2,1.5))
	bt = bt.fuse(bt.mirror(Vector(0,(psy+thick*2)/2,0),Vector(0,1,0)))
	pb = pb.fuse(bt)
	
	pt = Part.makeCylinder(thick/2,wide)
	pt.rotate(Vector(0,0,0),Vector(0,1,0),90)
	pt.translate(Vector(0,thick,psz+thick+ac.beamSize/2 + thick/2))
	pt = pt.fuse(pt.mirror(Vector(0,(psy+thick*2)/2,0),Vector(0,1,0)))
	pb = pb.fuse(pt)
	
	
	pb.translate(Vector(0,ac.framezmotorsupportsspacing/2-(psy+thick*2)/2,ac.frameringazpos-1.5))
	return pb

def ControllerArm():
	tall = 12
	mountsize = 8
	wall = 3
	mountscrewdia = 3.5
	cl = BeamClip(tall)
	mp = Part.makeBox(3,wall + mountsize,mountsize)
	mp = mp.makeFillet(wall/2-0.01,[mp.Edges[2],mp.Edges[6],mp.Edges[10],mp.Edges[11]])
	mp.translate(Vector(ac.beamSize/2,ac.beamSize/2,0))
	ms = Part.makeCylinder(mountscrewdia/2,wall)
	ms.rotate(Vector(0,0,0),Vector(0,1,0),90)
	ms.translate(Vector(ac.beamSize/2,ac.beamSize/2+wall+mountsize/2,mountsize/2))
	ca = cl.fuse(mp)
	ca = ca.cut(ms)
	if dc.forPrint == 1:
		ca = ca.fuse(ca.mirror(Vector(ac.beamSize/2+wall+2,0,0),Vector(1,0,0)))
		ca.translate(Vector(-ac.beamSize/2-wall-2,-ac.beamSize/2,0))
	else:
		ca.rotate(Vector(0,0,0),Vector(0,0,1),-90)
		ca = ca.fuse(ca.mirror(Vector(0,0,50),Vector(0,0,1)))
		ca.translate(Vector(ac.frameringxlen/2+ac.beamSize/2,ac.frameringylen/2+ac.tailadd/2+ac.beamSize/2))
	return ca

def SpanPlate(zsize=50,xsize=20):
	ztol = 0.25
	platethick = 3
	rib = 3
	off = 0.25
	#body blank
	bb = Part.makeBox(xsize,ac.beamSize/2+rib/2-off,zsize-ztol*2)
	bb.translate(Vector(0,off,ztol))
	#back fat
	bf = Part.makeBox(xsize,ac.beamSize+1,zsize-ztol*2-platethick*2)
	bf = bf.makeFillet(ac.beamSize,[bf.Edges[8],bf.Edges[9]])
	bf.translate(Vector(0,platethick,ztol+platethick))
	sp = bb.cut(bf)
	sp = sp.makeFillet(platethick*2,[sp.Edges[20],sp.Edges[21]])
	
	#Extrusion Nibs
	en = Part.makeCylinder(1.5,xsize)
	en.rotate(Vector(0,0,0),Vector(0,1,0),90)
	en.translate(Vector(0,ac.beamSize/2,ztol))
	en = en.fuse(en.mirror(Vector(0,0,zsize/2),Vector(0,0,1)))
	
	sp = sp.fuse(en)
	
	return sp

def DimmerMount():
	zsize = 60
	xsize = 40
	sc = SpanPlate(zsize,xsize)
	
	bh = Part.makeBox(ps.m3l[1]+ac.minthick*2,45,ac.minthick*2)
	bh = bh.makeFillet(ac.minthick,[bh.Edges[2],bh.Edges[6]])
	bhc = Part.makeBox(ps.m3l[1]+ac.minthick*2,45,ac.minthick*2)
	bhc = bhc.makeFillet(ac.minthick,[bhc.Edges[9]])
	bhc.translate(Vector(0,ac.minthick+2,-ac.minthick))
	bh=bh.cut(bhc)
	bhs = Part.makeBox(ps.m3l[1],30,ac.minthick)
	bhs.translate(Vector(ac.minthick,12,ac.minthick))
	bhs = bhs.makeFillet(ps.m3l[1]/2-0.01,[bhs.Edges[0],bhs.Edges[2],bhs.Edges[4],bhs.Edges[6]])
	bh=bh.cut(bhs)
	bh.translate(Vector(-(ps.m3l[1]+ac.minthick*2)/2+xsize/2-1.5,2,4))
	
	ph = Part.makeCylinder(7.2/2,ac.minthick)
	ph.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	ph.translate(Vector(xsize/2,0,zsize/2))
	
	dm = sc.fuse(bh)
	dm = dm.cut(ph)
	
	
	
	if dc.forPrint == 0:
		dm.translate(Vector(ac.frameringxlen/3-xsize/2,-ac.frameringylen/2+ac.tailadd/2-ac.beamSize,ac.frameringazpos+ac.beamSize/2))
	if dc.forPrint == 1:
		dm.rotate(Vector(0,0,0),Vector(1,0,0),90)
		dm.translate(Vector(-xsize/2,zsize/2,0))
		
	return dm

def VertConduitSeg(type=0):
	tall = 83
	#Beam Clip
	cl = BeamClip(tall)
	cl.rotate(Vector(0,0,0),Vector(0,0,1),180)
	clc = Part.makeCylinder(tall/3,ac.beamSize*2)
	clc.translate(Vector(0,0,-ac.beamSize))
	clc.rotate(Vector(0,0,0),Vector(1,0,0),90)
	clc.translate(Vector(ac.beamSize*1.5,0,0))
	clc = clc.fuse(clc.mirror(Vector(0,0,tall/2),Vector(0,0,1)))
	clcy = clc.copy()
	clcy.rotate(Vector(0,0,0),Vector(0,0,1),90)
	clc = clc.fuse(clcy)
	cl = cl.cut(clc)
	#Body
	size = 30
	thick = 3
	ob = Part.makeCylinder(size,tall,Vector(0,0,0),Vector(0,0,1),90)
	ob.rotate(Vector(0,0,0),Vector(0,0,1),180)
	ob.translate(Vector(-ac.beamSize/2,-ac.beamSize/2,0))
	ob = ob.makeFillet(ac.beamSize/2,[ob.Edges[1],ob.Edges[3]])
	ob = ob.makeFillet(ac.beamSize/5,[ob.Edges[14]])
	
	oc = Part.makeCylinder(size-thick*2,tall,Vector(0,0,0),Vector(0,0,1),90)
	oc.rotate(Vector(0,0,0),Vector(0,0,1),180)
	oc.translate(Vector(-ac.beamSize/2-thick*0.75,-ac.beamSize/2-thick*0.75,0))
	oc = oc.makeFillet(ac.beamSize/2-thick,[oc.Edges[1],oc.Edges[3]])
	oc = oc.makeFillet(ac.beamSize/5,[oc.Edges[14]])
	
	cb = ob.cut(oc)
	
	vc = cl.fuse(cb)
	
	#male side clip
	bendthick = 1.5
	bendtall = 2
	over = 4
	ball = 1.5
	ctall = ball + bendtall + over
	cwide = 10 
	msc = Part.makeBox(cwide,bendthick+ball,ctall)
	msc = msc.makeFillet(bendtall,[msc.Edges[3],msc.Edges[7]])
	msc = msc.makeFillet((bendthick+ball)-0.01,[msc.Edges[4]])
	bc = Part.makeBox(cwide,ball,bendtall)
	bc.translate(Vector(0,bendthick,over))
	msc = msc.cut(bc)
	
	msc = msc.makeFillet(ball/2-0.01,[msc.Edges[35],msc.Edges[40],msc.Edges[31]])
	
	
	msc.translate(Vector(-cwide/2,-bendthick-ball-thick/2,tall-over)) 
	
	mscy = msc.copy()
	mscy.translate(Vector(-size/2-ac.beamSize/2,-ac.beamSize/2,0))
	
	mscx = msc.copy()
	mscx.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	mscx.translate(Vector(-ac.beamSize/2,-size/2-ac.beamSize/2,0))
	
	mscset = mscy.fuse(mscx)
	
	#female side clip
	tol = 1.1
	fsc = Part.makeCylinder((ball*tol)/2,cwide*tol)
	fsc.translate(Vector(0,0,-(cwide*tol)/2))
	fsc.rotate(Vector(0,0,0),Vector(0,1,0),90)
	
	fscy = fsc.copy()
	fscy.translate(Vector(-size/2 - ac.beamSize/2,-ac.beamSize/2-thick+0.5,bendtall+ball/2))
	
	fscx = fsc.copy()
	fscx.rotate(Vector(0,0,0),Vector(0,0,1),90)
	fscx.translate(Vector(-ac.beamSize/2-thick+0.5,-size/2 - ac.beamSize/2,bendtall+ball/2))
	
	fscset = fscy.fuse(fscx)
	
	if type == 1:
		logosize=20
		logothick = 2.5
		logo = LE3Plogolong(logosize,logothick)
		logo.translate(Vector(-logosize,-logothick/2,0))
		logo.rotate(Vector(0,0,0),Vector(0,1,0),-90)
		logo.rotate(Vector(0,0,0),Vector(0,0,1),-45)
		logo.translate(Vector(-size+9,-size-4.8,tall/2))
		vc = vc.cut(logo)
		
	if type < 2:
		vc = vc.fuse(mscset)
	
	if type < 3:
		vc = vc.cut(fscset)
	
	if dc.forPrint == 0:
		vc.translate(Vector(ac.frameringxlen/2 + ac.beamSize/2,ac.frameringylen/2 + ac.beamSize/2 + ac.tailadd/2,ac.frameringbzpos+tall/9))
	
	
	
	return vc

def VertConduit():
	tall = 72
	spacing = 10
	if dc.forPrint == 0:
		a = VertConduitSeg(type = 0)
		b = VertConduitSeg(type = 0)
		b.translate(Vector(0,0,tall))
		c = VertConduitSeg(type = 0)
		c.translate(Vector(0,0,tall*2))
		d = VertConduitSeg(type = 2)
		d.translate(Vector(0,0,tall*3))
		vcs = a.fuse(b.fuse(c.fuse(d)))
		
	if dc.forPrint == 1:
		a = VertConduitSeg(type = 2)
		b = VertConduitSeg(type = 2)
		b.rotate(Vector(0,0,0),Vector(0,0,1),-90)
		b.translate(Vector(0,spacing,0))
		c = VertConduitSeg(type = 0)
		c.rotate(Vector(0,0,0),Vector(0,0,1),180)
		c.translate(Vector(spacing,spacing,0))
		d = VertConduitSeg(type = 2)
		d.rotate(Vector(0,0,0),Vector(0,0,1),90)
		d.translate(Vector(spacing,0,0))
		vcs = a.fuse(b.fuse(c.fuse(d)))
		vcs.rotate(Vector(0,0,0),Vector(0,0,1),-90)
	
	
	return a.fuse(b)
	