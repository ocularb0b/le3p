#le3p-v0.1.3 pCornerBracket.py

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

def SmallCornerBracket():
    size = ac.beamSize * 1.5
    bb = Part.makeBox(size,ac.beamSize,size)
    bb.translate(Vector(0,-ac.beamSize/2,0))
    bc=bb.copy()
    bc=bc.makeFillet(ac.beamSize/2,[bc.Edges[3]])
    bc.translate(Vector(ac.minthick,0,ac.minthick))
    bb=bb.makeFillet(ac.beamSize/2-0.01,[bb.Edges[4],bb.Edges[6],bb.Edges[9],bb.Edges[11]])
    scb = bb.cut(bc)
    s1 = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    s1.rotate(Vector(0,0,0),Vector(0,1,0),90)
    s1.translate(Vector(ac.minthick-ps.m3l[2],0,size-ac.beamSize/2))
    s2 = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    s2.translate(Vector(size-ac.beamSize/2,0,ac.minthick-ps.m3l[2]))
    scb=scb.cut(s1.fuse(s2))
    return scb

def LargeCornerBracket():
    xsize = ps.m3l[1]+ac.minthick*2
    ysize = ps.m3l[1]+ac.minthick*2
    zsize = ac.beamSize
    bb = Part.makeBox(xsize,ysize,zsize)
    bb.translate(Vector(ac.beamSize/2,ac.beamSize/2,-ac.beamSize/2))
    bbc = bb.copy()
    bbc.translate(Vector(ac.minthick,ac.minthick,0))
    bb = bb.cut(bbc)
    
    lcb = bb
    return lcb
