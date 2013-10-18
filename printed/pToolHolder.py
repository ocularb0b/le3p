#le3p-v0.1.3 - pToolHolder.py

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


def DualE3d():
    couplerdia = 10
    couplerlen = 6
    hemountdia = 16.5
    hemounttopringlen = 5
    hemountinnerlen = 5.5
    hemountinnerdia = 12.5
    #face plate
    fpx = ac.xBushing[2]
    fpy = ac.xrodypos-(ac.xBushing[1]/2+ac.minthick)+(ac.hotEndDia/2)-0.5
    fpz = (ac.xrodypos-ac.xBushing[1]/2-ac.minthick)+ps.m3l[2]/2+ac.minthick+ac.hotEndMountLen*2
    fp = Part.makeBox(fpx,fpy,fpz)
    fp.translate(Vector(-fpx/2,-ac.hotEndDia/2-0.5,ac.xrodzcenter-ac.hotEndMountLen*2))
    tcs = fp.copy()
    tc = fp.copy()
    fp = fp.makeFillet(ac.hotEndDia/4,[fp.Edges[0],fp.Edges[4]])
    #T Cuts
    tcs.translate(Vector(fpx*0.75+ac.minthick,0,ac.hotEndMountLen+couplerlen))
    tcs = tcs.makeFillet(ac.hotEndDia/2,[tcs.Edges[3]])
    tcs = tcs.fuse(tcs.mirror(Vector(0,0,0),Vector(1,0,0)))
    #Top Cut
    tc.translate(Vector(0,-ac.minthick,ac.hotEndMountLen+couplerlen))
    tc = tc.makeFillet(ac.hotEndDia,[tc.Edges[10]])
    
    fp = fp.cut(tcs.fuse(tc))
    fp = fp.makeFillet(ac.minthick,[fp.Edges[37],fp.Edges[34]])
    
    #HotEnd Slots
    hes=Part.makeBox(hemountdia,ac.hotEndDia,hemounttopringlen)
    hes = hes.makeFillet(hemountdia/2-0.01,[hes.Edges[2],hes.Edges[6]])
    hes.translate(Vector(-hemountdia/2-ac.hotEndDia/2-ac.hotEndSpacing/2,-ac.hotEndDia+hemountdia/2,ac.envelopeZ + ac.hotEndLen-hemounttopringlen))
    hesi=Part.makeBox(hemountinnerdia,ac.hotEndDia,hemountinnerlen)
    hesi = hesi.makeFillet(hemountinnerdia/2-0.01,[hesi.Edges[2],hesi.Edges[6]])
    hesi.translate(Vector(-hemountinnerdia/2-ac.hotEndDia/2-ac.hotEndSpacing/2,-ac.hotEndDia+hemountinnerdia/2,ac.envelopeZ + ac.hotEndLen-hemounttopringlen-hemountinnerlen))
    hesl=Part.makeBox(hemountdia,ac.hotEndDia,hemounttopringlen)
    hesl = hesl.makeFillet(hemountdia/2-0.01,[hesl.Edges[2],hesl.Edges[6]])
    hesl.translate(Vector(-hemountdia/2-ac.hotEndDia/2-ac.hotEndSpacing/2,-ac.hotEndDia+hemountdia/2,ac.envelopeZ + ac.hotEndLen-hemounttopringlen-hemountinnerlen-3.5))
    hesp=Part.makeBox(hemountdia,ac.hotEndDia,ac.hotEndMountLen)
    hesp = hesp.makeFillet(hemountdia/2-0.01,[hesp.Edges[2],hesp.Edges[6]])
    hesp.translate(Vector(-hemountdia/2-ac.hotEndDia/2-ac.hotEndSpacing/2,-ac.hotEndDia+hemountdia/2-ac.minthick*1.5,ac.envelopeZ + ac.hotEndLen-ac.hotEndMountLen))
    hes = hes.fuse(hesi.fuse(hesl.fuse(hesp)))
    hes = hes.fuse(hes.mirror(Vector(0,0,0),Vector(1,0,0)))
    
    #HotEnd Mount Screw
    hms = CapHeadScrew(l=26,d=ps.m4l[0],hd=ps.m4l[1],hh=ps.m4l[2],cut=1)
    hms.rotate(Vector(0,0,0),Vector(0,1,0),-90)
    hms.translate(Vector(-fpx/2+2,-hemountinnerdia/2-ps.m4l[0]/2+1,ac.envelopeZ + ac.hotEndLen-hemounttopringlen-ps.m4l[0]/2))
    hms = hms.fuse(hms.mirror(Vector(0,0,0),Vector(1,0,0)))
    #face rails
    railsize = ac.minthick
    fr = Part.makeBox(railsize,railsize,fpz+10)
    fr.translate(Vector(-railsize/2,-railsize/2,-fpz/2))
    fr.rotate(Vector(0,0,0),Vector(0,0,1),45)
    fr.translate(Vector(fpx/4,ac.xrodypos-ac.xBushing[1]/2-ac.minthick,ac.xrodzcenter))
    fr1=fr.copy()
    fr1.translate(Vector(-fpx/4,0,0))
    fr2=fr1.copy()
    fr2.translate(Vector(-fpx/4,0,0))
    
    th = fp.cut(hes)
    th = th.cut(hms)
    th = th.cut(fr.fuse(fr1.fuse(fr2)))
    
    #Coupler Holes
    ch1=Part.makeCylinder(couplerdia/2,fpz)
    ch1.translate(Vector(-ac.hotEndDia/2 - ac.hotEndSpacing/2,0,ac.envelopeZ + ac.hotEndLen))
    ch2=Part.makeCylinder(couplerdia/2+4,fpz)
    ch2.translate(Vector(-ac.hotEndDia/2 - ac.hotEndSpacing/2,0,ac.envelopeZ + ac.hotEndLen + couplerlen))
    
    chs = ch1.fuse(ch2)
    chs = chs.fuse(chs.mirror(Vector(0,0,0),Vector(1,0,0)))
    
    th = th.cut(chs)
    
    #Lower Screw Slots
    lss1 = Part.makeBox(ps.m3l[1],ps.m3l[2]+2,20)
    lss1 = lss1.makeFillet(ps.m3l[1]/2-0.01,[lss1.Edges[1],lss1.Edges[5]])
    lss1.translate(Vector(-ps.m3l[1]/2,-2,0))
    lss2 = Part.makeBox(ps.m3l[0],10,20)
    lss2 = lss2.makeFillet(ps.m3l[0]/2-0.01,[lss2.Edges[1],lss2.Edges[5]])
    lss2.translate(Vector(-ps.m3l[0]/2,0,-(ps.m3l[1]-ps.m3l[0])/2))
    #	Tool access
    ta = Part.makeCylinder(2,30)
    ta.translate(Vector(0,0,-2))
    ta.rotate(Vector(0,0,0),Vector(1,0,0),90)
    ta.rotate(Vector(0,0,0),Vector(0,0,1),35)
    ta.translate(Vector(0,0,20-ps.m3l[1]/2))
    
    lss = lss1.fuse(lss2.fuse(ta))
    lss.translate(Vector(fpx/2 - fpx/8,ac.xrodypos - ac.xBushing[1]/2-ac.minthick*2 - ps.m3l[2],ac.envelopeZ -ac.hotEndMountLen + ac.hotEndLen-20+ps.m3l[1]/2+ac.minthick+1))
    lss=lss.fuse(lss.mirror(Vector(0,0,0),Vector(1,0,0)))
    
    th = th.cut(lss)
    #Upper Mount Screws
    ums = CapHeadScrew(l=20,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ums.rotate(Vector(0,0,0),Vector(1,0,0),90)
    ums.translate(Vector(-fpx/8,ac.xrodypos-ac.xBushing[1]/2-ac.minthick*2-1 + ps.m3l[2],ac.gantrydrivecenter+ac.beltWidth/2+ac.minthick-1))
    ums=ums.fuse(ums.mirror(Vector(0,0,0),Vector(1,0,0)))
    th=th.cut(ums)
    
    
    #Cable Path
    cp = Part.makeBox(18,24,6)
    cp2 = Part.makeBox(18,18,20)
    cp2.translate(Vector(0,0,-14))
    cp = cp.fuse(cp2)
    cp = cp.makeFillet(2,[cp.Edges[16],cp.Edges[18],cp.Edges[19],cp.Edges[4],cp.Edges[5],cp.Edges[6],cp.Edges[26],cp.Edges[22],cp.Edges[14],cp.Edges[12]])
    cp.translate(Vector(-9,ac.xrodypos-10-ac.xBushing[1]/2-ac.minthick-2,ac.xrodzcenter-ac.minthick*2.5))
    
    
    th = th.cut(cp)
    
    if dc.forPrint == 0:
        th.translate(Vector(ac.mXpos,ac.mYpos,0))
    else:
        th.translate(Vector(0,-ac.xrodypos/2-1,-ac.xrodzcenter))
        th.rotate(Vector(0,0,0),Vector(1,0,0),-90)
    return th
   
