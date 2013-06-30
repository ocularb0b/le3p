#le3p-v0.1.3 - pZEnds.py

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


def zEnds():
  sizex = bc.zRodDia + ac.minthick*2
	sizey = ac.zrodspacing + bc.gantryRodDia + ac.minthick*4 + ps.m3l[1]*2 
	sizez = ac.beamSize
	#print 'ysize = {x}'.format(x=sizey)
	#body blank
	bb = Part.makeBox(sizex,sizey,sizez)
	bb.translate(Vector(-ac.frameringxlen/2,-sizey/2,0))
	bb = bb.makeFillet(ac.minthick*2,[bb.Edges[4],bb.Edges[6]])
	#inner clearance
	ic = Part.makeCylinder(sizey/2-bc.zRodDia/2,sizez)
	ic.translate(Vector(-ac.zrodxpos+sizey/2,0,0))
	#rod cuts
	rc = Part.makeBox(bc.zRodDia,bc.zRodDia,ac.beamSize)
	rc.translate(Vector(-ac.zrodxpos-bc.zRodDia/2,-ac.zrodspacing/2-bc.zRodDia/2,0))
	rc = rc.makeFillet(bc.zRodDia/2-0.01,[rc.Edges[4],rc.Edges[6]])
	rc = rc.fuse(rc.mirror(Vector(0,0,0),Vector(0,1,0)))
	#mount screws
	ms1 = CapHeadScrew(l=10,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	ms1.rotate(Vector(0,0,0),Vector(0,1,0),90)
	ms1.translate(Vector(-ac.frameringxlen/2+ac.minthick*2-2,sizey/2-ps.m3l[1]/2-ac.minthick,ac.beamSize/2))
	ms2 = ms1.copy().mirror(Vector(0,ac.zrodspacing/2,0),Vector(0,1,0))
	mss=ms1.fuse(ms2)
	mss=mss.fuse(mss.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	
	ze = bb.cut(ic)
	ze = ze.cut(rc)
	ze = ze.cut(mss)
	
	zeu = ze.copy()
	zeu.translate(Vector(0,0,ac.zrodlen - ac.framebasedeep - ac.bedThick - ac.beamSize))
	zel = ze.copy()
	zel.translate(Vector(0,0,ac.frameringbzpos - ac.beamSize/2))
	
	lca = lowClamp()
	
	
	zes = zeu.fuse(zel.fuse(lca))
	if dc.noMirror == 0:
		zes = zes.fuse(zes.mirror(Vector(0,0,0),Vector(1,0,0)))
	return zes

def lowClamp():
	r=0
	size = bc.gantryRodDia + ac.minthick + ps.m3l[1]
	bb = Part.makeBox(size,size,ac.beamSize)
	bb.translate(Vector(-ac.frameringxlen/2,ac.zrodspacing/2-bc.zRodDia/2,ac.frameringazpos - ac.beamSize/2))
	bb = bb.makeFillet(size-ac.minthick,[bb.Edges[6]])
	rc = Part.makeBox(bc.gantryRodDia,bc.gantryRodDia,ac.beamSize)
	rc.translate(Vector(-ac.frameringxlen/2,ac.zrodspacing/2-bc.zRodDia/2,ac.frameringazpos - ac.beamSize/2))
	rc = rc.makeFillet(ac.minthick,[rc.Edges[6]])
	
	#mount screws
	ms1 = CapHeadScrew(l=10,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	ms1.rotate(Vector(0,0,0),Vector(1,0,0),-90)
	ms1.translate(Vector(-ac.frameringxlen/2 + bc.gantryRodDia + (ac.minthick + ps.m3l[1])/2,ac.zrodspacing/2-bc.zRodDia/2+ac.minthick,ac.frameringazpos))
	
	ms2 = CapHeadScrew(l=10,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
	ms2.rotate(Vector(0,0,0),Vector(0,1,0),90)
	ms2.translate(Vector(-ac.frameringxlen/2+ac.minthick,ac.zrodspacing/2 + bc.zRodDia/2 + (ac.minthick + ps.m3l[1])/2,ac.frameringazpos))
	
	lc = bb.cut(rc)
	lc = lc.cut(ms1)
	lc = lc.cut(ms2)
	#lc = lc.makeFillet(1,[lc.Edges[43]])
	if dc.noMirror == 0:
		lc = lc.fuse(lc.mirror(Vector(0,0,0),Vector(0,1,0)))
	return lc
