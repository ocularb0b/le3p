#le3p-v0.1.3 - pZMotorMount.py

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


def zMotorMounts():
  xsize = ac.zMotor[0]
	ysize = ac.zrodspacing - bc.zRodDia
	zsize = ac.zMotor[1] + ac.minthick*2 - ac.beamSize
	#body blank
	bb = Part.makeBox(xsize,ysize,zsize)
	bb.translate(Vector(ac.zscrewxpos-xsize/2,-ysize/2,ac.frameringazpos + ac.beamSize/2))
	bb=bb.makeFillet(ac.minthick*2,[bb.Edges[0],bb.Edges[2],bb.Edges[4],bb.Edges[6]])
	#undercut
	ucy = ac.zrodspacing - bc.zRodDia - ac.beamSize*2
	uc = Part.makeBox(xsize,ucy,zsize-ac.minthick*2)
	uc.translate(Vector(ac.zscrewxpos-xsize/2,-ucy/2,ac.frameringazpos + ac.beamSize/2))
	uc=uc.makeFillet(ac.minthick,[uc.Edges[9],uc.Edges[11]])
	#motor face cut
	mfc = Part.makeCylinder(ac.zMotor[5]/2,ac.minthick*2)
	mfc.translate(Vector(ac.zscrewxpos,0,ac.frameringazpos + ac.beamSize/2+zsize-ac.minthick*2))
	#mount screws
	ms1 = Part.makeCylinder(ps.m3l[0]/2,zsize)
	ms1.translate(Vector(ac.zscrewxpos+ac.zMotor[0]/2-ac.beamSize/2,ysize/2-ac.beamSize/2,ac.frameringazpos + ac.beamSize/2))
	ms2 = Part.makeCylinder(ps.m3l[0]/2,zsize)
	ms2.translate(Vector(ac.zscrewxpos-ac.zMotor[0]/2+ac.beamSize/2,ysize/2-ac.beamSize/2,ac.frameringazpos + ac.beamSize/2))
	mss=ms1.fuse(ms2)
	mss=mss.fuse(mss.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	mh1 = Part.makeCylinder(ps.m3l[1]/2,zsize)
	mh1.translate(Vector(ac.zscrewxpos+ac.zMotor[0]/2-ac.beamSize/2,ysize/2-ac.beamSize/2,ac.frameringazpos + ac.beamSize/2+ac.minthick*2))
	mh2 = Part.makeCylinder(ps.m3l[1]/2,zsize)
	mh2.translate(Vector(ac.zscrewxpos-ac.zMotor[0]/2+ac.beamSize/2,ysize/2-ac.beamSize/2,ac.frameringazpos + ac.beamSize/2+ac.minthick*2))
	mhs=mh1.fuse(mh2)
	mhs=mhs.fuse(mhs.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	#motor mount screws
	ms1 = Part.makeCylinder(ps.m3l[0]/2,ac.minthick*2)
	ms1.translate(Vector(ac.zscrewxpos+ac.zMotor[4]/2,ac.zMotor[4]/2,ac.frameringazpos + ac.beamSize/2+zsize-ac.minthick*2))
	ms2 = Part.makeCylinder(ps.m3l[0]/2,ac.minthick*2)
	ms2.translate(Vector(ac.zscrewxpos-ac.zMotor[4]/2,ac.zMotor[4]/2,ac.frameringazpos + ac.beamSize/2+zsize-ac.minthick*2))
	mms = ms1.fuse(ms2)
	mms=mms.fuse(mms.mirror(Vector(0,0,0),Vector(0,1,0)))
	mh1 = Part.makeCylinder(ps.m3l[1]/2,ac.minthick*2)
	mh1.translate(Vector(ac.zscrewxpos+ac.zMotor[4]/2,ac.zMotor[4]/2,ac.frameringazpos + ac.beamSize/2+zsize-ps.m3l[2]))
	mh2 = Part.makeCylinder(ps.m3l[1]/2,ac.minthick*2)
	mh2.translate(Vector(ac.zscrewxpos-ac.zMotor[4]/2,ac.zMotor[4]/2,ac.frameringazpos + ac.beamSize/2+zsize-ps.m3l[2]))
	mmh = mh1.fuse(mh2)
	mmh=mmh.fuse(mmh.mirror(Vector(0,0,0),Vector(0,1,0)))
	
	
	zmm=bb.cut(uc.fuse(mfc.fuse(mss.fuse(mhs))))
	zmm=zmm.cut(mms.fuse(mmh))
	#stupid fix
	zmm = zmm.mirror(Vector(0,0,0),Vector(1,0,0))
	
	if dc.forPrint == 1:
		zmm.translate(Vector(ac.zscrewxpos-xsize/2-ac.minthick/2,0,-ac.frameringazpos-ac.beamSize/2-zsize))
		zmm.rotate(Vector(0,0,0),Vector(1,0,0),180)
	
	if dc.noMirror == 0:
		zmm=zmm.fuse(zmm.mirror(Vector(0,0,0),Vector(1,0,0)))
	return zmm
