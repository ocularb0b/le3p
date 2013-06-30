#le3p-v0.1.3 - pXCarriage.py

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
from include.shapes import USlice

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

def xCarriage():
  xsize = ac.xBushing[2] - 0.01
	ysize = ac.xBushing[1] + ac.minthick * 2
	#print 'yszie={y}'.format(y=ysize)
	zsize = ac.xrodspacing
	faceplatethick = ysize
	clampsize = ac.beltWidth + ps.m3i[1]*2 + ac.minthick
	extraclamp = 4
	railsize = ac.minthick
	
	#face plate
	fp = Part.makeBox(xsize,faceplatethick,zsize)
	fp.translate(Vector(-xsize/2,ac.xrodypos-ac.xBushing[1]/2 - ac.minthick,-zsize/2 + ac.xrodzcenter))
	#clamp add
	ec = Part.makeBox(xsize,extraclamp,clampsize)
	ec.translate(Vector(-xsize/2,ac.xrodypos+ysize/2,ac.gantrydrivecenter-clampsize/2))
	ec=ec.makeFillet(extraclamp-0.01,[ec.Edges[10],ec.Edges[11]])
	fp=fp.fuse(ec)
	#adjustable clamp cut
	acc = Part.makeBox(ps.m3n[1]+ac.minthick,extraclamp,clampsize)
	acc.translate(Vector(-xsize/2,ac.xrodypos+ysize/2,ac.gantrydrivecenter-clampsize/2))
	acc=acc.makeFillet(extraclamp-0.01,[acc.Edges[5],acc.Edges[7]])
	fp=fp.fuse(acc)
	
	#adjustable clamp add
	aca = Part.makeBox(ps.m3n[1]+ac.minthick,ac.minthick,clampsize)
	aca.translate(Vector(-xsize/2,ac.xrodypos+ysize/2+extraclamp+1,ac.gantrydrivecenter-clampsize/2))
	aca=aca.makeFillet(extraclamp-0.01,[aca.Edges[5],aca.Edges[7]])
	fp=fp.fuse(aca)
	
	#Face Rails
	fr = Part.makeBox(railsize,railsize,zsize)
	fr.translate(Vector(-railsize/2,-railsize/2,-zsize/2))
	fr.rotate(Vector(0,0,0),Vector(0,0,1),45)
	fr.translate(Vector(xsize/4,ac.xrodypos-ysize/2,ac.xrodzcenter))
	
	frm = Part.makeBox(railsize*2,railsize,zsize)
	frm.translate(Vector(-railsize,-railsize/2,-zsize/2))
	frm=frm.makeFillet(railsize-0.01,[frm.Edges[8],frm.Edges[9]])
	frm.translate(Vector(xsize/4,ac.xrodypos-ysize/2,ac.xrodzcenter))
	
	fr = fr.common(frm)
	
	fr1 = fr.copy()
	fr1.translate(Vector(-xsize/4,0,0))
	fr2 = fr1.copy()
	fr2.translate(Vector(-xsize/4,0,0))
	fr=fr.fuse(fr1.fuse(fr2))
	
	fp =fp.fuse(fr)
	
	#bushing tubes
	bt1 = Part.makeCylinder((ac.xBushing[1]+ac.minthick*2)/2,xsize)
	bt1.translate(Vector(0,0,-xsize/2))
	bt1.rotate(Vector(0,0,0),Vector(0,1,0),90)
	bt1.translate(Vector(0,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2))
	bt2=bt1.copy()
	bt2.translate(Vector(0,0,-ac.xrodspacing))
	bts = bt1.fuse(bt2)
	
	xc=bts.fuse(fp)
	
	#rod cuts
	xr=Part.makeCylinder((bc.gantryRodDia+bc.rodClearance)/2,xsize)
	xr.translate(Vector(0,0,-xsize/2))
	xr.rotate(Vector(0,0,0),Vector(0,1,0),90)
	xr.translate(Vector(0,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2))
	xr2=xr.copy()
	xr2.translate(Vector(0,0,-ac.xrodspacing))
	
	xc=xc.cut(xr.fuse(xr2))
	
	#bushing cuts
	xb=Part.makeCylinder((ac.xBushing[1]+bc.bushingTolerance)/2,ac.xBushing[2])
	xb.translate(Vector(0,0,-ac.xBushing[2]/2))
	xb.rotate(Vector(0,0,0),Vector(0,1,0),90)
	xb.translate(Vector(0,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2))
	xb2=xb.copy()
	xb2.translate(Vector(0,0,-ac.xrodspacing))
	
	xc=xc.cut(xb.fuse(xb2))
	
	#beltpath
	bpy=ac.beltThick+ac.beltPath*2
	bpz=ac.beltWidth+ac.beltPath*2
	bp = Part.makeBox(xsize,bpy,bpz)
	bp.translate(Vector(-xsize/2,ac.gantrybidlerypos+bc.gantryIdlerDia/2+ac.beltThick/2-bpy/2,ac.gantrydrivecenter-bpz/2))
	bp=bp.makeFillet(ac.beltWidth/4,[bp.Edges[8],bp.Edges[9],bp.Edges[10],bp.Edges[11]])
	xc=xc.cut(bp)
	
	#belt clamp path
	bcp = Part.makeBox(xsize,ac.beltThick,ac.beltWidth+0.5)
	bcp.translate(Vector(-xsize/1.5,ac.gantrycidlerypos - ps.z624[1]/2 - ac.beltThick,ac.gantrydrivecenter-(ac.beltWidth+0.5)/2))
	bcp1 = Part.makeBox(xsize - ps.m3l[1] - ac.minthick,ac.beltThick*2,ac.beltWidth+2)
	bcp1=bcp1.makeFillet(ac.beltWidth/2,[bcp1.Edges[4]])
	bcp1=bcp1.makeFillet(ac.beltWidth/4,[bcp1.Edges[6],bcp1.Edges[12]])
	bcp1.translate(Vector(-xsize/2,ac.gantrycidlerypos - ps.z624[1]/2 - ac.beltThick-2,ac.gantrydrivecenter-(ac.beltWidth+2)/2))
	#return bcp1
	bcp = bcp.fuse(bcp1)
	xc=xc.cut(bcp)
	
	#belt clamp fixed teeth
	bct = Part.makeCylinder(0.6,ac.beltWidth+0.5)
	bct.translate(Vector(xsize/2-1,ac.xrodypos+ysize/4-1.75,ac.gantrydrivecenter-(ac.beltWidth+0.5)/2))
	bcts=bct.copy()
	for i in range(0,5):
		a=bct.copy()
		a.translate(Vector(-2*i,0,0))
		bcts=bcts.fuse(a)
	
	xc=xc.cut(bcts)
	
	#belt clamp adj teeth
	bcta = Part.makeCylinder(0.6,ac.beltWidth+0.5)
	bcta.translate(Vector(-xsize/2+1,ac.xrodypos+ysize/2+ac.minthick,ac.gantrydrivecenter-(ac.beltWidth+0.5)/2))
	bctsa=bcta.copy()
	for i in range(0,5):
		a=bcta.copy()
		a.translate(Vector(2*i,0,0))
		bctsa=bctsa.fuse(a)
	
	xc=xc.cut(bctsa)
	
	#Belt Clamp Cut
	bccx = xsize
	bccy = 20
	bccz = clampsize + 2
	thick = 1
	rad = 4
	bcc = Part.makeBox(bccx,bccy,bccz)
	bcc = bcc.makeFillet(rad,[bcc.Edges[8],bcc.Edges[9]])
	bcctool = bcc.copy()
	bcctool.translate(Vector(xsize/2-bccx,ac.gantrycidlerypos-ps.z624[1]/2-ac.beltThick,ac.gantrydrivecenter-bccz/2))
	bcc2 = Part.makeBox(bccx,bccy-thick,bccz-thick*2)
	bcc2 = bcc2.makeFillet(rad-thick/2,[bcc2.Edges[8],bcc2.Edges[9]])
	bcc2.translate(Vector(0,thick,thick))
	bcc=bcc.cut(bcc2)
	#bcc.rotate(Vector(0,0,0),Vector(0,0,1),180)
	bcc.translate(Vector(xsize/2-bccx,ac.gantrycidlerypos-ps.z624[1]/2-ac.beltThick,ac.gantrydrivecenter-bccz/2))
	#center cut
	ccx = xsize - ac.minthick*3 - ps.m3l[1]*2
	cc=Part.makeBox(ccx,ysize/2,ac.beltWidth+ac.beltSpace*2)
	cc.translate(Vector(-ccx/2+ac.minthick,ac.gantrycidlerypos-ps.z624[1]/2-ac.beltThick/2,ac.gantrydrivecenter - ac.beltWidth/2-ac.beltSpace))
	cc = cc.makeFillet(ac.minthick,[cc.Edges[5],cc.Edges[7]])
	
	xc = xc.cut(bcc.fuse(cc))
	#Ram guide slot
	guidewide = 4
	guidedeep = 2
	guidetol = 0.5 #added to each side
	rgs = Part.makeBox(ccx-ac.minthick,guidewide+guidetol*2,guidedeep+guidetol)
	rgs.translate(Vector(-ccx/2+ac.minthick,\
		((ac.xrodypos+ysize/2+extraclamp)+(ac.gantrycidlerypos-ps.z624[1]/2-ac.beltThick*1))/2 - ac.beltThick,\
		ac.gantrydrivecenter+(ac.beltWidth+ac.beltSpace*2)/2))
	rgs=rgs.fuse(rgs.mirror(Vector(0,0,ac.gantrydrivecenter),Vector(0,0,1)))
	#xc = xc.cut(rgs)
	
	#Ram Screw and Insert
	rs = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	rs.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	rs.translate(Vector(-ccx/2+ac.minthick/2-ps.m3i[1],((ac.xrodypos+ysize/2+extraclamp)+(ac.gantrycidlerypos-ps.z624[1]/2))/2,ac.gantrydrivecenter))
	ins = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	ins.translate(Vector(0,0,-ac.minthick-3.5))
	ins.rotate(Vector(0,0,0),Vector(0,1,0),-90)
	ins.translate(Vector(-ccx/2+ac.minthick/2-ps.m3i[1],((ac.xrodypos+ysize/2+extraclamp)+(ac.gantrycidlerypos-ps.z624[1]/2))/2,ac.gantrydrivecenter))
	xc = xc.cut(rs.fuse(ins))
	
	#Belt Clamp Screws
	clslen=38
	adj1 = CapHeadScrew(l=clslen,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	adj1.rotate(Vector(0,0,0),Vector(1,0,0),90)
	adj1.translate(Vector(xsize/2-ac.minthick,ac.xrodypos-ysize/2+ps.m3l[2],ac.gantrydrivecenter+ac.beltWidth/2+ac.minthick-1))
	adj2 = CapHeadScrew(l=clslen,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	adj2.rotate(Vector(0,0,0),Vector(1,0,0),90)
	adj2.translate(Vector(xsize/2-ac.minthick,ac.xrodypos-ysize/2+ps.m3l[2],ac.gantrydrivecenter-ac.beltWidth/2-ac.minthick+1))
	adj = adj1.fuse(adj2)
	adj=adj.fuse(adj.mirror(Vector(0,0,0),Vector(1,0,0)))
	xc=xc.cut(adj)
	
	#Clamp Threaded inserts
	i1=Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	i1p=Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1])
	i1p.translate(Vector(0,0,-ps.m3i[1]))
	i1=i1.fuse(i1p)
	i1.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	i1.translate(Vector(xsize/2-ac.minthick,ac.xrodypos+ysize/2+extraclamp,ac.gantrydrivecenter+ac.beltWidth/2+ac.minthick-1))
	i2=i1.copy()
	i2.translate(Vector(0,0,-ac.beltWidth-ac.minthick*2+2))
	iss=i1.fuse(i2)
	iss=iss.fuse(iss.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	xc=xc.cut(iss)
	
	#Back Fat Cut
	bfc = Part.makeBox(xsize-ac.minthick-4,ysize-ac.minthick,zsize/2-ac.minthick*2)
	bfc.translate(Vector(-(xsize-ac.minthick-4)/2,ac.xrodypos-ysize/2+ac.minthick,ac.xrodzcenter-ac.xrodspacing/2+ac.minthick))
	bfc=bfc.makeFillet(ac.minthick*2,[bfc.Edges[1],bfc.Edges[5],bfc.Edges[9],bfc.Edges[3],bfc.Edges[7]])
	bfc = bfc.cut(bt2)
	xc = xc.cut(bfc)
	#Thread block
	tb = Part.makeBox(xsize-ac.minthick-2,ac.minthick*2,ps.m3i[0]+ac.minthick*1.5)
	tb.translate(Vector(-(xsize-ac.minthick-2)/2,ac.xrodypos-ysize/2+ac.minthick,ac.xrodzcenter-ac.xrodspacing/2+ac.xBushing[1]/2))
	tb = tb.makeFillet(ac.minthick/2,[tb.Edges[11]])
	xc = xc.fuse(tb)
	
	#ToolHolder Mount Screws
	tms1 = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	ins = Part.makeCylinder(ps.m3i[0]/2,ps.m3i[1]+ac.minthick)
	ins.translate(Vector(0,0,-20))
	tms1=tms1.fuse(ins)
	tms1.rotate(Vector(0,0,0),Vector(1,0,0),90)
	tms1.translate(Vector(-xsize/8,ac.xrodypos-ac.xBushing[1]/2-ac.minthick,ac.gantrydrivecenter+ac.beltWidth/2+ac.minthick-1))
	tms3 = tms1.copy()
	tms1 = tms1.fuse(tms1.mirror(Vector(0,0,0),Vector(1,0,0)))
	tms2 = tms1.mirror(Vector(0,0,ac.gantrydrivecenter),Vector(0,0,1))
	tms3 = tms3.mirror(Vector(0,0,ac.xrodzcenter),Vector(0,0,1))
	tms31= tms3.copy()
	tms31.translate(Vector(-xsize/4,0,0))
	tms3=tms3.fuse(tms31)
	tms3 = tms3.fuse(tms3.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	xc = xc.cut(tms1.fuse(tms2.fuse(tms3)))
	
	#Bushing Clamp Slots
	thick = 2
	bcs=Part.makeBox(xsize,ysize/2,thick)
	bcs.translate(Vector(-xsize/2,ac.xrodypos,ac.xrodzcenter+ac.xrodspacing/2-thick/2))
	bcs = bcs.fuse(bcs.mirror(Vector(0,0,ac.xrodzcenter),Vector(0,0,1)))
	
	xc = xc.cut(bcs)
	
	#EndStop Pocket
	esp = Part.makeBox(bc.gantrySwitchX,bc.gantrySwitchY,bc.gantrySwitchZ)
	esp = esp.makeFillet(bc.gantrySwitchZ/2-0.01,[esp.Edges[5],esp.Edges[7]])
	esp.translate(Vector(-xsize/2,ac.xrodypos - bc.gantrySwitchY/2,ac.gantrydrivecenter - bc.gantrySwitchZ - ac.beltThick - ac.minthick*2))
	#EndStop Screws
	ess = CapHeadScrew(l=16,d=bc.gantrySwitchScrewDia,hd=bc.gantrySwitchScrewDia*2,hh=bc.gantrySwitchScrewDia/2,cut=1)
	ess.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	ess.translate(Vector(-xsize/2+bc.gantrySwitchScrewOffset/2,ac.xrodypos+bc.gantrySwitchY/2+ac.minthick,ac.gantrydrivecenter - bc.gantrySwitchZ/2 + bc.gantrySwitchScrewSpacing/2- ac.beltThick - ac.minthick*2))
	ess1 = ess.copy()
	ess1.translate(Vector(0,0,-bc.gantrySwitchScrewSpacing))
	ess = ess.fuse(ess1)
	
	esp = esp.fuse(ess)
	esp = esp.fuse(esp.mirror(Vector(0,0,0),Vector(1,0,0)))
	xc = xc.cut(esp)
	
	#Cable Tie Off
	top = Part.makeBox(14,4,2)
	top.translate(Vector(-7,ac.xrodypos+ysize/2-ac.minthick-1,ac.xrodzcenter-2.5))
	end = Part.makeBox(3,4,10)
	end.translate(Vector(-7,ac.xrodypos+ysize/2-ac.minthick-1,ac.xrodzcenter-10.5))
	end=end.fuse(end.mirror(Vector(0,0,0),Vector(1,0,0)))
	
	cto = top.fuse(end)
	cto = cto.makeFillet(2,[cto.Edges[9],cto.Edges[18]])
	xc = xc.cut(cto)
	
	#Cable Path
	cp = Part.makeBox(24,30,9)
	cp = cp.makeFillet(2,[cp.Edges[1],cp.Edges[3],cp.Edges[5],cp.Edges[7]])
	#cp.rotate(Vector(0,0,0),Vector(1,0,0),-20)
	cp.translate(Vector(-12,ac.xrodypos - 10 - ysize/2,ac.xrodzcenter-ac.minthick*2-4))
	
	xc = xc.cut(cp)
	
	#Belt Ram
	brx = ccx/3
	bry = ac.minthick*2+1
	brz = ac.beltWidth+ac.beltSpace*2-2
	br = Part.makeBox(brx,bry,brz)
	br = br.makeFillet(bry/2-0.01,[br.Edges[4],br.Edges[6]])
	
	br.translate(Vector(0,((ac.xrodypos+ysize/2+extraclamp)+(ac.gantrycidlerypos-ps.z624[1]/2-ac.beltThick*1))/2-bry/2+1,ac.gantrydrivecenter-brz/2))
	br = br.cut(rs)
	if dc.forPrint == 1:
		br.rotate(Vector(0,0,0),Vector(0,1,0),90)
		br.translate(Vector(-ac.gantrydrivecenter-22.5,9,ac.gantrydrivecenter-13))
		
		
	xc = xc.fuse(br)
	
	#clamp solo
	#xc = xc.common(bcctool)
	#body solo
	#xc = xc.cut(bcctool)
	
	if dc.forPrint == 1:
		xc.translate(Vector(xsize/2,-ac.xrodypos,-ac.xrodzcenter))
		xc.rotate(Vector(0,0,0),Vector(0,1,0),-90)
		xc.rotate(Vector(0,0,0),Vector(0,0,1),180)
		
	else:
		xc.translate(Vector(ac.mXpos,ac.mYpos,0))
	return xc
