#le3p-v0.1.3 - pGantryMotorMount.py

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

from config import basicConfig
from config import advancedConfig
from config import displayConfig
from config import partSizes

from include.parts import CapHeadScrew

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()

def gantryMotorMounts():
    xsize = (ac.frameringxlen/2 + ac.beamSize/2) - (ac.gantrymotorxpos - ac.beamSize/2 - ac.gantryMotor[0]/2 - ac.minthick - ps.m3l[1])
    ysize = ac.minthick*2 + ac.gantryMotor[0] + 0.75
    zsize = (ac.frameringczpos + ac.beamSize/2) - (ac.yrodzpos - bc.gantryRodDia/2 - ac.beamSize)
    print 'zsize = {x}'.format(x=zsize)
    #Body Blank
    bb = Part.makeBox(xsize,ysize,zsize)
    bb.translate(Vector(ac.frameringxlen/2 - xsize + ac.beamSize,ac.frameringylen/2 + ac.tailadd/2 + ac.beamSize ,ac.frameringczpos - zsize + ac.beamSize/2))
    bb=bb.makeFillet(ac.minthick,[bb.Edges[1],bb.Edges[2],bb.Edges[3],bb.Edges[5],bb.Edges[6],bb.Edges[7],])
    #Upper Gusset
    ug = Part.makeBox(ac.gantryMotor[0]*2,ac.gantryMotor[0]*2,ac.gantryMotor[0]*2)
    ug.translate(Vector(ac.gantrymotorxpos-ac.gantryMotor[0],ac.gantrymotorypos+ac.gantryMotor[0]/2-ac.gantryMotor[0],ac.gantrymotorzpos+ac.minthick*2))
    ug=ug.makeFillet(ac.gantryMotor[0],[ug.Edges[8]])
    #Lower Gusset
    lg = Part.makeCylinder(ac.gantryMotor[0],ac.gantryMotor[0]*2)
    lg.translate(Vector(0,0,-ac.gantryMotor[0]))
    lg.rotate(Vector(0,0,0),Vector(0,1,0),90)
    lg.translate(Vector(ac.gantrymotorxpos,ac.gantrymotorypos+ac.gantryMotor[0]/2,ac.gantrymotorzpos-ac.gantryMotor[0]))
    
    #Motor Cut
    tol = 1
    mc = Part.makeBox(ac.gantryMotor[0]+tol,ac.gantryMotor[0]+tol,ac.gantryMotor[1])
    mc.translate(Vector(ac.gantrymotorxpos-ac.gantryMotor[0]/2-tol/2,ac.gantrymotorypos-ac.gantryMotor[0]/2-tol/2,ac.gantrymotorzpos-ac.gantryMotor[1]))
    #Idle Cut
    ic = Part.makeBox(ac.gantryMotor[0],ac.gantryMotor[0],ac.gantryMotor[1]*2)
    ic.translate(Vector(ac.gantrymotorxpos-ac.gantryMotor[0]/2,ac.gantrymotorypos-ac.gantryMotor[0]/2,ac.gantrymotorzpos+ac.minthick*2))
    ic = ic.makeFillet(ac.gantryMotor[0]/2 - 0.01,[ic.Edges[0],ic.Edges[4]])
    #Motor Face Cut
    mfc = Part.makeCylinder(ac.gantryMotor[5]/2+ac.minthick/2,ac.minthick*2)
    mfc.translate(Vector(ac.gantrymotorxpos,ac.gantrymotorypos,ac.gantrymotorzpos))
    #Motor Mount Screws
    mms = CapHeadScrew(l=10,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    mms.translate(Vector(ac.gantryMotor[4]/2,ac.gantryMotor[4]/2,ac.gantrymotorzpos + ac.minthick*2 - ps.m3l[2]))
    mms = mms.fuse(mms.mirror(Vector(0,0,0),Vector(1,0,0)))
    mms = mms.fuse(mms.mirror(Vector(0,0,0),Vector(0,1,0)))
    mms.translate(Vector(ac.gantrymotorxpos,ac.gantrymotorypos,0))
    #Mount Screws
    ms1 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms1.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms1.translate(Vector(ac.frameringxlen/2+ac.beamSize/2,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],ac.frameringczpos))
    ms2 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms2.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms2.translate(Vector(ac.frameringxlen/2+ac.beamSize*1.5-xsize,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],ac.frameringczpos))
    ms3 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms3.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms3.translate(Vector(ac.frameringxlen/2-ac.beamSize/2,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],ac.frameringczpos))
    ms4 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms4.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms4.translate(Vector(ac.frameringxlen/2+ac.beamSize/2,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],ac.yrodzpos-bc.gantryRodDia/2-ac.beamSize/2))
    ms5 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms5.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms5.translate(Vector(ac.frameringxlen/2+ac.beamSize*1.5-xsize,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],ac.yrodzpos-bc.gantryRodDia/2-ac.beamSize/2))
    ms6 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms6.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms6.translate(Vector(ac.frameringxlen/2-ac.beamSize/2,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],ac.yrodzpos-bc.gantryRodDia/2-ac.beamSize/2))
    ms7 = CapHeadScrew(l=8,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms7.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    ms7.translate(Vector(ac.frameringxlen/2+ac.beamSize/2,ac.frameringylen/2+ac.beamSize+ac.tailadd/2+ac.minthick*2-ps.m3l[2],((ac.frameringczpos)+(ac.yrodzpos-bc.gantryRodDia/2-ac.beamSize/2))/2))
    #belt paths
    bpx = ac.beltThick+ac.beltSpace
    bpy = ac.minthick*4
    bpz = ac.beltThick+ac.beltSpace*2
    bp = Part.makeBox(bpx,bpy,bpz)
    bp = bp.makeFillet(ac.beltThick/2,[bp.Edges[1],bp.Edges[3],bp.Edges[5],bp.Edges[7]])
    bpa = bp.copy()
    bpb = bp.copy()
    bpa.translate(Vector(ac.gantrymotorxpos+ps.z624[1]/2+ac.beltThick/2-bpx/2,ac.frameringylen/2+ac.tailadd/2+ac.beamSize/2+ac.minthick,ac.gantrydrivecenter-bpz/2))
    bpb.translate(Vector(ac.gantrymotorxpos-ps.z624[1]/2-ac.beltThick/2-bpx/2,ac.frameringylen/2+ac.tailadd/2+ac.beamSize/2+ac.minthick,ac.gantrydrivecenter-bpz/2))
    
    mss=ms1.fuse(ms2.fuse(ms3.fuse(ms4.fuse(ms5.fuse(ms6.fuse(ms7))))))
    
    gmm = bb.cut(ug)
    gmm = gmm.cut(lg)
    gmm = gmm.cut(mc.fuse(ic))
    gmm = gmm.cut(mfc)
    gmm = gmm.cut(mms)
    gmm = gmm.cut(mss)
    gmm = gmm.cut(bpa.fuse(bpb))
    
    #stupid fix
    gmm = gmm.mirror(Vector(0,0,0),Vector(1,0,0))
    
    if dc.noMirror == 0:
    	gmm = gmm.fuse(gmm.mirror(Vector(0,0,0),Vector(1,0,0)))
    return gmm
