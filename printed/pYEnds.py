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

bc = basicConfig.basicConfig()
dc = displayConfig.displayConfig()
ac = advancedConfig.advancedConfig()
ps = partSizes.partSizes()


def yEndIdle():
    sizex = bc.gantryRodDia + ac.minthick*2 + ps.m3l[1]*2
    sizez = (ac.gantrydrivecenter + ps.z624[2] + ac.minthick*2 + ps.m3l[1]) - (ac.yrodzpos - bc.gantryRodDia/2)
    icx = ps.z624[1]+ac.beltThick*2+ac.beltSpace
    icz = ps.z624[2]*2+2
    #body blank
    bb = Part.makeBox(sizex,ac.beamSize,sizez)
    bb.translate(Vector(-ac.frameringxlen/2,-ac.yrodlen/2,ac.yrodzpos - bc.gantryRodDia/2))
    bb = bb.makeFillet(ac.minthick*2,[bb.Edges[5]])
    #Idle screw bulge
    isbz = sizez-bc.gantryRodDia-ac.minthick
    isb = Part.makeCylinder(icx/2,isbz)
    isb.translate(Vector(-ac.gantryaidlerxpos,ac.gantryaidlerypos-ac.tailadd/2,ac.yrodzpos-bc.gantryRodDia/2-isbz+sizez))
    isb = isb.makeFillet(icx/2-0.01,[isb.Edges[2]])
    isb = isb.makeFillet(icx/3,[isb.Edges[2]])
    #rod cut
    rc = Part.makeBox(bc.gantryRodDia,ac.beamSize,bc.gantryRodDia)
    rc.translate(Vector(-ac.frameringxlen/2,-ac.yrodlen/2,ac.yrodzpos - bc.gantryRodDia/2))
    rc = rc.makeFillet(bc.gantryRodDia/2,[rc.Edges[5]])
    #Idler cut
    ic = Part.makeBox(icx,icx,icz)
    ic = ic.makeFillet(icx/2-0.01,[ic.Edges[0],ic.Edges[4]])
    ic.translate(Vector(-ac.gantryaidlerxpos-icx/2,ac.gantryaidlerypos-icx/2-ac.tailadd/2,ac.gantryaidlerzpos-icz/2))
    #idle screw cut
    isc = CapHeadScrew(l=30,d=ps.m4l[0],hd=ps.m4l[1],hh=ps.m4l[2],cut=1)
    isc.translate(Vector(-ac.gantryaidlerxpos,ac.gantryaidlerypos-ac.tailadd/2,ac.yrodzpos-bc.gantryRodDia/2+sizez-ps.m4l[2]))
    #mount screw cuts
    ms1 = CapHeadScrew(l=30,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms1.rotate(Vector(0,0,0),Vector(0,1,0),90)
    ms1.translate(Vector(-ac.frameringxlen/2+ac.minthick,-ac.yrodlen/2+ac.beamSize/2,ac.yrodzpos-bc.gantryRodDia/2+sizez-ps.m3l[1]-ac.minthick/2))
    mss = ms1.fuse(ms1.mirror(Vector(0,0,ac.gantrydrivecenter),Vector(0,0,1)))
    ms2 = CapHeadScrew(l=40,d=ps.m3l[0],hd=ps.m3l[1],hh=ps.m3l[2],cut=1)
    ms2.translate(Vector(-ac.frameringxlen/2 + sizex - ps.m3l[1]/2 - ac.minthick,-ac.yrodlen/2+ac.beamSize/2,ac.yrodzpos - bc.gantryRodDia/2 + ac.minthick*2))
    mss = mss.fuse(ms2)
    
    yei = bb.fuse(isb)
    yei = yei.cut(rc)
    yei = yei.cut(ic)
    yei = yei.cut(isc)
    yei = yei.cut(mss)
    
    yei.translate(Vector(0,ac.tailadd/2,0))
    
    yeil = yei.copy()
    yeir = yei.mirror(Vector(0,0,0),Vector(1,0,0))
    
    if dc.forPrint == 1:
        yeil.translate(Vector(ac.yrodxpos+ac.minthick+2,ac.yrodlen/2-ac.tailadd/2,-ac.frameysupportszpos-ac.beamSize/2-sizez/2))
        yeil.rotate(Vector(0,0,0),Vector(1,0,0),90)
        yeir.translate(Vector(-ac.yrodxpos-ac.minthick-2,ac.yrodlen/2-ac.tailadd/2,-ac.frameysupportszpos-ac.beamSize/2-sizez/2))
        yeir.rotate(Vector(0,0,0),Vector(1,0,0),90)
    
    if dc.noMirror == 0:
        yei = yeir.fuse(yeil)
    else:
        yei = yeil
    return yei

def yEndMotor():
    size = bc.gantryRodDia + ac.minthick + ps.m3l[1]
    bb = Part.makeBox(size,ac.beamSize,size)
    bb.translate(Vector(-ac.frameringxlen/2,ac.yrodlen/2 - ac.beamSize,ac.yrodzpos - bc.gantryRodDia/2))
    yem = bb
    yem.translate(Vector(0,ac.tailadd/2,0))
    yem = yem.makeFillet(size-ac.minthick,[yem.Edges[5]])
    rc = Part.makeBox(bc.gantryRodDia,ac.beamSize,bc.gantryRodDia)
    rc.translate(Vector(-ac.frameringxlen/2,ac.yrodlen/2 - ac.beamSize + ac.tailadd/2,ac.yrodzpos - bc.gantryRodDia/2))
    rc = rc.makeFillet(ac.minthick,[rc.Edges[5]])
    yem = yem.cut(rc)
    
    if dc.forPrint == 1:
        yem.translate(Vector(ac.frameringxlen/2+2,-ac.yrodlen/2 + ac.beamSize - ac.tailadd/2,-ac.yrodzpos + bc.gantryRodDia/2))
        yem.rotate(Vector(0,0,0),Vector(1,0,0),90)
    
    if dc.noMirror == 0:
        yem = yem.fuse(yem.mirror(Vector(0,0,0),Vector(1,0,0)))
    return yem
















